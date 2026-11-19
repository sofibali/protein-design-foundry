---
key: bravo
title: Bravo liquid handler, 96-channel head
standfirst: The system bottleneck. Everything that pipettes queues here, and a 384-well plate costs it four times a 96-well plate.
specs:
  - {label: Head, value: 96-channel fixed-span}
  - {label: Throughput ceiling, value: "~75 two-plate protocols per 20-hour day (modelled)"}
  - {label: One 96-well transfer, value: "~8 min"}
  - {label: One 384-well transfer, value: "~32 min — four offset quadrant transfers"}
  - {label: Deck magnet, value: Bead separation for magnetic purification}
  - {label: Deck temperature nests, value: "Two Peltier positions, −20 to 99.9 °C, 12 K/min, held at 4 °C and 42 °C"}
  - {label: Bead purification rate, value: "~60 min per 96-well plate (96 lysates/hour)"}
unknown:
  - Price of a 384-channel head, and whether heads swap without re-integration
  - Whether the achieved heat-shock CV across a 96-well plate matches bench transformation
---

Read the throughput line before planning anything. The Bravo and the
[PHERAstar]({{ '/inventory/pherastar/' | relative_url }}) are tied as the
system bottleneck, and the Bravo is the one that binds first for any workflow
involving transfers.

**The 4× is the single most important number on this page.** A 96-channel head
filling a 384-well plate has to make four offset quadrant transfers, so a 384
plate costs 32 minutes of the bottleneck against 8 for a 96 plate. This is why
most well-designed workflows here put the
[Echo]({{ '/inventory/echo/' | relative_url }}) in the chain and keep the Bravo
out of it entirely: on the Echo, 384 costs the same as 96.

## Two deck features that matter more than the pipetting

**The magnet** makes this the purification instrument. It is also where the
*E. coli* route loses its time: 60 minutes per 96-well plate means a full
14-plate round is a 14-hour serial step, roughly a quarter of the whole run.

**The two temperature nests** are what make heat-shock transformation possible
at all. A single ramping block takes about three minutes to go from 4 °C to
42 °C at 12 K/min, and a thermal cycler on another cart cannot time a
45-second step. Two fixed positions and one plate move does it. That is a
capability the deck turned out to have, rather than a decision anyone made.

## Raising the ceiling

Two things would, and both are open. A 384-channel head would remove the 4×
penalty outright. Pushing more dispensing to the Echo is free and is already
the design of most workflows here.

<div class="note" markdown="1">
The rates above are arithmetic off the vendor's own throughput figures, not
measurements taken on our system. Treat the **ratio** between two workflows as
more trustworthy than the absolute number on either.
</div>
