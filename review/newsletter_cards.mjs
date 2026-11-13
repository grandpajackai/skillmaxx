import { chromium } from 'playwright';
const [base, out] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
const pages = ['/', '/newsletter/', '/newsletter/issue-1/', '/newsletter/issue-2/', '/newsletter/issue-3/', '/reports/latest/', '/reports/2026-11-13/'];
for (const path of pages) {
  await p.goto(base + path + '?qa=' + Date.now(), { waitUntil: 'load' });
  const cards = p.locator('.bhf'); const n = await cards.count();
  const res = [];
  for (let i = 0; i < n; i++) {
    await cards.nth(i).scrollIntoViewIfNeeded();
    try { await cards.nth(i).locator('iframe').first().waitFor({ state: 'visible', timeout: 15000 }); } catch {}
    res.push(await cards.nth(i).evaluate(e => ({ iframe: !!e.querySelector('iframe'), h: e.querySelector('iframe')?.offsetHeight || 0, placeholder: !!e.querySelector('.bhph'), src: e.querySelector('iframe')?.src || '' })));
  }
  const heads = await p.locator('section.nlcard h2').allTextContents();
  console.log(path, JSON.stringify({ cards: res.map(r => [r.iframe, r.h, r.placeholder]), heads, src: res[0]?.src.split('?')[0] }));
  if (path === '/newsletter/issue-2/' && out) { await p.waitForTimeout(1500); await p.locator('section.nlcard').last().screenshot({ path: out }); }
}
await b.close();
