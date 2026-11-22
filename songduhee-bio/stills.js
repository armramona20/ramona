// Quick preview: render chosen timestamps to PNGs. Usage: node stills.js outdir t1 t2 ...
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [out, ...ts] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'index.html') + '?render=1'); await p.evaluate(() => window.ready());
  for (const t of ts) { await p.evaluate(t => window.renderAt(t), +t); await p.screenshot({ path: `${out}/t${t}.jpg`, type: 'jpeg', quality: 70 }); }
  await b.close();
})();
