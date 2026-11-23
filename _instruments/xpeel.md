---
key: xpeel
title: XPeel Automated Plate Seal Remover
standfirst: De-sealing between steps. It shares cart 1 with the PlateLoc, so a plate can be opened and reclosed without leaving the enclosure.
specs:
  - {label: Function, value: Automated removal of adhesive and heat seals}
  - {label: Method, value: "Adhesive peel tape, applied and pulled across the seal"}
  - {label: Consumable, value: Peel tape roll}
  - {label: Cart, value: "Shares cart 1 with the PlateLoc, so seal and peel are one stop"}
unknown:
  - Tape roll length and plates per roll, which sets how often a run needs a consumable change
  - Whether it lifts all three seal types in use here, particularly the foil
  - Whether a partially peeled seal is detected or passes silently to the next step
---


The XPeel is the step that is easy to forget when planning a workflow and then
blocks it. Cell-free expression, for example, seals before the thermal cycler
and has to open again before the detection reagent goes in; without an
automated peel that is a person opening the enclosure in the middle of a run.

Pairing it with the [PlateLoc]({{ '/inventory/plateloc/' | relative_url }}) on
the same cart means the arm makes one trip rather than two.

<details markdown="1">
<summary>What we do not know yet</summary>

This is the thinnest specification on the system, and that is worth saying
plainly rather than padding. The consumable question matters most: a peel tape
roll that runs out mid-campaign stops an unattended run exactly as effectively
as a hardware fault, and we do not yet know the interval.

</details>
