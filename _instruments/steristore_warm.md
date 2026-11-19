---
key: steristore_warm
title: SteriStore D, 37 °C
standfirst: Static incubation at production scale. Four thermal cycler blocks are the flexible route; this is the wide one.
specs:
  - {label: Temperature, value: "37 °C"}
  - {label: Capacity, value: "288 standard + 20 deep-well positions"}
  - {label: Allocation, value: "12 standard stackers + 2 deep-well"}
  - {label: Humidity, value: "Up to 98% RH"}
  - {label: Agitation, value: "None — static incubation only"}
  - {label: Holds, value: "Assay-plate incubation, cell-free reactions, static non-shaking culture, transformation recovery"}
---

The humidity specification is the one that earns its place. At 98% RH a plate
can sit through a long incubation without the edge wells drying, which is what
otherwise turns a 384-well cell-free plate into a 300-well plate with a
gradient around the outside.

## Why this and not the thermal cyclers

Both hold 37 °C, and for a four-arm temperature experiment the
[cyclers]({{ '/inventory/atc/' | relative_url }}) are the right answer because
each block runs its own program.

At production scale that stops being the point. Four blocks is four plates.
This store is 288 standard positions, all at one temperature, and when a
campaign is running one condition across many plates that is the instrument
that matters. The cyclers are for finding the condition; this is for using it.

## What it is not

It does not shake. Deep-well *E. coli* growth needs aeration and therefore
goes to the [Cytomat]({{ '/inventory/cytomat/' | relative_url }}), which is a
14-position cap on the whole *in vivo* route. The 20 deep-well positions here
are for static recovery steps, not for growth.
