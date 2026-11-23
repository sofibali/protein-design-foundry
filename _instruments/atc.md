---
key: atc
title: Automated thermal cyclers, 4 units
standfirst: Four independently programmable blocks in one cart, which is what makes temperature a real experimental factor rather than a plate-level confound.
specs:
  - {label: Configuration, value: "3 × 96-well blocks + 1 × 384-well block, all four in a single cart"}
  - {label: Independent programs, value: Four at once}
  - {label: "Fill volume, 96-well", value: "10–100 µL"}
  - {label: "Fill volume, 384-well", value: "5–20 µL"}
  - {label: Optical detection, value: None}
  - {label: Uses here, value: "PCR, Golden Gate cycling at 37/16 °C, heat lysis at 95 °C, held-temperature cell-free incubation, thermal-challenge ladders"}
unknown:
  - Vendor and model are not confirmed on the proposal
  - Whether swapping one 96 block for a second 384 is price-neutral; it would take retrieval PCR for 1,152 designs from 12 plates to 3
  - An internal note put the 384 block at roughly 30 µL against the 5–20 µL in the vendor documentation; the vendor figure is used here
---


Four blocks in one cart is a better deal than it first looks. Most workflows
need a cycler for a single step, so four of them rarely means four times the
PCR. What it means is that a four-level temperature arm runs as four parallel
plates with identical handling, instead of as four sequential runs where the
day of the week is confounded with the condition.

That is how the expression optimisation treats temperature, and it is the only
way to get a clean effect size out of it.

<details markdown="1">
<summary>The volume split matters</summary>

The 384 block takes 5–20 µL and the 96 blocks take 10–100 µL, so they are not
interchangeable. Golden Gate, heat lysis and held-temperature incubations want
the 96 range. Retrieval PCR and anything at 384 density wants the small one.
Keeping at least two 96 blocks is therefore a real constraint on the
swap-for-a-second-384 question, not a preference.

</details>


<details markdown="1">
<summary>No melt curves</summary>

There is no optical detection in any of the four blocks, so differential
scanning fluorimetry has nowhere to be read and **this system cannot measure a
Tm**. The workable substitute is a thermal challenge: incubate aliquots across
a temperature ladder on these blocks, then read residual binding on the
[PHERAstar]({{ '/inventory/pherastar/' | relative_url }}). That is a genuine
stability readout. It is just not a melting temperature, and it should never be
reported as one.

</details>


<details markdown="1">
<summary>The cheapest capability on the system</summary>

Heat lysis at 95 °C in a 96-well block costs nothing, needs no new hardware,
and removes the single most expensive step in the *E. coli* route — the
fourteen-hour magnetic bead clean-up on the
[Bravo]({{ '/inventory/bravo/' | relative_url }}). Whether the target survives
it is what the
[MD1 thermal project]({{ '/projects/md1-thermal/' | relative_url }}) is for.

</details>
