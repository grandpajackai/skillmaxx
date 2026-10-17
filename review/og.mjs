import {chromium} from 'playwright';const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});
await p.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700&family=JetBrains+Mono&display=swap" rel="stylesheet"></head><body style="margin:0;background:radial-gradient(circle at 80% 20%,rgba(198,244,50,.18),transparent 50%),#0A0A0B;color:#F4F4F5;font-family:Inter;width:1200px;height:630px;box-sizing:border-box;padding:72px">
<div style="display:flex;align-items:center;gap:14px;font-size:32px;font-weight:700"><span style="background:#C6F432;color:#0A0A0B;width:52px;height:52px;border-radius:12px;display:grid;place-items:center">S</span>Skill<span style="color:#C6F432">Maxx</span></div>
<h1 style="font-size:76px;line-height:1.05;letter-spacing:-.03em;margin:56px 0 24px">Find agent skills that actually work in <span style="color:#C6F432">your</span> agent.</h1>
<div style="font:24px 'JetBrains Mono';color:#A1A1AA">Claude Code · Codex · Grok Build · Cursor · Pi</div></body></html>`,{waitUntil:'networkidle'});
await p.screenshot({path:'src/assets/og.png'});await b.close();
