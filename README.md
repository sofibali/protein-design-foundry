# Protein Design Foundry

Public-facing documentation for an automated protein design facility at UCSF
Mission Bay. Plain Jekyll on GitHub Pages, matching the stack the lab already
runs for `fraser-lab.github.io`.

## This repository contains no pricing

It is intended to become public. Vendor pricing from the system proposal is
commercially confidential and must never be committed here, **including in a
commit that is later reverted**, because git history keeps it.

Priced line items, quotes and vendor correspondence live in the separate private
repository `protein-design-foundry-internal`. So do the cost model and the
register of open decisions: a public list of what is not yet settled reads as a
list of what the facility cannot do, and the shape of the spend invites the
question the figures are withheld from. Nothing in this repository should
reintroduce either, and `scripts/check_data.py` fails the build if
`_data/decisions.yml` reappears.

Their removal is split across two commits, which `git log` on the deleted
files will not explain on its own. `ef32f41` carries the reasoning and the
rewritten references; the four deletions themselves landed in `d472824`,
whose message is about cart schematics. Three sessions were committing
through one shared git index at the time, and `git add -A` takes whatever is
staged, not only your own work. Use `git commit -- <paths>`.

**Nor does it name anyone.** The four pages in `static/pages/` are mailed and
dropped in Slack, so a source comment, a form field or a bundled data blob
travels with them even when nothing on screen shows it. Who decided a threshold,
and when, belongs in `_data` and in the internal repo; the page carries the
decision, not the decider. Two things this has already cost: the nine gate notes
were shipping inside every page without being rendered, so `build_pages.py` now
strips `note` from the gate data at bundle time, leaving `gates.yml` whole; and
the intake form leaves its contact field empty rather than prefilling it.

## Where everything lives

Two repositories, one job each.

| | |
|---|---|
| **this one** | What the machine does. Public, no pricing, ever. |
| **`protein-design-foundry-internal`** | What was said and what it costs. Meeting record, quotes, vendor questions, floorplans. Private. |

There was a third, `~/foundry`, which started on 15 November as the decision
gates and grew into a second description of the same machine. It was merged in
here on 19 November. **Do not add a git remote to it** — its history contains
vendor pricing.

```
_config.yml        site config, nav, collections
_data/
  protocols.yml    THE SOURCE for the device set: instruments, carts, workflows
  gates.yml        the nine decision gates a run is judged against
  stages.yml       the four loop stages
  future.yml       carts the layout reserves, and capabilities we do not have
  instruments.yml  GENERATED from protocols.yml - do not edit by hand
_projects/         one Markdown file per project: front matter + prose
_instruments/      one spec sheet per instrument, keyed to instruments.yml
_layouts/          default, page, project, instrument
_includes/         the generated tables (Liquid, rendered at build time)
pages/             templates for the four self-contained pages
protocols/         one Markdown file per protocol
reference/         research notes on outside platforms and instruments
static/pages/      the built self-contained pages
scripts/
  build_pages.py   builds static/pages/* and writes _data/instruments.yml
  check_data.py    validates everything, including the device set
```

**`_data/protocols.yml` is the single source for the device set.** The carts on
the blueprint and the rows in the inventory table come from the same file, so
they cannot drift. `_data/instruments.yml` is written by `build_pages.py` and
committed only because GitHub Pages needs it at build time.

```bash
python3 scripts/build_pages.py   # rebuild the pages and the inventory
python3 scripts/check_data.py    # validate; runs the device-set checks too
```

`check_data.py` fails if an instrument is on the capability map and on no cart,
or on two, or if a workflow's cost disagrees with its deck, or if a YAML value
was truncated by an unquoted comma in a flow mapping. It also fails if a
protocol, a cart or a loop step has no drawing, or names one that does not
exist: the figures are drawing code, so they live in the pages and in
`pages/figkit.js`, and the build reads the registries back out of them.

**Every protocol carries its own procedure, as a comparison.** `steps:` under a
workflow in `_data/protocols.yml` is one row per unit operation, each said
twice: `hand:` is what it is at the bench, `deck:` is what it becomes on the
rack. `at:` is the list of machines the row uses and `t:` a timing, only where
the rate model has a real figure. Keep the rows short — they are read side by
side, and the contrast is the content. The build checks that every machine in
the workflow's `deck:` chain is used by some step, and that no step claims a
machine the workflow does not have — so the deck chain, the drawing and the
written method cannot drift apart. `at:` is spelt `at` and not `on` on purpose:
YAML 1.1 reads a bare `on:` key as the boolean `true`, which is the comma
trap's cousin and just as silent. `boolkeys()` in `build_pages.py` now fails
the build on any boolean key, beside the `nulls()` scan for the comma trap.

**Phase 2 is hidden.** `SHOW_PHASE2 = False` in `build_pages.py` keeps the four
reserved crystallography carts, the phase 2 entries in `_data/future.yml` and
the phase 2 programme out of every page and out of the generated inventory.
Nothing is deleted from `_data/`, so the flag reverses it — with one manual
step. The four phase 2 cart drawings were taken out of `pages/blueprint.html`,
because these pages get mailed and hiding has to mean not shipped. Setting the
flag back to `True` fails the build naming exactly those four; they are in
commit `ed3d02f`.

There is no build step for the site's tables. Jekyll reads `_data/` natively and
the includes render them when the site builds.

## Why Jekyll rather than a docs framework

GitHub Pages builds Jekyll natively, as first-party infrastructure, with no CI
workflow and no third-party theme to age out. `jekyll-sitemap` is on the Pages
allowlist. The lab already maintains a Jekyll site, so the idiom is familiar and
anyone here can edit this one.

Keep plugins to the GitHub Pages allowlist or the build will silently drop them.

## Working on it

```bash
bundle install
bundle exec jekyll serve
```

Validate the data files without a Ruby toolchain:

```bash
python3 scripts/check_data.py
```

## Adding a project

Add a Markdown file to `_projects/` with front matter (`title`, `summary`,
`status`, `lead`, optional `scale`, `exercises`, `tests`, `open`) and the prose
below it. It appears on the index automatically.

Write up what did not work. A test project that found a limit has done its job.
