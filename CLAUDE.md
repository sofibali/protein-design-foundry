# Working in this repository

Several Claude sessions work here at once, in **one checkout with one git
index**. That is the whole reason this file exists. On 2026-11-23 three
sessions produced sixteen commits in twenty-five minutes and four of them
carried other sessions' work under the wrong message. Nothing was lost, but
the history stopped being able to say who changed what or why.

Two rules carry most of the weight, and both are conventions rather than
anything git enforces: **name the paths you own before you write them**, and
**only the main session talks to Sofia**. The rest of this file is the detail
of those two and the backstops for when someone forgets.

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

## Sessions: one front door

**A side session never asks Sofia anything.** It asks the session that started
it. That session collects the questions from every lane and puts them to her
once, in one place, with the options side by side.

This is the rule that matters most, and it is not about tidiness. On
2026-11-23 the same question — whether the cost model should come off the
public site — reached her from three sessions separately, after she had
already answered it in the main chat. Two of those sessions then spent a turn
each withdrawing it. The cost of a side session asking directly is not one
message; it is her having to hold what she told chat #2 while reading chat #4.

So:

- **A question that only Sofia can answer ends your run.** Send it to the
  session that started you, say what you did and did not finish, and stop. Do
  not idle with a question open, and do not start something else to fill the
  time — that is how a lane drifts into another lane's files.
- **Report back, don't wait to be asked.** When your lane's work is done,
  message the parent with what landed, the commit SHAs, and anything you
  could not verify. That message is the handoff.
- **Reactivation comes from the main session**, by `SendMessage` to your
  session id, with her answer in it. She should never have to open a side
  chat to unblock one.
- **Answer the parent, not the user, even when the question is for the user.**
  If you think the parent has it wrong, say so to the parent. Disagreement
  between sessions is settled between sessions; only the outcome goes to her.

### Opening one

Open a session when the work is a lane of its own — it outlives a turn, it
ends in something of its own, and it will not touch another lane's paths.
Anything smaller stays where it is. A brief must carry, before any work
starts:

1. **The paths it owns**, from the table above. If the work needs a path
   another lane owns, that is not a new session, it is a message to that lane.
2. **What done looks like**, concretely enough that the session knows when to
   report and stop.
3. **The instruction to report to you and not to Sofia.** New sessions do not
   read this file until they are already running in the repository.

Two lanes can run at once. Three is what produced the mess this file exists
to prevent.

### Finishing and archiving

A session that has reported and stopped is finished, and the main session
archives it with `archive_session`. An idle session is not the same thing as
a finished one: idle with an open question means someone is waiting.

Before archiving, check the lane actually landed — the commits are on `main`,
the tree is clean, and `check_data.py` passes. A session's own report is its
account of what it did, not proof that it worked.

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
