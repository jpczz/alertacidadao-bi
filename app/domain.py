"""Deterministic eligibility rules. All shipped scenarios are synthetic."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal

ZONES = {"TESTE-A": "Jardim Exemplo A", "TESTE-B": "Jardim Exemplo B", "TESTE-C": "Jardim Exemplo C"}

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def iso(value: datetime) -> str:
    return value.isoformat(timespec="milliseconds")

def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

@dataclass(frozen=True)
class Notice:
    code: str
    version: int
    kind: Literal['chuva', 'calor']
    title: str
    severity: str
    zones: tuple[str, ...]
    starts_at: datetime
    ends_at: datetime
    status: str = 'active'
    body: str = 'Cen\u00e1rio sint\u00e9tico para avaliar a comunica\u00e7\u00e3o. N\u00e3o \u00e9 um alerta real.'
    source: str = 'Laborat\u00f3rio AlertaCidad\u00e3o'

    def as_dict(self):
        return {**self.__dict__, 'zones': list(self.zones), 'starts_at': iso(self.starts_at), 'ends_at': iso(self.ends_at), 'synthetic': True}

SCENARIOS = {
    'chuva': ('Chuva intensa', 'Um aviso sint\u00e9tico para a \u00e1rea TESTE-A.'),
    'calor': ('Calor extremo', 'Um aviso sint\u00e9tico para as \u00e1reas TESTE-A e TESTE-B.'),
    'fora': ('Outra regi\u00e3o', 'Aviso apenas para TESTE-C: verifica a exclus\u00e3o territorial.'),
    'expirado': ('Aviso expirado', 'Fora da validade; nenhuma nova notifica\u00e7\u00e3o deve ser criada.'),
    'futuro': ('Aviso futuro', 'Ainda n\u00e3o vigente; n\u00e3o deve notificar.'),
    'cancelado': ('Aviso cancelado', 'Um aviso cancelado na origem n\u00e3o deve notificar.'),
    'atualizacao': ('Atualiza\u00e7\u00e3o de chuva', 'Vers\u00e3o 2 do mesmo aviso: uma nova comunica\u00e7\u00e3o.'),
    'falha': ('Fonte indispon\u00edvel', 'Falha controlada de coleta, sem inventar novos avisos.'),
}

def make_notice(scenario: str, now: datetime | None = None) -> Notice:
    now = now or utcnow()
    base = dict(code='CHUVA-A', version=1, kind='chuva', title='Chuva intensa na \u00e1rea de teste A', severity='Aten\u00e7\u00e3o', zones=('TESTE-A',), starts_at=now-timedelta(minutes=5), ends_at=now+timedelta(hours=6))
    changes = {
        'chuva': {},
        'calor': dict(code='CALOR-AB', kind='calor', title='Calor extremo nas \u00e1reas de teste A e B', severity='Aten\u00e7\u00e3o', zones=('TESTE-A','TESTE-B')),
        'fora': dict(code='CHUVA-C', title='Chuva na \u00e1rea de teste C', zones=('TESTE-C',)),
        'expirado': dict(code='EXPIRADO-A', title='Aviso de teste expirado', starts_at=now-timedelta(hours=5), ends_at=now-timedelta(hours=1)),
        'futuro': dict(code='FUTURO-A', title='Aviso de teste futuro', starts_at=now+timedelta(hours=2), ends_at=now+timedelta(hours=8)),
        'cancelado': dict(code='CANCELADO-A', title='Aviso de teste cancelado', status='cancelled'),
        'atualizacao': dict(version=2, title='Atualiza\u00e7\u00e3o: chuva na \u00e1rea de teste A'),
    }
    if scenario not in changes:
        raise ValueError('Cen\u00e1rio desconhecido.')
    return Notice(**(base | changes[scenario]))

def eligible(place: dict, notice: dict, now: datetime | None = None) -> tuple[bool, str]:
    now=now or utcnow()
    if notice['status'] != 'active': return False, 'cancelado'
    if now < parse_time(notice['starts_at']): return False, 'futuro'
    if now >= parse_time(notice['ends_at']): return False, 'expirado'
    if not place['consent']: return False, 'sem_consentimento'
    if place['zone'] not in notice['zones']: return False, 'fora_da_area'
    if not place[notice['kind']]: return False, 'preferencia_desativada'
    return True, 'elegivel'
