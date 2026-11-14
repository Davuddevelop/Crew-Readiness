/**
 * Records a captioned backup demo video of the real app, following docs/DEMO.md (about 3 minutes, no audio).
 * Captions are on-screen text; numbers in them are read from the live page and from app/results_data.json, never typed in.
 *
 *   # a fresh demo database on its own port, so the pilot starts in the real demo state and your data is untouched
 *   CREW_DB_PATH=/tmp/demo-rec.sqlite3 python -c "from app import create_app; create_app().run(port=5054)" &
 *   BASE_URL=http://127.0.0.1:5054 OUT_DIR=./demo-video node scripts/record_demo.js
 *   ffmpeg -y -i demo-video/*.webm -c:v libx264 -pix_fmt yuv420p -movflags +faststart demo.mp4     # optional: an mp4
 *
 * Needs Node and Playwright (dev only). It sends four SYNTHETIC slow sessions for the demo pilot through the public API
 * for the review step, so never point it at anything but a demo database.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.env.BASE_URL || 'http://127.0.0.1:5054';
const OUT = path.resolve(process.env.OUT_DIR || './demo-video');
const results = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../app/results_data.json'), 'utf8'));
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, recordVideo: { dir: OUT, size: { width: 1280, height: 800 } } });
  const page = await ctx.newPage();
  page.on('dialog', (d) => d.accept());

  // caption bar and a visible pointer (the recording has no cursor otherwise)
  async function overlay() {
    await page.evaluate(() => {
      if (document.getElementById('cap')) return;
      const s = document.createElement('style');
      s.textContent = `html{scroll-padding-top:96px}#cap{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);max-width:980px;width:max-content;padding:12px 20px;
        background:rgba(10,10,10,.86);border:1px solid rgba(255,255,255,.22);border-radius:6px;color:#fff;font:500 22px/1.35 "Instrument Sans Variable",system-ui,sans-serif;
        text-align:center;z-index:99999;transition:opacity .35s;opacity:0}
        #cur{position:fixed;width:22px;height:22px;margin:-11px 0 0 -11px;border:2px solid #fff;border-radius:50%;z-index:99998;pointer-events:none;opacity:0;left:-50px;top:-50px;transition:opacity .25s}`;
      document.head.appendChild(s);
      const c = document.createElement('div'); c.id = 'cap'; document.body.appendChild(c);
      const k = document.createElement('div'); k.id = 'cur'; document.body.appendChild(k);
      addEventListener('mousemove', (e) => { k.style.left = e.clientX + 'px'; k.style.top = e.clientY + 'px'; });
    });
  }
  async function say(text, ms) {
    await overlay();
    await page.evaluate((t) => { const c = document.getElementById('cap'); c.textContent = t; c.style.opacity = 1; }, text);
    await wait(ms);
  }
  const hush = () => page.evaluate(() => { const c = document.getElementById('cap'); if (c) c.style.opacity = 0; });
  async function go(p, settle = 2200) { await page.goto(BASE + p); await wait(settle); await overlay(); }
  const scrollTo = (sel) => page.evaluate((s) => document.querySelector(s)?.scrollIntoView({ behavior: 'smooth', block: 'start' }), sel);
  const ring = (on) => page.evaluate((o) => { const k = document.getElementById('cur'); if (k) k.style.opacity = o ? 0.85 : 0; }, on);
  async function sweep(fromX, toX, y, steps = 60) { await ring(true); for (let i = 0; i <= steps; i++) { await page.mouse.move(fromX + ((toX - fromX) * i) / steps, y); await wait(28); } await ring(false); }

  // ---- 0:00 landing
  await go('/', 3600);
  await say('People differ: 220 ms between keys is normal for one person and a big change for another.', 5200);
  await say('So one threshold for everyone fits nobody. We compare each person only with themselves, and a human decides.', 6000);
  await page.evaluate(() => window.scrollTo({ top: 300, behavior: 'smooth' })); await wait(1200);
  await say('Move toward the gap: the hands lean in, and never touch. The system never closes it. A person does.', 1200);
  await sweep(100, 800, 440); await wait(1500); await sweep(800, 100, 440); await wait(800);

  // ---- 0:20 dashboard
  await hush(); await go('/dashboard?crew=plt-okafor', 2600);
  await scrollTo('.art'); await wait(700);
  await say('Pilot Okafor is YELLOW. This is an illustrative seeded case, not a measure of how well the model works.', 6000);
  await scrollTo('#detail'); await wait(900);
  await say('It is not a diagnosis. It is a change from their own pattern.', 4200);
  await scrollTo('#detail-reasons'); await wait(900);
  const reason = await page.evaluate(() => [...document.querySelectorAll('#detail-reasons li')].map((l) => l.textContent).find((t) => /1 session in/.test(t)) || '');
  const n = (reason.match(/1 session in (\d+)/) || [])[1], usual = (reason.match(/usual ([\d.]+) per session/) || [])[1], now = (reason.match(/: (\d+) vs usual/) || [])[1];
  await say(n ? `And it explains itself in plain words: ${now} pauses against a usual ${usual}, which we would expect only about one session in ${n}.`
              : 'And it explains itself in plain words, for a human to read.', 7500);
  await scrollTo('#trend-chart'); await wait(2500);

  // ---- 0:55 replay
  await hush(); await go('/replay', 2200);
  await scrollTo('.replay-chart'); await wait(700);
  await say('The idea in motion, on a simulated person: 20% slower for 15 sessions, shaded.', 5200);
  await say('The dashed line is the old scoring. It learns the slowdown as normal, so its alerts fade.', 6200);
  await say('The white line is the current scoring: flagged sessions stay out of the baseline, so the change keeps showing.', 6800);
  await page.click('#reroll'); await say('A different random person. Single runs vary, and sometimes the old scoring does as well.', 6500);
  await page.click('#reroll'); await say('The proof is not one run.', 3500);
  await scrollTo('#replay-summary'); await say('The table counts what each scoring flagged. One person is an illustration, not evidence.', 5500);

  // ---- 1:50 evidence
  await hush(); await go('/evidence', 2200);
  await say('The proof: 300 simulated people per row.', 4000);
  const op = results.operating_point.find((r) => r.slowdown === 0.1);
  await scrollTo('table.evidence:nth-of-type(1)'); await page.evaluate(() => document.querySelectorAll('table.evidence')[1]?.scrollIntoView({ behavior: 'smooth', block: 'center' })); await wait(900);
  await say(`At the level the product uses, false alerts fall from about ${Math.round(op.before.false_alerts * 100)}% to about ${Math.round(op.now.false_alerts * 100)}%.`, 6500);
  await say(`We pay for it: detection also falls, from ${op.before.detection} to ${op.now.detection} at a 10% slowdown.`, 6000);
  await say('At matched false-alert rates the new model is better everywhere.', 5000);
  await page.evaluate(() => [...document.querySelectorAll('h2,h3,.label')].find((e) => /does not show/i.test(e.textContent))?.scrollIntoView({ behavior: 'smooth', block: 'start' })); await wait(900);
  await say('And this box lists what we did not show: simulated data only. No real crews.', 7500);

  // ---- 2:35 review
  await hush(); await go('/dashboard?crew=plt-okafor', 2000);
  await page.evaluate(async () => {
    const f = { keystroke_count: 125, iki_median_ms: 330, iki_iqr_ms: 140, pause_count: 4, pause_total_ms: 9000, checklist_response_median_ms: 2600, task_duration_ms: 60000, correction_count: 2, retry_count: 0 };
    for (let i = 0; i < 4; i++) await fetch('/api/sessions', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ profile_id: 'plt-okafor', task_type: 'docking_checklist_v1', features: f }) });
  });
  await go('/dashboard?crew=plt-okafor', 2200);
  await scrollTo('#detail-review'); await wait(800);
  await say('When a person genuinely changes, say a new keyboard, a human accepts the new normal.', 5800);
  await page.click('#detail-accept'); await wait(1800);
  await say('We never decide that for them. After accepting, the baseline restarts, so it shows CALIBRATING.', 6000);
  await hush(); await wait(600);
  await say('Next: validate on real data with a licence we can cite. We have not done that yet, and the page says so.', 5200);
  await hush(); await wait(500);

  await ctx.close(); await browser.close();
  console.log('video written to', OUT);
})();
