---
title: Thermal survival of MD1 under heat-lysis conditions
summary: Whether the target survives the only lysis route the system can actually deliver.
status: running
lead: Sofia Bali
scale: Temperature ladder plus a time course, with a lysate-matrix arm
exercises: [atc, hig3, pherastar, bravo]
tests:
  - Whether heat lysis at 95 °C destroys the target along with the cells
  - Interference from lysate matrix in the binding readout
---

Detergent lysis needs a 15,000 g clearing spin. The centrifuge here reaches
5,000 g and is not refrigerated, so it cannot clear that lysate. **Heat lysis at
95 °C for 15 minutes in the thermal cycler is the only route the device set
supports without compromise** — provided the target survives it.

If it does not, a whole branch of the pipeline closes and the in-cell route has
to fall back on a lysis chemistry the hardware cannot properly clear. That is
worth knowing early and cheaply, which is the entire point of this project.

## Why the second arm matters

Turbid lysate defeats AlphaScreen and fluorescence polarisation, the two readout
modes that otherwise give the most signal per well. The lysate-matrix arm spikes
purified protein into blank lysate to separate two failure modes that look
identical in the raw data: the target being destroyed, and the readout being
blinded by what the lysis left behind.

A clean result here sets the lysis conditions for every subsequent campaign, so
it is a protocol that earns its cost once and then stops.
