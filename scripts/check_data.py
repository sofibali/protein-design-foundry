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

STATUSES = {"open", "pending", "settled", "dropped"}
PROJECT_STATUSES = {"proposed", "running", "blocked", "complete"}
INSTRUMENT_STATUSES = {"quoted", "phase2", "gap"}


def fail(where, msg):
    PROBLEMS.append(f"{where}: {msg}")


def front_matter(path):
    text = path.read_text()
    if not text.startswith("---"):
        fail(path.name, "no YAML front matter")
        return None, ""
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm), body


def main():
    instruments = yaml.safe_load((ROOT / "_data/instruments.yml").read_text())
    decisions = yaml.safe_load((ROOT / "_data/decisions.yml").read_text())

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

    placed = [i["rac"] for i in instruments["instruments"] if i["status"] == "quoted"]
    for rid in sorted(rac_ids):
        if rid not in placed:
            fail("instruments.yml", f"cart {rid} has no instrument on it")

    seen = set()
    for d in decisions["decisions"]:
        if d["id"] in seen:
            fail("decisions.yml", f"duplicate id {d['id']}")
        seen.add(d["id"])
        if d["status"] not in STATUSES:
            fail(f"decision {d['id']}", f"unknown status {d['status']!r}")
        if d["status"] in {"settled", "dropped"} and not d.get("date"):
            fail(f"decision {d['id']}", f"{d['status']} but no date")
        if not d.get("why") and not d.get("answer"):
            fail(f"decision {d['id']}", "no why and no answer, so the table cell is blank")

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

    print(f"{len(keys)} instruments on {len(rac_ids)} carts, "
          f"{len(decisions['decisions'])} decisions, {len(projects)} projects")
    if PROBLEMS:
        print(f"\n{len(PROBLEMS)} problem(s):")
        for p in PROBLEMS:
            print("  !", p)
        return 1
    print("clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
