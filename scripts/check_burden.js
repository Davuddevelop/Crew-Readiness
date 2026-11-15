/**
 * Dev check for the alert-burden calculator on /evidence, in a real browser. Default inputs (4 people, 1 check-in a day, 180 days,
 * 1 in 20, 10 minutes) must give 720 check-ins and the arithmetic from the page's own embedded rate; the page makes no write requests.
 *   python run.py &    node scripts/check_burden.js
 */
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://127.0.0.1:5050';
let failures = 0;
const check = (ok, what) => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) failures += 1; };
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const errs = [], writes = []; p.on('pageerror', (e) => errs.push(e.message)); p.on('request', (r) => { if (r.method() !== 'GET') writes.push(r.url()); });
  await p.goto(`${BASE}/evidence`); await p.waitForSelector('#b-out tr');
  const rate = await p.evaluate(() => { const d = JSON.parse(document.getElementById('burden-data').textContent); return d.options[1].rate; });
  const text = async () => (await p.innerText('#b-out')).replace(/\s+/g, ' ');
  const fmt = (x) => (x >= 10 ? Math.round(x).toString() : x.toFixed(1));
  let t = await text();
  check(t.includes('720'), 'default crew gives 720 check-ins (4 x 1 x 180)');
  check(t.includes(`False alerts over the mission ${fmt(720 * rate)}`), `false alerts over the mission = 720 x ${(rate * 100).toFixed(1)} % = ${fmt(720 * rate)}`);
  check(t.includes(`Reviewer time over the mission ${fmt((720 * rate * 10) / 60)} hours`), 'reviewer time = alerts x 10 minutes');
  await p.fill('#b-crew', '6'); await p.fill('#b-days', '100'); await p.selectOption('#b-budget', '2');
  t = await text();
  check(t.includes('600'), 'changing the crew and the length updates the check-ins (6 x 1 x 100)');
  await p.fill('#b-crew', '9999'); t = await text();
  check(t.includes('1,200'), 'an absurd crew size is clamped to 12, not crashed (12 x 1 x 100 = 1,200)');
  check(errs.length === 0, `no script errors${errs.length ? ': ' + errs[0] : ''}`);
  check(writes.length === 0, 'the calculator makes no write requests');
  await b.close();
  console.log(failures ? `\nBURDEN CHECK FAILED (${failures})` : '\nBURDEN CHECK OK'); process.exit(failures ? 1 : 0);
})();
