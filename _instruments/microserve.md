---
key: microserve
title: MicroServe
standfirst: Tips and consumables for the whole system. Every tip box lives here, which makes it the unglamorous thing that decides how long a run goes unattended.
specs:
  - {label: Function, value: Tip and consumable store}
  - {label: Scope, value: All tip boxes on the system live here — there is no separate tip stacker}
  - {label: Serves, value: "Bravo, Lynx and Magniflex tip formats"}
unknown:
  - Position count, and therefore how many tip boxes of each type can be resident at once
  - Whether all three tip formats used on the system fit simultaneously
  - Whether an empty tip box is detected before a protocol starts or at the moment it fails
---


An eight-position tip-box stacker was considered and dropped: all tip boxes
live in this unit instead. That is tidier, and it concentrates a risk.

<details markdown="1">
<summary markdown="span">Why it decides unattended run length</summary>

The point of an enclosed system is that a twenty-hour run needs nobody.
Running out of tips breaks that as effectively as any hardware fault, and the
[Lynx]({{ '/inventory/lynx/' | relative_url }}) alone uses three tip formats —
35, 300 and 1200 µL — with filter variants of each.

So the real specification question is not capacity in the abstract. It is
whether the mix of tip types a given campaign needs can all be resident at the
same time, and how many plates' worth that is. We do not have those numbers,
which is why they are listed as unknown rather than estimated.

</details>


<details markdown="1">
<summary markdown="span">The detection question</summary>

The difference between a protocol that refuses to start and one that stops
halfway through with a half-processed plate is entirely about whether tip
inventory is checked up front. Worth confirming before the first long
unattended campaign rather than after it.

</details>
