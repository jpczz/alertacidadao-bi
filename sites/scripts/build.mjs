import { build } from 'esbuild';
import { readdir, readFile, writeFile, mkdir, rm, cp } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.txt':'text/plain; charset=utf-8','.svg':'image/svg+xml','.pdf':'application/pdf','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2','.xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','.pptx':'application/vnd.openxmlformats-officedocument.presentationml.presentation'};
const textual = new Set(['.html','.css','.js','.json','.txt','.svg']);
await build({entryPoints:['client/finalizar.js'],outfile:'public/static/finalizar.js',bundle:true,format:'esm',platform:'browser',target:'es2022',minify:true,legalComments:'eof'});
const assets = {};
async function walk(dir, prefix='') {
  for (const ent of await readdir(dir, {withFileTypes:true})) {
    const rel = path.posix.join(prefix, ent.name);
    if(ent.isDirectory()) { await walk(path.join(dir,ent.name),rel);continue; }
    const ext=path.extname(ent.name).toLowerCase();
    if(!mime[ext]) continue;
    const data=await readFile(path.join(dir,ent.name));
    assets['/'+rel]={mime:mime[ext],encoding:textual.has(ext)?'utf-8':'base64',content:textual.has(ext)?data.toString('utf8'):data.toString('base64')};
  }
}
await walk(path.join(root,'public'));
await writeFile('worker/assets.generated.js','export const assets = '+JSON.stringify(assets)+';\n');
await rm('dist',{recursive:true,force:true});
await mkdir('dist/server',{recursive:true});await mkdir('dist/.openai',{recursive:true});
await build({entryPoints:['worker/index.js'],outfile:'dist/server/index.js',bundle:true,format:'esm',platform:'neutral',target:'es2022',conditions:['workerd','worker','browser','import'],mainFields:['module','main'],minify:true,legalComments:'eof',external:['node:*','@napi-rs/canvas','pdfjs-dist','pdfjs-dist/*']});
await cp('.openai/hosting.json','dist/.openai/hosting.json');
try { await cp('drizzle','dist/.openai/drizzle',{recursive:true}); }catch(error){if(error.code!=='ENOENT')throw error;}
console.log(JSON.stringify({assets:Object.keys(assets).length,worker_bytes:(await readFile('dist/server/index.js')).length}));
