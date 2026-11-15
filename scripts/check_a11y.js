/**
 * Dev check: accessibility audit of every page at desktop and phone width with axe-core (WCAG 2.0/2.1 A and AA plus best practices).
 *
 *   npm install axe-core          # dev only, in any folder; or set AXE_PATH to its axe.min.js
 *   python run.py &               # on :5050
 *   node scripts/check_a11y.js    # prints NO VIOLATIONS, or each violation with a page and a selector; exits 1 if any
 */
const { chromium } = require('playwright'); const fs=require('fs');
const axe=fs.readFileSync(process.env.AXE_PATH || require.resolve('axe-core/axe.min.js'),'utf8');
(async()=>{const b=await chromium.launch();const out={};
for (const [name,vp] of [['desktop',{width:1280,height:900}],['phone',{width:390,height:844}]]) {
 const p=await b.newPage({viewport:vp});
 for (const path of ['/','/me?crew=plt-okafor','/monitor','/attention','/mission','/dashboard?crew=plt-okafor','/brief','/replay','/evidence','/about','/status']) {
  await p.goto('http://127.0.0.1:5050'+path);await p.waitForTimeout(2200);
  await p.evaluate(axe);
  const r=await p.evaluate(()=>axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','best-practice']}}));
  for (const v of r.violations) { const k=v.id+' | '+v.impact; (out[k]=out[k]||{help:v.help,pages:new Set(),nodes:[]}); out[k].pages.add(name+' '+path); if(out[k].nodes.length<2) out[k].nodes.push(v.nodes[0].target.join(' ')+'  '+(v.nodes[0].failureSummary||'').split('\n').slice(0,2).join(' ').slice(0,160)); }
 }
 await p.close();}
for (const [k,v] of Object.entries(out)) console.log(k,'\n  ',v.help,'\n  pages:',[...v.pages].slice(0,6).join('; '),'(',v.pages.size,')\n  e.g.',v.nodes.join('\n       '));
if(!Object.keys(out).length) console.log('NO VIOLATIONS'); else process.exitCode = 1;
await b.close();})();
