---
key: plateloc
title: PlateLoc Thermal Microplate Sealer
standfirst: The primary sealer. One of two on the system, which is what lets a culture seal and a foil seal both stay loaded.
specs:
  - {label: Function, value: Thermal (heat) sealing of SBS-format plates}
  - {label: Settable temperature, value: 30–200 °C}
  - {label: Working range here, value: 130–180 °C}
  - {label: Seal time, value: 1–3 s}
  - {label: Seal stock, value: Roll or sheet, changed by hand}
  - {label: Seal types in use, value: "Gas-permeable for culture, foil for anaerobic deep-well, clear peelable for crystallography"}
unknown:
  - Whether a crystallisation plate that already holds nanolitre drops survives a heat seal at all
  - The exact clear peelable part number for crystallography trays
  - Settable range is from vendor documentation; the 130–180 °C figure came from the proposal and the two have not been reconciled against a single sheet
---

Sealing is not a detail on this system. A plate that moves between carts with
an open top will evaporate, aerosolise or cross-contaminate, so almost every
transfer between unit operations has a seal or a peel on one side of it.

The PlateLoc is a thermal sealer, which means it presses heated film onto the
plate rim for one to three seconds. That works for everything the expression
routes need and is the reason a twenty-hour deep-well culture can run
anaerobically: a foil seal off this instrument closes the block completely.

## Why there are two sealers

The [a4S]({{ '/inventory/a4s/' | relative_url }}) on cart 15 is also a sealer,
not the lidder it was first recorded as. Having two means the PlateLoc can hold
foil while the a4S holds the gas-permeable roll, and neither needs a human to
change film in the middle of a run. That is a genuine capability, and it was
discovered rather than designed.

## Where it stops

Both sealers on the system are thermal. A 200 nL crystallisation drop has
almost no thermal mass, so neither is obviously safe over a wet tray, and
crystallography trays are closed with a lid instead — except that nothing on
the system currently handles lids either. That gap is
[decision 16]({{ '/decisions/' | relative_url }}).
