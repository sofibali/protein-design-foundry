// The drawing kit the figures on these pages are made of.
//
// Shared by the protocol library (workflows.html) and the cart details
// (blueprint.html), inlined into both by scripts/build_pages.py so each page
// stays a single file you can mail. Every panel is built from these few
// primitives, which is what keeps fifteen protocols and nineteen carts
// looking like they came out of the same pen.
(function () {
const esc = t => String(t).replace(/[&<>]/g, m => ({'&': '&amp;', '<': '&lt;', '>': '&gt;'}[m]));
// Two panels per protocol, drawn the way panel A of a paper is drawn: what
// physically happens on the deck, and what the readout looks like when it
// comes back. The sample panels are sketches of the shape of the answer,
// not measurements - every one of them carries a tag saying so.
const gv = (o, k, d) => (o && o[k] !== undefined) ? o[k] : d;
const n1 = v => Math.round(v * 10) / 10;
const G = {
  // primitives
  r: (x, y, w, h, o) => `<rect x="${n1(x)}" y="${n1(y)}" width="${n1(w)}" height="${n1(h)}"`
    + ` rx="${gv(o, 'r', 2.5)}" class="${gv(o, 'c', 'ln')}"`
    + ((o && o.f) ? ` fill="${o.f}" fill-opacity="${gv(o, 'o', .16)}"` : '') + `/>`,
  c: (x, y, rr, o) => `<circle cx="${n1(x)}" cy="${n1(y)}" r="${n1(rr)}" class="${gv(o, 'c', 'ln')}"`
    + ((o && o.f) ? ` fill="${o.f}" fill-opacity="${gv(o, 'o', .16)}"` : '') + `/>`,
  dot: (x, y, rr, col) => `<circle cx="${n1(x)}" cy="${n1(y)}" r="${n1(rr)}" class="fl"`
    + ` fill="${col || 'var(--ink)'}"/>`,
  l: (x1, y1, x2, y2, o) => `<line x1="${n1(x1)}" y1="${n1(y1)}" x2="${n1(x2)}" y2="${n1(y2)}"`
    + ` class="${gv(o, 'c', 'ln')}"/>`,
  p: (d, o) => `<path d="${d}" class="${gv(o, 'c', 'ln')}"`
    + ((o && o.f) ? ` fill="${o.f}" fill-opacity="${gv(o, 'o', .16)}"` : '') + `/>`,
  t: (x, y, s, o) => `<text x="${n1(x)}" y="${n1(y)}" class="${gv(o, 'c', 'lb')}"`
    + ` text-anchor="${gv(o, 'a', 'middle')}"`
    + ((o && o.rot) ? ` transform="rotate(${o.rot} ${n1(x)} ${n1(y)})"` : '') + `>${esc(s)}</text>`,

  // an arrow with its head drawn as a path, so no page-wide marker ids
  a: (x1, y1, x2, y2, o) => {
    const an = Math.atan2(y2 - y1, x2 - x1), hh = gv(o, 'h', 4.2);
    const bx = x2 - Math.cos(an) * hh, by = y2 - Math.sin(an) * hh;
    const px = Math.sin(an) * hh * .52, py = -Math.cos(an) * hh * .52;
    const col = gv(o, 'fill', 'var(--muted)');
    return G.l(x1, y1, bx, by, {c: gv(o, 'c', 'mu')})
      + `<path class="fl" fill="${col}" d="M${n1(x2)} ${n1(y2)}L${n1(bx + px)} ${n1(by + py)}`
      + `L${n1(bx - px)} ${n1(by - py)}Z"/>`;
  },

  // a plate seen from above, optionally with wells filled by a function
  plate: (x, y, w, h, cols, rows, o) => {
    o = o || {};
    let s = G.r(x, y, w, h, {r: 2, f: o.f, o: o.o, c: gv(o, 'c', 'ln')});
    const pd = gv(o, 'pad', 3), dx = (w - 2 * pd) / cols, dy = (h - 2 * pd) / rows;
    const rr = Math.min(dx, dy) * gv(o, 'wr', .32);
    for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) {
      const cx = x + pd + dx * (i + .5), cy = y + pd + dy * (j + .5);
      const fill = o.well ? o.well(i, j) : null;
      s += fill ? G.dot(cx, cy, rr, fill) : G.c(cx, cy, rr, {c: 'mu'});
    }
    return s;
  },

  // a single well seen in section, and the liquid standing in it
  well: (x, y, w, h, o) => G.p(`M${n1(x)} ${n1(y)}V${n1(y + h - 5)}Q${n1(x)} ${n1(y + h)}`
    + ` ${n1(x + 5)} ${n1(y + h)}H${n1(x + w - 5)}Q${n1(x + w)} ${n1(y + h)} ${n1(x + w)}`
    + ` ${n1(y + h - 5)}V${n1(y)}`, o),
  liq: (x, y, w, h, top, col) => G.p(`M${n1(x)} ${n1(top)}V${n1(y + h - 5)}Q${n1(x)} ${n1(y + h)}`
    + ` ${n1(x + 5)} ${n1(y + h)}H${n1(x + w - 5)}Q${n1(x + w)} ${n1(y + h)} ${n1(x + w)}`
    + ` ${n1(y + h - 5)}V${n1(top)}Z`, {c: 'none', f: col, o: .22}),

  // axes, drawn as an L
  ax: (x, y, w, h) => G.p(`M${n1(x)} ${n1(y)}V${n1(y + h)}H${n1(x + w)}`, {c: 'mu'}),
  poly: (pts, o) => `<polyline points="${pts.map(p => n1(p[0]) + ',' + n1(p[1])).join(' ')}"`
    + ` class="${gv(o, 'c', 'ln')}"/>`,
  arc: (cx, cy, rr, a0, a1, col, wd) => {
    const pt = a => [cx + rr * Math.cos(a * Math.PI / 180), cy + rr * Math.sin(a * Math.PI / 180)];
    const s = pt(a0), e = pt(a1);
    return `<path d="M${n1(s[0])} ${n1(s[1])}A${rr} ${rr} 0 ${(a1 - a0) > 180 ? 1 : 0} 1`
      + ` ${n1(e[0])} ${n1(e[1])}" fill="none" stroke="${col}" stroke-width="${wd || 4}"/>`;
  }
};
// deterministic pseudo-random, so a figure draws the same way every time
const rnd = seed => { let s = seed; return () => (s = (s * 1103515245 + 12345) % 2147483648) / 2147483648; };
const svg = (body, label, h, w) => `<svg viewBox="0 0 ${w || 320} ${h || 136}" role="img"`
  + ` aria-label="${esc(label)}">` + body + `</svg>`;

// STEP GLYPHS START
// One small drawing per kind of step - what happens at that stop on a
// loop, and what each protocol in a proposed pipeline does. Keyed by
// draw: in _data/protocols.yml; the build fails on a step whose draw: is
// not here, and on a glyph here that nothing uses.
const STEP = {
'model': (x, y, c) => G.r(x - 13, y - 9, 26, 18, {r: 2, c: 'mu'})
  + G.p(`M${x - 8} ${y + 4}Q${x - 5} ${y - 7} ${x - 1} ${y}T${x + 8} ${y - 5}`, {c: 'ln'}),
'plot': (x, y, c) => G.p(`M${x - 11} ${y - 9}V${y + 8}H${x + 12}`, {c: 'mu'})
  + [6, 12, 9, 15].map((h, i) => G.r(x - 8 + i * 5.2, y + 8 - h, 3.6, h, {r: .6, f: c, o: .6, c: 'none'})).join(''),
'tune': (x, y, c) => G.arc(x, y, 10, 130, 400, 'var(--ink)', 1.3)
  + G.p(`M${x + 3} ${y - 12}L${x + 8} ${y - 8}L${x + 2} ${y - 4}`, {c: 'ln'})
  + G.dot(x, y, 2.6, c),
'plate': (x, y, c) => G.plate(x - 14, y - 8, 28, 16, 4, 2, {f: c, pad: 2.2}),
'assay': (x, y, c) => G.plate(x - 14, y - 2, 28, 12, 4, 2, {f: c, pad: 2})
  + G.a(x - 9, y - 14, x - 3, y - 5, {h: 3}) + G.a(x + 3, y - 5, x + 9, y - 14, {h: 3}),
'curve': (x, y, c) => G.p(`M${x - 12} ${y - 9}V${y + 8}H${x + 12}`, {c: 'mu'})
  + G.p(`M${x - 10} ${y + 6}Q${x - 1} ${y + 6} ${x + 1} ${y - 2}T${x + 10} ${y - 7}`, {c: 'ln'})
  + G.dot(x + 1, y - 2, 2, c),
'counter': (x, y, c) => G.r(x - 15, y - 1, 14, 10, {r: 5, f: c, o: .45})
  + G.r(x + 1, y - 1, 14, 10, {r: 5, c: 'mu dash'})
  + G.l(x + 4, y - 14, x + 12, y - 6, {c: 'mu'}) + G.l(x + 12, y - 14, x + 4, y - 6, {c: 'mu'}),
'pick': (x, y, c) => [0, 1, 2].map(i => G.l(x - 12, y - 6 + i * 6, x + 4, y - 6 + i * 6, {c: 'mu'})).join('')
  + G.r(x - 14, y - 9, 20, 6, {r: 1, f: c, o: .55})
  + G.p(`M${x + 8} ${y - 2}L${x + 8} ${y + 9}L${x + 11} ${y + 6}L${x + 14} ${y + 10}`, {c: 'ln'}),
'flask': (x, y, c) => G.p(`M${x - 4} ${y - 10}V${y - 3}L${x - 11} ${y + 8}H${x + 11}L${x + 4} ${y - 3}V${y - 10}Z`, {f: c, o: .35})
  + G.l(x - 6, y - 10, x + 6, y - 10),
'drop': (x, y, c) => G.l(x - 13, y + 7, x + 13, y + 7, {c: 'mu'})
  + G.p(`M${x - 9} ${y + 7}A9 7 0 0 1 ${x + 9} ${y + 7}Z`, {f: c, o: .4})
  + G.p(`M${x} ${y - 2}L${x + 4} ${y + 1}L${x} ${y + 5}L${x - 4} ${y + 1}Z`, {f: 'var(--ink)', o: .7, c: 'ln'}),
'xray': (x, y, c) => G.c(x, y, 3, {f: c, o: .8})
  + [7, 11].map(r => G.c(x, y, r, {c: 'mu'})).join('')
  + [[-7, -4], [6, -6], [9, 4], [-5, 8], [-11, 1], [3, 10]].map(d => G.dot(x + d[0], y + d[1], 1.4)).join(''),
'chem': (x, y, c) => G.p(`M${x - 5} ${y - 9}H${x + 5}L${x + 10} ${y}L${x + 5} ${y + 9}H${x - 5}`
    + `L${x - 10} ${y}Z`, {f: c, o: .35}) + G.c(x, y, 4, {c: 'mu'}),
'overlay': (x, y, c) => G.p(`M${x - 11} ${y + 5}Q${x - 7} ${y - 7} ${x - 2} ${y}T${x + 8} ${y - 6}`, {c: 'ln'})
  + G.p(`M${x - 8} ${y + 8}Q${x - 4} ${y - 4} ${x + 1} ${y + 3}T${x + 11} ${y - 3}`, {c: 'mu dash'}),
'dna': (x, y, c) => G.p(`M${x - 10} ${y - 9}Q${x} ${y} ${x - 10} ${y + 9}`, {c: 'ln'})
  + G.p(`M${x + 10} ${y - 9}Q${x} ${y} ${x + 10} ${y + 9}`, {c: 'ln'})
  + [-5, 0, 5].map(d => G.l(x - 7 + Math.abs(d) * .5, y + d, x + 7 - Math.abs(d) * .5, y + d, {c: 'mu'})).join(''),
'cells': (x, y, c) => G.c(x, y, 10, {f: c, o: .25})
  + [[-4, -3], [3, -4], [5, 2], [-2, 4], [-6, 1]].map(d => G.dot(x + d[0], y + d[1], 1.5)).join(''),
'beads': (x, y, c) => G.well(x - 7, y - 8, 18, 16) + G.liq(x - 7, y - 8, 18, 16, y - 4, c)
  + [0, 1, 2, 3].map(k => G.dot(x - 4, y - 4 + k * 3.4, 1.5)).join('')
  + G.r(x - 12, y - 4, 3.5, 11, {r: 1, f: 'var(--ink)', o: 1, c: 'fl'}),
'heat': (x, y, c) => G.r(x - 12, y, 24, 9, {r: 1.5, f: c, o: .5})
  + [0, 1, 2, 3].map(k => G.l(x - 9 + k * 6, y - 2 - k * 2.6, x - 9 + k * 6, y, {c: 'mu'})).join('')
  + G.p(`M${x - 10} ${y - 11}L${x - 4} ${y - 11}L${x + 2} ${y - 11}`, {c: 'mu'})
  + G.poly([[x - 10, y - 4], [x - 4, y - 7], [x + 2, y - 10], [x + 9, y - 12]], {c: 'ln'}),
};
// STEP GLYPHS END



window.FIGKIT = {G: G, svg: svg, rnd: rnd, gv: gv, STEP: STEP};
})();
