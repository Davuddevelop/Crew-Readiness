/**
 * Dev check for the attention page (task A-1): drives a full run in a real browser with a fake clock.
 *
 *   python run.py &              # the app must be running on :5050
 *   node scripts/check_attention.js
 *
 * Math.random is pinned to 0.5, so every foreperiod is 2750 ms and every reaction time is exact.
 * Checks: premature before the light, premature under 100 ms, a miss after 1500 ms, Space and click
 * responses, held-Space repeats ignored, the exact POST body (only the four summary numbers), the
 * result label, and that Escape cancels without sending anything. Exits 1 on any failure.
 */
const { chromium } = require('playwright');

const BASE = process.env.BASE_URL || 'http://127.0.0.1:5050';
const FORE = 2750; // 1500 + 0.5 * (4000 - 1500)
let failures = 0;
function check(ok, what) {
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${what}`);
  if (!ok) failures += 1;
}

async function open(browser) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  const posts = [];
  page.on('request', (r) => {
    if (r.url().endsWith('/api/attention') && r.method() === 'POST') posts.push(r.postDataJSON());
  });
  await page.addInitScript(() => { Math.random = () => 0.5; });
  await page.clock.install();
  await page.goto(`${BASE}/attention?crew=plt-okafor`);
  await page.waitForFunction(() => !document.getElementById('rt-start').disabled);
  await page.clock.pauseAt(Date.now() + 1000); // from here on, only runFor() moves time
  return { ctx, page, posts, errors };
}

const lit = (page) => page.$eval('#rt-stage', (el) => el.classList.contains('rt-go'));

(async () => {
  const browser = await chromium.launch();

  // ---- a full run ----
  {
    const { ctx, page, posts, errors } = await open(browser);
    await page.click('#rt-start');
    check(await page.evaluate(() => document.activeElement.id) === 'rt-stage', 'focus moves to the reaction area on start');
    check(await page.isDisabled('#profile-select'), 'crew selector is locked during a run');

    // trial 1: too early (before the light), then too fast (50 ms), then a valid 250 ms response
    await page.clock.runFor(1000);
    await page.keyboard.press('Space');
    await page.clock.runFor(FORE);
    check(await lit(page), 'the light comes on after the foreperiod');
    await page.clock.runFor(50);
    await page.keyboard.press('Space');
    check(!(await lit(page)), 'a 50 ms response turns the light off (premature)');
    await page.clock.runFor(FORE);
    await page.clock.runFor(250);
    await page.keyboard.down('Space');
    await page.keyboard.down('Space'); // auto-repeat while held: must be ignored
    await page.keyboard.up('Space');

    // trial 2: a miss
    await page.clock.runFor(FORE);
    check(await lit(page), 'trial 2 lights up');
    await page.clock.runFor(1500);
    check(!(await lit(page)), 'no response for 1500 ms ends the trial as a miss');

    // trials 3-10: valid, alternating click and Space
    const rts = [200, 210, 220, 230, 240, 260, 270, 280];
    for (const [i, rt] of rts.entries()) {
      await page.clock.runFor(FORE);
      await page.clock.runFor(rt);
      if (i % 2) await page.keyboard.press('Space');
      else await page.click('#rt-stage');
    }
    await page.waitForSelector('#rt-result:not([hidden])');
    const text = await page.textContent('#rt-result');
    check(posts.length === 1, `exactly one POST (${posts.length})`);
    const expected = { profile_id: 'plt-okafor', trials: 10, median_rt_ms: 240, premature_count: 2, miss_count: 1 };
    check(JSON.stringify(posts[0]) === JSON.stringify(expected), `POST body ${JSON.stringify(posts[0])}`);
    check(text.includes('Illustrative reaction-time check. Not a medical test.'), 'result carries the label');
    check(text.includes('240 ms') && text.includes('9 of 10'), 'result shows median and valid trials');
    check(text.includes('Saved.'), 'result says it was saved');
    check(!(await page.textContent('body')).includes('Not implemented'), 'no "Not implemented" text');
    check(!(await page.isDisabled('#profile-select')), 'crew selector unlocked after the run');
    check(errors.length === 0, `no console errors ${errors.join(' | ')}`);
    await ctx.close();
  }

  // ---- Escape cancels and sends nothing ----
  {
    const { ctx, page, posts } = await open(browser);
    await page.click('#rt-start');
    await page.clock.runFor(FORE + 200);
    await page.keyboard.press('Space');
    await page.keyboard.press('Escape');
    await page.clock.runFor(20000);
    check(posts.length === 0, 'Escape cancels the run without a POST');
    check((await page.textContent('#rt-message')).includes('Nothing was sent'), 'cancel message shown');
    check(await page.evaluate(() => document.activeElement.id) === 'rt-start', 'focus returns to Start after cancel');
    await ctx.close();
  }

  await browser.close();
  console.log(failures ? `\n${failures} FAILED` : '\nATTENTION CHECK OK');
  process.exit(failures ? 1 : 0);
})();
