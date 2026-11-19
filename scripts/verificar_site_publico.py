#!/usr/bin/env python3
"""Verify the published demo with fresh synthetic sessions and real HTTP calls.

Uses Python's standard library only. No login or bypass token is used. Cookies
and CSRF values live only in memory and are never written to the evidence.
Only the sessions created by this run are reset at the end.
"""
from __future__ import annotations

import argparse
import copy
import csv
import io
import json
import sys
import uuid
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URL = "https://alertacidadao-bi-jpczz.est-dio-like-0113.chatgpt.site"


class Client:
    def __init__(self, base: str):
        self.base = base.rstrip("/")
        self.cookies = CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.cookies))
        self.csrf = ""
        self.started = False

    def request(self, method: str, path: str, data=None, headers=None, raw=None):
        h = {"User-Agent": "AlertaCidadao-Academic-Verification/1.0"}
        if method != "GET" and self.csrf:
            h["X-CSRF-Token"] = self.csrf
            h["Origin"] = self.base
        if data is not None:
            raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
            h["Content-Type"] = "application/json"
        h.update(headers or {})
        request = Request(self.base + path, data=raw, headers=h, method=method)
        try:
            response = self.opener.open(request, timeout=35)
        except HTTPError as error:
            response = error
        with response:
            status, response_headers = response.status, response.headers
            url, body = response.geturl(), response.read()
        return status, response_headers, body, url

    def json(self, method, path, data=None, expected=200, headers=None):
        status, response_headers, body, url = self.request(method, path, data, headers)
        if status != expected:
            raise RuntimeError(f"Unexpected HTTP {status} at {method} {path}; expected {expected}")
        try:
            return json.loads(body), response_headers
        except json.JSONDecodeError as error:
            raise RuntimeError(f"Non-JSON response at {method} {path}") from error

    def start(self):
        payload, headers = self.json("GET", "/api/session")
        self.csrf = payload.get("csrf", "")
        self.started = bool(self.csrf)
        return payload, headers

    def state(self):
        return self.json("GET", "/api/state")[0]

    def scenario(self, name):
        return self.json("POST", "/api/scenarios/run", {"scenario": name})[0]

    def duplicate_cookie_client(self):
        client = Client(self.base)
        for cookie in self.cookies:
            client.cookies.set_cookie(copy.copy(cookie))
        return client


def check_sensitive_keys(value):
    sensitive = {"csrf", "session_id", "cookie", "authorization", "access_token", "secret"}
    if isinstance(value, dict):
        return any(str(k).lower() in sensitive or check_sensitive_keys(v) for k, v in value.items())
    if isinstance(value, list):
        return any(check_sensitive_keys(v) for v in value)
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output", type=Path, default=ROOT / "evidencias/site_publico_verificado.json")
    parser.add_argument("--samples", type=Path, default=ROOT / "app/samples")
    args = parser.parse_args()
    args.url = args.url.rstrip("/")
    parsed = urlsplit(args.url)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc or parsed.username or parsed.password:
        parser.error("Use an HTTP(S) origin without credentials.")

    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "url": args.url,
        "method": "Real HTTP requests to the public deployment, Python standard library, fresh cookie sessions; no authentication or bypass token.",
        "scope": "Synthetic demonstration only; public HTTP/API verification, not a human usability interview, load test or real emergency notification.",
        "human_participants": 0,
        "external_messages_requested": 0,
        "checks": [],
        "cleanup": [],
    }
    clients = []

    def record(name, expected, observed):
        passed = observed == expected
        report["checks"].append({"check": name, "expected": expected, "observed": observed, "passed": passed})
        print(f"{'PASS' if passed else 'FAIL'} {name}", flush=True)
        return passed

    try:
        anonymous = Client(args.url)
        status, headers, body, final_url = anonymous.request("GET", "/")
        record("public_home_without_login", True, status == 200 and urlsplit(final_url).netloc == parsed.netloc and b"<html" in body.lower())
        health, _ = anonymous.json("GET", "/api/health")
        report["health"] = {k: health.get(k) for k in ("status", "version", "mode", "storage")}
        record("live_database_health", {"status": "ok", "mode": "synthetic-demo", "storage": "cloudflare-d1"}, {k: health.get(k) for k in ("status", "mode", "storage")})
        status = anonymous.request("GET", "/api/state")[0]
        record("anonymous_state_rejected", 401, status)

        a = Client(args.url)
        clients.append(a)
        session, headers = a.start()
        record("session_created_with_cookie_and_csrf", True, a.started and any(c.name == "ac_workspace" for c in a.cookies))
        cookie_header = headers.get("Set-Cookie", "")
        record("session_cookie_security_flags", True, all(flag in cookie_header for flag in ("HttpOnly", "SameSite=Strict", "Secure")))
        record("external_delivery_disabled", False, session.get("external_delivery_enabled"))
        record("fresh_session_starts_empty", [0, 0, 0], [a.state()["metrics"][k] for k in ("places", "notifications", "confirmed")])

        fields_by_zone = {}
        for zone in ("A", "B", "C"):
            pdf = (args.samples / f"comprovante_{zone}.pdf").read_bytes()
            expected_fields = json.loads((args.samples / f"gabarito_{zone}.json").read_text("utf-8"))
            boundary = "ac-test-" + uuid.uuid4().hex
            payload = (
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"comprovante_{zone}.pdf\"\r\nContent-Type: application/pdf\r\n\r\n".encode()
                + pdf + f"\r\n--{boundary}--\r\n".encode()
            )
            status, _, response_body, _ = a.request("POST", "/api/documents/extract", headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, raw=payload)
            if status != 200:
                raise RuntimeError(f"PDF {zone} extraction returned HTTP {status}")
            extracted = json.loads(response_body)
            fields_by_zone[zone] = extracted["fields"]
            record(f"real_pdf_{zone}_matches_ground_truth", expected_fields, extracted.get("fields"))
            record(f"pdf_{zone}_requires_review_without_storage", ["texto_pdf", True, False, []], [extracted.get("method"), extracted.get("review_required"), extracted.get("stored"), extracted.get("missing_fields")])

        def place(zone):
            return {**fields_by_zone[zone], "chuva": True, "calor": True, "consent": True, "synthetic": True}

        status = a.request("POST", "/api/places", place("A"), {"X-CSRF-Token": "invalid-test-value"})[0]
        record("invalid_csrf_rejected", 403, status)
        status = a.request("POST", "/api/places", place("A"), {"Origin": "https://unrelated.example"})[0]
        record("foreign_origin_rejected", 403, status)
        record("rejected_writes_leave_no_place", 0, a.state()["metrics"]["places"])

        for zone in ("A", "B"):
            created, _ = a.json("POST", "/api/places", place(zone), expected=201)
            record(f"synthetic_place_{zone}_saved", True, created.get("saved"))
        record("two_places_persisted", 2, a.state()["metrics"]["places"])

        rain = a.scenario("chuva")
        record("rain_creates_only_one_notification", 1, rain.get("created"))
        record("place_B_excluded_by_region", 1, rain.get("reasons", {}).get("fora_da_area"))
        before = a.state()
        report["before_confirmation"] = before["metrics"]
        record("notification_targets_place_A", ["TESTE-A"], [n.get("zone") for n in before["notifications"]])
        record("before_reading_counter", [1, 0, 1], [before["metrics"][k] for k in ("notifications", "confirmed", "unread")])
        nid = before["notifications"][0]["id"]
        route = f"/api/notifications/{nid}/confirm"
        confirmation, _ = a.json("POST", route)
        record("reading_confirmation_saved", True, confirmation.get("confirmed") and bool(confirmation.get("read_at")))
        after = a.state()
        report["after_confirmation"] = after["metrics"]
        record("after_reading_counter_and_rate", [1, 1, 0, 100], [after["metrics"][k] for k in ("notifications", "confirmed", "unread", "confirmation_rate")])
        repeated, _ = a.json("POST", route)
        record("repeat_confirmation_is_idempotent", True, repeated.get("already_confirmed") is True and repeated.get("read_at") == confirmation.get("read_at"))
        record("rain_reprocessing_is_idempotent", 0, a.scenario("chuva").get("created"))
        outside = a.scenario("fora")
        record("region_C_excludes_A_and_B", [0, 2], [outside.get("created"), outside.get("reasons", {}).get("fora_da_area")])
        stable = a.state()
        record("single_notification_preserved", 1, stable["metrics"]["notifications"])

        same_cookie = a.duplicate_cookie_client()
        persisted = same_cookie.state()
        record("new_http_client_same_cookie_preserves_state", stable["metrics"], persisted["metrics"])
        b = Client(args.url)
        clients.append(b)
        b.start()
        record("other_visitor_starts_isolated", [0, 0, 0], [b.state()["metrics"][k] for k in ("places", "notifications", "confirmed")])
        record("other_visitor_cannot_confirm_our_notification", 404, b.request("POST", route)[0])

        exported, _ = a.json("GET", "/api/export")
        record("json_export_matches_session", stable["metrics"], exported["metrics"])
        text = json.dumps(exported, ensure_ascii=False)
        secrets = [a.csrf, b.csrf] + [c.value for client in clients for c in client.cookies]
        record("json_export_has_no_session_secrets", True, not check_sensitive_keys(exported) and all(secret not in text for secret in secrets if secret))
        status, headers, content, _ = a.request("GET", "/api/export.csv")
        rows = list(csv.reader(io.StringIO(content.decode("utf-8-sig"))))
        record("csv_export_contains_real_notification", True, status == 200 and len(rows) == 2 and rows[1][1] == "TESTE-A" and rows[1][4] == "internal")
        record("only_internal_channels_and_no_external_deliveries", True, exported["metrics"]["external_deliveries"] == 0 and all(n.get("channel") == "internal" for n in exported["notifications"]))
        report["final_metrics_before_cleanup"] = exported["metrics"]
        report["external_messages_sent_as_reported_by_application"] = exported["metrics"]["external_deliveries"]
    except (URLError, OSError, RuntimeError, KeyError, IndexError, ValueError) as error:
        report["execution_error"] = {"type": type(error).__name__, "message": str(error)[:400]}
        print("ERROR " + type(error).__name__, flush=True)
    finally:
        for index, client in enumerate(clients, 1):
            if not client.started:
                continue
            try:
                result, _ = client.json("POST", "/api/reset", {"confirm": "APAGAR"})
                metrics = client.state()["metrics"]
                clean = result.get("reset") is True and all(metrics[k] == 0 for k in ("places", "notices", "notifications"))
                report["cleanup"].append({"test_session": index, "success": clean})
            except Exception as error:
                report["cleanup"].append({"test_session": index, "success": False, "error_type": type(error).__name__})
        checks = report["checks"]
        report["completed_at"] = datetime.now(timezone.utc).isoformat()
        report["total_checks"] = len(checks)
        report["passed_checks"] = sum(item["passed"] for item in checks)
        report["failed_checks"] = sum(not item["passed"] for item in checks)
        report["success"] = bool(checks) and report["failed_checks"] == 0 and "execution_error" not in report and all(item["success"] for item in report["cleanup"])
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", "utf-8")
        lines = [
            "AlertaCidadão — verificação HTTP pública",
            "URL: " + args.url,
            "Início UTC: " + report["checked_at"],
            "Fim UTC: " + report["completed_at"],
            f"Resultado: {report['passed_checks']}/{report['total_checks']} verificações aprovadas",
            "Sessões próprias de teste; documentos sintéticos; nenhuma autenticação ou token de bypass.",
            "Cookies e CSRF mantidos somente em memória e omitidos das evidências.",
            "Este teste não comprova usabilidade humana, entrega externa ou redução de danos.",
            "",
        ]
        lines += [("PASS " if item["passed"] else "FAIL ") + item["check"] for item in checks]
        lines += ["", "Limpeza das sessões próprias: " + json.dumps(report["cleanup"], ensure_ascii=False)]
        if "execution_error" in report:
            lines.append("Erro de execução: " + json.dumps(report["execution_error"], ensure_ascii=False))
        args.output.with_suffix(".txt").write_text("\n".join(lines) + "\n", "utf-8")
        print(f"RESULT {report['passed_checks']}/{report['total_checks']} success={report['success']}", flush=True)
    return 0 if report["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
