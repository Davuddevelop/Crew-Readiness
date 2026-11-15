/**
 * Dev check for the store-and-forward summary on /mission, in a real browser: the text is built on the device from the page, carries the
 * suggestion, the check-in notice and the honest disclaimer, can be saved as a file, and nothing is sent.
 *   python run.py &  (demo data: flask --app run reset-demo)   node scripts/check_ground.js
 */
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://127.0.0.1:5050';
let failures = 0;
const check = (ok, what) => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${what}`); if (!ok) failures += 1; };
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ acceptDownloads: true, permissions: ['clipboard-read', 'clipboard-write'] });
  const p = await ctx.newPage(); const errs = [], writes = [];
  p.on('pageerror', (e) => errs.push(e.message)); p.on('request', (r) => { if (r.method() !== 'GET') writes.push(r.url()); });
  await p.goto(`${BASE}/mission`); await p.waitForFunction(() => document.querySelector('#advisory .chip'));
  await p.click('#ground-make');
  const t = await p.inputValue('#ground-text');
  check(t.startsWith('CREW READINESS: SUMMARY FOR THE GROUND') && t.includes('the software did not send it'), 'the summary says it was prepared by a person, not sent');
  check(/SUGGESTION: (NOMINAL|CHECK_IN|REVIEW)/.test(t) && t.includes('CHECK-INS:'), 'it carries the suggestion and the check-in notice');
  check(t.includes('not a medical assessment') && t.includes('simulated data'), 'it carries the honest disclaimer');
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#ground-save')]);
  check(dl.suggestedFilename() === 'crew-readiness-summary-for-the-ground.txt', 'it can be saved as a text file');
  await p.click('#ground-copy'); check((await p.evaluate(() => navigator.clipboard.readText())).startsWith('CREW READINESS'), 'it can be copied');
  check(writes.length === 0, `nothing was sent: no write requests${writes.length ? ' (' + writes[0] + ')' : ''}`);
  check(errs.length === 0, `no script errors${errs.length ? ': ' + errs[0] : ''}`);
  await b.close(); console.log(failures ? `\nGROUND CHECK FAILED (${failures})` : '\nGROUND CHECK OK'); process.exit(failures ? 1 : 0);
})();
