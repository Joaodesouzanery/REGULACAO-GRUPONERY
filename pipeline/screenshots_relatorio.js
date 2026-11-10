const {chromium} = require('playwright');
(async () => {
  const f = process.argv[2], out = process.argv[3];
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1280, height: 720}});
  await p.goto('file://' + f, {waitUntil: 'networkidle'});
  const els = await p.$$('.pg');
  for (let i = 0; i < els.length; i++) {
    await els[i].screenshot({path: out + '/p' + String(i + 1).padStart(2, '0') + '.png', scale: 'css'});
  }
  const ov = await p.$$eval('.pg', ps => ps.map((pg, i) => {
    const r = [];
    pg.querySelectorAll('.ev,.lead,.q-c,.sc-b,.mini,.evs,.sc').forEach(e => { if (e.scrollHeight > e.clientHeight + 2) r.push(e.className); });
    return r.length ? (i + 1) + ':' + r.join(',') : null;
  }).filter(Boolean));
  console.log('paginas', els.length, 'overflow', JSON.stringify(ov));
  await b.close();
})();
