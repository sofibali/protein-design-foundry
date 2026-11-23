# Working in this repository

Several Claude sessions work here at once, in **one checkout with one git
index**. That is the whole reason this file exists. On 2026-11-23 three
sessions produced sixteen commits in twenty-five minutes and four of them
carried other sessions' work under the wrong message. Nothing was lost, but
the history stopped being able to say who changed what or why.

## Before you start: say what you own

The two boundaries that held that day were the two agreed **in words, before
anyone started typing**. Neither was enforceable by git and both survived.
Everything that went wrong went wrong where no owner had been named.

So: name the paths you are about to write, to whoever else is working, before
you write them. That is the mechanism. Everything below is a backstop for
when someone forgets.

| Lane | Owns |
|---|---|
| Jekyll layer | `_instruments/`, `_layouts/`, `_includes/`, `index.md`, `*/index.md`, `scripts/check_data.py`, `pages/intake.html` |
| Device set | `pages/blueprint.html`, `_data/stages.yml`, and `racs:` + `cart_groups:` in `_data/protocols.yml` |
| Schematics | `pages/workflows.html`, and `workflows:` in `_data/protocols.yml` |

`_data/protocols.yml` is shared **by section, not by path**, so no path rule
can express it. Check the comment above the section before editing it.

Two files have no owner and everyone has a reason to want them:
`scripts/build_pages.py` and `README.md`. Ask before editing either.

## Commit only your own paths

```
git commit -- <paths>
```

Never a bare `git add -A && git commit`. The index is shared, so `-A` stages
whatever anyone else has in flight and your commit carries it out under your
message. This protects other people from you, not you from them, so it only
works if everyone does it.

## Five files are generated. Never hand-edit them

`_data/instruments.yml` and the four pages in `static/pages/`. They are
written by `scripts/build_pages.py` from `_data/protocols.yml` and `pages/`.
`check_data.py` fails the build if `instruments.yml` loses its GENERATED
header.

**One session runs the builder.** It rewrites all five files every time, so
two sessions building at once is the main way one session's output lands in
another's commit. If you need to *test* a build, copy the tree to your
scratchpad and run it there:

```
git archive HEAD | tar -x -C <scratch>/tree && cd <scratch>/tree
```

That answers the question without touching anyone's checkout.

## Before you commit

```
python3 scripts/check_data.py        # data, sheets, and the device set
python3 scripts/build_pages.py       # only if you own the builder
```

A rebuild that produces no diff means the generated files match their
sources. That is the check worth running when the history looks confused.

## What must never reach this repository

It is public. See the confidentiality section of `README.md` for the full
rule, which covers pricing, the decisions register, and names. In short: no
vendor figures ever, including in a commit you later revert, because git
history keeps it; and the pages carry a decision and its date, not the person
who made it.
