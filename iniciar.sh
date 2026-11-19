#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
printf '\nAbra http://127.0.0.1:8000 no navegador.\n'
exec .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
