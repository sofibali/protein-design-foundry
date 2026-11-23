---
key: a4s
title: a4S automated roll heat sealer
standfirst: The second sealer. Recorded as a lidder for most of the planning period, which turned out to be wrong in a way that matters both ways.
specs:
  - {label: Function, value: Roll heat sealing}
  - {label: Temperature range, value: "100–195 °C"}
  - {label: Seal stock, value: "Roll-fed, so a long run does not need a film change"}
  - {label: Role here, value: Holds the gas-permeable culture roll while the PlateLoc holds foil}
  - {label: Lidding, value: "None — this instrument does not handle lids"}
unknown:
  - Roll length and plates per roll
  - Whether the roll can be changed without taking the cart out of a scheduled run
---


This cart was recorded as a lidder from the first device list onward, and
vendor documentation checked on 17 November 2026 says otherwise: it is a roll
heat sealer running 100–195 °C. The correction cuts both ways, and both
directions are worth stating.

<details markdown="1">
<summary>What we gained</summary>

**The system has two sealers**, which is better than having a sealer and a
lidder. Because this one is roll-fed and the
[PlateLoc]({{ '/inventory/plateloc/' | relative_url }}) takes a different
film, a gas-permeable culture seal and a foil seal can both stay loaded
indefinitely. Nobody changes film mid-campaign.

That is what makes the *E. coli* route work unattended: a foil seal off the
PlateLoc takes a twenty-hour deep-well culture anaerobic, while this
instrument applies the gas-permeable roll to the plates that need to breathe,
and the arm chooses between them without a human in the room.

</details>


<details markdown="1">
<summary>What we lost</summary>

**Nothing on the system handles lids.** Plating is in scope, agar plates carry
lids, and filter-plus-carrier plate combinations are too tall for either
sealer. That gap opened the day this was corrected and is
still open.

It also closes off an idea that had been floated for crystallography. Both
sealers here are thermal — the PlateLoc at 30–200 °C, this one at
100–195 °C — and a 200 nL drop has no thermal mass to survive either. A wet
crystallisation tray wants a lid, and there is no longer a candidate
instrument for putting one on.

</details>
