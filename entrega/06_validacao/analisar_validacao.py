"""Summarize actual CSV entries. Empty files never become success results."""
import argparse,csv,json,statistics
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--csv',default='sessoes_cidadaos.csv');p.add_argument('--output',default='resumo_validacao.json');a=p.parse_args()
with open(a.csv,encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
if not rows:result={'state':'coleta_nao_iniciada','participants':0,'warning':'Nenhum resultado humano foi coletado. Nao preencher com exemplos.'}
else:
 ids=[r['participante_id'].strip() for r in rows]
 if any(not x for x in ids) or len(ids)!=len(set(ids)):p.error('Each participant must have a unique non-empty ID.')
 required=['consentimento','concluiu_cadastro','intervencoes','evento_correto','area_correta','validade_correta','acao_correta','confirmou_leitura']
 for r in rows:
  if r['consentimento']!='1':p.error('Only include consented records; consentimento must be 1.')
  for k in required:
   if not r[k].strip():p.error('Missing actual observation: '+r['participante_id']+'/'+k)
  for k in ['concluiu_cadastro','evento_correto','area_correta','validade_correta','acao_correta','confirmou_leitura']:
   if r[k] not in ('0','1'):p.error('Binary observations use 0 or 1: '+k)
  try:
   if int(r['intervencoes'])<0:raise ValueError()
   if r['tempo_cadastro_s'] and float(r['tempo_cadastro_s'])<0:raise ValueError()
  except ValueError:p.error('Non-negative numeric time/interventions required.')
 times=[float(r['tempo_cadastro_s']) for r in rows if r['tempo_cadastro_s']]
 result={'state':'dados_fornecidos_pelo_grupo_nao_auditados','participants':len(rows),'completed_without_help':sum(r['concluiu_cadastro']=='1' and int(r['intervencoes'])==0 for r in rows),'all_four_information_correct':sum(all(r[k]=='1' for k in ['evento_correto','area_correta','validade_correta','acao_correta']) for r in rows),'median_registration_seconds':statistics.median(times) if times else None,'timed_participants':len(times),'limitations':'Exploratory convenience sample. No population inference or loss reduction claim.'}
Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
