import httpx,pytest
from app.messaging import TwilioAdapter,TwilioConfig,MessagingError
CFG=TwilioConfig('AC'+'1'*32,'private-test-token','whatsapp:+15005550006','whatsapp:+15005550007')

def client(status_code=201,state='queued'):
    return httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(status_code,json={'sid':'SM'+'2'*32,'status':state})))

def test_send_requires_explicit_authorization():
    with pytest.raises(MessagingError):TwilioAdapter(CFG,client()).send_test('test')

def test_queued_is_not_delivery():
    r=TwilioAdapter(CFG,client()).send_test('test',authorized=True)
    assert r['provider_status']=='queued' and not r['delivery_confirmed']

def test_delivery_status_interpreted_separately():
    r=TwilioAdapter(CFG,client(200,'delivered')).status('SM'+'2'*32)
    assert r['delivery_confirmed']

def test_failure_reported_without_credentials():
    with pytest.raises(MessagingError) as e:TwilioAdapter(CFG,client(401)).send_test('test',authorized=True)
    assert CFG.token not in str(e.value)

def test_invalid_message_sid_rejected():
    with pytest.raises(MessagingError):TwilioAdapter(CFG,client()).status('../../unsafe')

def test_unconfigured_adapter_fails_closed(monkeypatch):
    for key in ['TWILIO_ACCOUNT_SID','TWILIO_AUTH_TOKEN','TWILIO_FROM','TWILIO_TEST_TO']:monkeypatch.delenv(key,raising=False)
    with pytest.raises(MessagingError):TwilioConfig.from_environment()
