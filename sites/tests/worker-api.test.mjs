import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { handleApi } from '../worker/api.js';

// D1-shaped adapter over a real SQLite engine. No HTTP responses or SQL results are stubbed.
class LocalD1 {
  constructor() {
    this.sqlite = new DatabaseSync(':memory:');
    this.sqlite.exec('PRAGMA foreign_keys=ON;');
    this.sqlite.exec(readFileSync(new URL('../drizzle/0000_init.sql', import.meta.url), 'utf8'));
  }
  prepare(sql) {
    const db = this.sqlite;
    const make = args => ({
      bind: (...bound) => make(bound),
      first: async () => db.prepare(sql).get(...args) || null,
      all: async () => ({ results: db.prepare(sql).all(...args), success: true }),
      run: async () => { const result = db.prepare(sql).run(...args); return { success: true, meta: { changes: Number(result.changes) } }; },
    });
    return make([]);
  }
  async batch(statements) {
    this.sqlite.exec('BEGIN');
    try { const results = []; for (const statement of statements) results.push(await statement.run()); this.sqlite.exec('COMMIT'); return results; }
    catch (error) { this.sqlite.exec('ROLLBACK'); throw error; }
  }
}
const sample = suffix => ({ label: 'Local de teste ' + suffix, street: 'Rua Exemplo ' + suffix, number: '120', neighborhood: 'Jardim Exemplo ' + suffix, city: 'Cidade Exemplo', state: 'SP', postal_code: suffix === 'A' ? '00000-001' : suffix === 'B' ? '00000-002' : '00000-003', zone: 'TESTE-' + suffix, chuva: true, calor: true, consent: true, synthetic: true });
async function client(db = new LocalD1()) {
  const env = { DB: db }; let cookie = '', csrf = '';
  const request = async (method, path, body, extra = {}) => {
    const headers = { cookie, 'X-CSRF-Token': csrf, ...extra };
    let payload = body;
    if (body !== undefined && !(body instanceof FormData) && !(body instanceof Uint8Array)) { headers['Content-Type'] = 'application/json'; payload = JSON.stringify(body); }
    const response = await handleApi(new Request('https://test.example' + path, { method, headers, body: payload }), env);
    return response;
  };
  const sessionResponse = await request('GET', '/api/session'); assert.equal(sessionResponse.status, 200);
  cookie = sessionResponse.headers.get('set-cookie').split(';')[0]; csrf = (await sessionResponse.json()).csrf;
  const json = async (method, path, body, expected = 200, headers) => { const res = await request(method, path, body, headers); const data = await res.json(); assert.equal(res.status, expected, JSON.stringify(data)); return data; };
  return { db, env, request, json, cookie, csrf, state: () => json('GET', '/api/state'), run: kind => json('POST', '/api/scenarios/run', { scenario: kind }), add: data => json('POST', '/api/places', data, 201) };
}

test('complete controlled A/B journey: 12 expected outcomes, no external sends', async () => {
  const c = await client(); const checks = [];
  const record = (name, expected, observed) => { assert.deepEqual(observed, expected, name); checks.push({ check: name, expected, observed, passed: true }); };
  await c.add(sample('A')); await c.add(sample('B'));
  record('two_synthetic_places', 2, (await c.state()).metrics.places);
  const rain = await c.run('chuva'); record('rain_A_only', 1, rain.created); record('B_excluded', 1, rain.reasons.fora_da_area);
  const before = await c.state(); record('before_confirmation', 0, before.metrics.confirmed);
  const nid = before.notifications[0].id;
  await c.json('POST', `/api/notifications/${nid}/confirm`);
  const after = await c.state(); record('after_confirmation', 1, after.metrics.confirmed); record('confirmation_rate', 100, after.metrics.confirmation_rate);
  record('repeat_deduplicated', 0, (await c.run('chuva')).created);
  record('C_excludes_A_and_B', 0, (await c.run('fora')).created);
  record('one_notification_total', 1, (await c.state()).metrics.notifications);
  record('external_sends', 0, (await c.state()).metrics.external_deliveries);
  const other = await client(c.db); record('other_session_isolated', 0, (await other.state()).metrics.places);
  record('export_consistency', 1, (await c.json('GET', '/api/export')).metrics.confirmed);
  const dir = new URL('./evidence/', import.meta.url); mkdirSync(dir, { recursive: true });
  writeFileSync(new URL('worker-controlled-journey.json', dir), JSON.stringify({ checked_at: new Date().toISOString(), method: 'Worker Request/Response handlers backed by real SQLite via a D1-shaped adapter. No public deployment or human participants implied.', before: before.metrics, after: after.metrics, checks, human_participants: 0, external_messages_sent: 0 }, null, 2));
});

test('CSRF, origin and anonymous requests are rejected', async () => {
  const c = await client();
  assert.equal((await handleApi(new Request('https://test.example/api/state'), c.env)).status, 401);
  assert.equal((await c.request('POST', '/api/places', sample('A'), { 'X-CSRF-Token': '' })).status, 403);
  assert.equal((await c.request('POST', '/api/places', sample('A'), { Origin: 'https://other.example' })).status, 403);
  const r = await c.request('GET', '/api/session'); assert.match(r.headers.get('set-cookie'), /HttpOnly.*SameSite=Strict.*Secure/);
});

test('requires synthetic data, coherent zone, plain text and explicit consent', async () => {
  const c = await client();
  for (const patch of [{ synthetic: false }, { postal_code: '01310-100' }, { zone: 'TESTE-B' }, { label: '<b>bad</b>' }, { unknown: 1 }]) await c.json('POST', '/api/places', { ...sample('A'), ...patch }, 422);
  const noConsent = sample('A'); delete noConsent.consent; await c.json('POST', '/api/places', noConsent, 422);
  await c.json('POST', '/api/scenarios/run', { scenario: 'toString' }, 422);
});

test('duplicate places and maximum of ten places are enforced', async () => {
  const c = await client(); await c.add(sample('A'));
  await c.json('POST', '/api/places', sample('A'), 409);
  for (let i = 1; i < 10; i++) await c.add({ ...sample('A'), number: String(120 + i) });
  await c.json('POST', '/api/places', { ...sample('A'), number: '999' }, 422);
});

test('invalid temporal scenarios and failed source never create notifications', async () => {
  const c = await client(); await c.add(sample('A'));
  for (const kind of ['expirado', 'futuro', 'cancelado']) assert.equal((await c.run(kind)).created, 0);
  const before = (await c.state()).metrics.notices;
  assert.equal((await c.run('falha')).status, 'source_unavailable');
  assert.equal((await c.state()).metrics.notices, before); assert.equal((await c.state()).metrics.notifications, 0);
});

test('preferences and revoked consent control subsequent notifications', async () => {
  const c = await client(); const p = await c.add({ ...sample('A'), calor: false });
  assert.equal((await c.run('calor')).reasons.preferencia_desativada, 1);
  await c.json('PATCH', '/api/places/' + p.id, { chuva: true, calor: true, consent: false });
  assert.equal((await c.run('chuva')).reasons.sem_consentimento, 1);
});

test('versions and readings are idempotent and counters use latest notice', async () => {
  const c = await client(); await c.add(sample('A')); await c.run('chuva');
  assert.equal((await c.run('atualizacao')).created, 1); assert.equal((await c.run('atualizacao')).created, 0);
  assert.deepEqual((await c.run('chuva')).reasons, { versao_superada: 1 });
  const s = await c.state(); assert.equal(s.metrics.active_notices, 1); assert.equal(s.metrics.notifications, 2);
  const route = `/api/notifications/${s.notifications[0].id}/confirm`;
  const a = await c.json('POST', route), b = await c.json('POST', route);
  assert.equal(a.read_at, b.read_at); assert.equal(b.already_confirmed, true);
  assert.equal((await c.state()).events.filter(e => e.kind === 'reading_confirmed').length, 1);
});

test('new place only receives current notice version', async () => {
  const c = await client(); await c.run('chuva'); await c.run('atualizacao'); await c.add(sample('A'));
  const s = await c.state(); assert.equal(s.notifications.length, 1); assert.equal(s.notifications[0].notice.version, 2);
});

test('cross-session access, deletion cascade and reset remain isolated', async () => {
  const a = await client(), b = await client(a.db); const p = await a.add(sample('A')); await a.run('chuva'); await b.add(sample('B'));
  const nid = (await a.state()).notifications[0].id;
  await b.json('DELETE', '/api/places/' + p.id, undefined, 404); await b.json('POST', `/api/notifications/${nid}/confirm`, undefined, 404);
  await a.json('DELETE', '/api/places/' + p.id); assert.equal((await a.state()).metrics.notifications, 0);
  await a.json('POST', '/api/reset', { confirm: 'yes' }, 422); await a.json('POST', '/api/reset', { confirm: 'APAGAR' });
  assert.equal((await b.state()).metrics.places, 1);
});

test('exports omit secrets and escape spreadsheet formulas', async () => {
  const c = await client(); await c.add({ ...sample('A'), label: '=2+2' }); await c.run('chuva');
  const json = await (await c.request('GET', '/api/export')).text(); assert.ok(!json.includes('csrf')); assert.ok(!json.includes('session_id')); assert.ok(!json.includes(c.csrf));
  const csv = await (await c.request('GET', '/api/export.csv')).text(); assert.ok(csv.includes("'=2+2"));
});

test('request body limit protects even routes with no JSON payload', async () => {
  const c = await client();
  assert.equal((await c.request('POST', '/api/scenarios/run', new Uint8Array(2 * 1024 * 1024 + 100001))).status, 413);
  assert.equal((await c.request('POST', '/api/notifications/none/confirm', new Uint8Array(2 * 1024 * 1024 + 100001))).status, 413);
});

test('real sample PDFs are parsed against ground truth; images fail clearly', async () => {
  const c = await client();
  const base = new URL('../public/samples/', import.meta.url);
  for (const zone of ['A', 'B', 'C']) {
    const form = new FormData(); form.append('file', new Blob([readFileSync(new URL('comprovante_' + zone + '.pdf', base))], { type: 'application/pdf' }), zone + '.pdf');
    const result = await c.json('POST', '/api/documents/extract', form);
    assert.deepEqual(result.fields, JSON.parse(readFileSync(new URL('gabarito_' + zone + '.json', base), 'utf8')));
    assert.equal(result.method, 'texto_pdf'); assert.equal(result.stored, false); assert.equal(result.review_required, true);
  }
  const image = new FormData(); image.append('file', new Blob([new Uint8Array([137, 80, 78, 71])], { type: 'image/png' }), 'example.png');
  const response = await c.json('POST', '/api/documents/extract', image, 422); assert.match(response.detail, /OCR.*Python/);
});
