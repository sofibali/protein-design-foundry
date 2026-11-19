---
key: steristore_cold
title: SteriStore D, 4 °C
standfirst: The coldest position on the system. Everything that cannot be frozen has to be scheduled around that fact.
specs:
  - {label: Temperature, value: "4 °C"}
  - {label: Capacity, value: "216 standard + 50 deep-well positions"}
  - {label: Allocation, value: "9 standard stackers + 5 deep-well"}
  - {label: Holds, value: "DNA, detection reagents, competent cells on the day, grown deep-well blocks, transformation outgrowth"}
unknown:
  - Achieved stability under repeated door cycling during a long unattended run
---

This is the coldest thing on the rack. There is no −20 °C and no −80 °C
position anywhere on the system, so this store defines the lower bound of what
can be kept without leaving the enclosure.

The practical consequence is a scheduling one. Competent cells arrive cold on
the day of a transformation rather than living on the system; enzyme stocks do
the same. Any workflow that assumed a freezer two steps away has to be
rewritten as a workflow with a delivery in it.

## What actually lives here

Two different things, and they are easy to conflate. **Reagents** — DNA,
detection chemistry — sit here between runs. **Grown deep-well blocks** come
here after overnight culture on the
[Cytomat]({{ '/inventory/cytomat/' | relative_url }}) and wait for
purification, which is the step that cannot keep up with them.

That second use is the one that sizes the deep-well allocation. Fourteen
blocks can be grown in a night and purification clears roughly one plate an
hour, so the backlog has to go somewhere cold.
