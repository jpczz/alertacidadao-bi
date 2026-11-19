"""AlertaCidadao: autonomous, synthetic BI demonstration. Not an emergency service."""
import csv, hashlib, hmac, io, json, os, secrets, time, uuid
from collections import Counter, defaultdict, deque
from datetime import timedelta
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse
from fastapi import FastAPI, Request, Response, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ConfigDict, field_validator
from .db import Store
from .middleware import BodyLimitMiddleware
from .domain import ZONES, SCENARIOS, make_notice, utcnow, iso, eligible, parse_time
from .documents import extract_fields, DocumentError, MAX_SIZE

BASE=Path(__file__).resolve().parent
TTL_HOURS=24
COOKIE='ac_workspace'

def uid(): return uuid.uuid4().hex

def session_hash(token): return hashlib.sha256(token.encode()).hexdigest()

class PlaceInput(BaseModel):
    model_config=ConfigDict(extra='forbid',str_strip_whitespace=True)
    label: str=Field(min_length=2,max_length=48)
    street: str=Field(min_length=3,max_length=120)
    number: str=Field(min_length=1,max_length=12,pattern=r'^[0-9A-Za-z /-]+$')
    neighborhood: str=Field(min_length=3,max_length=80)
    city: str=Field(min_length=3,max_length=80)
    state: Literal['SP']='SP'
    postal_code: str=Field(pattern=r'^00000-00[123]$')
    zone: Literal['TESTE-A','TESTE-B','TESTE-C']
    chuva: bool=True
    calor: bool=True
    consent: bool
    synthetic: Literal[True]
    @field_validator('label','street','neighborhood','city')
    @classmethod
    def no_markup(cls,v):
        if any(c in v for c in '<>\x00\r\n'): raise ValueError('Use texto simples, sem marca\u00e7\u00e3o.')
        return v

class PrefInput(BaseModel):
    model_config=ConfigDict(extra='forbid')
    chuva: bool
    calor: bool
    consent: bool

class ScenarioInput(BaseModel):
    model_config=ConfigDict(extra='forbid')
    scenario: Literal['chuva','calor','fora','expirado','futuro','cancelado','atualizacao','falha']

class ConfirmReset(BaseModel):
    confirm: Literal['APAGAR']

class Limiter:
    """Per-process demo abuse guard. Deploy one worker; use a shared limiter for scale."""
    def __init__(self): self.records=defaultdict(deque)
    def check(self,key,limit=90,window=60):
        now=time.monotonic()
        if len(self.records)>5000:
            self.records={k:q for k,q in self.records.items() if q and q[-1]>now-3600}
            self.records=defaultdict(deque,self.records)
        q=self.records[key]
        while q and q[0]<now-window: q.popleft()
        if len(q)>=limit: raise HTTPException(429,'Muitas opera\u00e7\u00f5es. Tente novamente em instantes.')
        q.append(now)


def create_app(db_path: str|None=None):
    app=FastAPI(title='AlertaCidad\u00e3o | Demonstra\u00e7\u00e3o',version='2.0.0',docs_url=None,redoc_url=None,openapi_url='/api/openapi.json')
    store=Store(db_path or os.getenv('DATABASE_URL') or os.getenv('DATABASE_PATH',str(BASE.parent/'data'/'alerta.db')))
    limiter=Limiter()
    app.add_middleware(BodyLimitMiddleware)
    app.state.store=store
    secure=os.getenv('COOKIE_SECURE','0')=='1'

    @app.middleware('http')
    async def headers_and_limit(request,call_next):
        length=request.headers.get('content-length')
        if length and (not length.isdigit() or int(length)>MAX_SIZE+100000):
            return JSONResponse({'detail':'Requisi\u00e7\u00e3o acima de 2 MB.'},status_code=413)
        response=await call_next(request)
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['X-Frame-Options']='DENY'
        response.headers['Referrer-Policy']='no-referrer'
        response.headers['Permissions-Policy']='camera=(), microphone=(), geolocation=()'
        response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        if request.url.path.startswith('/api'): response.headers['Cache-Control']='no-store'
        if secure: response.headers['Strict-Transport-Security']='max-age=31536000; includeSubDomains'
        return response

    @app.exception_handler(RequestValidationError)
    async def invalid(request,exc):
        return JSONResponse(status_code=422,content={'detail':'Revise os campos: use apenas dados de teste, CEP 00000-001/002/003 e confirme a demonstra\u00e7\u00e3o.','fields':[str(e['loc'][-1]) for e in exc.errors()]})

    def current(request: Request):
        token=request.cookies.get(COOKIE,'')
        if not token: raise HTTPException(401,'Inicie uma sess\u00e3o de demonstra\u00e7\u00e3o.')
        sid=session_hash(token)
        with store.connect() as con:
            row=con.execute('SELECT * FROM sessions WHERE id=?',(sid,)).fetchone()
            if not row or parse_time(row['expires_at'])<=utcnow():
                raise HTTPException(401,'Sess\u00e3o expirada. Recarregue a p\u00e1gina para reiniciar.')
            return dict(row)

    def write_session(request: Request,session=Depends(current)):
        expected=session['csrf']
        if not hmac.compare_digest(request.headers.get('x-csrf-token',''),expected):
            raise HTTPException(403,'Token de seguran\u00e7a inv\u00e1lido. Recarregue a p\u00e1gina.')
        origin=request.headers.get('origin')
        if origin and urlparse(origin).netloc!=request.url.netloc:
            raise HTTPException(403,'Origem n\u00e3o permitida.')
        limiter.check(session['id'])
        return session

    def notify(con,sid,notice_id,payload):
        places=store.rows(con,'SELECT * FROM places WHERE session_id=?',(sid,))
        reasons=Counter()
        created=0
        for place in places:
            ok,reason=eligible(place,payload)
            if ok:
                exists=con.execute('SELECT id FROM notifications WHERE session_id=? AND place_id=? AND notice_id=?',(sid,place['id'],notice_id)).fetchone()
                if exists: reason='duplicado'
                else:
                    nid=uid()
                    con.execute('INSERT INTO notifications(id,session_id,place_id,notice_id,created_at) VALUES (?,?,?,?,?)',(nid,sid,place['id'],notice_id,iso(utcnow())))
                    store.event(con,sid,'notification_created',{'notification_id':nid,'place':place['label'],'notice':payload['code'],'version':payload['version'],'channel':'internal'},iso(utcnow()))
                    created+=1
            reasons[reason]+=1
        return {'created':created,'evaluated':len(places),'reasons':dict(reasons)}

    @app.get('/api/health')
    def health():
        with store.connect() as con: con.execute('SELECT 1').fetchone()
        return {'status':'ok','version':'2.0.0','mode':'synthetic-demo'}

    @app.get('/api/session')
    def start_session(request:Request,response:Response):
        token=request.cookies.get(COOKIE,'')
        now=utcnow()
        with store.connect() as con:
            con.execute('DELETE FROM sessions WHERE expires_at<=?',(iso(now),))
            row=con.execute('SELECT * FROM sessions WHERE id=?',(session_hash(token),)).fetchone() if token else None
            if not row:
                limiter.check('new:'+str(request.client.host),30,3600)
                if con.execute('SELECT count(*) FROM sessions').fetchone()[0]>=1500:
                    raise HTTPException(503,'Limite tempor\u00e1rio de demonstra\u00e7\u00f5es atingido.')
                token=secrets.token_urlsafe(32)
                sid=session_hash(token)
                csrf=secrets.token_urlsafe(32)
                expires=iso(now+timedelta(hours=TTL_HOURS))
                con.execute('INSERT INTO sessions VALUES (?,?,?,?)',(sid,csrf,iso(now),expires))
                row={'id':sid,'csrf':csrf,'expires_at':expires}
                store.event(con,sid,'session_started',{'synthetic':True},iso(now))
            response.set_cookie(COOKIE,token,httponly=True,secure=secure,samesite='strict',max_age=TTL_HOURS*3600,path='/')
        return {'csrf':row['csrf'],'expires_at':row['expires_at'],'demo':True,'zones':ZONES,'external_delivery_enabled':False}

    @app.get('/api/state')
    def state(session=Depends(current)):
        sid=session['id']
        with store.connect() as con:
            places=store.rows(con,'SELECT * FROM places WHERE session_id=? ORDER BY created_at',(sid,))
            notices=store.rows(con,'SELECT * FROM notices WHERE session_id=? ORDER BY created_at DESC',(sid,))
            notifications=store.rows(con,'SELECT n.*,p.label AS place_label,p.zone AS zone,a.payload FROM notifications n JOIN places p ON p.id=n.place_id JOIN notices a ON a.id=n.notice_id WHERE n.session_id=? ORDER BY n.created_at DESC',(sid,))
            events=store.rows(con,'SELECT kind,detail,created_at FROM events WHERE session_id=? ORDER BY id DESC LIMIT 150',(sid,))
        for p in places: p.pop('session_id',None)
        for n in notices:
            n['notice']=json.loads(n.pop('payload')); n.pop('session_id',None)
        for n in notifications:
            n['notice']=json.loads(n.pop('payload'));n.pop('session_id',None)
        for e in events: e['detail']=json.loads(e['detail'])
        latest_versions={}
        for n in notices:
            latest_versions[n['code']]=max(latest_versions.get(n['code'],0),n['version'])
        active=sum(1 for n in notices if n['version']==latest_versions[n['code']] and n['notice']['status']=='active' and parse_time(n['notice']['starts_at'])<=utcnow()<parse_time(n['notice']['ends_at']))
        read=sum(1 for n in notifications if n['read_at'])
        return {'places':places,'notices':notices,'notifications':notifications,'events':events,'metrics':{'places':len(places),'notices':len(notices),'active_notices':active,'notifications':len(notifications),'confirmed':read,'unread':len(notifications)-read,'confirmation_rate':round(read/len(notifications)*100,1) if notifications else None,'external_deliveries':0},'mode':'synthetic-demo','generated_at':iso(utcnow())}

    @app.post('/api/places',status_code=201)
    def add_place(data:PlaceInput,session=Depends(write_session)):
        sid=session['id']; pid=uid();now=iso(utcnow())
        expected={'TESTE-A':'00000-001','TESTE-B':'00000-002','TESTE-C':'00000-003'}
        if data.postal_code!=expected[data.zone]: raise HTTPException(422,'CEP sint\u00e9tico e \u00e1rea precisam corresponder.')
        with store.connect() as con:
            if con.execute('SELECT count(*) FROM places WHERE session_id=?',(sid,)).fetchone()[0]>=10: raise HTTPException(422,'M\u00e1ximo de dez locais por demonstra\u00e7\u00e3o.')
            if con.execute('SELECT id FROM places WHERE session_id=? AND street=? AND number=? AND zone=?',(sid,data.street,data.number,data.zone)).fetchone(): raise HTTPException(409,'Este local j\u00e1 est\u00e1 cadastrado.')
            con.execute('INSERT INTO places VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(pid,sid,data.label,data.street,data.number,data.neighborhood,data.city,data.state,data.postal_code,data.zone,int(data.chuva),int(data.calor),int(data.consent),now))
            store.event(con,sid,'place_confirmed',{'place_id':pid,'label':data.label,'zone':data.zone},now)
            # A new place receives already available, current versions, never superseded versions.
            rows=store.rows(con,'SELECT n.id,n.payload FROM notices n WHERE session_id=? AND version=(SELECT MAX(version) FROM notices m WHERE m.session_id=n.session_id AND m.code=n.code)',(sid,))
            for n in rows: notify(con,sid,n['id'],json.loads(n['payload']))
        return {'id':pid,'saved':True}

    @app.patch('/api/places/{pid}')
    def prefs(pid:str,data:PrefInput,session=Depends(write_session)):
        with store.connect() as con:
            result=con.execute('UPDATE places SET chuva=?,calor=?,consent=? WHERE id=? AND session_id=?',(int(data.chuva),int(data.calor),int(data.consent),pid,session['id']))
            if result.rowcount!=1: raise HTTPException(404,'Local n\u00e3o encontrado nesta sess\u00e3o.')
            store.event(con,session['id'],'preferences_updated',{'place_id':pid,**data.model_dump()},iso(utcnow()))
        return {'updated':True}

    @app.delete('/api/places/{pid}')
    def delete_place(pid:str,session=Depends(write_session)):
        with store.connect() as con:
            cur=con.execute('DELETE FROM places WHERE id=? AND session_id=?',(pid,session['id']))
            if cur.rowcount!=1: raise HTTPException(404,'Local n\u00e3o encontrado nesta sess\u00e3o.')
            store.event(con,session['id'],'place_deleted',{'place_id':pid},iso(utcnow()))
        return {'deleted':True}

    @app.post('/api/documents/extract')
    def extract(file:UploadFile=File(...),session=Depends(write_session)):
        data=file.file.read(MAX_SIZE+1)
        try: result=extract_fields(data,file.filename or '')
        except DocumentError as exc: raise HTTPException(422,str(exc)) from exc
        finally: file.file.close()
        with store.connect() as con:
            store.event(con,session['id'],'document_extracted',{'method':result['method'],'stored':False},iso(utcnow()))
        return result

    @app.get('/api/scenarios')
    def scenarios(): return [{'id':k,'title':v[0],'description':v[1]} for k,v in SCENARIOS.items()]

    @app.post('/api/scenarios/run')
    def run_scenario(data:ScenarioInput,session=Depends(write_session)):
        sid=session['id'];now=iso(utcnow())
        with store.connect() as con:
            if data.scenario=='falha':
                store.event(con,sid,'source_failed',{'scenario':'falha','synthetic':True},now)
                return {'status':'source_unavailable','created':0,'evaluated':0,'reasons':{},'message':'Falha simulada de coleta. N\u00e3o significa aus\u00eancia de risco.'}
            notice=make_notice(data.scenario).as_dict()
            row=con.execute('SELECT id,payload FROM notices WHERE session_id=? AND code=? AND version=?',(sid,notice['code'],notice['version'])).fetchone()
            if row:
                nid=row['id']; notice=json.loads(row['payload'])
            else:
                nid=uid()
                con.execute('INSERT INTO notices VALUES (?,?,?,?,?,?)',(nid,sid,notice['code'],notice['version'],json.dumps(notice,ensure_ascii=False),now))
            latest=con.execute('SELECT MAX(version) FROM notices WHERE session_id=? AND code=?',(sid,notice['code'])).fetchone()[0]
            if latest>notice['version']:
                result={'created':0,'evaluated':0,'reasons':{'versao_superada':1}}
            else: result=notify(con,sid,nid,notice)
            store.event(con,sid,'scenario_processed',{'scenario':data.scenario,**result},now)
        return {'status':'processed','notice_id':nid,**result}

    @app.post('/api/notifications/{nid}/confirm')
    def confirm(nid:str,session=Depends(write_session)):
        with store.connect() as con:
            row=con.execute('SELECT * FROM notifications WHERE id=? AND session_id=?',(nid,session['id'])).fetchone()
            if not row: raise HTTPException(404,'Notifica\u00e7\u00e3o n\u00e3o encontrada nesta sess\u00e3o.')
            read_at=row['read_at'] or iso(utcnow())
            if not row['read_at']:
                con.execute('UPDATE notifications SET read_at=? WHERE id=? AND session_id=?',(read_at,nid,session['id']))
                store.event(con,session['id'],'reading_confirmed',{'notification_id':nid},read_at)
        return {'confirmed':True,'read_at':read_at,'already_confirmed':bool(row['read_at'])}

    @app.post('/api/reset')
    def reset(data:ConfirmReset,session=Depends(write_session)):
        with store.connect() as con:
            for table in ('notifications','places','notices','events'): con.execute(f'DELETE FROM {table} WHERE session_id=?',(session['id'],))
            store.event(con,session['id'],'session_reset',{},iso(utcnow()))
        return {'reset':True}

    @app.get('/api/export')
    def export(session=Depends(current)):
        result=state(session)
        return JSONResponse(result,headers={'Content-Disposition':'attachment; filename="alertacidadao-evidencias.json"'})

    @app.get('/api/export.csv')
    def export_csv(session=Depends(current)):
        result=state(session)
        out=io.StringIO(); writer=csv.writer(out)
        writer.writerow(['local','area','aviso','versao','canal','criada_em','leitura_confirmada_em'])
        def safe(v):
            s=str(v or '')
            return "'"+s if s.startswith(('=','+','-','@','\t','\r')) else s
        for n in result['notifications']:
            writer.writerow([safe(v) for v in [n['place_label'],n['zone'],n['notice']['code'],n['notice']['version'],n['channel'],n['created_at'],n['read_at']]])
        return Response('\ufeff'+out.getvalue(),media_type='text/csv',headers={'Content-Disposition':'attachment; filename="alertacidadao-comunicacoes.csv"'})

    app.mount('/static',StaticFiles(directory=BASE/'static'),name='static')
    app.mount('/samples',StaticFiles(directory=BASE/'samples'),name='samples')
    @app.get('/',include_in_schema=False)
    def index(): return FileResponse(BASE/'static'/'index.html')
    @app.get('/robots.txt',include_in_schema=False)
    def robots(): return Response('User-agent: *\nDisallow: /\n',media_type='text/plain')
    return app

app=create_app()
