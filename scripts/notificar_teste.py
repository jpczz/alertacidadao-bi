"""Explicit, operator-only Twilio test. Default mode sends NOTHING."""
import argparse,json,sys
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from app.messaging import TwilioConfig,TwilioAdapter,MessagingError

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--send',action='store_true',help='Actually call the provider; may incur costs.')
p.add_argument('--acknowledge-costs',action='store_true')
p.add_argument('--poll',help='Check an existing SM... message; does not send a new one.')
p.add_argument('--output',default='prova_provedor.json')
a=p.parse_args()
if not a.send and not a.poll:
    print('DRY RUN: nenhum envio. Leia 07_publicacao/MENSAGERIA.md antes de habilitar.')
    sys.exit(0)
if a.send and not a.acknowledge_costs:p.error('--send exige --acknowledge-costs e destinatario de teste optante.')
try:
    adapter=TwilioAdapter(TwilioConfig.from_environment())
    result=adapter.status(a.poll) if a.poll else adapter.send_test('Teste do AlertaCidadao. Consulte a central de demonstracao. Nenhum risco real esta sendo informado.',authorized=True)
    result['checked_at']=datetime.now(timezone.utc).isoformat()
    result['academic_test']=True
    Path(a.output).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
except MessagingError as e:print(str(e),file=sys.stderr);sys.exit(1)
