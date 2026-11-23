---
key: echo
title: Echo acoustic liquid handler, 6XX series
standfirst: Tipless nanolitre transfer. The one instrument on the system that does something no person can match.
specs:
  - {label: Method, value: "Acoustic droplet ejection — no tips, no contact, no carryover"}
  - {label: Throughput, value: "~400 plates per 20-hour day at 384 format (modelled)"}
  - {label: Per plate, value: "~3 min"}
  - {label: Per crystallography tray, value: "~9 min"}
  - {label: Destination formats, value: "Up to 1536"}
  - {label: DMSO, value: "Supported on the 6XX series — required for fragment screening"}
  - {label: Source, value: "Plates only; no source tubes"}
  - {label: Required model, value: "6XX. The proposal line reads Echo 525, which cannot do DMSO, 1536, or the drop volumes crystallography needs"}
unknown:
  - "650 against 655 is still open on dispense speed for our plate types — decision 2"
  - Which precipitant fluid classes are validated; 25–35% PEG, high salt and glycerol fall outside the published set
---


The Echo is the answer to the [Bravo's]({{ '/inventory/bravo/' | relative_url }})
4× penalty on 384-well plates. A 96-channel head fills a 384 plate in four
offset quadrant transfers; acoustic transfer does not care about density at
all, so 384 costs the same as 96 and 1536 is reachable.

That is why most workflows here are designed to put the Echo in the chain and
keep the Bravo out of it. It is not a preference about instruments. It is a
factor of ten on the system bottleneck.

<details markdown="1">
<summary markdown="span">What it is uniquely good at</summary>

**Dose–response.** The dilution series is built acoustically in the
destination plate. No serial pipetting, no tip-to-tip carryover, and
arbitrary non-linear spacing if the curve wants it.

**Fragment soaking.** Thousands of compounds from DMSO stocks into existing
crystallisation drops. This is the thing no person can match, and it is the
reason the 6XX requirement is not negotiable — the 525 handles neither DMSO
nor the volumes.

</details>


<details markdown="1">
<summary markdown="span">The fluid class problem</summary>

Acoustic dispensing works by matching a calibrated fluid class to the liquid
in the source well. Crystallisation precipitants are where that breaks down:
25–35% PEG, high salt and glycerol all fall outside the published classes, and
the realistic expectation is losing 10–30% of a commercial screen.

Glycerol-based enzyme master mixes are refused outright, which is what the
[Magniflex]({{ '/inventory/magniflex/' | relative_url }}) is for.

</details>
