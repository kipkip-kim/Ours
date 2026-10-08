const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [page_, out, fpsS, durS, wS, nwS] = process.argv.slice(2);
  const fps = +fpsS, n = Math.round(+durS * fps), w = +wS, nw = +nwS;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(page_));
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => i.onload = r))); });
  await page.evaluate(() => window.fitAll && window.fitAll());
  const per = Math.ceil(n / nw);
  for (let i = w * per; i < Math.min(n, (w + 1) * per); i++) {
    await page.evaluate(t => window.render(t), i / fps);
    await page.screenshot({ path: path.join(out, `f_${String(i).padStart(5, '0')}.png`) });
  }
  await browser.close();
})();
