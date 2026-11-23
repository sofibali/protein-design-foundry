#!/usr/bin/env python3
"""Validate the data files and project front matter.

Jekyll renders an empty row for a key that does not resolve, so a typo in
`exercises:` disappears silently. This catches that, plus the handful of other
things that quietly rot in a data-driven site. Runs without a Ruby toolchain.

    python3 scripts/check_data.py
"""
import pathlib
import sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is missing: pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROBLEMS = []
NOTES = []

PROJECT_STATUSES = {"proposed", "running", "blocked", "complete"}
INSTRUMENT_STATUSES = {"quoted", "phase2", "gap"}


def fail(where, msg):
    PROBLEMS.append(f"{where}: {msg}")


def note(where, msg):
    """Worth seeing, but not worth failing a build over."""
    NOTES.append(f"{where}: {msg}")


def front_matter(path):
    text = path.read_text()
    if not text.startswith("---"):
        fail(path.name, "no YAML front matter")
        return None, ""
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm), body


def main():
    instruments = yaml.safe_load((ROOT / "_data/instruments.yml").read_text())

    rac_ids = {r["id"] for r in instruments["racs"]}
    keys = set()

    for i in instruments["instruments"]:
        key = i.get("key")
        if not key:
            fail("instruments.yml", f"entry with no key: {i.get('name')}")
            continue
        if key in keys:
            fail("instruments.yml", f"duplicate key {key!r}")
        keys.add(key)
        if i["status"] not in INSTRUMENT_STATUSES:
            fail(key, f"unknown status {i['status']!r}")
        if i["status"] == "quoted":
            if i.get("rac") not in rac_ids:
                fail(key, f"rac {i.get('rac')!r} is not a defined cart")
            if not i.get("role"):
                fail(key, "quoted instrument with no role")

    # A cart that is installed must carry something. A phase2 cart is a
    # position the layout reserves, so it is allowed to be empty - that is
    # what reserving it means.
    placed = [i["rac"] for i in instruments["instruments"] if i["status"] == "quoted"]
    reserved = {r["id"] for r in instruments["racs"] if r.get("status") == "phase2"}
    for r in instruments["racs"]:
        if r["id"] not in placed and r["id"] not in reserved:
            fail("instruments.yml", f"cart {r['id']} is installed but has no instrument on it")

    # instruments.yml is generated. If someone edits it by hand the next build
    # silently reverts them, so say so rather than let them find out later.
    head = (ROOT / "_data/instruments.yml").read_text(errors="replace")[:200]
    if "GENERATED" not in head:
        fail("instruments.yml", "missing its GENERATED header - it is written by "
                                "scripts/build_pages.py from _data/protocols.yml")

    # The decisions register lives in the internal repo: a public list of what
    # is unsettled reads as a list of what the facility cannot do. Nothing here
    # should reintroduce it.
    if (ROOT / "_data/decisions.yml").exists():
        fail("decisions.yml", "is back in the public repo - it belongs in "
                              "protein-design-foundry-internal")

    projects = sorted((ROOT / "_projects").glob("*.md"))
    if not projects:
        fail("_projects", "no project files")
    for path in projects:
        fm, body = front_matter(path)
        if fm is None:
            continue
        for required in ("title", "summary", "status", "lead"):
            if not fm.get(required):
                fail(path.name, f"missing {required}")
        if fm.get("status") not in PROJECT_STATUSES:
            fail(path.name, f"unknown status {fm.get('status')!r}")
        for k in fm.get("exercises", []):
            if k not in keys:
                fail(path.name, f"exercises {k!r}, which is not an instrument key")
        if len(body.strip()) < 200:
            fail(path.name, "almost no prose; a project page needs to say something")

    sheets = sorted((ROOT / "_instruments").glob("*.md"))
    documented = set()
    for path in sheets:
        fm, body = front_matter(path)
        if fm is None:
            continue
        key = fm.get("key")
        if key not in keys:
            fail(path.name, f"key {key!r}, which is not in instruments.yml")
            continue
        if key in documented:
            fail(path.name, f"second spec sheet for {key!r}")
        documented.add(key)
        if path.stem != key:
            fail(path.name, f"filename does not match key {key!r}, so the URL will not")
        if not fm.get("standfirst"):
            fail(path.name, "no standfirst, so the page opens on a bare heading")
        specs = fm.get("specs") or []
        if len(specs) < 3:
            fail(path.name, "fewer than three specs; this is a specification page")
        for s in specs:
            if not s.get("label") or s.get("value") in (None, ""):
                fail(path.name, f"spec row with an empty side: {s!r}")
            # `{label: Seal stock, value: Roll-fed, so a long run does not need
            # a film change}` is a flow mapping, so YAML reads the clause after
            # the second comma as a THIRD key with a null value and the spec
            # table silently loses it. label and value both survive, which is
            # why the check above waves it through. Any other key is that trap.
            for k, v in s.items():
                if k not in ("label", "value"):
                    fail(path.name, f"spec row has a stray key {k!r} "
                                    f"(value {v!r}) - this is the flow-mapping "
                                    f"comma trap: quote the value")
        if len(body.strip()) < 400:
            fail(path.name, "almost no prose; the table alone is a datasheet, not a page")

    for i in instruments["instruments"]:
        if i["status"] == "quoted" and i["key"] not in documented:
            note(i["key"], "quoted instrument with no spec sheet")

    # the device set, the gates and the workflows, checked against each other
    # by the same code that builds the pages
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import build_pages
        g, st, pr, pg = build_pages.load()
        build_pages.check(g, st, pr, pg)
    except SystemExit:
        fail("build_pages.check", "the device set, gates and workflows disagree - "
                                  "run python3 scripts/build_pages.py for the detail")
    except Exception as exc:                      # a missing file, a YAML error
        fail("build_pages.check", f"could not run: {exc}")

    print(f"{len(keys)} instruments on {len(rac_ids)} carts, "
          f"{len(projects)} projects, {len(sheets)} spec sheets")
    if NOTES:
        print(f"\n{len(NOTES)} note(s):")
        for n in NOTES:
            print("  -", n)
    if PROBLEMS:
        print(f"\n{len(PROBLEMS)} problem(s):")
        for p in PROBLEMS:
            print("  !", p)
        return 1
    print("clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
