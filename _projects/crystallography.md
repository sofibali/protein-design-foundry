---
title: Automated crystallography and fragment soaking
summary: The workflow that drives the most hardware decisions and is the least automated of them.
status: proposed
lead: Sofia Bali
scale: 20 complexes across 4 screens, 80 plates, 23,040 drops
exercises: [echo, bravo, ambistore, plateloc, xpeel, a4s, hig3]
tests:
  - Acoustic drop setting against commercial screens
  - Sealing a plate that already holds nanolitre drops
  - Scheduled imaging without a human opening the enclosure
open:
  - Viscous precipitants fall outside the acoustic dispenser's fluid classes
  - Milligram-scale protein is made off-system
  - Imaging has no instrument on the system at all
---

Crystallography drives more hardware decisions here than any other workflow:
the ambient store's 9-to-5 stacker split, the acoustic dispenser model, the clear
peelable seal, the lidding cart, the custom arm work for larger-volume dispensing
and the whole phase-two imaging cart. It is also the least automated of them.

It is where the acoustic dispenser does something no person can match, which is
soaking thousands of fragments into drops.

## Where the time goes

| Scenario | Total |
|---|---|
| On-system steps only | **11.5 h** |
| Plus imaging by hand, 7 timepoints | **48.9 h** |
| Plus imaging on a dedicated cart | **20.9 h** |

**37 of those 48.9 hours are a person carrying trays to a microscope.** 80 trays
at 7 timepoints is 560 imaging events. That ratio, not the drop-setting problem,
is the largest single argument for the phase-two imaging cart.

## Drop volume is a throughput decision

A 96-well three-subwell plate holds 288 drops. Protein is half of each drop, and
a four-screen campaign is four plates per complex. At 10 mg/mL:

| Drop, protein side | Per plate | Four screens | Cultures needed | Complexes per round |
|---|---|---|---|---|
| 200 nL | 0.58 mg | 2.30 mg | 31 wells | 43 |
| 100 nL | 0.29 mg | 1.15 mg | 16 wells | 84 |
| 50 nL | 0.14 mg | 0.58 mg | 8 wells | 168 |
| 25 nL | 0.07 mg | 0.29 mg | 4 wells | 336 |

Dropping from 200 nL to 50 nL takes a round from 43 complexes to 168. The honest
counter-argument: crystals grown in 50 nL drops are small and harder to harvest
by hand, and harvesting is entirely manual.

## The three things that are not solved

**Drop setting.** Acoustic dispensing of crystallisation drops is published, but
every precipitant needs a validated fluid class, and 25–35% PEG, high salt and
glycerol fall outside them. Expect to lose 10–30% of a commercial screen. The
obvious dedicated alternative has no drop-setting API, so it would be a custom
integration.

**Sealing.** The sealer is thermal. Whether a plate already holding 200 nL drops
survives one to three seconds at 130–180 °C has not been established, and 200 nL
has no thermal mass to speak of. If it does not, the system needs a cold film
applicator, and the lidding cart is not one.

**Imaging.** There is no instrument. Every tray leaves the enclosure on a
schedule, which is exactly the thing the automation was bought to stop.
