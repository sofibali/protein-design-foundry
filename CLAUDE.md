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

Two files have no owner and everyone has a reason to want them.
`scripts/build_pages.py` is shared by region, like `protocols.yml`: the
cart and group validation belongs to the device-set lane, the workflow-steps
validation and `boolkeys()` to the schematics lane. `README.md` is genuinely
co-written. Ask before editing either.

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

**Anyone may run the builder; commit only the generated file whose source you
own.** The build is global but its output is per page, so a run that rewrites
all five files is harmless as long as you commit the one your own source
produced. Do not reach for a rule that says only one session may build: for
the schematics lane the build *is* the validation, because it reads the
FIGURES registry back out of `pages/workflows.html` and fails when a protocol
has no drawing. A one-builder rule would stop that lane committing at all.

**`_data/instruments.yml` is the exception, and has exactly one owner.** It is
generated from `_data/protocols.yml`, which two lanes edit, so it cannot be
separated by path: whoever commits it publishes the other lane's data edits
too. It belongs to whoever owns `racs:`, since that is what drives it.

**`pages/figkit.js` is the shared drawing kit.** All four pages build against
it, so one editor at a time; a change there moves every page's output at once.

If you only need to *test* a build, copy the tree to your scratchpad and run
it there:

```
git archive HEAD | tar -x -C <scratch>/tree && cd <scratch>/tree
```

That answers the question without touching anyone's checkout.

## Before you commit

```
python3 scripts/check_data.py        # data, sheets, and the device set
python3 scripts/build_pages.py       # then commit only your own output
```

A rebuild that produces no diff means the generated files match their
sources. That is the check worth running when the history looks confused.

## What must never reach this repository

It is public. See the confidentiality section of `README.md` for the full
rule, which covers pricing, the decisions register, and names. In short: no
vendor figures ever, including in a commit you later revert, because git
history keeps it; and the pages carry a decision and its date, not the person
who made it.

Check the **repository**, not the built pages. A name in a build script, a
data comment or a protocol file is exactly as public as one in a page, and a
`grep` of `static/pages/` will not see it:

```
git grep -nIE "Sofia|sofia\.bali"
```

What should come back: `lead:` lines in `_projects/`, which are ordinary
authorship credit, and the intake page's mail target. Anything else is a
leak.
