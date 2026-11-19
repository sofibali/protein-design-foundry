---
key: multiflo
title: MultiFlo bulk dispenser
standfirst: Common reagent into every well at once. Cheap, fast, and the step that makes 1536-well screening affordable.
specs:
  - {label: Function, value: Bulk reagent addition — the same liquid into every well}
  - {label: 1536 performance, value: "1 µL per well, full plate in 21 s"}
  - {label: Formats, value: "96 through 1536"}
  - {label: Uses here, value: "Cell-free master mix, detection reagent, SOC after transformation, inoculation, lysis buffer"}
unknown:
  - Dead volume per reagent line, which sets the real cost of a short run
  - Whether a light-sensitive or expensive reagent can be run without priming waste
---

Bulk dispensing is unglamorous and it is what makes the cheap workflows cheap.
A cell-free plate is built by the [Echo]({{ '/inventory/echo/' | relative_url }})
putting a different template into every well, then this instrument putting the
same master mix into all of them. Neither step touches the
[Bravo]({{ '/inventory/bravo/' | relative_url }}).

## The 1536 answer

This was an open question and it is now closed: 1 µL per well across a full
1536 plate in 21 seconds. A 2.5 µL cell-free reaction sits comfortably inside
that, so **the 230,400-reaction route is open on the dispenser side**.

That matters more than it sounds. Going from 384 to 1536 costs nothing in
reagent — the same volume runs four times the reactions — so the only
questions were whether the dispenser could reach the volume and whether the
reader could see the plate. Both answers are now yes.

## The priming constraint

The pump has to be primed, and priming means pushing reagent through the line
and discarding it. For a master mix that is a rounding error. For something
light-sensitive or genuinely expensive it is a real cost, and that pushes the
reagent back onto the Echo or the
[Lynx]({{ '/inventory/lynx/' | relative_url }}) despite the throughput
penalty. The dead volume per line is the number that decides this, and we do
not have it.
