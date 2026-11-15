/**
 * Dev check for "your sleep and your reaction time, on this device" (plan v4, W2), in a real browser. Notes are written straight into
 * localStorage on the dates of the demo person's real reaction checks; the page must compare them in the browser, say "not enough"
 * when it should, label the example as made up, and make no write requests.
 *   python run.py &    (demo data: flask --app run reset-demo)    node scripts/check_insight.js
 */
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://127.0.0.1:5050';
let failures = 0;
const check = (ok, what) => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) failures += 1; };
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const errs = [], writes = [], gets = [];
  p.on('pageerror', (e) => errs.push(e.message));
  p.on('request', (r) => { if (r.method() !== 'GET') writes.push(`${r.method()} ${r.url()}`); else if (r.url().includes('/api/attention/')) gets.push(r.url()); });
  await p.goto(`${BASE}/me?crew=plt-okafor`);
  await p.waitForFunction(() => document.getElementById('insight-text').textContent.length > 5);
  check((await p.textContent('#insight-text')).includes('Not enough paired days yet'), 'with no notes it says there is not enough yet');

  const dates = await p.evaluate(async () => (await (await fetch('/api/attention/plt-okafor')).json()).checks.map((c) => c.created_at));
  const days = [...new Set(dates.map((d) => new Date(d).toLocaleDateString('en-CA')))].slice(0, 6);
  check(days.length === 6, `the demo person has reaction checks on at least 6 different days (${days.length})`);
  await p.evaluate((ds) => {
    const notes = ds.map((d, i) => ({ t: new Date(`${d}T12:00:00`).toISOString(), sleep: i < 3 ? 5 : 8, feel: 5 }));
    localStorage.setItem('crew-readiness-notes-v1:plt-okafor', JSON.stringify(notes));
  }, days);
  await p.reload();
  await p.waitForFunction(() => /On the 3 days/.test(document.getElementById('insight-text').textContent));
  const t = await p.textContent('#insight-text');
  check(/On the 3 days you noted under 6 hours of sleep, your reaction time was (about \d+ ms (slower|faster) than|the same as) on the 3 days you noted 6 or more/.test(t), `it compares the two groups: ${t.slice(0, 120)}`);

  await p.click('#insight-example');
  check((await p.textContent('#insight-text')).startsWith('EXAMPLE (made-up numbers):'), 'the example is labelled as made-up numbers');
  check(gets.every((u) => !/sleep|note|feel/i.test(u)), 'the only request is a GET of the person\'s own checks, carrying no note data');
  check(writes.length === 0, `no write requests${writes.length ? ' (' + writes[0] + ')' : ''}`);
  check(errs.length === 0, `no script errors${errs.length ? ': ' + errs[0] : ''}`);
  await b.close();
  console.log(failures ? `\nINSIGHT CHECK FAILED (${failures})` : '\nINSIGHT CHECK OK'); process.exit(failures ? 1 : 0);
})();
