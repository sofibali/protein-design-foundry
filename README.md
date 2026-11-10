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

## Layout

```
_config.yml        site config, nav, collections
_data/             source of truth: instruments.yml, decisions.yml
_projects/         one Markdown file per project: front matter + prose
_layouts/          default, page, project
_includes/         the generated tables (Liquid, rendered at build time)
static/css/        one stylesheet, no framework
scripts/check_data.py
```

There is no build step for the tables. Jekyll reads `_data/` natively and the
includes render the tables when the site builds, so nothing generated is ever
committed and nothing can go stale.

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
