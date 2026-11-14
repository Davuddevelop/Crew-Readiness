/** Renders app/static/img/share-card.png (1200 x 630) from scripts/assets/share-card.html. Needs Playwright (dev only).
 *    node scripts/assets/make_share_card.js */
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(__dirname, 'share-card.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: path.resolve(__dirname, '../../app/static/img/share-card.png') });
  await b.close(); console.log('wrote app/static/img/share-card.png');
})();
