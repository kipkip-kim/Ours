// usage: node render_seg.js page.html out.mp4 fps duration worker nWorkers
// Renders this worker's contiguous slice of frames and pipes them straight into ffmpeg
// (near-lossless x264), so the full 60fps song never has to sit on disk as PNGs.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [page_, out, fpsS, durS, wS, nwS] = process.argv.slice(2);
  const fps = +fpsS, n = Math.round(+durS * fps), w = +wS, nw = +nwS;
  const per = Math.ceil(n / nw), i0 = w * per, i1 = Math.min(n, (w + 1) * per);
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '8', '-pix_fmt', 'yuv444p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(page_));
  await page.evaluate(async () => { await document.fonts.ready; });
  await page.evaluate(() => window.fitAll && window.fitAll());
  for (let i = i0; i < i1; i++) {
    await page.evaluate(t => window.render(t), i / fps);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((i - i0) % 600 === 0) console.log(`w${w} ${i - i0}/${i1 - i0}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
})();
