"""Optional outbound adapter. Disabled unless explicitly configured and authorized.
This module is not exposed through the public demo API. Never call from a public
session: a recipient is fixed by an operator-controlled environment variable.
"""
import os,re
from dataclasses import dataclass
import httpx

class MessagingError(RuntimeError):pass

@dataclass(frozen=True)
class TwilioConfig:
    sid:str
    token:str
    sender:str
    recipient:str
    content_sid:str=''

    @classmethod
    def from_environment(cls):
        cfg=cls(os.getenv('TWILIO_ACCOUNT_SID',''),os.getenv('TWILIO_AUTH_TOKEN',''),os.getenv('TWILIO_FROM',''),os.getenv('TWILIO_TEST_TO',''),os.getenv('TWILIO_CONTENT_SID',''))
        if not re.fullmatch(r'AC[a-fA-F0-9]{32}',cfg.sid):raise MessagingError('Configure TWILIO_ACCOUNT_SID com um SID valido.')
        if not cfg.token or not cfg.sender or not cfg.recipient:raise MessagingError('Configure as variaveis TWILIO_AUTH_TOKEN, TWILIO_FROM e TWILIO_TEST_TO.')
        for address in (cfg.sender,cfg.recipient):
            if not re.fullmatch(r'(whatsapp:)?\+[1-9][0-9]{7,14}',address):raise MessagingError('Use destino de teste autorizado em formato E.164, com whatsapp: para esse canal.')
        if cfg.sender.startswith('whatsapp:')!=cfg.recipient.startswith('whatsapp:'):raise MessagingError('Origem e destino devem usar o mesmo canal.')
        if cfg.content_sid and not re.fullmatch(r'HX[a-fA-F0-9]{32}',cfg.content_sid):raise MessagingError('Content SID invalido.')
        return cfg

class TwilioAdapter:
    def __init__(self,config:TwilioConfig,client:httpx.Client|None=None):
        self.config=config;self.client=client or httpx.Client(timeout=20)
    def send_test(self,body:str,authorized:bool=False):
        if not authorized:raise MessagingError('Envio bloqueado: autorize explicitamente o teste e seu custo.')
        cfg=self.config
        data={'From':cfg.sender,'To':cfg.recipient}
        if cfg.content_sid:data['ContentSid']=cfg.content_sid
        else:data['Body']='[DEMONSTRACAO ACADEMICA - NAO E ALERTA REAL] '+body[:800]
        url=f'https://api.twilio.com/2010-04-01/Accounts/{cfg.sid}/Messages.json'
        try:
            r=self.client.post(url,data=data,auth=(cfg.sid,cfg.token))
            r.raise_for_status();result=r.json()
        except (httpx.HTTPError,ValueError) as exc:raise MessagingError('Falha no provedor. Verifique conta, adesao ao sandbox, template e logs privados do provedor.') from exc
        return {'message_sid':result.get('sid'),'provider_status':result.get('status','unknown'),'delivery_confirmed':result.get('status') in ('delivered','read'),'test_recipient_suffix':cfg.recipient[-4:]}
    def status(self,message_sid:str):
        if not re.fullmatch(r'SM[a-fA-F0-9]{32}',message_sid):raise MessagingError('Message SID invalido.')
        cfg=self.config
        try:
            r=self.client.get(f'https://api.twilio.com/2010-04-01/Accounts/{cfg.sid}/Messages/{message_sid}.json',auth=(cfg.sid,cfg.token))
            r.raise_for_status();result=r.json()
        except (httpx.HTTPError,ValueError) as exc:raise MessagingError('Nao foi possivel consultar o estado no provedor.') from exc
        status=result.get('status','unknown')
        return {'message_sid':message_sid,'provider_status':status,'delivery_confirmed':status in ('delivered','read'),'error_code':result.get('error_code')}
