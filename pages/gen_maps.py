#!/usr/bin/env python3
"""
Build maps.html - five one-page maps of the foundry pipelines.

Rules for this file, and they are strict:
  - labels, not sentences. No headline, no subtitle, no body copy, no callout.
  - counts are digits, never words.
  - one flat layer. No box inside a box, no tinted fill behind text.
  - nothing floats. Every slide is framed top and bottom, and every label
    is anchored to a rule, an axis or a shape - never adrift in whitespace.

Detail lives in foundry.html, workflows.html and gates.yml.

    python3 gen_maps.py          -> writes maps.html beside this file
"""

from pathlib import Path
from html import escape as esc

W, H = 1600, 900
L, R = 80, 1520          # the margins everything aligns to
TOP, BOT = 96, 828       # the frame rules; all content lives between them

BLUE = "#0072B2"
GREEN = "#009E73"
SKY = "#56B4E9"
ORANGE = "#D55E00"
PINK = "#CC79A7"

INK, MUTED, RULE = "var(--ink)", "var(--muted)", "var(--rule)"


# --------------------------------------------------------------------------

def t(x, y, s, size=20, fill=INK, weight=400, anchor="start", ls=0, op=1):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    o = f' fill-opacity="{op}"' if op != 1 else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}"{a}{l}{o}>{esc(s)}</text>')


def bar(x, y, w, col, h=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}"/>'


def line(x1, y1, x2, y2, col=RULE, sw=1.5, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' stroke-opacity="{op}"' if op != 1 else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" '
            f'stroke-width="{sw}"{d}{o}/>')


def arrow(x1, y1, x2, y2, col=MUTED, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" '
            f'stroke-width="{sw}" marker-end="url(#tip)"{d}/>')


def curve(x1, y1, x2, y2, cx, cy, col=RULE, sw=1.5, dash=None, tip=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#tip)"' if tip else ""
    return (f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="{col}" '
            f'stroke-width="{sw}"{m}{d}/>')


def dot(cx, cy, r, fill):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'


def gate(x, y, g, col):
    return (f'<rect x="{x}" y="{y}" width="50" height="30" rx="15" fill="none" '
            f'stroke="{col}" stroke-width="1.5"/>'
            + t(x + 25, y + 20, g, 15, col, 500, anchor="middle"))


def cap(x, y, s, fill=MUTED, anchor="start"):
    """A small-caps section marker."""
    return t(x, y, s, 15, fill, 500, anchor=anchor, ls="2.2")


def frame(name, n):
    """Identical chrome on every page - this is what stops things floating."""
    return (cap(L, 70, name)
            + t(R, 70, f"{n}/5", 17, MUTED, anchor="end")
            + line(L, TOP, R, TOP, RULE, 1)
            + line(L, BOT, R, BOT, RULE, 1))


# ==========================================================================

def slide1():
    s = [frame("CAMPAIGN", 1)]

    s.append(cap(L, 300, "TARGET IN"))
    s.append(cap(R, 300, "VERDICTS OUT", anchor="end"))

    cols = [
        (BLUE, "Design", "worth making?", "UCSF compute", ["D0"]),
        (GREEN, "Express", "usable?", "on the machine", ["D1", "D2"]),
        (ORANGE, "Test", "real?", "on the machine", ["D3", "D4", "D5", "D6"]),
        (PINK, "Structure", "as designed?", "off the machine", ["D7", "D8"]),
    ]
    cw, cg, ry = 330, 40, 452
    for i, (col, name, dec, where, gates) in enumerate(cols):
        x = L + i * (cw + cg)
        s.append(t(x, ry - 20, name, 42, INK, 500))
        s.append(bar(x, ry, cw, col))
        s.append(t(x, ry + 50, dec, 23, col))
        gx = x
        for g in gates:
            s.append(gate(gx, ry + 78, g, col))
            gx += 58
        s.append(t(x, ry + 160, where, 18, MUTED))
        # the column keeps going to the frame, so nothing sits adrift
        s.append(line(x, ry + 186, x + cw, ry + 186, RULE, 1, op=0.7))
        if i < 3:
            s.append(arrow(x + cw + 8, ry + 4, x + cw + cg - 4, ry + 4, RULE, 3))

    return "".join(s)


# ==========================================================================

def slide2():
    s = [frame("FUNNEL", 2)]

    x0, segw, cy = 110, 232, 462
    halves = [170, 112, 64, 33, 17, 10]
    bands = [
        (BLUE, "1,000+", "designed", "worth making?"),
        (GREEN, "100s", "made", "expresses?"),
        (ORANGE, "10s", "bind", "binds?"),
        (ORANGE, "<10", "confirmed", "how tight?  which face?"),
        (PINK, "4", "per round", "structure?"),
    ]

    for i, (col, big, small, q) in enumerate(bands):
        x1, x2 = x0 + i * segw, x0 + (i + 1) * segw
        h1, h2 = halves[i], halves[i + 1]
        s.append(f'<path d="M{x1},{cy-h1} L{x2},{cy-h2} L{x2},{cy+h2} L{x1},{cy+h1} Z" '
                 f'fill="{col}" fill-opacity="0.13" stroke="{col}" stroke-width="1.5"/>')
        mx = (x1 + x2) / 2
        s.append(t(mx, 252, big, 30, INK, 500, anchor="middle"))
        s.append(t(mx, 277, small, 17, MUTED, anchor="middle"))
        s.append(t(mx, 700, q, 17, col, 500, anchor="middle"))

    # the two rails the labels hang from
    s.append(line(x0, 292, x0 + 5 * segw, 292, RULE, 1))
    s.append(line(x0, 676, x0 + 5 * segw, 676, RULE, 1))

    xe = x0 + 5 * segw
    s.append(arrow(xe + 8, cy, xe + 46, cy, PINK, 2.5))
    s.append(t(xe + 62, cy + 8, "ranked set", 24, INK, 500))

    s.append(curve(660, 762, 142, 762, 400, 840, ORANGE, 2.5, tip=True))
    s.append(t(680, 769, "measured  ·  kept", 20, ORANGE, 500))

    return "".join(s)


# ==========================================================================

def slide3():
    s = [frame("ROUTES", 3)]

    s.append(cap(L, 300, "MAKE"))
    s.append(cap(700, 300, "TEST"))

    lanes = [(GREEN, "Cell-free", 370), (GREEN, "E. coli", 462), (BLUE, "In-vitro assembly", 554)]
    for col, name, y in lanes:
        s.append(t(L + 20, y - 18, name, 28, INK))
        s.append(bar(L + 20, y, 300, col, 6))
        s.append(curve(L + 324, y + 3, 686, 476, 560, y + 3, RULE, 1.5))

    spine = [(SKY, "Purify"), (ORANGE, "Bind"), (ORANGE, "Confirm"), (ORANGE, "Selectivity")]
    sx, sw_, sg, ry = 700, 182, 24, 472
    for i, (col, name) in enumerate(spine):
        x = sx + i * (sw_ + sg)
        s.append(t(x, ry - 18, name, 30, INK, 500))
        s.append(bar(x, ry, sw_, col))
        if i < 3:
            s.append(arrow(x + sw_ + 4, ry + 4, x + sw_ + sg - 2, ry + 4, RULE, 3))

    s.append(t(L + 20, 668, "Make + bind, one well", 28, MUTED))
    s.append(bar(L + 20, 686, 300, MUTED, 6))
    s.append(t(L + 20, 716, "in build", 17, MUTED))
    s.append(curve(L + 324, 689, 940, 512, 700, 680, MUTED, 1.5, dash="6 6", tip=True))

    return "".join(s)


# ==========================================================================

def slide4():
    s = [frame("LOOP", 4)]

    cx, cy, r = 340, 462, 196
    nodes = [(BLUE, "Design", cx, cy - r), (GREEN, "Make", cx + r, cy),
             (ORANGE, "Measure", cx, cy + r), (PINK, "Learn", cx - r, cy)]
    for col, name, nx, ny in nodes:
        s.append(f'<circle cx="{nx}" cy="{ny}" r="64" fill="none" stroke="{col}" '
                 f'stroke-width="3"/>')
        s.append(t(nx, ny + 8, name, 23, INK, 500, anchor="middle"))

    arcs = [(cx + 50, cy - r + 42, cx + r - 42, cy - 50),
            (cx + r - 42, cy + 50, cx + 50, cy + r - 42),
            (cx - 50, cy + r - 42, cx - r + 42, cy + 50),
            (cx - r + 42, cy - 50, cx - 50, cy - r + 42)]
    for x1, y1, x2, y2 in arcs:
        s.append(f'<path d="M{x1},{y1} A{r},{r} 0 0 1 {x2},{y2}" fill="none" '
                 f'stroke="{RULE}" stroke-width="3" marker-end="url(#tip)"/>')

    s.append(cap(760, 300, "LOOPS"))
    s.append(cap(R, 300, "PERIOD", anchor="end"))

    rows = [(BLUE, "Binder", "a campaign round"),
            (GREEN, "Expression", "a target"),
            (PINK, "Structure", "months")]
    y = 364
    for col, name, period in rows:
        s.append(t(760, y, name, 30, INK, 500))
        s.append(t(R, y, period, 21, col, anchor="end"))
        s.append(bar(760, y + 18, R - 760, col, 6))
        y += 116

    return "".join(s)


# ==========================================================================

def slide5():
    s = [frame("SCALE", 5)]

    s.append(cap(L, 300, "ASKING"))
    s.append(cap(R, 300, "RETURNED", anchor="end"))

    areas = ["Parkinson's", "Avoidome", "Autism genes", "HIV",
             "Neurosurgery", "Hearing institute"]
    y0, step = 356, 54
    s.append(line(L + 6, y0 - 26, L + 6, y0 + 5 * step + 10, RULE, 1.5))
    for i, a in enumerate(areas):
        y = y0 + i * step
        s.append(dot(L + 6, y - 8, 6, MUTED))
        s.append(t(L + 28, y, a, 23, INK))
        s.append(line(410, y - 8, 596, 470, RULE, 1, op=0.8))

    s.append(arrow(596, 470, 634, 470, RULE, 2.5))
    s.append(f'<rect x="640" y="388" width="320" height="164" rx="16" fill="none" '
             f'stroke="{INK}" stroke-width="2.5"/>')
    s.append(t(800, 462, "one deck", 32, INK, 500, anchor="middle"))
    s.append(t(800, 498, "4 labs  →  12", 22, MUTED, anchor="middle"))
    s.append(arrow(966, 470, 1004, 470, RULE, 2.5))

    outs = ["verdict per design", "measured negatives", "affinity",
            "epitope", "quality record"]
    oy0, ostep = 364, 56
    s.append(line(1126, oy0 - 26, 1126, oy0 + 4 * ostep + 10, RULE, 1.5))
    for i, o in enumerate(outs):
        oy = oy0 + i * ostep
        s.append(line(1004, 470, 1126, oy - 8, RULE, 1, op=0.8))
        s.append(dot(1126, oy - 8, 6, MUTED))
        s.append(t(1148, oy, o, 23, INK))

    s.append(line(L, 688, R, 688, RULE, 1))
    s.append(cap(L, 736, "POOLS", GREEN))
    s.append(t(260, 738, "expression  ·  solubility  ·  integrity  ·  specificity", 25, INK))
    s.append(cap(L, 790, "DOES NOT"))
    s.append(t(260, 792, "affinity", 25, MUTED))

    return "".join(s)


# ==========================================================================

CSS = """
:root{
  --bg:#fff; --ink:#1d1d1f; --muted:#86868b; --rule:#d2d2d7; --shadow:rgba(0,0,0,.09);
  --font:"Helvetica Neue",Helvetica,Arial,sans-serif;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme=light]){
  --bg:#141416; --ink:#f2f2f4; --muted:#9a9aa0; --rule:#3a3a3d; --shadow:rgba(0,0,0,.5);
}}
:root[data-theme=dark]{ --bg:#141416; --ink:#f2f2f4; --muted:#9a9aa0; --rule:#3a3a3d;
  --shadow:rgba(0,0,0,.5); }
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);
  -webkit-font-smoothing:antialiased}
.deck{display:flex;flex-direction:column;align-items:center;gap:28px;padding:28px 16px 60px}
.slide{width:100%;max-width:1600px;background:var(--bg);border:1px solid var(--rule);
  border-radius:16px;overflow:hidden;box-shadow:0 1px 3px var(--shadow)}
.slide svg{display:block;width:100%;height:auto;font-family:var(--font)}
.bar{position:sticky;top:0;z-index:5;display:flex;gap:14px;align-items:center;
  justify-content:center;padding:10px;background:var(--bg);border-bottom:1px solid var(--rule);
  font-size:13px;color:var(--muted);flex-wrap:wrap}
.bar a{color:var(--muted);text-decoration:none;padding:3px 9px;border-radius:999px}
.bar a:hover,.bar a:focus-visible{color:var(--ink);background:var(--rule)}
.bar b{font-weight:500;color:var(--ink)}
@media print{
  :root, :root:not([data-theme=light]), :root[data-theme=dark]{
    --bg:#fff; --ink:#1d1d1f; --muted:#86868b; --rule:#d2d2d7;
  }
  @page{size:landscape;margin:0}
  .bar{display:none}
  .deck{gap:0;padding:0}
  .slide{max-width:none;height:100vh;display:grid;place-items:center;
    border:0;border-radius:0;box-shadow:none;break-after:page;page-break-after:always}
  .slide svg{max-height:100vh}
  .slide:last-child{break-after:auto;page-break-after:auto}
}
@media (max-width:700px){ .bar{font-size:12px;gap:8px} .deck{padding:16px 10px 40px;gap:16px} }
"""

DEFS = """<defs>
  <marker id="tip" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5"
          orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker>
</defs>"""

TITLES = ["Campaign", "Funnel", "Routes", "Loop", "Scale"]


def main():
    slides = [slide1(), slide2(), slide3(), slide4(), slide5()]
    nav = "".join(f'<a href="#s{i+1}">{esc(ti)}</a>' for i, ti in enumerate(TITLES))
    body = "".join(
        f'<section class="slide" id="s{i+1}">'
        f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(TITLES[i])}">'
        f'{DEFS}{sv}</svg></section>'
        for i, sv in enumerate(slides))

    out = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           f'<title>Foundry Pipeline Maps</title>\n<style>{CSS}</style>\n</head>\n<body>\n'
           f'<nav class="bar"><b>UCSF Protein Design Foundry</b>{nav}'
           f'<span>press P to print</span></nav>\n'
           f'<div class="deck">{body}</div>\n'
           f'<script>\ndocument.addEventListener("keydown",function(e){{\n'
           f'  if(e.key==="p"||e.key==="P"){{window.print();}}\n'
           f'}});\n</script>\n</body>\n</html>\n')

    p = Path(__file__).with_name("maps.html")
    p.write_text(out, encoding="utf-8")
    print(f"wrote {p}  ({len(out):,} bytes, {len(slides)} slides)")


if __name__ == "__main__":
    main()
