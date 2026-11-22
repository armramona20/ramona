// Render cover.html -> cover.jpg (1080x1920)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'cover.html'));
  await p.evaluate(async () => { await document.fonts.ready;
    await Promise.all(['700','800','900'].map(w => document.fonts.load(`${w} 40px Kanit`, 'กข')));
    await Promise.all([...document.images].map(i => i.decode())); });
  await p.locator('#c').screenshot({ path: path.join(__dirname, 'cover.jpg'), type: 'jpeg', quality: 92 });
  await b.close();
})();
