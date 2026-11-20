# Protein Design Foundry

Public-facing documentation for an automated protein design facility at UCSF
Mission Bay. Plain Jekyll on GitHub Pages, matching the stack the lab already
runs for `fraser-lab.github.io`.

## This repository contains no pricing

It is intended to become public. Vendor pricing from the system proposal is
commercially confidential and must never be committed here, **including in a
commit that is later reverted**, because git history keeps it.

Priced line items, quotes and vendor correspondence live in the separate private
repository `protein-design-foundry-internal`. The cost model page here gives the shape of
the costs without the figures, which is the part that transfers to another
institution anyway.

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
  decisions.yml    build decisions and what each one blocks
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
was truncated by an unquoted comma in a flow mapping.

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
