# Gene to kinetics in three days, without cells

Ruiz Espi, Avelar Molina, Buch, Heyd, Unger, Gormsen, Lund, Sahni Ray,
Williams, Hald, Jenkins, Rivera-de-Torre. DTU Center for Translational
Protein Design and the DTU Arena for Life Science Automation, with
Fraunhofer ITMP, Fida Biosystems, LenioBio and Novo Nordisk.
bioRxiv, posted ~2026-10-20, doi 10.64898/2026.10.19.759856.

**Preprint, not peer reviewed.** Funded by Novo Nordisk; two authors are
co-founders of AffinityAI; one author each from Fida Biosystems and
LenioBio, whose instrument and reagent the pipeline depends on. Read the
performance claims with that in mind.

This is the closest published match to what the foundry is trying to be:
an automated, metric-driven design loop feeding a cell-free, purification-
free, immobilisation-free assay, with standardised per-design data coming
back out for model training. **Their front half runs on our deck almost
unchanged. Their readout does not exist here.**

---

## What they did

RFdiffusion → ProteinMPNN (5 sequences per scaffold) → AlphaFold2
initial-guess, keeping designs at ipAE < 8 Å and pLDDT > 80, up to five
rounds of partial diffusion. Final ranking by Boltz-2 ipSAE. Top 32
ordered as linear dsDNA, assembled, expressed and measured.

Target: human growth hormone. Three campaigns — one blind, two seeded on
different hot-spot sets.

| | |
|---|---|
| Designs tested | 32 (four full columns of a 96-well plate) |
| Expressed | **30 of 32, 94%** |
| Bound | **11 of 30, 37%** |
| Affinities, top four | **K_D 0.93 ± 0.36 to 9.98 ± 2.24 nM** |
| k_on | 3.8 × 10⁵ to 5.8 × 10⁶ M⁻¹s⁻¹ |
| k_off | 6.7 × 10⁻⁴ to 1.8 × 10⁻² s⁻¹ |
| Throughput | 288 designs per 5 days on one instrument |
| Time from DNA to kinetics | three days |

---

## The part we can take today

**No cells anywhere.** This is the piece worth copying, and it is not the
assay. Their build is:

```
linear dsDNA gene fragment
  → PCR
  → SPRI cleanup
  → Golden Gate into a CIRCULARISING CFPS vector
  → SPRI cleanup
  → straight into cell-free
```

Golden Gate closes a circle *in vitro*. There is no transformation, no
outgrowth, no colony, no miniprep, no sequencing — the circular product
goes directly into the expression reaction. **That removes the one step in
workflow 4.2 that the deck cannot do well**, because nothing here needs a
colony picker.

Their reagents and conditions, which map onto our instruments one-to-one:

| Step | Theirs | Ours |
|---|---|---|
| PCR | Platinum SuperFi II 2× master mix, 30 µL in an Armadillo 384 plate, 30 cycles | Echo + MultiFlo → ATC |
| SPRI | MagMAX Pure Bind, 1.8× beads, 2 × 70% EtOH, elute 15 µL | Bravo + magnet |
| Golden Gate | 16 µL: BsaI-HFv2, T4 ligase, 1,800 ng vector; 30 × (37 °C 60 s / 16 °C 60 s), 60 °C 10 min | Echo → ATC |
| SPRI again | 27 µL beads, elute 15 µL | Bravo + magnet |
| Expression | 2 µL DNA + 18 µL lysate | MultiFlo |

Automation was a Tecan Fluent 780 with an 8-channel arm, a 384-channel
head, a gripper, an INHECO ODTC 384XL cycler, a BioShake and an Alpaqua
Magnum FLX magnet. Every one of those has a counterpart on our rack. They
used self-sealing PCR lids and a permeable polyolefin lid rather than a
heat sealer, so **the PlateLoc/XPeel pair replaces two consumables here,
not one instrument.**

**One honest flaw in their protocol:** insert was added as a fixed volume,
not normalised by mass, so the insert-to-vector molar ratio varied design
to design. On an Echo there is no reason to copy that — normalise.

---

## The expression system is new to this repo

**ALiCE** (LenioBio) is a *tobacco BY-2* lysate — eukaryotic cell-free,
not *E. coli*. 18 µL reagent + 2 µL DNA, **36 h at 25 °C, 800 rpm, 85%
relative humidity**, in a low-protein-binding 384-well plate under a
permeable lid.

That is a third expression route beyond lysate *E. coli* and PURE, and it
matters for anything needing eukaryotic folding or disulfides. But read
the conditions against our deck:

- **25 °C with shaking for 36 h.** The Cytomat shakes and incubates, but
  most incubators floor out around ambient + 5 °C. **Ask whether it can
  hold 25 °C**, not just whether it reaches 30 °C.
- **85% RH.** Nothing in the current spec says any deck position controls
  humidity. A permeable lid over 36 h without it will concentrate the
  reaction by evaporation.
- 36 h occupies a position for a day and a half, which is a scheduling
  fact, not a technical one.

---

## The readout does not exist here, and it is the interesting part

**FIDA** — flow-induced dispersion analysis — measures the hydrodynamic
radius of a fluorescent species in a capillary under pressure-driven flow.
Binding makes the fusion bigger; ΔRh > 0.1 nm is the call. It needs no
immobilisation, no labelling beyond the fusion the construct already
carries, no purification, and no wash.

They read **1 µL of crude cell-free diluted 1:100** and got, per design:

- expression level, by fluorescence against a calibration curve
- hydrodynamic radius, so oligomeric and aggregation state
- whether the fusion was cleaved (two designs were excluded this way)
- equilibrium K_D, in PreMix mode
- **k_on and k_off, in CapMix mode, from the same material**

That is the entire D1/D2/D4/D5 column from one instrument on unpurified
lysate. It is also, precisely, the gap in our deck: §6 of
`capabilities.md` says *no kinetics, no BLI or SPR, hits that need
kinetics go offline.*

**But it is a FIDA Neo, a capillary instrument, not a plate reader.**
There is no substitute on the rack and the paper does not suggest one.
It is serial — 288 designs per five days is about 58 per day, against a
PHERAstar's 384 wells in minutes. The trade is depth per design against
throughput, and it is a real trade, not a free win.

Its stated weakness: binding is hard to see when the expected radius
change is under about 5%. A small binder on a large target is the good
case; a small target on an FP-fusion binder is the bad one.

---

## The construct trick worth stealing

Their fusion is `[design] — linker — mChartreuse — FXa site — Strep-tag II`.

A **whole fluorescent protein**, not a split tag. That means expression is
read directly off the fusion with nothing added — no GFP1-10 spike, no
second reagent — and every number downstream is normalised per design by
that same fluorescence. They name unnormalised expression as the reason a
previous method missed a low-µM binder.

Against our standing split-GFP11 cassette:

| | split-GFP11 | full FP fusion |
|---|---|---|
| Size added | 16 aa | ~27 kDa |
| Needs a reagent | yes, GFP1-10 | no |
| Reads in crude lysate | yes | yes |
| Effect on hydrodynamic radius | negligible | dominates |
| Irreversible, over-reports weak signal | yes | n/a |

**Pick by readout.** Split-GFP11 for a plate assay where mass matters;
a full FP where the measurement *is* fluorescence and you want it free.
The FXa site is how they get the tag off again, which is worth keeping in
mind for anything going to structure.

They purified only five designs, on **MagStrep Strep-Tactin XT beads**
(IBA 2-5090-010) — the same beads already specified in
`reference/constructs.md` §6 — and only to build the calibration curve
and run gels, not for the screen.

---

## The negative result is the most useful thing in the paper

**None of the in-silico scores predicted which designs would bind.**

| Metric | ROC AUC |
|---|---|
| AF2-IG ipAE | 0.58 |
| AF3 ipSAE min | 0.50 |
| **Boltz-2 ipSAE min** | **0.43** |

0.5 is a coin flip. **Boltz-2 ipSAE came out below it** — the metric used
to pick the 32 ranked them slightly worse than random among those that
passed the filters.

The authors' explanation is restricted range: everything had already
cleared ipAE < 8 Å and pLDDT > 80, so there was little signal left to
rank on. That is plausible and it is the charitable reading. Either way
the operational lesson stands and it bears directly on Aim 2:

> **A score that filters well does not necessarily rank well.** Once a
> set has passed a filter, re-scoring it with a related metric may add
> nothing. Validate a ranking metric against measured outcomes on your
> own target before trusting it to choose what gets ordered.

Two more of their nulls, both underpowered but worth noting: hot-spot
seeding did not beat blind design on hit rate (8/20, 2/9, 1/3; Fisher
P = 0.65), and per-trajectory hit rate was indistinguishable from
binomial noise (P = 0.40).

---

## What I would not take at face value

- **One target.** Everything rests on hGH. No panel, and **no unrelated-
  target negative control is reported** — the only specificity argument is
  that the lysate itself is a complex background. Our D4 plate carries
  decoys for exactly this reason; theirs does not.
- **Small n.** 32 tested, 11 bound. None of the residue-level contact
  comparisons survived multiple-testing correction (q = 0.41, q = 0.72).
- **Internal inconsistencies.** The introduction says 11 of 32; the
  abstract and results say 11 of 30. The results give the ΔRh range as
  "0.43–0.11 nm" and the discussion as 0.43–1.11 nm. The PreMix method
  lists steps 1, 2, 3, 5. The pooled meta-analysis counts 201 designs
  where the campaign totals give 212. None of these change the
  conclusions, but they are the kind of thing peer review should catch.
- **Conflicts.** The two commercial dependencies — FIDA Neo and ALiCE —
  each have an author from the supplying company.

---

## What to do about it

1. **Adopt the cells-free build now.** Golden Gate into a circularising
   CFPS vector, SPRI, straight into expression. It removes transformation
   and outgrowth from the arrayed route and needs nothing we do not have.
2. **Ask Ginkgo two questions** the ALiCE conditions raise: can any deck
   position hold **25 °C with shaking**, and does anything control
   **humidity**?
3. **Put FIDA on the instrument wish-list, costed against BLI.** It fills
   the kinetics gap from crude lysate, which BLI does not, but it is
   serial and it is a single-vendor dependency.
4. **Do not order designs on a Boltz rescore alone** until it has been
   checked against measured outcomes on a foundry target.
