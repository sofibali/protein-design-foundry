---
key: cytomat
title: Cytomat 2 C-LiN
standfirst: The only shaking position on the system, and therefore the hard ceiling on everything grown in cells.
specs:
  - {label: Capacity, value: "14 deep-well positions"}
  - {label: Concurrent culture protocols, value: "7"}
  - {label: Function, value: Shaking and incubation in one unit}
  - {label: Temperature range, value: "To 50 °C (70 °C on the C470 variant)"}
  - {label: Quoted orbit, value: "1–3 mm at 100–1200 rpm"}
  - {label: Orbit wanted, value: "25 mm at 100–350 rpm, offered on the Selector variant"}
  - {label: Vendor validation, value: Tested and used by the integrator for E. coli}
unknown:
  - Whether the quoted 1–3 mm orbit aerates a deep-well E. coli culture, which is the one open question on this unit
---


This unit decides the scale of the entire *in vivo* route. Fourteen deep-well
positions, seven concurrent culture protocols, and no amount of clever
scheduling moves either number. A 1,152-design library is 12 plates at 96-well
format, so one round of *E. coli* expression essentially fills it.

The [37 °C store]({{ '/inventory/steristore-warm/' | relative_url }}) holds 288
plates and the [Bravo]({{ '/inventory/bravo/' | relative_url }}) deck has
temperature-controlled nests, but neither shakes, and a deep-well culture that
does not aerate does not grow. There is no second option on this system.

<details markdown="1">
<summary markdown="span">Temperature is not the constraint</summary>

This was an open question and it is now closed. The C-LiN series runs to 50 °C,
and the unit has to reach 37 °C for *E. coli* anyway, so **30 °C growth for
yeast costs no hardware at all**. A third expression route is a scheduling
change rather than a purchase.

</details>


<details markdown="1">
<summary markdown="span">The orbit is</summary>

1–3 mm at 100–1200 rpm is a mammalian-suspension specification. Published
deep-well microbial protocols run at 25 mm. The concern is not speed, it is
throw: a small orbit at high rpm swirls the surface without turning over the
column of liquid underneath, and a deep-well block is mostly column.

The Selector variant offers 25 mm. Whether the quoted unit aerates adequately
is worth a growth curve before anyone designs a campaign around 14 plates a
night, and it is the one specification on this instrument still genuinely
open.

</details>
