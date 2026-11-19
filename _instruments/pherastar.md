---
key: pherastar
title: PHERAstar FSX
standfirst: Every readout the system has. It is also, with the Bravo, one of the two instruments that caps the working day.
specs:
  - {label: Detection modes, value: "Fluorescence intensity and polarisation, luminescence, BRET, absorbance 220–1000 nm, time-resolved FRET/HTRF, AlphaScreen"}
  - {label: Plate formats, value: "Every detection method from 6-well through 3456-well"}
  - {label: Throughput ceiling, value: "150 384-well TR-FRET plates per 20-hour day (modelled)"}
  - {label: Per TR-FRET or FI read, value: "~8 min"}
  - {label: Per luminescence read, value: "~3 min"}
  - {label: TRF module, value: High-End TRF/HTRF with two red-sensitive photon-counting PMTs}
  - {label: AlphaScreen, value: HTS laser included}
  - {label: Injectors, value: "Two reagent injectors"}
  - {label: FP precision, value: "±3–5 mP"}
  - {label: Absorbance noise floor, value: "~0.005 AU"}
unknown:
  - "A UV TR-FRET laser for flying-mode reading and wider dynamic range is a priced option, not included — it likely matters most at 1536"
---

This is a **homogeneous mix-and-read** instrument, and that single fact shapes
what kind of foundry this is. No wash, no immobilisation, no regeneration, no
sensor tips. There is no BLI and no SPR anywhere on the system.

The cost is real: you cannot get k<sub>on</sub> or k<sub>off</sub> here. You
get endpoint and equilibrium. Anything needing kinetics goes offline.

The gain is equally real: 1,536 wells read in minutes, straight out of crude
reactions, with no consumable per sample beyond the reagent itself.

## The format line is the one to notice

"Every detection method from 6 through 3456 wells" is what opens the
1536 route. It means AlphaScreen and HTRF are both available at 1536, so the
cheapest-per-design workflows are not limited by the reader. Combined with the
[MultiFlo]({{ '/inventory/multiflo/' | relative_url }}) reaching 1 µL per well
at that density, the 230,400-reaction ceiling is real rather than theoretical.

## It ties with the Bravo as the bottleneck

150 plate reads a day against the
[Bravo's]({{ '/inventory/bravo/' | relative_url }}) ~75 two-plate protocols.
For the assay workflows — which are built to keep the Bravo out of the chain
entirely — **the reader is what binds**, not the liquid handler.

One scheduling trap: a long kinetic read occupies the instrument for the day.
An endpoint read usually recovers most of the discrimination and frees it.
That is worth deciding before any kinetic protocol goes on a shared schedule.

## Known precision limits

Two numbers worth carrying into experimental design. Fluorescence polarisation
reads to ±3–5 mP, which is enough to detect aggregation but not to resolve
oligomer-level change. Absorbance noise sits near 0.005 AU, which is why A280
is not a usable concentration readout at the microgram scale this system works
at — that job goes to a complementation assay instead.
