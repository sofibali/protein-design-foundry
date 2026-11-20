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
const svg = (body, label, h) => `<svg viewBox="0 0 320 ${h || 136}" role="img"`
  + ` aria-label="${esc(label)}">` + body + `</svg>`;


window.FIGKIT = {G: G, svg: svg, rnd: rnd, gv: gv};
})();
