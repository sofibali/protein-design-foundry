---
key: lynx
title: Lynx LM900 VVP
standfirst: The only variable-volume channel on the system, and the only one that measures what it actually moved.
specs:
  - {label: Heads, value: "96-channel and 8-channel, both Volume Verified Pipetting"}
  - {label: Minimum volume, value: "1 µL"}
  - {label: Best accuracy, value: "2 µL at 2% CV"}
  - {label: Tip types, value: "35 µL, 300 µL, 1200 µL — filter tips available in all three"}
  - {label: Verification, value: "In-line flow sensor on every channel, measuring aspirate and dispense in real time"}
  - {label: Per-channel features, value: "Tip detection, contact dispense, mixing by pipetting"}
  - {label: Primary job, value: Concentration normalisation before assay}
unknown:
  - "VVP 2.0 reaches 1 µL and ships at SLAS in late January at no price difference — the upgrade path should be in the contract before signing, or we buy 1.0 weeks before 2.0 exists"
---

Volume Verified Pipetting is the reason this instrument is here rather than a
second [Bravo]({{ '/inventory/bravo/' | relative_url }}). An in-line flow
sensor on every channel measures what was actually aspirated and dispensed,
per channel, as it happens.

That turns a normalised plate from a nominal claim into a measured one. The
per-well correction can be logged against the design, which is what makes a
concentration series comparable between campaigns rather than only within one.

## Where it sits in a run

After expression and quality control, before any assay. Protein comes off
purification at whatever concentration each well happened to give; the Lynx
flattens that, so a dose–response starts from a known plate instead of from
accumulated variation.

Skipping this step does not produce an obvious failure. It produces a
dose–response curve whose spread is expression noise wearing the costume of
biology, which is considerably worse.

## The 1 µL question

1 µL is the stated minimum and 2 µL is where it holds 2% CV. Those are
different claims and the gap matters: a 2.5 µL cell-free reaction in 1536 is
comfortably inside the good-CV point, so the Lynx could set one up even where
the [MultiFlo]({{ '/inventory/multiflo/' | relative_url }}) is the planned
route.
