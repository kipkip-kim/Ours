// usage: node render.js page.html outDir fps duration [stillTimes(comma)]
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [page_, out, fpsS, durS, stills] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(page_));
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => i.onload = r))); });
  await page.evaluate(() => window.fitAll && window.fitAll());
  fs.mkdirSync(out, { recursive: true });
  const times = stills ? stills.split(',').map(Number) : null;
  const fps = +fpsS, n = times ? times.length : Math.round(+durS * fps);
  for (let i = 0; i < n; i++) {
    const t = times ? times[i] : i / fps;
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: path.join(out, times ? `still_${t.toFixed(2)}.png` : `f_${String(i).padStart(5, '0')}.png`) });
  }
  await browser.close();
})();
