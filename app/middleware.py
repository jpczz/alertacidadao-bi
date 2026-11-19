"""Bound request bodies even when Transfer-Encoding is chunked."""
from starlette.responses import JSONResponse

class BodyLimitMiddleware:
    def __init__(self,app,max_bytes=2*1024*1024+100000):
        self.app=app;self.max_bytes=max_bytes
    async def __call__(self,scope,receive,send):
        if scope['type']!='http' or scope['method'] not in ('POST','PUT','PATCH'):
            return await self.app(scope,receive,send)
        messages=[];total=0
        while True:
            message=await receive()
            if message['type']=='http.disconnect':return
            total+=len(message.get('body',b''))
            if total>self.max_bytes:
                return await JSONResponse({'detail':'Requisicao acima de 2 MB.'},status_code=413)(scope,receive,send)
            messages.append(message)
            if not message.get('more_body',False):break
        iterator=iter(messages)
        async def replay():
            try:return next(iterator)
            except StopIteration:return await receive()
        return await self.app(scope,replay,send)
