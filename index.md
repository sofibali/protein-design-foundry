---
layout: page
title: Automated Protein Design Foundry
standfirst: An automated protein design facility at UCSF Mission Bay, built on fifteen enclosed robotic carts.
---

The system is meant to take a designed sequence to measured data without a
person moving a plate. This site is the working record of that build: what it
can do, what it cannot, what is still undecided, and what it costs.

It is kept honest on purpose. A facility that publishes only its capabilities
is useless to someone trying to work out whether their experiment will run here.

<div class="cards" markdown="0">
  <div class="card"><h3><a href="{{ '/capabilities/' | relative_url }}">Capabilities</a></h3>
    <p>What the system does, at what scale, and where it stops.</p></div>
  <div class="card"><h3><a href="{{ '/projects/' | relative_url }}">Projects</a></h3>
    <p>Foundational test projects. Each is a claim about a capability.</p></div>
  <div class="card"><h3><a href="{{ '/decisions/' | relative_url }}">Decisions</a></h3>
    <p>{{ site.data.decisions.decisions | where: "status", "open" | size }} still open, and what each one blocks.</p></div>
  <div class="card"><h3><a href="{{ '/inventory/' | relative_url }}">Inventory</a></h3>
    <p>{{ site.data.instruments.instruments | where: "status", "quoted" | size }} instruments across {{ site.data.instruments.racs | size }} carts.</p></div>
</div>

## The shape of it

Each cart is a sealed micro-environment with its own six-axis arm, sitting on a
shared magnetic transport track. Plates move between instruments without anyone
opening a door, which is what makes a twenty-hour unattended run possible.

Two expression routes run on the same hardware. The in-cell route is capped by
shaking positions and takes about **51 hours** for a 1,152-member library. The
cell-free route skips growth entirely and takes about **12 hours** for the same
library, with a ceiling more than a hundred times higher. Neither is the right
answer on its own, which is the point of having both.

## Working with us

Not open for general submissions yet. If you think a workflow belongs here, the
most useful thing you can send is the step list, the plate formats and the
volumes, because that is what determines whether it fits.

## How this stays accurate

Inventory and decisions live in `_data/` and the tables are rendered from them
at build time. A number changes in one place. Figures taken from somewhere else
say where they came from.
