"""Manual browser smoke runner. Not collected by pytest. Use with a running server."""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8000');p.add_argument('--output',default='browser-evidence');p.add_argument('--chromium',default=None);a=p.parse_args()
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=a.chromium)
 page=browser.new_page(viewport={'width':1440,'height':960});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(a.url,wait_until='networkidle');page.locator('a[href="#cadastro"]').first.click();page.wait_for_selector('#place-form')
 page.locator('[data-action=fill][data-zone=A]').click();page.locator('input[name=synthetic]').check();page.locator('button[type=submit]').click();page.wait_for_selector('.place-head')
 page.locator('nav a[href="#laboratorio"]').click();page.locator('[data-scenario=chuva]').click();page.wait_for_timeout(600)
 page.locator('nav a[href="#notificacoes"]').click();page.wait_for_selector('.notification');page.locator('[data-action=confirm]').click();page.wait_for_selector('.notification:not(.unread)')
 page.locator('nav a[href="#institucional"]').click();page.wait_for_selector('.big-ratio');page.screenshot(path=str(out/'painel.png'),full_page=True)
 state=page.evaluate('async()=>await (await fetch("/api/state")).json()');assert state['metrics']['confirmed']==1;assert not errors,errors
 (out/'result.json').write_text(json.dumps({'url':a.url,'confirmed':1,'javascript_errors':errors,'method':'normal browser navigation'},indent=2),encoding='utf-8')
 browser.close();print('Browser smoke passed. This does not test every scenario or accessibility requirement.')
