from datetime import datetime,timezone,timedelta
import pytest
from app.domain import make_notice, eligible

NOW=datetime(2026,11,17,15,tzinfo=timezone.utc)
P={'zone':'TESTE-A','consent':True,'chuva':True,'calor':True}

@pytest.mark.parametrize('scenario,expected,reason',[
 ('chuva',True,'elegivel'),('calor',True,'elegivel'),('fora',False,'fora_da_area'),
 ('expirado',False,'expirado'),('futuro',False,'futuro'),('cancelado',False,'cancelado'),
 ('atualizacao',True,'elegivel')])
def test_eligibility(scenario,expected,reason):
    assert eligible(P,make_notice(scenario,NOW).as_dict(),NOW)==(expected,reason)

def test_disabled_heat():
    assert eligible(P|{'calor':False},make_notice('calor',NOW).as_dict(),NOW)==(False,'preferencia_desativada')

def test_no_consent():
    assert eligible(P|{'consent':False},make_notice('chuva',NOW).as_dict(),NOW)==(False,'sem_consentimento')

def test_expiry_boundary_excluded():
    n=make_notice('chuva',NOW)
    assert eligible(P,n.as_dict(),n.ends_at)==(False,'expirado')

def test_start_boundary_included():
    n=make_notice('chuva',NOW)
    assert eligible(P,n.as_dict(),n.starts_at)==(True,'elegivel')

def test_unknown_scenario_rejected():
    with pytest.raises(ValueError):make_notice('unknown',NOW)
