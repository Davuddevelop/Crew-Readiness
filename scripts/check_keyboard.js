/**
 * Dev check for keyboard behaviour on Dashboard, Replay and Evidence (polish pass, F-3).
 *
 *   python run.py &              # the app must be running on :5050
 *   node scripts/check_keyboard.js
 *
 * 1. Dashboard "Review needed": accepting a new normal with the keyboard keeps focus on the page (on the updated
 *    advisory) instead of dropping it to <body>. The accept call is stubbed in the browser, so the database is untouched.
 * 2. Every horizontally scrolling table can be reached with Tab, so keyboard users can scroll it at phone width.
 * 3. No page scrolls sideways at 390 px.
 * Exits 1 on any failure.
 */
const { chromium } = require('playwright');

const BASE = process.env.BASE_URL || 'http://127.0.0.1:5050';
let failures = 0;
function check(ok, what) {
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${what}`);
  if (!ok) failures += 1;
}

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' });

  // ---- 1. Review needed -> accept, keyboard only ----
  {
    const page = await ctx.newPage();
    let accepted = false;
    await page.route('**/api/readiness/plt-okafor', async (route) => {
      const res = await route.fetch();
      const body = await res.json();
      body.baseline_review = accepted ? null : { message: 'Stubbed: the last sessions were kept out of the baseline.' };
      await route.fulfill({ response: res, json: body });
    });
    await page.route('**/api/readiness/plt-okafor/accept-new-normal', (route) => {
      accepted = true;
      return route.fulfill({ status: 200, json: { accepted: [] } });
    });
    page.on('dialog', (d) => d.accept());
    await page.goto(`${BASE}/dashboard?crew=plt-okafor`);
    await page.waitForSelector('#detail-review:not([hidden])');
    await page.focus('#detail-accept');
    await page.keyboard.press('Enter');
    await page.waitForSelector('#detail-review', { state: 'hidden' });
    const focused = await page.evaluate(() => document.activeElement.id || document.activeElement.tagName);
    check(focused === 'detail-advisory', `after accepting, focus is on the advisory (${focused})`);
    await page.close();
  }

  // ---- 2 and 3. tables reachable by Tab; no sideways scroll ----
  for (const path of ['/dashboard', '/replay', '/evidence']) {
    const page = await ctx.newPage();
    await page.goto(BASE + path);
    await page.waitForTimeout(1200);
    const r = await page.evaluate(() => {
      const wraps = [...document.querySelectorAll('.table-wrap')].filter((w) => w.offsetParent !== null);
      return {
        total: wraps.length,
        reachable: wraps.filter((w) => w.tabIndex === 0 && w.getAttribute('aria-label')).length,
        sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      };
    });
    check(r.total === r.reachable, `${path}: ${r.reachable} of ${r.total} scrolling tables reachable by Tab, with a name`);
    check(r.sideways <= 0, `${path}: no sideways page scroll at 390 px (${r.sideways})`);
    await page.close();
  }

  await browser.close();
  console.log(failures ? `\n${failures} FAILED` : '\nKEYBOARD CHECK OK');
  process.exit(failures ? 1 : 0);
})();
