// Renders all raster brand assets from the chosen vector mark. Run: node growth/brand/render.mjs
import {chromium} from 'playwright';import fs from 'fs';
const mark=fs.readFileSync('growth/brand/b-mark.svg','utf8');const b64=f=>fs.readFileSync(f).toString('base64');const font=`@font-face{font-family:'Inter Variable';font-weight:100 900;src:url(data:font/woff2;base64,${b64('node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2')}) format('woff2')}@font-face{font-family:'JBM';src:url(data:font/woff2;base64,${b64('node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2')}) format('woff2')}`;
const b=await chromium.launch();
const shot=async(w,h,html,path,transparent=true)=>{const p=await b.newPage({viewport:{width:w,height:h}});await p.setContent(`<style>${font}html,body{margin:0;background:transparent;font-family:'Inter Variable'}</style>${html}`,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.screenshot({path,omitBackground:transparent});await p.close()};
const m=s=>mark.replace('<svg ',`<svg width="${s}" height="${s}" style="display:block" `);
for(const s of [16,32,48,180,192,512]) await shot(s,s,m(s),`/tmp/m${s}.png`);
fs.copyFileSync('/tmp/m32.png','src/assets/favicon-32.png');fs.copyFileSync('/tmp/m192.png','src/assets/icon-192.png');fs.copyFileSync('/tmp/m512.png','src/assets/icon-512.png');
// apple touch: full-bleed square, no transparency
await shot(180,180,`<div style="width:180px;height:180px;background:#C6F432">${mark.replace('<svg ','<svg width="180" height="180" style="display:block" ').replace('rx="8"','rx="0"')}</div>`,'src/root/apple-touch-icon.png',false);
// Beehiiv
await shot(1024,1024,`<div style="width:1024px;height:1024px;background:#0A0A0B;display:grid;place-items:center">${m(680)}</div>`,'growth/brand/beehiiv/skillmaxx-logo-1024.png',false);
await shot(512,512,`<div style="width:512px;height:512px;background:#0A0A0B;display:grid;place-items:center">${m(340)}</div>`,'growth/brand/beehiiv/skillmaxx-logo-512.png',false);
await shot(1200,300,`<div style="width:1200px;height:300px;box-sizing:border-box;padding:0 80px;display:flex;align-items:center;gap:28px;background:radial-gradient(500px 220px at 90% 0%,rgba(198,244,50,.22),transparent),#0A0A0B;color:#F4F4F5">${m(112)}<div><div style="font-size:72px;font-weight:700;letter-spacing:-2px;line-height:1">Skill<span style="color:#C6F432">Maxx</span></div><div style="font-size:24px;color:#A1A1AA;margin-top:12px">This week in agent skills · tested in 5 coding agents</div></div></div>`,'growth/brand/beehiiv/skillmaxx-banner-1200x300.png',false);
// OG
await shot(1200,630,`<div style="width:1200px;height:630px;box-sizing:border-box;padding:72px;background:radial-gradient(circle at 80% 20%,rgba(198,244,50,.18),transparent 50%),#0A0A0B;color:#F4F4F5"><div style="display:flex;align-items:center;gap:16px;font-size:34px;font-weight:700;letter-spacing:-.5px">${m(56)}Skill<span style="color:#C6F432;margin-left:-16px">Maxx</span></div><h1 style="font-size:76px;line-height:1.05;letter-spacing:-.03em;margin:56px 0 24px;font-weight:700">Find agent skills that actually work in <span style="color:#C6F432">your</span> agent.</h1><div style="font:24px JBM,monospace;color:#A1A1AA">Claude Code · Codex · Grok Build · Cursor · Pi</div></div>`,'src/assets/og.png',false);
await b.close();
