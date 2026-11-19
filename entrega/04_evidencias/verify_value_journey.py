"""Observed synthetic API journey. No human research or real-world alerts."""
import httpx, json, argparse
from pathlib import Path
from datetime import datetime,timezone
parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8765');parser.add_argument('--output',required=True)
a=parser.parse_args();base=a.url.rstrip('/')
checks=[]
def record(name,expected,observed):
 checks.append({'check':name,'expected':expected,'observed':observed,'passed':expected==observed})
 assert expected==observed,(name,expected,observed)
with httpx.Client(base_url=base,timeout=45,trust_env=False) as c:
 r=c.get('/api/session');r.raise_for_status();c.headers['X-CSRF-Token']=r.json()['csrf']
 def get():
  r=c.get('/api/state');r.raise_for_status();return r.json()
 def scenario(kind):
  r=c.post('/api/scenarios/run',json={'scenario':kind});r.raise_for_status();return r.json()
 try:
  for suffix in ['A','B']:
   p={'label':'Local de teste '+suffix,'street':'Rua Exemplo '+suffix,'number':'120','neighborhood':'Jardim Exemplo '+suffix,'city':'Cidade Exemplo','state':'SP','postal_code':'00000-00'+('1' if suffix=='A' else '2'),'zone':'TESTE-'+suffix,'chuva':True,'calor':True,'consent':True,'synthetic':True}
   r=c.post('/api/places',json=p);r.raise_for_status()
  record('two_synthetic_places',2,get()['metrics']['places'])
  rain=scenario('chuva');record('rain_A_delivered_only_to_A',1,rain['created']);record('B_excluded_by_area',1,rain['reasons'].get('fora_da_area'))
  before=get();record('before_read_confirmation',0,before['metrics']['confirmed']);nid=before['notifications'][0]['id']
  r=c.post('/api/notifications/'+nid+'/confirm');r.raise_for_status()
  after=get();record('after_read_confirmation',1,after['metrics']['confirmed']);record('confirmation_ratio',100.0,after['metrics']['confirmation_rate'])
  repeated=scenario('chuva');record('repeat_does_not_create_notification',0,repeated['created'])
  outside=scenario('fora');record('notice_for_C_excludes_A_and_B',0,outside['created'])
  record('notification_total_remains_one',1,get()['metrics']['notifications'])
  record('external_message_deliveries',0,get()['metrics']['external_deliveries'])
  with httpx.Client(base_url=base,timeout=45,trust_env=False) as other:
   other.get('/api/session').raise_for_status();record('isolated_session_stays_empty',0,other.get('/api/state').json()['metrics']['places'])
  export=c.get('/api/export');export.raise_for_status();record('export_matches_real_session',1,export.json()['metrics']['confirmed'])
  final=get()
  report={'checked_at':datetime.now(timezone.utc).isoformat(),'url':base,'method':'HTTP API with fresh synthetic session; automated technical test, not a user interview','data':'Two fictional places TESTE-A and TESTE-B, one rainfall notice for TESTE-A and one out-of-area notice for TESTE-C','checks':checks,'before':before['metrics'],'after':after['metrics'],'final_metrics':final['metrics'],'functional_benefit_evidenced':'The engine excluded the nonmatching place, created one internal notification, recorded one acknowledgement and avoided reprocessing duplicates. No inference about comprehension, risk reduction, real delivery or willingness to pay.','human_participants':0,'external_messages_sent':0}
  Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2))
  print(json.dumps({'checks':len(checks),'passed':all(c['passed'] for c in checks),'output':a.output}))
 finally:
  c.post('/api/reset',json={'confirm':'APAGAR'}).raise_for_status()
