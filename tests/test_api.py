import json
from fastapi.testclient import TestClient

def add(client,data):
    result=client.post('/api/places',json=data)
    assert result.status_code==201,result.text
    return result.json()['id']

def run(client,scenario='chuva'):
    r=client.post('/api/scenarios/run',json={'scenario':scenario})
    assert r.status_code==200,r.text
    return r.json()

def test_health_and_static(client):
    assert client.get('/api/health').json()['status']=='ok'
    r=client.get('/')
    assert r.status_code==200 and 'app.js' in r.text
    assert client.get('/static/app.js').status_code==200

def test_complete_journey(client,place_data):
    add(client,place_data)
    assert run(client)['created']==1
    s=client.get('/api/state').json()
    assert s['metrics']['confirmed']==0
    nid=s['notifications'][0]['id']
    assert client.post(f'/api/notifications/{nid}/confirm').json()['confirmed'] is True
    s=client.get('/api/state').json()
    assert s['metrics']['confirmed']==1 and s['metrics']['confirmation_rate']==100
    assert any(e['kind']=='reading_confirmed' for e in s['events'])

def test_persistence_across_requests(client,place_data):
    add(client,place_data)
    assert client.get('/api/state').json()['metrics']['places']==1
    assert client.get('/api/session').status_code==200
    assert client.get('/api/state').json()['metrics']['places']==1

def test_duplicate_notice_is_idempotent(client,place_data):
    add(client,place_data);run(client)
    second=run(client)
    assert second['created']==0 and second['reasons']['duplicado']==1
    assert client.get('/api/state').json()['metrics']['notifications']==1

def test_duplicate_read_is_idempotent(client,place_data):
    add(client,place_data);run(client)
    nid=client.get('/api/state').json()['notifications'][0]['id']
    a=client.post(f'/api/notifications/{nid}/confirm').json()
    b=client.post(f'/api/notifications/{nid}/confirm').json()
    assert a['read_at']==b['read_at'] and b['already_confirmed']
    events=client.get('/api/state').json()['events']
    assert sum(e['kind']=='reading_confirmed' for e in events)==1

def test_version_update_notifies_once(client,place_data):
    add(client,place_data);run(client)
    assert run(client,'atualizacao')['created']==1
    assert run(client,'atualizacao')['created']==0
    assert client.get('/api/state').json()['metrics']['notifications']==2

def test_old_version_after_update_ignored(client,place_data):
    add(client,place_data);run(client,'atualizacao')
    assert run(client,'chuva')['reasons']=={'versao_superada':1}

def test_outside_area(client,place_data):
    add(client,place_data)
    assert run(client,'fora')['created']==0

def test_heat_disabled(client,place_data):
    add(client,place_data|{'calor':False})
    r=run(client,'calor')
    assert r['created']==0 and r['reasons']['preferencia_desativada']==1

def test_consent_revoked(client,place_data):
    pid=add(client,place_data)
    r=client.patch(f'/api/places/{pid}',json={'chuva':True,'calor':True,'consent':False})
    assert r.status_code==200
    assert run(client)['reasons']['sem_consentimento']==1

def test_missing_consent_rejected(client,place_data):
    del place_data['consent']
    assert client.post('/api/places',json=place_data).status_code==422

def test_expired_future_cancelled(client,place_data):
    add(client,place_data)
    for kind in ['expirado','futuro','cancelado']:
        assert run(client,kind)['created']==0
    assert client.get('/api/state').json()['metrics']['notifications']==0

def test_source_failure_does_not_invent_notice(client,place_data):
    add(client,place_data)
    r=run(client,'falha')
    assert r['status']=='source_unavailable'
    assert client.get('/api/state').json()['metrics']['notices']==0
    assert client.get('/api/state').json()['events'][0]['kind']=='source_failed'

def test_new_place_receives_existing_current_notice(client,place_data):
    run(client)
    add(client,place_data)
    assert client.get('/api/state').json()['metrics']['notifications']==1

def test_new_place_ignores_superseded_version(client,place_data):
    run(client);run(client,'atualizacao');add(client,place_data)
    ns=client.get('/api/state').json()['notifications']
    assert len(ns)==1 and ns[0]['notice']['version']==2

def test_place_duplicate_rejected(client,place_data):
    add(client,place_data)
    assert client.post('/api/places',json=place_data).status_code==409

def test_only_synthetic_postal_code(client,place_data):
    assert client.post('/api/places',json=place_data|{'postal_code':'01310-100'}).status_code==422
    assert client.post('/api/places',json=place_data|{'synthetic':False}).status_code==422

def test_zone_postal_code_must_match(client,place_data):
    assert client.post('/api/places',json=place_data|{'zone':'TESTE-B'}).status_code==422

def test_missing_csrf_rejected(client,place_data):
    del client.headers['X-CSRF-Token']
    assert client.post('/api/places',json=place_data).status_code==403

def test_cross_origin_rejected(client,place_data):
    assert client.post('/api/places',json=place_data,headers={'Origin':'https://evil.example'}).status_code==403

def test_anonymous_state_denied(app):
    with TestClient(app) as c: assert c.get('/api/state').status_code==401

def test_session_isolation(app,client,place_data):
    pid=add(client,place_data);run(client)
    nid=client.get('/api/state').json()['notifications'][0]['id']
    with TestClient(app) as b:
        b.headers['X-CSRF-Token']=b.get('/api/session').json()['csrf']
        assert b.get('/api/state').json()['metrics']['places']==0
        assert b.delete(f'/api/places/{pid}').status_code==404
        assert b.post(f'/api/notifications/{nid}/confirm').status_code==404

def test_reset_only_own_session(app,client,place_data):
    add(client,place_data)
    with TestClient(app) as b:
        b.headers['X-CSRF-Token']=b.get('/api/session').json()['csrf']
        add(b,place_data)
        assert client.post('/api/reset',json={'confirm':'APAGAR'}).status_code==200
        assert client.get('/api/state').json()['metrics']['places']==0
        assert b.get('/api/state').json()['metrics']['places']==1

def test_reset_requires_confirmation(client,place_data):
    add(client,place_data)
    assert client.post('/api/reset',json={'confirm':'yes'}).status_code==422
    assert client.get('/api/state').json()['metrics']['places']==1

def test_delete_cascades_notifications(client,place_data):
    pid=add(client,place_data);run(client)
    assert client.delete(f'/api/places/{pid}').status_code==200
    assert client.get('/api/state').json()['metrics']['notifications']==0

def test_no_false_external_delivery(client,place_data):
    add(client,place_data);run(client)
    s=client.get('/api/state').json()
    assert s['metrics']['external_deliveries']==0
    assert s['notifications'][0]['channel']=='internal'
    assert client.get('/api/session').json()['external_delivery_enabled'] is False

def test_export_no_tokens(client,place_data):
    add(client,place_data);run(client)
    r=client.get('/api/export')
    assert 'attachment' in r.headers['content-disposition']
    assert 'csrf' not in r.text and 'session_id' not in r.text
    assert r.json()['metrics']['notifications']==1

def test_csv_injection_escaped(client,place_data):
    add(client,place_data|{'label':'=2+2'});run(client)
    r=client.get('/api/export.csv')
    assert "'=2+2" in r.text

def test_security_headers_and_cookie(client):
    r=client.get('/api/session')
    assert 'HttpOnly' in r.headers['set-cookie'] and 'SameSite=strict' in r.headers['set-cookie']
    assert r.headers['x-content-type-options']=='nosniff'
    assert r.headers['cache-control']=='no-store'
    assert "frame-ancestors 'none'" in r.headers['content-security-policy']

def test_markup_rejected(client,place_data):
    assert client.post('/api/places',json=place_data|{'label':'<script>bad</script>'}).status_code==422

def test_oversized_request_rejected(client):
    assert client.post('/api/scenarios/run',content=b'x'*(2*1024*1024+100001)).status_code==413

def test_invalid_scenario_rejected(client):
    assert client.post('/api/scenarios/run',json={'scenario':'inventado'}).status_code==422

def test_unknown_notification_rejected(client):
    assert client.post('/api/notifications/none/confirm').status_code==404

def test_database_reopen_persists_session(tmp_path,place_data):
    from app.main import create_app
    path=str(tmp_path/'persistent.db')
    with TestClient(create_app(path)) as first:
        first.headers['X-CSRF-Token']=first.get('/api/session').json()['csrf']
        add(first,place_data)
        token=first.cookies.get('ac_workspace')
    with TestClient(create_app(path)) as second:
        second.cookies.set('ac_workspace',token)
        assert second.get('/api/state').json()['metrics']['places']==1

def test_chunked_oversized_request_rejected(client):
    def chunks():
        for _ in range(25):yield b'x'*100000
    r=client.post('/api/scenarios/run',content=chunks(),headers={'Content-Type':'application/json'})
    assert r.status_code==413


def test_active_metric_counts_only_latest_version(client,place_data):
    client.post('/api/places',json=place_data)
    client.post('/api/scenarios/run',json={'scenario':'chuva'})
    client.post('/api/scenarios/run',json={'scenario':'atualizacao'})
    metrics=client.get('/api/state').json()['metrics']
    assert metrics['active_notices']==1
    assert metrics['notices']==2
    assert metrics['notifications']==2
