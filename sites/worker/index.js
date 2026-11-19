import { handleApi } from './api.js';
import { assets } from './assets.generated.js';

function secure(response, pathname) {
  const headers = new Headers(response.headers);
  headers.set('X-Content-Type-Options', 'nosniff');
  headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  headers.set('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; media-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self' https://chatgpt.com; form-action 'self'");
  headers.set('Cache-Control', pathname.startsWith('/api/') ? 'no-store' : 'no-cache');
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    try {
      if (url.pathname.startsWith('/api/')) {
        return secure(await handleApi(request, env, ctx), url.pathname);
      }
      if (!['GET', 'HEAD'].includes(request.method)) {
        return secure(new Response('Método não permitido.', {status:405,headers:{Allow:'GET, HEAD'}}),url.pathname);
      }
      const aliases = {'/':'/index.html','/entrega':'/entrega.html','/gravacao':'/gravacao.html','/pitch':'/pitch.html','/finalizar':'/finalizar.html'};
      const key = aliases[url.pathname] || url.pathname;
      const asset = assets[key];
      if (!asset) return secure(new Response('Página não encontrada.',{status:404}),url.pathname);
      const bytes = asset.encoding === 'base64' ? Uint8Array.from(atob(asset.content), c=>c.charCodeAt(0)) : asset.content;
      const headers = {'Content-Type':asset.mime};
      if (asset.download) headers['Content-Disposition'] = 'attachment; filename="'+asset.download+'"';
      return secure(new Response(request.method === 'HEAD' ? null : bytes,{headers}),url.pathname);
    } catch (error) {
      console.error('AlertaCidadão request error', error?.name || 'Error', error?.message || 'unknown');
      return secure(Response.json({detail:'Não foi possível concluir a operação. Tente novamente.'},{status:500}),url.pathname);
    }
  }
};
