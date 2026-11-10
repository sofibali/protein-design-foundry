---
layout: page
title: Capabilities
standfirst: What the system does, at what scale, and what each route costs in instrument time.
---

## Throughput, measured against a real library

The numbers below are for **1,152 designed binders**, the scale of the first
campaign. They come from a stage-by-stage model of the device set, not from
vendor marketing, and the per-stage figures in that model are estimates.

| Route | 1,152 designs | Ceiling per round | Limited by |
|---|---|---|---|
| In-cell expression | **51.5 h** | 1,344 cultures | 14 shaking deep-well positions |
| Cell-free, 384-well | **11.7 h** | 57,600 reactions | reagent cost, then reader time |
| Cell-free, 1536-well | **11.7 h** | 230,400 reactions | reagent cost, then reader time |
| Crystallography screening | 11.5 h on-system | 150 tray positions | tray positions, then imaging |

Of the 51.5 hours on the in-cell route, 20 are unattended overnight expression
and **12 are magnetic-bead clean-up**, which is 23% of the run. If an assay
tolerates crude lysate, deleting that step is the largest single saving
available anywhere in the pipeline.

<div class="note" markdown="1">
Going from 384- to 1536-well format costs nothing in reagent. The same volume
runs four times the reactions, so the only question is whether the dispenser and
the reader support the format. Both do.
</div>

## What it can do

**Molecular biology at plate scale.** Four independently programmable thermal
cyclers in one cart, so four protocols run at once. A 1,152-member library is
3 plates at 384-well or 12 at 96-well.

**Protein expression, two routes.** Deep-well culture with shaking, or cell-free
with no growth step. The cell route gives milligram-per-millilitre yields and
needs transformation. The cell-free route gives 100 to 500 µg/mL, needs none,
and the identity of a well is simply what the dispenser put in it.

**Purification at screening scale.** Magnetic beads in plate format, around 96
lysates per hour. Enough for binding assays, not for structural work.

**Readout.** One reader covering fluorescence intensity and polarisation,
luminescence, BRET, absorbance from 220 to 1000 nm, time-resolved FRET and
AlphaScreen, **in every plate format from 6 to 3456 wells**.

**Liquid handling to 1 µL,** with 2 µL the smallest volume holding 2% CV, plus
acoustic nanolitre transfer with no tips.

**Storage under three conditions,** with plates presented on demand:

| Store | Standard | Deep-well | Holds |
|---|---|---|---|
| Ambient, controlled | 216 | 50 | crystallography trays, bulk, plates in flight |
| 4 °C | 216 | 50 | DNA, detection reagents, grown blocks |
| 37 °C | 288 | 20 | assay incubation, cell-free, static culture |
| Shaking | — | 14 | all shaking growth |
| **Total** | **720** | **134** | 2.0× headroom over peak demand |

## What it cannot do

Read [the limits]({{ '/capabilities/limits/' | relative_url }}) before planning
around any of the above. In short: no frozen storage, no size exclusion, no
concentrator, no colony picking, and no crystal imaging yet.
