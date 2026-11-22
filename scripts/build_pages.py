#!/usr/bin/env python3
"""Build the self-contained pages, and the site data they share.

    python3 scripts/build_pages.py

      static/pages/foundry.html     the loop and the gates
      static/pages/workflows.html   every workflow as a deck sequence
      static/pages/blueprint.html   the RAC system blueprint
      static/pages/intake.html      propose a campaign, with its pipeline
      _data/instruments.yml         GENERATED - do not edit by hand

Reads _data/gates.yml, _data/stages.yml and _data/protocols.yml, checks them
against each other, then inlines the data and every images/* file as a data
URI so each page works on its own: email it, drop it in Slack, open it
offline.

_data/protocols.yml is the single source for the device set. The Jekyll
site's _data/instruments.yml is generated from it here, so the carts on the
blueprint and the carts in the inventory table cannot drift apart.

Pattern borrowed from gcorrey/ginkgo-crystal, with the data generated from
YAML and checked, rather than hand-maintained as JS.
"""
import base64, json, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
OUTDIR = ROOT / "static" / "pages"
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}

STATUSES = ("draft", "planned", "piloted", "validated", "retired")
WF_STATUSES = ("ready", "limited", "build", "offline")
WHERES = ("compute", "rac", "offrac")

# How an instrument is allowed to be claimed by a workflow.
#   deck        it acts on the plate, so it belongs in an ordered deck: chain
#   store       it holds the plate between steps -> holds:
#   consumable  it feeds the deck rather than touching a plate -> holds:
#   virtual     not an instrument; the chain leaves the rack here -> deck:
# Nine of the nineteen devices are storage or logistics. Before this existed,
# the only way to put them on the map was to invent a workflow step for them,
# which would have made the page lie about what the machine does. The rule is
# that every instrument is still claimed by a real workflow - just in the
# field that matches what it actually does.
KINDS = {"deck": "deck", "store": "holds", "consumable": "holds", "virtual": "deck"}
COST_KEYS = ("bravo", "echo", "reader")
RAC_STATUSES = ("installed", "phase2")

# Sofia, 2026-11-20: hide all phase 2 crystallography from the pages. The data
# stays in _data/ and is still checked - phase 2 carts, the phase 2 entries in
# future.yml and the phase 2 programme are simply not bundled into any page.
#
# Putting it back is this line AND four drawings. The CART FIGURES entries
# for imaging, ambient2, handler2 and sealer2 were taken out of
# pages/blueprint.html to satisfy the guard in check(), so setting this True
# on its own fails the build naming all four. Lift them back first:
#     git show ed3d02f:pages/blueprint.html
# README.md, "Phase 2 is hidden", says the same thing at more length.
SHOW_PHASE2 = False


def load():
    data = ROOT / "_data"
    gates = {g["id"]: g for g in yaml.safe_load((data / "gates.yml").read_text())["gates"]}
    stages = yaml.safe_load((data / "stages.yml").read_text())
    protos = yaml.safe_load((data / "protocols.yml").read_text())
    progs = yaml.safe_load((data / "programmes.yml").read_text())
    return gates, stages, protos, progs


def nulls(obj, path=""):
    """Every key in these files whose value parsed as null.

    Always the same bug, and this project has now hit it four times: an
    unquoted comma inside a YAML flow mapping. `{note: a, b}` is not a note
    reading "a, b" — it is {note: "a", "b": None}, so the text ships silently
    truncated at the first comma and the rest becomes a key nobody reads.
    Nothing in these files is legitimately null, so any null is that bug.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            here = f"{path}.{k}" if path else str(k)
            if v is None:
                yield path or "(root)", str(k)
            yield from nulls(v, here)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from nulls(v, f"{path}[{i}]")


def figures(page, marker, keys):
    """What a page can draw, read back out of the page itself.

    The figures are drawing code, so they live in the pages rather than in the
    YAML. This reads a registry between its markers so the build can still
    check that every protocol, and every cart, has one.
    """
    src = (PAGES / page).read_text(encoding="utf-8")
    m = re.search(r"// %s START(.*?)// %s END" % (marker, marker), src, re.S)
    if not m:
        sys.exit(f"pages/{page} has no {marker} block - it has nothing to draw with")
    block = m.group(1)
    # a registry key: quoted, at the top level of its object literal
    ids = set(re.findall(r"^ {0,2}'([^']+)':", block, re.M))
    shapes = {k: len(re.findall(r"^    %s:" % k, block, re.M)) for k in keys}
    return ids, shapes


def check(gates, stages, protos, progs):
    """Fail the build rather than ship pages that disagree with each other."""
    errs = []

    # --- the YAML flow-mapping comma trap, before anything else is checked ---
    for label, blob in (("gates.yml", {"gates": gates}),
                        ("data/stages.yml", stages),
                        ("data/protocols.yml", protos),
                        ("data/programmes.yml", progs)):
        for where, key in nulls(blob):
            errs.append(f"{label}: {where} has a null-valued key — quote the value. "
                        f"An unquoted comma in a flow mapping split it, and the text "
                        f"after the comma became this key: {key[:70]!r}")

    # --- stages against gates ---
    used = set()
    staged = set()
    for st in stages["stages"]:
        for gid in st["gates"]:
            used.add(gid)
            if gid not in gates:
                errs.append(f"stage {st['id']!r} references unknown gate {gid!r}")
        if st["where"] not in WHERES:
            errs.append(f"stage {st['id']!r} has unknown where {st['where']!r}")
        for p in st["protocols"]:
            staged.add(p["id"])
            if p["status"] not in STATUSES:
                errs.append(f"{p['id']}: bad status {p['status']!r}")
    for gid in gates:
        if gid not in used:
            errs.append(f"gate {gid!r} belongs to no stage")
    for gid, g in gates.items():
        for k in ("name", "pass", "fail", "ambiguous", "by"):
            if not g.get(k):
                errs.append(f"gate {gid!r} is missing {k!r}")

    # --- workflows against instruments, phases, gates and the protocol files ---
    insts = {i["id"] for i in protos["instruments"]}
    kind = {}
    for i in protos["instruments"]:
        k = i.get("kind")
        if k not in KINDS:
            errs.append(f"instrument {i['id']!r}: kind must be one of {', '.join(KINDS)}, not {k!r}")
        if not i.get("role"):
            errs.append(f"instrument {i['id']!r} is missing a role")
        # every device carries its own numbers. A device nobody can size is a
        # device nobody can plan against, so a thin entry fails the build.
        if k != "virtual" and len((i.get("spec") or "").split()) < 25:
            errs.append(f"instrument {i['id']!r}: spec must carry the device's actual "
                        f"figures — formats, capacity, range, throughput — not a phrase")
        kind[i["id"]] = k

    rates = protos.get("rates") or {}
    for k in ("day_min", "bravo_96", "bravo_384", "echo_pl", "read_trf", "read_lum"):
        if not rates.get(k):
            errs.append(f"rates is missing {k!r} — every cost: below is quoted against it")
    if not rates.get("ceilings"):
        errs.append("rates lists no ceilings — the throughput ceiling has to be on the page")

    phases = {p["id"] for p in protos["phases"]}
    touched = set()
    held = set()
    seen = set()
    for w in protos["workflows"]:
        wid = w["id"]
        if wid in seen:
            errs.append(f"workflow {wid!r} is defined twice")
        seen.add(wid)
        if w["status"] not in WF_STATUSES:
            errs.append(f"workflow {wid!r}: bad status {w['status']!r}")
        if w["phase"] not in phases:
            errs.append(f"workflow {wid!r}: unknown phase {w['phase']!r}")
        if not w["deck"]:
            errs.append(f"workflow {wid!r}: empty deck sequence")
        for d in w["deck"]:
            touched.add(d)
            if d not in insts:
                errs.append(f"workflow {wid!r}: unknown instrument {d!r}")
            elif KINDS.get(kind[d]) != "deck":
                errs.append(f"workflow {wid!r}: {d!r} is a {kind[d]}, so it belongs in holds:, "
                            f"not in the deck chain — it does not act on the plate")
        for h in w.get("holds", []):
            held.add(h)
            if h not in insts:
                errs.append(f"workflow {wid!r}: unknown instrument {h!r} in holds")
            elif KINDS.get(kind[h]) != "holds":
                errs.append(f"workflow {wid!r}: {h!r} acts on the plate, so it belongs in the "
                            f"deck chain, not in holds:")
            elif h in w["deck"]:
                errs.append(f"workflow {wid!r}: {h!r} is in both deck and holds")

        # what this workflow costs the day, and does the cost match the deck
        c = w.get("cost") or {}
        for k in COST_KEYS:
            if k not in c or not isinstance(c[k], int) or c[k] < 0:
                errs.append(f"workflow {wid!r}: cost.{k} must be whole minutes, 0 or more")
        if not c.get("binds"):
            errs.append(f"workflow {wid!r}: cost.binds must name what actually limits this workflow")
        uses_bravo = bool({"bravo", "bioshake"} & set(w["deck"]))
        for k, on_deck in (("bravo", uses_bravo),
                           ("echo", "echo" in w["deck"]),
                           ("reader", "pherastar" in w["deck"])):
            if on_deck and not c.get(k):
                errs.append(f"workflow {wid!r}: its deck uses the {k}, so cost.{k} cannot be 0")
            if not on_deck and c.get(k):
                errs.append(f"workflow {wid!r}: cost.{k} is {c[k]} but the {k} is not in its deck")
        for gid in w.get("gates", []):
            if gid not in gates:
                errs.append(f"workflow {wid!r}: unknown gate {gid!r}")
        for k in ("name", "sub", "gives", "scale", "time"):
            if not w.get(k):
                errs.append(f"workflow {wid!r} is missing {k!r}")
        # every workflow states, in one plain line each, what it takes and
        # what it hands back. These are the headers on the card: Input and
        # Output, not "what goes in" and "what comes back".
        for k in ("input", "output"):
            v = w.get(k)
            if not v or not isinstance(v, str) or len(v.split()) < 4:
                errs.append(f"workflow {wid!r}: {k}: must name in plain words what the "
                            f"protocol takes or hands back")
        # every workflow states what goes into it
        if not w.get("inputs"):
            errs.append(f"workflow {wid!r} lists no inputs")
        for x in w.get("inputs", []):
            if not x.get("item") or not x.get("spec"):
                errs.append(f"workflow {wid!r}: an input is missing item or spec")
        # a named protocol has to be a real file AND be on a stage
        pid = w.get("protocol")
        if pid:
            if not (ROOT / "protocols" / f"{pid}.md").exists():
                errs.append(f"workflow {wid!r}: no protocols/{pid}.md")
            if pid not in staged:
                errs.append(f"workflow {wid!r}: protocol {pid!r} is on no stage")
    for i in sorted(insts - touched - held):
        where = "deck chain" if KINDS.get(kind.get(i)) == "deck" else "workflow's holds: list"
        errs.append(f"instrument {i!r} appears in no {where} — it would render as a dead chip")

    # --- every protocol is drawn ---
    # The planner page carries two panels per protocol: a schematic of what
    # physically happens, and a sketch of the readout. They live in the page
    # because they are drawing code, but a protocol added to the YAML with no
    # figure would render as a card with a hole in it, so the build checks the
    # registry here rather than letting the page fall back silently.
    drawn, shapes = figures("workflows.html", "FIGURES", ("s", "o", "oc"))
    for wid in sorted({w["id"] for w in protos["workflows"]} - drawn):
        errs.append(f"workflow {wid!r} has no figure - add a '{wid}' entry to the FIGURES "
                    f"block in pages/workflows.html, with s:, o: and oc:")
    for wid in sorted(drawn - {w["id"] for w in protos["workflows"]}):
        errs.append(f"pages/workflows.html draws a figure for {wid!r}, which is not a workflow")
    for key, n in sorted(shapes.items()):
        if n != len(drawn):
            errs.append(f"the FIGURES block has {len(drawn)} protocols but {n} {key!r} keys - "
                        f"every protocol needs a schematic (s:), a sample output (o:) and "
                        f"its caption (oc:)")

    # Every cart is drawn too, on the blueprint: what the unit operation does
    # to a plate, as against the elevation, which is how the cart is built.
    cdrawn, cshapes = figures("blueprint.html", "CART FIGURES", ("s",))
    cart_ids = {r["id"] for r in protos.get("racs", [])}
    shown = {r["id"] for r in protos.get("racs", [])
             if SHOW_PHASE2 or r["status"] == "installed"}
    for rid in sorted(shown - cdrawn):
        errs.append(f"cart {rid!r} has no figure - add a '{rid}' entry to the CART FIGURES "
                    f"block in pages/blueprint.html")
    for rid in sorted(cdrawn - cart_ids):
        errs.append(f"pages/blueprint.html draws a figure for {rid!r}, which is not a cart")
    if cshapes["s"] != len(cdrawn):
        errs.append(f"the CART FIGURES block has {len(cdrawn)} carts but "
                    f"{cshapes['s']} s: keys")
    if not SHOW_PHASE2 and (cdrawn - shown):
        errs.append(f"pages/blueprint.html still draws {sorted(cdrawn - shown)}, which "
                    f"phase 2 hiding takes off the page - drop the figure or set SHOW_PHASE2")

    # --- the carts, against the instruments ---
    # The capability map and the floor plan have to describe the same machine.
    # Every real instrument sits on exactly one cart; a device that is on one
    # and not the other is precisely how the device set drifted before.
    on_cart, seen_rac = {}, set()
    for r in protos.get("racs", []):
        rid = r["id"]
        if rid in seen_rac:
            errs.append(f"cart {rid!r} is defined twice")
        seen_rac.add(rid)
        if r["status"] not in RAC_STATUSES:
            errs.append(f"cart {rid!r}: bad status {r['status']!r}")
        for k in ("unitop", "note", "n"):
            if not r.get(k):
                errs.append(f"cart {rid!r} is missing {k!r}")
        for i in r["instruments"]:
            if i not in insts:
                errs.append(f"cart {rid!r}: unknown instrument {i!r}")
            elif kind.get(i) == "virtual":
                errs.append(f"cart {rid!r}: {i!r} is virtual — it is not on the floor")
            elif i in on_cart:
                errs.append(f"instrument {i!r} is on two carts: {on_cart[i]!r} and {rid!r}")
            else:
                on_cart[i] = rid
        if r["status"] == "installed" and not r["instruments"]:
            errs.append(f"cart {rid!r} is installed but holds no instrument")
        if r["status"] == "phase2" and r["instruments"]:
            errs.append(f"cart {rid!r} is phase 2, so its instruments are not quoted yet")
    for i in sorted(insts):
        if kind.get(i) != "virtual" and i not in on_cart:
            errs.append(f"instrument {i!r} is on the capability map but on no cart — "
                        f"add it to racs: in data/protocols.yml")

    # --- routes: a day is a chain, and each link has to exist ---
    for r in protos.get("routes", []):
        for k in ("id", "name", "sub"):
            if not r.get(k):
                errs.append(f"route {r.get('id', '?')!r} is missing {k!r}")
        if len(r.get("steps", [])) < 2:
            errs.append(f"route {r.get('id', '?')!r}: a route needs at least two steps")
        for s in r.get("steps", []):
            if s not in seen:
                errs.append(f"route {r['id']!r}: unknown workflow {s!r}")

    # --- every loop step and every protocol is drawn, and says which drawing ---
    glyphs, _ = figures("figkit.js", "STEP GLYPHS", ())
    for w in protos["workflows"]:
        d = w.get("draw")
        if not d:
            errs.append(f"workflow {w['id']!r} has no draw: - the proposal page draws the "
                        f"pipeline it puts this protocol in")
        elif d not in glyphs:
            errs.append(f"workflow {w['id']!r} draws {d!r}, which is not in the STEP GLYPHS "
                        f"block in pages/figkit.js ({', '.join(sorted(glyphs))})")
    for lp in protos["loops"]:
        for st in lp.get("steps", []):
            d = st.get("draw")
            if not d:
                errs.append(f"loop {lp['id']!r}: step {st.get('label')!r} has no draw: - "
                            f"every step on the loop is drawn, so it has to name its glyph")
            elif d not in glyphs:
                errs.append(f"loop {lp['id']!r}: step {st.get('label')!r} draws {d!r}, which is "
                            f"not in the LOOP GLYPHS block in pages/workflows.html "
                            f"({', '.join(sorted(glyphs))})")
    # NOT `used`: that name already holds the gates the stages reference, and
    # check() returns its length as the gate count.
    drawn_with = {st.get("draw") for lp in protos["loops"] for st in lp.get("steps", [])}
    drawn_with |= {w.get("draw") for w in protos["workflows"]}
    for g in sorted(glyphs - drawn_with):
        errs.append(f"pages/figkit.js draws a step glyph {g!r} that nothing uses")

    # --- loops ---
    seen = set()
    for lp in protos["loops"]:
        lid = lp["id"]
        if lid in seen:
            errs.append(f"loop {lid!r} is defined twice")
        seen.add(lid)
        for k in ("name", "closes", "returns"):
            if not lp.get(k):
                errs.append(f"loop {lid!r} is missing {k!r}")
        if len(lp.get("steps", [])) < 3:
            errs.append(f"loop {lid!r}: a loop needs at least three steps")
        for st in lp.get("steps", []):
            if st["where"] not in WHERES:
                errs.append(f"loop {lid!r}: step {st['label']!r} has unknown where {st['where']!r}")
        # a loop that never touches the rack does not belong on this page
        if not any(st["where"] == "rac" for st in lp.get("steps", [])):
            errs.append(f"loop {lid!r}: no step runs on the rack")

    # --- the intake blueprint needs a short name per workflow ---
    for w in protos["workflows"]:
        sh = w.get("short")
        if not sh:
            errs.append(f"workflow {w['id']!r}: no short: - the intake blueprint "
                        f"has nothing to label the step with")
        elif len(sh) > 28:
            errs.append(f"workflow {w['id']!r}: short: is {len(sh)} chars, max 28 "
                        f"- it has to fit the blueprint column: {sh!r}")
    for r in protos.get("routes", []):
        for sid in r["steps"]:
            if sid not in {w["id"] for w in protos["workflows"]}:
                errs.append(f"route {r['id']!r}: step {sid!r} is not a workflow")

    # --- the user-facing blocks ---
    fit = stages.get("fit")
    if not fit:
        errs.append("stages.yml has no fit block - the landing page cannot ask "
                    "what the project is")
    else:
        if len(fit.get("asks", [])) < 2:
            errs.append("fit needs at least two questions")
        for c in fit.get("asks", []):
            for k in ("id", "q", "sub", "why"):
                if not c.get(k):
                    errs.append(f"fit question {c.get('id', '?')!r} is missing {k!r}")
        lv = (fit.get("scale") or {}).get("levels") or []
        if not lv:
            errs.append("fit states no risk levels, so the ratings on the "
                        "programmes mean nothing to a reader")
        for l in lv:
            for k in ("id", "name", "say"):
                if not l.get(k):
                    errs.append(f"risk level {l.get('id', '?')!r} is missing {k!r}")
            # A level with no worked example is an adjective. The examples are
            # what let a reader place their own target on the scale.
            if len(l.get("eg", [])) < 2:
                errs.append(f"risk level {l.get('id', '?')!r} gives fewer than "
                            f"two example targets, so a reader cannot place theirs")

    gd = stages.get("guidance")
    if not gd:
        errs.append("stages.yml has no guidance block - the proposal page has "
                    "nothing to say about shaping a binder question")
    else:
        for c in gd.get("items", []):
            for k in ("id", "t", "v", "do"):
                if not c.get(k):
                    errs.append(f"guidance item {c.get('id', '?')!r} is missing {k!r}")
        if not gd.get("scope"):
            errs.append("guidance has no scope - it reads as applying to every "
                        "loop when it is about binder campaigns")
    for key in ("provide", "returns", "limits"):
        blk = stages.get(key)
        if not blk or not blk.get("items"):
            errs.append(f"stages.yml {key!r} block is missing or empty")
            continue
        for it in blk["items"]:
            # A YAML flow mapping splits on an unquoted comma, so
            # {k: a, v: b, c} silently parses 'c' as a key and drops the rest.
            # Truncated copy shipped that way once already. Catch it here.
            if key == "limits":
                if not isinstance(it, str):
                    errs.append(f"{key}: item should be a plain string, got {it!r}")
            elif set(it) != {"k", "v"}:
                errs.append(f"{key}: item has keys {sorted(it)}, expected k and v only "
                            f"- an unquoted comma in a flow mapping? {it!r}")
            elif not str(it["v"]).rstrip().endswith((".", "?", "!")):
                errs.append(f"{key}: value looks truncated (no end punctuation): {it['v']!r}")

    # --- the programmes on the landing page ---
    # Each one claims a loop and sometimes a route. A programme pointing at a
    # loop that does not exist is a landing page promising work the machine
    # has no shape for, which is the one thing this page must not do.
    loop_ids = {lp["id"] for lp in protos["loops"]}
    route_ids = {r["id"] for r in protos.get("routes", [])}
    wf_ids = {w["id"] for w in protos["workflows"]}
    if not progs.get("lede"):
        errs.append("programmes.yml has no lede")
    seen_pr = set()
    for p in progs.get("programmes", []):
        pid = p.get("id", "?")
        if pid in seen_pr:
            errs.append(f"programme {pid!r} is defined twice")
        seen_pr.add(pid)
        for k in ("id", "name", "sub", "status", "problem", "strategy", "bring", "back"):
            if not p.get(k):
                errs.append(f"programme {pid!r} is missing {k!r}")
        if not p.get("areas"):
            errs.append(f"programme {pid!r} names no areas")
        if p.get("loop") not in loop_ids:
            errs.append(f"programme {pid!r}: unknown loop {p.get('loop')!r}")
        if p.get("route") and p["route"] not in route_ids:
            errs.append(f"programme {pid!r}: unknown route {p['route']!r}")
        for gid in p.get("gates", []):
            if gid not in gates:
                errs.append(f"programme {pid!r}: unknown gate {gid!r}")
        # Deliberately no risk level here. A tier rates a TARGET - how well
        # characterised it is, how large, how ordered - and a project style
        # holds targets of every difficulty, so a single level against a
        # whole style would be rating the method instead, which is a
        # different thing and not what the 19 November session asked for.
        if p.get("risk"):
            errs.append(f"programme {pid!r} carries a risk level. Risk is a "
                        f"property of a target, not of a style of work: the "
                        f"same binder campaign is low risk against a "
                        f"well-characterised domain and high against a "
                        f"disordered assembly. The scale is in stages.yml.")
    if len(seen_pr) < 2:
        errs.append("programmes.yml lists fewer than two programmes")

    if errs:
        print("Build failed:", file=sys.stderr)
        for e in errs:
            print("  -", e, file=sys.stderr)
        sys.exit(1)
    return len(used)


def pipeline(protos):
    """The slice of the deck the intake blueprint assembles a route from.

    intake.html used to carry a hand-copied table of ids, gates and minutes.
    It matched, but only because it was checked by hand; nothing stopped a
    cost edit here from leaving the proposal page quoting last month's day.
    This is that table, derived, so the two cannot disagree.
    """
    ph = {p["id"]: p["c"] for p in protos["phases"]}
    return {
        "day": protos["rates"]["day_min"],
        "workflows": {w["id"]: {"n": w["short"],
                                "g": w.get("gates", []),
                                "c": sum(w["cost"][k] for k in COST_KEYS),
                                "d": w["draw"],
                                "p": ph[w["phase"]]}
                      for w in protos["workflows"]},
        "routes": {r["id"]: r["steps"] for r in protos["routes"]},
    }


def hide_phase2(protos, progs):
    """The pages' view of the data, with everything phase 2 left out.

    These pages are mailed and dropped in Slack, so hiding has to mean not
    shipped rather than not displayed: a reader who opens the source should
    not find the reserved carts in it either.
    """
    protos = dict(protos)
    protos["racs"] = [r for r in protos["racs"] if r["status"] == "installed"]
    progs = dict(progs)
    progs["programmes"] = [p for p in progs["programmes"]
                           if str(p.get("status", "")).replace(" ", "") != "phase2"]
    return protos, progs


def derive(protos):
    """Turn each workflow's machine-time cost into a share of the day.

    Computed here rather than written into the YAML so the two can never
    drift: edit a cost and the page's day-share follows on the next build.
    """
    # what runs through each cart - the thing a static blueprint image cannot do
    for r in protos.get("racs", []):
        mine = set(r["instruments"])
        r["runs"] = [w["id"] for w in protos["workflows"]
                     if mine & (set(w["deck"]) | set(w.get("holds", [])))]

    day = protos["rates"]["day_min"]
    for w in protos["workflows"]:
        c = w["cost"]
        worst = max(c[k] for k in COST_KEYS)
        c["worst"] = worst
        c["runs"] = (day // worst) if worst else None
        c["share"] = round(100 * worst / day, 1) if worst else 0.0
    return protos


def embed_images(text):
    used = []

    def repl(m):
        rel = m.group(1)
        path = ROOT / rel
        if not path.exists():
            sys.exit(f"Missing image referenced in a page: {rel}")
        used.append(rel)
        return f"data:{MIME[path.suffix.lower()]};base64," + \
            base64.b64encode(path.read_bytes()).decode("ascii")

    return re.sub(r"(images/[\w.\-]+\.(?:png|jpe?g|svg))", repl, text), used


def site_url():
    """The site's own address, from _config.yml.

    These pages are built to be self-contained - opened from the file system,
    mailed, dropped in Slack - so a root-relative "/inventory/echo/" would
    resolve against whatever host the file is sitting on, and on the site
    itself would miss the project baseurl entirely. Anything pointing back at
    the site has to be absolute, and this is where that address comes from.
    """
    cfg = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8"))
    return (cfg.get("url", "") + cfg.get("baseurl", "")).rstrip("/")


def sheet_specs():
    """The structured spec rows from _instruments/*.md, keyed by instrument id.

    Each sheet already carries a `specs:` list of {label, value} - that is what
    the inventory pages render as a table, and it is the same fact in a shape a
    table can use. The blueprint's own `spec:` string stays as the one-paragraph
    summary; these rows are what the cart detail opens into, so the reader gets
    a table instead of a wall of prose.

    A sheet is optional. An instrument with none keeps its paragraph and shows
    no table, which is what `offline` does.
    """
    site = site_url()
    out = {}
    for path in sorted((ROOT / "_instruments").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        _, fm, _ = text.split("---", 2)
        front = yaml.safe_load(fm) or {}
        key, rows = front.get("key"), front.get("specs") or []
        if not key:
            continue
        clean = []
        for row in rows:
            # The flow-mapping comma trap puts a third, null-valued key on the
            # row and drops the text after the comma. check_data.py fails the
            # build on it; refuse to render one here too rather than publish a
            # half sentence.
            stray = [k for k in row if k not in ("label", "value")]
            if stray:
                sys.exit(f"{path.name}: spec row {row!r} has stray key(s) "
                         f"{stray} - quote the value")
            clean.append({"label": str(row["label"]), "value": str(row["value"])})
        out[key] = {"rows": clean, "url": site + "/inventory/%s/" % key}
    return out


# The four pages are a path, not a ring. Every page used to link to every
# other one, which gives a reader twelve edges, no sense of where they are and
# no way to tell they have seen everything - the endless loop. This is the
# order instead: what the place does, what it runs, what it runs on, how to
# ask for it. Each page says where it sits, and offers exactly one next step.
PATH = [
    ("foundry.html",   "What happens here", "what the foundry is for"),
    ("workflows.html", "Sample protocols",  "what it runs, and what each step decides"),
    ("blueprint.html", "System blueprint",  "the machine the protocols run on"),
    ("intake.html",    "Propose a campaign", "send us a target"),
]
PATHCSS = """<style>
  .path{display:flex;flex-wrap:wrap;gap:2px;margin:0 0 20px;padding:0;list-style:none;
        border:1px solid var(--rule);border-radius:9px;overflow:hidden}
  .path li{flex:1 1 150px;min-width:0}
  .path a,.path span{display:block;padding:9px 12px;font-size:12.5px;text-decoration:none;
        color:var(--muted);background:transparent;border-left:1px solid var(--rule);
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .path li:first-child a,.path li:first-child span{border-left:0}
  .path a:hover{color:var(--ink);background:var(--tab-bg)}
  .path a:focus-visible,.path span:focus-visible{outline:2px solid var(--ink);outline-offset:-2px}
  .path .n{font-variant-numeric:tabular-nums;margin-right:7px;opacity:.65}
  .path [aria-current=step]{color:var(--ink);font-weight:500;background:var(--tab-bg)}
  .next{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin:34px 0 0;
        padding:15px 17px;border:1px solid var(--rule);border-radius:10px}
  .next .k{font-size:10.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
  .next a{font-size:15px;color:var(--ink);text-decoration:none;font-weight:500;
        border-bottom:1px solid var(--rule)}
  .next a:hover{border-bottom-color:var(--ink)}
  .next .w{flex:1 1 100%;font-size:12.5px;color:var(--muted);margin-top:1px}
  .skip{position:absolute;left:-9999px}
  .skip:focus{left:8px;top:8px;z-index:50;position:fixed;background:var(--bg);color:var(--ink);
        border:1px solid var(--ink);border-radius:7px;padding:9px 13px;font-size:13px}
</style>"""


def pathbar(page):
    """Where this page sits in the path, as an ordered list."""
    out = [PATHCSS, '<nav aria-label="Where you are"><ol class="path">']
    for n, (href, label, _) in enumerate(PATH, 1):
        num = f'<span class="n">{n}</span>'
        if href == page:
            out.append(f'<li><span aria-current="step">{num}{label}</span></li>')
        else:
            out.append(f'<li><a href="{href}">{num}{label}</a></li>')
    out.append('</ol></nav>')
    return "\n".join(out)


def nextstep(page):
    """Exactly one way onward, so the path has a direction and an end."""
    ids = [h for h, _, _ in PATH]
    i = ids.index(page)
    if i + 1 < len(PATH):
        href, label, why = PATH[i + 1]
        return (f'<div class="next"><span class="k">Next</span>'
                f'<a href="{href}">{label} &rarr;</a>'
                f'<span class="w">{why.capitalize()}.</span></div>')
    return ('<div class="next"><span class="k">That is the path</span>'
            '<a href="{{SITE}}/">Back to the foundry site &rarr;</a>'
            '<span class="w">Capabilities, projects, decisions and the cost model '
            'are on the main site.</span></div>')


def bundle(page, src_tag, var, payload):
    """Inline one data blob into one page and write it to dist/."""
    blob = json.dumps(payload, indent=1, sort_keys=False)
    (PAGES / src_tag).write_text(f"window.{var} = {blob};\n", encoding="utf-8")

    html = (PAGES / page).read_text(encoding="utf-8")

    # {{PATH}} and {{NEXT}} put the same four-step path on every page, so a
    # reader always knows where they are and has one way onward. {{SITE}} is
    # how a built page points back at the Jekyll site it belongs to. All three
    # are defined once, here.
    html = html.replace("{{PATH}}", pathbar(page))
    html = html.replace("{{NEXT}}", nextstep(page))
    html = html.replace("{{SITE}}", site_url())
    for ph in ("{{PATH}}", "{{NEXT}}"):
        if ph in html:
            sys.exit(f"{page}: {ph} survived substitution")

    tag = f'<script src="{src_tag}"></script>'
    if tag not in html:
        sys.exit(f"Expected {tag} in {page}")
    html = html.replace(tag, f"<script>\nwindow.{var} = {blob};\n</script>")

    # the shared drawing kit, inlined wherever a page asks for it. It is one
    # file so the protocol panels and the cart panels cannot drift into two
    # different hands.
    kit_tag = '<script src="figkit.js"></script>'
    if kit_tag in html:
        html = html.replace(kit_tag, "<script>\n%s</script>"
                            % (PAGES / "figkit.js").read_text(encoding="utf-8"))

    leftover = re.findall(r'<script src="([^"]+)"', html)
    if leftover:
        sys.exit(f"{page}: unbundled external scripts remain: {leftover}")

    html, images = embed_images(html)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = OUTDIR / page
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} ({out.stat().st_size/1e3:.0f} KB)")
    return images


# Jekyll reads _data/instruments.yml natively and the site's includes and
# layouts query it by key. Rather than maintain a second device list, write it
# from protocols.yml on every build. The shape below is the one the templates
# already expect: racs [{id, name}] and instruments [{key, name, vendor, rac,
# status, role, note}].
def write_inventory(protos):
    racs, insts, on_cart = [], [], {}
    for r in protos["racs"]:
        racs.append({"id": r["n"], "name": r["unitop"], "classes": list(r["class"]),
                     "status": r["status"], "io": bool(r["io"])})
        for i in r["instruments"]:
            on_cart[i] = r
    for i in protos["instruments"]:
        if i["kind"] == "virtual":
            continue
        cart = on_cart.get(i["id"])
        insts.append({"key": i["id"], "name": i["label"], "vendor": i.get("vendor", ""),
                      "rac": cart["n"] if cart else None,
                      "status": "quoted" if cart and cart["status"] == "installed" else "phase2",
                      "role": i["role"], "note": " ".join(i["spec"].split())})
    # carts the layout reserves, and capabilities the system does not have.
    # Hand-maintained in _data/future.yml because protocols.yml describes the
    # machine as quoted and should not have to carry an absence.
    fut = ROOT / "_data" / "future.yml"
    if fut.exists():
        later = (yaml.safe_load(fut.read_text()) or {}).get("future", [])
        if not SHOW_PHASE2:
            later = [i for i in later if i.get("status") != "phase2"]
        insts += later

    racs.sort(key=lambda r: r["id"])
    insts.sort(key=lambda i: (i["rac"] or 99, i["key"]))
    (ROOT / "_data" / "instruments.yml").write_text(
        "# GENERATED by scripts/build_pages.py from _data/protocols.yml.\n"
        "# Do not edit by hand - edit protocols.yml and re-run the script.\n"
        "# protocols.yml is the single source for the device set; this file\n"
        "# exists because Jekyll reads _data/ natively and the site's includes\n"
        "# and layouts query instruments by key.\n\n"
        + yaml.safe_dump({"racs": racs, "instruments": insts},
                         sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8")
    return len(racs), len(insts)


def main():
    gates, stages, protos, progs = load()
    n = check(gates, stages, protos, progs)
    protos = derive(protos)
    if not SHOW_PHASE2:
        protos, progs = hide_phase2(protos, progs)

    # The landing page answers "can the foundry take my project". It needs the
    # programmes, the loops each one runs, and the gates those loops decide at
    # — but not the limits block, which moved to the capability page where a
    # reader is already looking at what the deck does.
    loop = dict(stages)
    loop.pop("limits", None)
    # The binder guidance belongs on the proposal page, next to the form it is
    # advice for. It left the landing page on 2026-11-20 because four
    # preconditions under "can the foundry take your project" read as entry
    # requirements, which is the opposite of what they are.
    loop.pop("guidance", None)
    loop["gates"] = gates
    loop["programmes"] = progs
    loop["loops"] = protos["loops"]
    loop["routes"] = protos.get("routes", [])
    loop["wf"] = {w["id"]: {"name": w["name"], "short": w["short"],
                            "phase": w["phase"], "gates": w.get("gates", [])}
                  for w in protos["workflows"]}
    loop["phases"] = protos["phases"]
    imgs = bundle("foundry.html", "data.js", "FOUNDRY", loop)

    # The campaign planner needs each gate's three outcomes, because what a
    # campaign is, is the chain those outcomes pick out.
    wfdata = dict(protos)
    wfdata["gates"] = gates
    wfdata["limits"] = stages["limits"]
    imgs += bundle("workflows.html", "protocols.js", "PROTOCOLS", wfdata)
    sheets = sheet_specs()
    imgs += bundle("blueprint.html", "blueprint.js", "BLUEPRINT", {
        "title": "UCSF Protein Design Foundry",
        "subtitle": "RAC system blueprint",
        "racs": protos["racs"],
        "instruments": [dict(i, **sheets.get(i["id"], {}))
                        for i in protos["instruments"]],
        "workflows": [{"id": w["id"], "name": w["name"], "phase": w["phase"]}
                      for w in protos["workflows"]],
        "phases": protos["phases"],
    })

    pipe = pipeline(protos)
    pipe["guidance"] = stages["guidance"]
    imgs += bundle("intake.html", "pipeline.js", "PIPE", pipe)

    nr, ni = write_inventory(protos)
    print(f"Wrote _data/instruments.yml ({nr} carts, {ni} instruments)")

    print(f"  {len(stages['stages'])} stages, {n} gates, "
          f"{sum(len(s['protocols']) for s in stages['stages'])} protocols")
    print(f"  {len(protos.get('routes', []))} costed routes")
    rs = protos["racs"]
    print(f"  {len(rs)} carts on the pages" if SHOW_PHASE2 else
          f"  {len(rs)} carts on the pages, phase 2 hidden")
    print(f"  {len(protos['workflows'])} workflows across "
          f"{len(protos['instruments'])} instruments, {len(protos['loops'])} loops, "
          f"{sum(len(w['inputs']) for w in protos['workflows'])} inputs")
    worst = max(protos["workflows"], key=lambda w: w["cost"]["worst"])
    print(f"  most expensive workflow: {worst['id']} at {worst['cost']['worst']} min "
          f"({worst['cost']['share']}% of a 20 h day)")
    if imgs:
        print(f"  embedded {len(set(imgs))} images")


if __name__ == "__main__":
    main()
