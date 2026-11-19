---
key: hig3
title: HiG 3 automated centrifuge
standfirst: 5,000 g, unrefrigerated. Those two numbers constrain the lysis chemistry of every workflow on the system.
specs:
  - {label: Maximum force, value: "5,000 g"}
  - {label: Refrigeration, value: "None"}
  - {label: Uses here, value: "Cell harvest, plate clarification, filter-plate spins"}
unknown:
  - Achieved plate temperature after a long spin, which decides whether a labile target survives harvest
---

Read both specifications together, because the limit they create is not
obvious from either one alone.

**5,000 g is below what detergent lysis needs.** Clearing a detergent lysate
properly takes around 15,000 g. At 5,000 g the lysate stays turbid, and turbid
lysate defeats AlphaScreen and fluorescence polarisation — the two readout
modes that otherwise give the most signal per well on the
[PHERAstar]({{ '/inventory/pherastar/' | relative_url }}).

**It is not refrigerated.** A long spin warms the plate, which matters for
anything labile.

## What that forces

Heat lysis at 95 °C in a 96-well
[thermal cycler block]({{ '/inventory/atc/' | relative_url }}) is the only
lysis route this device set supports without compromise. That is a fortunate
accident rather than a design: heat lysis also happens to delete the 14-hour
bead purification step from the *E. coli* route.

The whole thing rests on whether the target survives 95 °C for 15 minutes,
which is what the
[MD1 thermal project]({{ '/projects/md1-thermal/' | relative_url }}) tests. If
it does not, this centrifuge becomes a real constraint rather than an
interesting one.

## The decision that was already weighed

A refrigerated centrifuge was considered and rejected: it would need its own
enclosure, a different vendor and true refrigeration, which is not worth it
against what it buys. That is
[decision 10]({{ '/decisions/' | relative_url }}), and it stays on the list so
nobody re-opens it without knowing it was priced.
