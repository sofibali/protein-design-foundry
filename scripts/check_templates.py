#!/usr/bin/env python3
"""Check the templates, which check_data.py does not look at.

There is no Ruby here, so nothing renders the site locally and a template
fault first appears in the Pages build log or, worse, on the live page. This
catches the three kinds that have actually happened:

  - an unbalanced Liquid block tag
  - an {% include %} whose target does not exist
  - a `'...' | relative_url` link that nothing serves

The third is the one that bites. Jekyll's :name permalink is the SLUG of the
filename, so `steristore_cold.md` is served at /inventory/steristore-cold/,
and two hand-written links to the underscore form were dead on the live site
for a day. A checker that builds its expectations the same wrong way the
code does will confirm the bug instead of finding it, so the slug rule is
applied here deliberately.

    python3 scripts/check_templates.py
"""
import pathlib
import re
import sys

ROOT = (pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1
        else pathlib.Path(__file__).resolve().parent.parent)
PAIRS = {"for": "endfor", "if": "endif", "unless": "endunless",
         "case": "endcase", "capture": "endcapture", "comment": "endcomment",
         "raw": "endraw", "tablerow": "endtablerow"}
problems = []

# _config.yml `exclude:` keeps directories out of the build entirely, so a
# file in one is never rendered and needs no front matter. Without this the
# linter cries wolf over every research note and nobody runs it.
excluded = set()
cfg = ROOT / "_config.yml"
if cfg.exists():
    in_ex = False
    for line in cfg.read_text().splitlines():
        if re.match(r"^exclude:", line):
            in_ex = True
            continue
        if in_ex:
            m = re.match(r"^\s+-\s+([^#]+)", line)
            if m:
                excluded.add(m.group(1).strip().strip("/"))
            elif line.strip() and not line.startswith(" "):
                in_ex = False

files = [p for p in ROOT.rglob("*") if p.suffix in {".html", ".md"}
         and ".git" not in p.parts and "_site" not in p.parts
         and not (set(p.relative_to(ROOT).parts) & excluded)]

# Every URL the site can serve.
served = {"/"}
for p in files:
    rel = p.relative_to(ROOT)
    if rel.parts[0] in {"_layouts", "_includes"}:
        continue
    # Jekyll's :name permalink is the SLUG of the basename, so an underscore
    # in a filename is served as a hyphen. steristore_cold.md is at
    # /inventory/steristore-cold/, and a hand-written link to the underscore
    # form 404s. Slugify here or this linter reproduces the bug it should catch.
    slug = p.stem.replace("_", "-")
    if rel.parts[0] == "_projects":
        served.add(f"/projects/{slug}/")
    elif rel.parts[0] == "_instruments":
        served.add(f"/inventory/{slug}/")
    elif p.name == "index.md":
        served.add("/" + "/".join(rel.parts[:-1]) + ("/" if rel.parts[:-1] else ""))
    else:
        served.add("/" + str(rel.with_suffix("")) + "/")
for p in ROOT.rglob("static/**/*"):
    if p.is_file():
        served.add("/" + str(p.relative_to(ROOT)))

for p in files:
    text = p.read_text()
    name = p.relative_to(ROOT)

    stack = []
    for tag in re.findall(r"\{%-?\s*(\w+)", text):
        if tag in PAIRS:
            stack.append((tag, PAIRS[tag]))
        elif tag.startswith("end"):
            if not stack:
                problems.append(f"{name}: stray {{% {tag} %}}")
            elif stack[-1][1] != tag:
                problems.append(f"{name}: {{% {tag} %}} closes {{% {stack[-1][0]} %}}")
                stack.pop()
            else:
                stack.pop()
    for open_tag, _ in stack:
        problems.append(f"{name}: unclosed {{% {open_tag} %}}")

    for inc in re.findall(r"\{%-?\s*include\s+([\w.\-/]+)", text):
        if not (ROOT / "_includes" / inc).exists():
            problems.append(f"{name}: includes missing {inc}")

    for url in re.findall(r"'([^']+)'\s*\|\s*relative_url", text):
        if url not in served:
            problems.append(f"{name}: links {url}, which nothing serves")

    if p.suffix == ".md" and not text.startswith("---") and name.name != "README.md":
        problems.append(f"{name}: no front matter")

print(f"{len(files)} templates, {len(served)} served URLs")
for q in problems:
    print("  !", q)
print("clean" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
