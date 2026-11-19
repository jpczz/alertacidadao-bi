/* Functional academic demonstration. All weather scenarios and addresses are synthetic. */
const COOKIE = 'ac_workspace';
const TTL_SECONDS = 24 * 60 * 60;
const MAX_DOCUMENT = 2 * 1024 * 1024;
const MAX_BODY = MAX_DOCUMENT + 100000;
export const ZONES = { 'TESTE-A': 'Jardim Exemplo A', 'TESTE-B': 'Jardim Exemplo B', 'TESTE-C': 'Jardim Exemplo C' };
const SCENARIOS = {
  chuva: ['Chuva intensa', 'Um aviso sintético para a área TESTE-A.'],
  calor: ['Calor extremo', 'Um aviso sintético para as áreas TESTE-A e TESTE-B.'],
  fora: ['Outra região', 'Aviso apenas para TESTE-C: verifica a exclusão territorial.'],
  expirado: ['Aviso expirado', 'Fora da validade; nenhuma nova notificação deve ser criada.'],
  futuro: ['Aviso futuro', 'Ainda não vigente; não deve notificar.'],
  cancelado: ['Aviso cancelado', 'Um aviso cancelado na origem não deve notificar.'],
  atualizacao: ['Atualização de chuva', 'Versão 2 do mesmo aviso: uma nova comunicação.'],
  falha: ['Fonte indisponível', 'Falha controlada de coleta, sem inventar novos avisos.'],
};
const rateRecords = new Map();
const requestBodies = new WeakMap();
class ApiError extends Error {
  constructor(status, detail, fields) { super(detail); this.status = status; this.fields = fields; }
}
const now = () => new Date().toISOString();
const id = () => crypto.randomUUID().replaceAll('-', '');
const token = () => {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  return btoa(String.fromCharCode(...bytes)).replaceAll('+', '-').replaceAll('/', '_').replaceAll('=', '');
};
async function hash(value) {
  const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
  return [...new Uint8Array(bytes)].map(v => v.toString(16).padStart(2, '0')).join('');
}
function equal(a, b) {
  if (typeof a !== 'string' || a.length !== b.length) return false;
  let diff = 0; for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}
function limited(key, limit = 90, windowMs = 60000) {
  const t = Date.now();
  if (rateRecords.size > 5000) {
    for (const [k, entries] of rateRecords) if (!entries.length || entries.at(-1) < t - 3600000) rateRecords.delete(k);
  }
  const entries = (rateRecords.get(key) || []).filter(n => n > t - windowMs);
  if (entries.length >= limit) throw new ApiError(429, 'Muitas operações. Tente novamente em instantes.');
  entries.push(t); rateRecords.set(key, entries);
}
function json(value, status = 200, extra = {}) {
  return new Response(JSON.stringify(value), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', ...extra } });
}
const stmt = (db, sql, args = []) => db.prepare(sql).bind(...args);
const first = (db, sql, args = []) => stmt(db, sql, args).first();
const all = async (db, sql, args = []) => (await stmt(db, sql, args).all()).results || [];
const run = (db, sql, args = []) => stmt(db, sql, args).run();
const eventStmt = (db, sid, kind, detail, at = now()) => stmt(db, 'INSERT INTO events(session_id,kind,detail,created_at) VALUES (?,?,?,?)', [sid, kind, JSON.stringify(detail), at]);
const event = (db, sid, kind, detail, at) => eventStmt(db, sid, kind, detail, at).run();
function cookieValue(request) {
  const match = (request.headers.get('cookie') || '').match(/(?:^|;\s*)ac_workspace=([^;]*)/);
  return match && match[1].length <= 128 ? match[1] : '';
}
async function current(request, db) {
  const t = cookieValue(request);
  if (!t) throw new ApiError(401, 'Inicie uma sessão de demonstração.');
  const row = await first(db, 'SELECT * FROM sessions WHERE id=?', [await hash(t)]);
  if (!row || row.expires_at <= now()) throw new ApiError(401, 'Sessão expirada. Recarregue a página para reiniciar.');
  return row;
}
async function writable(request, db) {
  const session = await current(request, db);
  if (!equal(request.headers.get('x-csrf-token') || '', session.csrf)) throw new ApiError(403, 'Token de segurança inválido. Recarregue a página.');
  const origin = request.headers.get('origin');
  if (origin && origin !== new URL(request.url).origin) throw new ApiError(403, 'Origem não permitida.');
  limited(session.id);
  return session;
}
async function readBounded(request) {
  if (requestBodies.has(request)) return requestBodies.get(request);
  const length = request.headers.get('content-length');
  if (length && (!/^\d+$/.test(length) || Number(length) > MAX_BODY)) throw new ApiError(413, 'Requisição acima de 2 MB.');
  if (!request.body) return new Uint8Array();
  const reader = request.body.getReader(); const chunks = []; let size = 0;
  try {
    for (;;) {
      const result = await reader.read(); if (result.done) break;
      size += result.value.byteLength;
      if (size > MAX_BODY) { await reader.cancel(); throw new ApiError(413, 'Requisição acima de 2 MB.'); }
      chunks.push(result.value);
    }
  } finally { reader.releaseLock(); }
  const bytes = new Uint8Array(size); let pos = 0;
  for (const part of chunks) { bytes.set(part, pos); pos += part.byteLength; }
  requestBodies.set(request, bytes);
  return bytes;
}
async function input(request, allowed) {
  let data;
  try { data = JSON.parse(new TextDecoder().decode(await readBounded(request))); }
  catch (error) { if (error instanceof ApiError) throw error; throw new ApiError(422, 'Revise os campos enviados.'); }
  if (!data || typeof data !== 'object' || Array.isArray(data)) throw new ApiError(422, 'Revise os campos enviados.');
  const extras = Object.keys(data).filter(k => !allowed.includes(k));
  if (extras.length) throw new ApiError(422, 'Existem campos não reconhecidos.', extras);
  return data;
}
function validatePlace(p) {
  const fields = { label: [2, 48], street: [3, 120], number: [1, 12], neighborhood: [3, 80], city: [3, 80] };
  for (const [name, [min, max]] of Object.entries(fields)) {
    if (typeof p[name] !== 'string') throw new ApiError(422, 'Revise os campos do endereço.', [name]);
    p[name] = p[name].trim();
    if (p[name].length < min || p[name].length > max || /[<>\0\r\n]/.test(p[name])) throw new ApiError(422, 'Use texto simples nos campos do endereço.', [name]);
  }
  if (!/^[0-9A-Za-z /-]+$/.test(p.number)) throw new ApiError(422, 'Número de teste inválido.', ['number']);
  p.state ??= 'SP'; p.chuva ??= true; p.calor ??= true;
  if (p.state !== 'SP' || !Object.hasOwn(ZONES, p.zone) || !/^00000-00[123]$/.test(p.postal_code || '') || p.synthetic !== true) throw new ApiError(422, 'Use apenas dados de teste, CEP 00000-001/002/003 e confirme a demonstração.');
  if (['chuva', 'calor', 'consent'].some(k => typeof p[k] !== 'boolean')) throw new ApiError(422, 'Revise as preferências e o consentimento.');
  const expected = { 'TESTE-A': '00000-001', 'TESTE-B': '00000-002', 'TESTE-C': '00000-003' };
  if (p.postal_code !== expected[p.zone]) throw new ApiError(422, 'CEP sintético e área precisam corresponder.');
  return p;
}
function makeNotice(scenario, t = Date.now()) {
  const n = { code: 'CHUVA-A', version: 1, kind: 'chuva', title: 'Chuva intensa na área de teste A', severity: 'Atenção', zones: ['TESTE-A'], starts_at: new Date(t - 300000).toISOString(), ends_at: new Date(t + 21600000).toISOString(), status: 'active', body: 'Cenário sintético para avaliar a comunicação. Não é um alerta real.', source: 'Laboratório AlertaCidadão', synthetic: true };
  const changes = {
    chuva: {},
    calor: { code: 'CALOR-AB', kind: 'calor', title: 'Calor extremo nas áreas de teste A e B', zones: ['TESTE-A', 'TESTE-B'] },
    fora: { code: 'CHUVA-C', title: 'Chuva na área de teste C', zones: ['TESTE-C'] },
    expirado: { code: 'EXPIRADO-A', title: 'Aviso de teste expirado', starts_at: new Date(t - 18000000).toISOString(), ends_at: new Date(t - 3600000).toISOString() },
    futuro: { code: 'FUTURO-A', title: 'Aviso de teste futuro', starts_at: new Date(t + 7200000).toISOString(), ends_at: new Date(t + 28800000).toISOString() },
    cancelado: { code: 'CANCELADO-A', title: 'Aviso de teste cancelado', status: 'cancelled' },
    atualizacao: { version: 2, title: 'Atualização: chuva na área de teste A' },
  };
  return { ...n, ...changes[scenario] };
}
function eligibility(place, notice) {
  const t = Date.now();
  if (notice.status !== 'active') return 'cancelado';
  if (t < Date.parse(notice.starts_at)) return 'futuro';
  if (t >= Date.parse(notice.ends_at)) return 'expirado';
  if (!place.consent) return 'sem_consentimento';
  if (!notice.zones.includes(place.zone)) return 'fora_da_area';
  if (!place[notice.kind]) return 'preferencia_desativada';
  return 'elegivel';
}
async function notify(db, sid, noticeId, notice) {
  const places = await all(db, 'SELECT * FROM places WHERE session_id=?', [sid]);
  const reasons = {}; let created = 0;
  for (const place of places) {
    let reason = eligibility(place, notice);
    if (reason === 'elegivel') {
      const nid = id(), at = now();
      const detail = { notification_id: nid, place: place.label, notice: notice.code, version: notice.version, channel: 'internal' };
      const results = await db.batch([
        stmt(db, 'INSERT OR IGNORE INTO notifications(id,session_id,place_id,notice_id,created_at) VALUES (?,?,?,?,?)', [nid, sid, place.id, noticeId, at]),
        stmt(db, 'INSERT INTO events(session_id,kind,detail,created_at) SELECT ?,?,?,? FROM notifications WHERE id=? AND session_id=?', [sid, 'notification_created', JSON.stringify(detail), at, nid, sid]),
      ]);
      if (results[0].meta?.changes === 1) created++; else reason = 'duplicado';
    }
    reasons[reason] = (reasons[reason] || 0) + 1;
  }
  return { created, evaluated: places.length, reasons };
}
async function state(db, session) {
  const sid = session.id;
  const [places, stored, noticesDelivered, events] = await Promise.all([
    all(db, 'SELECT * FROM places WHERE session_id=? ORDER BY created_at', [sid]),
    all(db, 'SELECT * FROM notices WHERE session_id=? ORDER BY created_at DESC', [sid]),
    all(db, 'SELECT n.*,p.label AS place_label,p.zone AS zone,a.payload FROM notifications n JOIN places p ON p.id=n.place_id JOIN notices a ON a.id=n.notice_id WHERE n.session_id=? ORDER BY n.created_at DESC', [sid]),
    all(db, 'SELECT kind,detail,created_at FROM events WHERE session_id=? ORDER BY id DESC LIMIT 150', [sid]),
  ]);
  for (const p of places) delete p.session_id;
  const convert = row => { row.notice = JSON.parse(row.payload); delete row.payload; delete row.session_id; return row; };
  const notices = stored.map(convert), notifications = noticesDelivered.map(convert);
  for (const e of events) e.detail = JSON.parse(e.detail);
  const versions = {};
  for (const n of notices) versions[n.code] = Math.max(versions[n.code] || 0, n.version);
  const t = Date.now();
  const active = notices.filter(n => n.version === versions[n.code] && n.notice.status === 'active' && Date.parse(n.notice.starts_at) <= t && t < Date.parse(n.notice.ends_at)).length;
  const confirmed = notifications.filter(n => n.read_at).length;
  return { places, notices, notifications, events, metrics: { places: places.length, notices: notices.length, active_notices: active, notifications: notifications.length, confirmed, unread: notifications.length - confirmed, confirmation_rate: notifications.length ? Math.round(confirmed / notifications.length * 1000) / 10 : null, external_deliveries: 0 }, mode: 'synthetic-demo', generated_at: now() };
}
async function extractDocument(request, db, session) {
  const bytes = await readBounded(request);
  let form;
  try { form = await new Response(bytes, { headers: { 'content-type': request.headers.get('content-type') || '' } }).formData(); }
  catch { throw new ApiError(422, 'Envie um PDF sintético com texto.'); }
  const file = form.get('file');
  if (!file || typeof file.arrayBuffer !== 'function' || !file.size || file.size > MAX_DOCUMENT) throw new ApiError(422, 'Arquivo vazio ou acima de 2 MB.');
  const data = new Uint8Array(await file.arrayBuffer());
  if (new TextDecoder().decode(data.slice(0, 4)) !== '%PDF') throw new ApiError(422, 'Nesta versão web, use o PDF de exemplo com texto ou o cadastro manual. OCR de PNG/JPG está disponível no aplicativo Python do repositório.');
  let document;
  try {
    const { getDocumentProxy, extractText } = await import('unpdf');
    document = await getDocumentProxy(data, { maxImageSize: 16777216, isEvalSupported: false });
    if (document.numPages > 2) throw new ApiError(422, 'Use um PDF de teste sem senha, com no máximo duas páginas.');
    const extracted = await extractText(document, { mergePages: true });
    const text = String(extracted.text || '').normalize('NFKD').replace(/\p{M}/gu, '').toUpperCase();
    if (!text.trim()) throw new ApiError(422, 'PDF sem camada de texto. Use o PDF de exemplo ou o cadastro manual.');
    if (!text.includes('DOCUMENTO SINTETICO')) throw new ApiError(422, 'Esta demonstração aceita somente documentos sintéticos. Não envie contas reais.');
    const labels = { label: 'LOCAL', street: 'ENDERECO', number: 'NUMERO', neighborhood: 'BAIRRO', city: 'CIDADE', state: 'UF', postal_code: 'CEP', zone: 'AREA' };
    const fields = {};
    for (const [key, label] of Object.entries(labels)) {
      const match = text.match(new RegExp('^\\s*' + label + '\\s*[:\\-]\\s*(.+?)\\s*$', 'm'));
      if (match) fields[key] = match[1].trim();
    }
    if (!Object.hasOwn(ZONES, fields.zone)) throw new ApiError(422, 'Área de teste não reconhecida. Revise manualmente.');
    await event(db, session.id, 'document_extracted', { method: 'texto_pdf', stored: false });
    return { fields, method: 'texto_pdf', missing_fields: Object.keys(labels).filter(k => !(k in fields)), review_required: true, synthetic: true, stored: false };
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(422, 'Não foi possível ler o PDF. Use o exemplo sem senha ou preencha manualmente.');
  } finally { if (document?.loadingTask) await document.loadingTask.destroy().catch(() => {}); }
}
export async function handleApi(request, env) {
  try {
    const db = env.DB;
    if (!db) throw new ApiError(503, 'O ambiente está sendo preparado. Tente novamente em instantes.');
    const path = new URL(request.url).pathname, method = request.method;
    if (path === '/api/health' && method === 'GET') {
      await first(db, 'SELECT COUNT(*) AS total FROM sessions');
      return json({ status: 'ok', version: '2.1.0', mode: 'synthetic-demo', storage: 'cloudflare-d1' });
    }
    if (path === '/api/scenarios' && method === 'GET') return json(Object.entries(SCENARIOS).map(([key, [title, description]]) => ({ id: key, title, description })));
    if (path === '/api/session' && method === 'GET') {
      const at = now();
      await run(db, 'DELETE FROM sessions WHERE expires_at<=?', [at]);
      let t = cookieValue(request), row = t ? await first(db, 'SELECT * FROM sessions WHERE id=?', [await hash(t)]) : null;
      if (!row) {
        if ((await first(db, 'SELECT COUNT(*) AS total FROM sessions')).total >= 1500) throw new ApiError(503, 'Limite temporário de demonstrações atingido.');
        t = token(); row = { id: await hash(t), csrf: token(), created_at: at, expires_at: new Date(Date.now() + TTL_SECONDS * 1000).toISOString() };
        await db.batch([stmt(db, 'INSERT INTO sessions(id,csrf,created_at,expires_at) VALUES (?,?,?,?)', [row.id, row.csrf, at, row.expires_at]), eventStmt(db, row.id, 'session_started', { synthetic: true }, at)]);
      }
      const secure = new URL(request.url).protocol === 'https:' ? '; Secure' : '';
      return json({ csrf: row.csrf, expires_at: row.expires_at, demo: true, zones: ZONES, external_delivery_enabled: false }, 200, { 'Set-Cookie': `${COOKIE}=${t}; Path=/; HttpOnly; SameSite=Strict; Max-Age=${TTL_SECONDS}${secure}` });
    }
    const session = ['POST', 'PATCH', 'PUT', 'DELETE'].includes(method) ? await writable(request, db) : await current(request, db);
    const sid = session.id;
    if (['POST', 'PATCH', 'PUT', 'DELETE'].includes(method)) await readBounded(request);
    if (path === '/api/state' && method === 'GET') return json(await state(db, session));
    if (path === '/api/places' && method === 'POST') {
      const data = validatePlace(await input(request, ['label', 'street', 'number', 'neighborhood', 'city', 'state', 'postal_code', 'zone', 'chuva', 'calor', 'consent', 'synthetic']));
      if ((await first(db, 'SELECT COUNT(*) AS total FROM places WHERE session_id=?', [sid])).total >= 10) throw new ApiError(422, 'Máximo de dez locais por demonstração.');
      if (await first(db, 'SELECT id FROM places WHERE session_id=? AND street=? AND number=? AND zone=?', [sid, data.street, data.number, data.zone])) throw new ApiError(409, 'Este local já está cadastrado.');
      const pid = id(), at = now();
      await db.batch([
        stmt(db, 'INSERT INTO places(id,session_id,label,street,number,neighborhood,city,state,postal_code,zone,chuva,calor,consent,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [pid, sid, data.label, data.street, data.number, data.neighborhood, data.city, data.state, data.postal_code, data.zone, Number(data.chuva), Number(data.calor), Number(data.consent), at]),
        eventStmt(db, sid, 'place_confirmed', { place_id: pid, label: data.label, zone: data.zone }, at),
      ]);
      const notices = await all(db, 'SELECT n.id,n.payload FROM notices n WHERE session_id=? AND version=(SELECT MAX(version) FROM notices m WHERE m.session_id=n.session_id AND m.code=n.code)', [sid]);
      for (const n of notices) await notify(db, sid, n.id, JSON.parse(n.payload));
      return json({ id: pid, saved: true }, 201);
    }
    const placeMatch = path.match(/^\/api\/places\/([^/]+)$/);
    if (placeMatch && method === 'PATCH') {
      const pid = placeMatch[1], data = await input(request, ['chuva', 'calor', 'consent']);
      if (['chuva', 'calor', 'consent'].some(k => typeof data[k] !== 'boolean')) throw new ApiError(422, 'Revise as preferências e o consentimento.');
      if (!await first(db, 'SELECT id FROM places WHERE id=? AND session_id=?', [pid, sid])) throw new ApiError(404, 'Local não encontrado nesta sessão.');
      await db.batch([stmt(db, 'UPDATE places SET chuva=?,calor=?,consent=? WHERE id=? AND session_id=?', [Number(data.chuva), Number(data.calor), Number(data.consent), pid, sid]), eventStmt(db, sid, 'preferences_updated', { place_id: pid, ...data })]);
      return json({ updated: true });
    }
    if (placeMatch && method === 'DELETE') {
      const pid = placeMatch[1];
      if (!await first(db, 'SELECT id FROM places WHERE id=? AND session_id=?', [pid, sid])) throw new ApiError(404, 'Local não encontrado nesta sessão.');
      await db.batch([stmt(db, 'DELETE FROM places WHERE id=? AND session_id=?', [pid, sid]), eventStmt(db, sid, 'place_deleted', { place_id: pid })]);
      return json({ deleted: true });
    }
    if (path === '/api/documents/extract' && method === 'POST') return json(await extractDocument(request, db, session));
    if (path === '/api/scenarios/run' && method === 'POST') {
      const data = await input(request, ['scenario']);
      if (!Object.hasOwn(SCENARIOS, data.scenario)) throw new ApiError(422, 'Cenário desconhecido.');
      if (data.scenario === 'falha') {
        await event(db, sid, 'source_failed', { scenario: 'falha', synthetic: true });
        return json({ status: 'source_unavailable', created: 0, evaluated: 0, reasons: {}, message: 'Falha simulada de coleta. Não significa ausência de risco.' });
      }
      const notice = makeNotice(data.scenario);
      await run(db, 'INSERT OR IGNORE INTO notices(id,session_id,code,version,payload,created_at) VALUES (?,?,?,?,?,?)', [id(), sid, notice.code, notice.version, JSON.stringify(notice), now()]);
      const stored = await first(db, 'SELECT id,payload FROM notices WHERE session_id=? AND code=? AND version=?', [sid, notice.code, notice.version]);
      const latest = await first(db, 'SELECT MAX(version) AS version FROM notices WHERE session_id=? AND code=?', [sid, notice.code]);
      const result = latest.version > notice.version ? { created: 0, evaluated: 0, reasons: { versao_superada: 1 } } : await notify(db, sid, stored.id, JSON.parse(stored.payload));
      await event(db, sid, 'scenario_processed', { scenario: data.scenario, ...result });
      return json({ status: 'processed', notice_id: stored.id, ...result });
    }
    const notificationMatch = path.match(/^\/api\/notifications\/([^/]+)\/confirm$/);
    if (notificationMatch && method === 'POST') {
      const nid = notificationMatch[1], row = await first(db, 'SELECT * FROM notifications WHERE id=? AND session_id=?', [nid, sid]);
      if (!row) throw new ApiError(404, 'Notificação não encontrada nesta sessão.');
      const at = now();
      await db.batch([
        stmt(db, 'INSERT INTO events(session_id,kind,detail,created_at) SELECT ?,?,?,? FROM notifications WHERE id=? AND session_id=? AND read_at IS NULL', [sid, 'reading_confirmed', JSON.stringify({ notification_id: nid }), at, nid, sid]),
        stmt(db, 'UPDATE notifications SET read_at=COALESCE(read_at,?) WHERE id=? AND session_id=?', [at, nid, sid]),
      ]);
      const updated = await first(db, 'SELECT read_at FROM notifications WHERE id=? AND session_id=?', [nid, sid]);
      return json({ confirmed: true, read_at: updated.read_at, already_confirmed: !!row.read_at });
    }
    if (path === '/api/reset' && method === 'POST') {
      const data = await input(request, ['confirm']);
      if (data.confirm !== 'APAGAR') throw new ApiError(422, 'Confirme a exclusão digitando APAGAR.');
      await db.batch(['notifications', 'places', 'notices', 'events'].map(table => stmt(db, `DELETE FROM ${table} WHERE session_id=?`, [sid])).concat(eventStmt(db, sid, 'session_reset', {})));
      return json({ reset: true });
    }
    if (path === '/api/export' && method === 'GET') return json(await state(db, session), 200, { 'Content-Disposition': 'attachment; filename="alertacidadao-evidencias.json"' });
    if (path === '/api/export.csv' && method === 'GET') {
      const data = await state(db, session);
      const safe = value => { const s = String(value ?? ''); return /^[=+\-@\t\r]/.test(s) ? "'" + s : s; };
      const cell = v => '"' + safe(v).replaceAll('"', '""') + '"';
      const rows = [['local', 'area', 'aviso', 'versao', 'canal', 'criada_em', 'leitura_confirmada_em'], ...data.notifications.map(n => [n.place_label, n.zone, n.notice.code, n.notice.version, n.channel, n.created_at, n.read_at])];
      return new Response('\ufeff' + rows.map(row => row.map(cell).join(',')).join('\r\n') + '\r\n', { headers: { 'Content-Type': 'text/csv; charset=utf-8', 'Cache-Control': 'no-store', 'Content-Disposition': 'attachment; filename="alertacidadao-comunicacoes.csv"' } });
    }
    throw new ApiError(404, 'Recurso não encontrado.');
  } catch (error) {
    if (error instanceof ApiError) return json({ detail: error.message, ...(error.fields ? { fields: error.fields } : {}) }, error.status);
    // Diagnostic errors stay in server logs and never expose SQL or secrets to callers.
    console.error('AlertaCidadao API failure', error?.name || 'Error', error?.message || 'Unexpected failure');
    return json({ detail: 'Não foi possível concluir a operação. Tente novamente em instantes.' }, 503);
  }
}
