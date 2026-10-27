import { chromium } from 'playwright';
import { writeFileSync, mkdirSync } from 'fs';

mkdirSync('src/assets/social/placements', { recursive: true });
mkdirSync('review/sponsor-mock', { recursive: true });

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();

async function shot(path) {
  await page.screenshot({ path, type: 'png' });
  console.log('wrote', path);
}

// --- Homepage Featured card ---
await page.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle', timeout: 60000 });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(400);
const sponsor = page.locator('article.card.sponsor').first();
await sponsor.scrollIntoViewIfNeeded();
await page.evaluate(() => {
  const el = document.querySelector('article.card.sponsor');
  if (!el) return;
  el.innerHTML = `
    <div class="ch"><span class="mono">+</span><div class="cn"><h3>ExampleMCP</h3><span class="meta2">Example sponsor · not a real listing</span></div><span class="spon">Sponsored</span></div>
    <p>Example: a one-line pitch (max 90 characters) plus logo and link. Always labeled Sponsored.</p>
    <a class="btn ghost" href="/advertise/">example.com →</a>`;
  const badge = document.createElement('div');
  badge.textContent = 'EXAMPLE';
  badge.style.cssText = 'position:absolute;top:8px;right:8px;background:#C6F432;color:#0A0A0B;font:700 11px/1 system-ui;padding:4px 8px;border-radius:4px;z-index:5';
  el.style.position = 'relative';
  el.appendChild(badge);
});
const box = await sponsor.boundingBox();
await page.screenshot({
  path: 'src/assets/social/placements/featured-card-example.png',
  clip: { x: Math.max(0, box.x - 8), y: Math.max(0, box.y - 8), width: box.width + 16, height: box.height + 16 },
  type: 'png'
});
console.log('featured ok', box);

// --- Category page: inject sponsor strip ---
await page.goto('http://127.0.0.1:8080/?cat=database#browse', { waitUntil: 'networkidle', timeout: 60000 });
await page.waitForTimeout(500);
await page.evaluate(() => {
  const wrap = document.querySelector('#browse') || document.querySelector('.wrap') || document.body;
  const bar = document.createElement('aside');
  bar.id = 'ex-cat-sponsor';
  bar.innerHTML = `
    <div style="display:flex;align-items:center;gap:14px;padding:14px 16px;margin:12px 0 18px;border:1px solid rgba(198,244,50,.45);border-radius:12px;background:rgba(198,244,50,.06);position:relative">
      <div style="width:48px;height:48px;border-radius:10px;background:#C6F432;color:#0A0A0B;display:flex;align-items:center;justify-content:center;font:800 14px system-ui">EX</div>
      <div style="flex:1;min-width:0">
        <div style="font-size:12px;opacity:.7;margin-bottom:2px">Sponsored · Category: Database</div>
        <div style="font-weight:700">ExampleDB Tools</div>
        <div style="font-size:13px;opacity:.85">Example logo + link on this category page. One sponsor per category.</div>
      </div>
      <a href="/advertise/" style="font-size:13px">example.com →</a>
      <span style="position:absolute;top:8px;right:8px;background:#C6F432;color:#0A0A0B;font:700 11px/1 system-ui;padding:4px 8px;border-radius:4px">EXAMPLE</span>
    </div>`;
  const h = wrap.querySelector('h2, .sh, .rowh') || wrap.firstElementChild;
  if (h && h.parentNode) h.parentNode.insertBefore(bar, h.nextSibling);
  else wrap.prepend(bar);
});
const cat = page.locator('#ex-cat-sponsor');
await cat.scrollIntoViewIfNeeded();
const cbox = await cat.boundingBox();
await page.screenshot({
  path: 'src/assets/social/placements/category-slot-example.png',
  clip: { x: Math.max(0, cbox.x - 8), y: Math.max(0, cbox.y - 8), width: Math.min(1200, cbox.width + 16), height: cbox.height + 16 },
  type: 'png'
});
console.log('category ok', cbox);

// --- Newsletter mock (standalone HTML) ---
await page.setContent(`<!doctype html><html><head><meta charset=utf-8>
<style>
  body{margin:0;background:#111;font:16px/1.5 system-ui,sans-serif;color:#eee}
  .mail{max-width:560px;margin:24px auto;background:#1a1a1c;border-radius:12px;overflow:hidden;border:1px solid #333}
  .banner{background:#C6F432;color:#0A0A0B;padding:18px 20px;font-weight:800;font-size:18px}
  .body{padding:20px}
  .muted{color:#9a9a9e;font-size:13px}
  .spon{margin-top:22px;padding:14px 16px;border:1px dashed rgba(198,244,50,.55);border-radius:10px;position:relative;background:rgba(198,244,50,.05)}
  .spon b{color:#C6F432}
  .tag{position:absolute;top:8px;right:8px;background:#C6F432;color:#0A0A0B;font:700 11px/1 system-ui;padding:4px 8px;border-radius:4px}
  a{color:#C6F432}
</style></head><body>
<div class="mail">
  <div class="banner">SkillMaxx Weekly · Issue #2 (example layout)</div>
  <div class="body">
    <p class="muted">Sample issue body — not a real send.</p>
    <p>Weekly install scorecard and one tip go here.</p>
    <div class="spon" id="nl">
      <span class="tag">EXAMPLE</span>
      <div class="muted" style="margin-bottom:6px"><b>Sponsor</b> · labeled in every issue</div>
      <p style="margin:0 0 8px"><b>ExampleMCP</b> — About fifty words introducing the tool, who it helps, and one clear install or docs link. This block is the newsletter sponsor placement.</p>
      <a href="https://skillmaxx.gilventures.ai/advertise/">https://example.com/skill</a>
    </div>
  </div>
</div>
</body></html>`, { waitUntil: 'load' });
await page.setViewportSize({ width: 640, height: 520 });
const nl = page.locator('#nl');
const nbox = await nl.boundingBox();
// shot whole mail for context + tight crop of sponsor
await page.locator('.mail').screenshot({ path: 'src/assets/social/placements/newsletter-sponsor-example.png', type: 'png' });
console.log('newsletter ok', nbox);

await b.close();
