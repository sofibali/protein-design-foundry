---
title: Designed binders against the PARP14 MD1 macrodomain
summary: Library design through assay readout as one unbroken run, on both expression routes.
status: running
lead: Sofia Bali
scale: 1,152 designs, one backbone
exercises: [atc, bravo, cytomat, echo, hig3, pherastar, plateloc, xpeel]
tests:
  - Library design through assay readout as one unbroken run
  - Both expression routes, in vivo and cell-free, at the same scale
  - Whether well position can carry identity without colony picking
open:
  - Arraying to one variant per well is unsolved
  - Bead clean-up is 23% of the run time and may be removable
---

The macrodomain is small, well behaved and has a known ligand, so a binder that
works can be confirmed independently. That makes it a good first load: if the
pipeline is wrong, the biology will not hide it.

## What the run costs

A 1,152-member library is **3 plates at 384-well** or **12 at 96-well**.

| Route | Instrument time | Attended |
|---|---|---|
| In-cell | 51.5 h | ~31 h, with 20 h unattended overnight expression |
| Cell-free | 11.7 h | nearly all of it |

**Magnetic-bead clean-up is 12 hours, 23% of the in-cell run.** It is there to
keep lysate out of the binding readout. If the assay tolerates crude lysate, the
run drops to about 40 hours, and that is the single largest saving available
anywhere in the pipeline.

## The constraint nobody expects

Oligo pool synthesis caps a single ordered fragment at 350 nucleotides, which
after the fixed 45-nucleotide overhead leaves **101 amino acids**. Binders
longer than that need two-fragment assembly, which doubles the assembly step and
halves the effective library for a fixed synthesis budget. Design length is
therefore a throughput decision, not only a biophysical one.

## Why arraying is the real problem

Plating is in scope and colony picking is not, so nothing returns a clone from
agar to liquid. Without that, a well does not know what is in it. Two honest
options: accept pooled libraries and deconvolute by amplicon sequencing, or add
a picker. The cell-free route sidesteps it entirely, because a well contains
exactly what the acoustic dispenser put there.

This is the step that decides whether the in-cell route is a screening platform
or a re-expression service for hits found elsewhere.
