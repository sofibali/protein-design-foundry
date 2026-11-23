# express.cfps.doe

**Stage** express · **Gate** D1 · **Status** draft · **Evidence** none yet

Find a cell-free condition that expresses a new target, and learn which
factors moved it. First protocol every onboarded target runs.

```yaml
in:   {format: 96, contents: dna_template, conc_ng_ul: [20, 200]}
out:  {format: 96, contents: cfps_reaction, readout: rfu}
gate: D1
duration_h: 6
```

---

## The design

Six factors, 16 conditions, **2^(6-2) resolution IV** — main effects are
clean of each other and of two-factor interactions. Four replicates per
condition. One target per round.

**Temperature is not in the matrix.** It cannot be randomised inside a
plate, so putting it in the matrix would make this a split-plot and the
analysis would be wrong. Instead: **run the same 96-well plate in all
four ATCs at four temperatures.** Four independently controlled blocks
turn temperature into a real, replicated factor for free, and all four ATCs
run independent programs at once, which is what the design rests on. The
fourth block is the 384-well unit — see **Scaling** below.

Suggested arms: **20 / 25 / 30 / 37 °C**.

| Run | Mg | K-glu | Energy | Volume | Template | Lot | Wells |
|---|---|---|---|---|---|---|---|
| 1 | 8 mM | 80 mM | 1x | 5 uL | linear | lot A | B6, C7, D8, F11 |
| 2 | 8 mM | 80 mM | 1x | 15 uL | linear | lot B | A2, B1, H1, H3 |
| 3 | 8 mM | 80 mM | 1.5x | 5 uL | plasmid | lot B | A3, A4, C4, F5 |
| 4 | 8 mM | 80 mM | 1.5x | 15 uL | plasmid | lot A | A1, A12, B8, D6 |
| 5 | 8 mM | 180 mM | 1x | 5 uL | plasmid | lot B | C12, C5, E10, E7 |
| 6 | 8 mM | 180 mM | 1x | 15 uL | plasmid | lot A | E11, E2, F4, H7 |
| 7 | 8 mM | 180 mM | 1.5x | 5 uL | linear | lot A | B3, B4, C8, G5 |
| 8 | 8 mM | 180 mM | 1.5x | 15 uL | linear | lot B | D10, D4, G7, H5 |
| 9 | 16 mM | 80 mM | 1x | 5 uL | plasmid | lot A | B5, D2, F12, F3 |
| 10 | 16 mM | 80 mM | 1x | 15 uL | plasmid | lot B | B10, E4, H4, H8 |
| 11 | 16 mM | 80 mM | 1.5x | 5 uL | linear | lot B | D5, D7, F2, G8 |
| 12 | 16 mM | 80 mM | 1.5x | 15 uL | linear | lot A | A10, D3, H10, H6 |
| 13 | 16 mM | 180 mM | 1x | 5 uL | linear | lot B | A11, C3, G1, G2 |
| 14 | 16 mM | 180 mM | 1x | 15 uL | linear | lot A | C11, C2, D1, H11 |
| 15 | 16 mM | 180 mM | 1.5x | 5 uL | plasmid | lot A | B11, B7, E8, F6 |
| 16 | 16 mM | 180 mM | 1.5x | 15 uL | plasmid | lot B | A7, D11, E9, F10 |

Levels are literature starting ranges for lysate-based CFPS — confirm
against your kit's recommendation before the first run.

### Controls, same plate

- **NTC** (8 wells): B12, C10, C9, D12, D9, F7, G12, G9
- **PosCtrl** (8 wells): A8, B9, E5, E6, F1, G4, H12, H9
- **StdCurve** (16 wells): A5, A6, A9, B2, C1, C6, E1, E12, E3, F8, F9, G10, G11, G3, G6, H2

NTC is no-template at that condition and gives per-condition background.
PosCtrl is a known-expressing construct, carried on every plate forever,
so plate-to-plate drift is visible. StdCurve is 8 points in duplicate.

Well assignment is randomised with **seed 20270401** — record it, do not
re-roll between rounds, or plates stop being comparable.

---

## On deck

| | Step | Instrument |
|---|---|---|
| 1 | Acoustic-dispense Mg, K-glutamate and energy stocks to build the 16 conditions | **Echo** |
| 2 | Add template (linear dsDNA or plasmid per run) | **Echo** |
| 3 | Bulk-dispense the common lysate mix to final volume | **MultiFlo** |
| 4 | Seal | **PlateLoc** |
| 5 | Incubate 4–6 h at the arm's temperature | **ATC** ×4 — 3 × 96 + 1 × 384 |
| 6 | Peel | **XPeel** |
| 7 | Add GFP1-10 detection reagent in excess, 30 min | **MultiFlo** |
| 8 | Read fluorescence | **PHERAstar** |

**Building the matrix on the Echo rather than hand-mixing 16 master
mixes** is the point of this layout — 2.5 nL increments, no pipetting
error between conditions, and the matrix is a transfer list, not a
bench protocol. Check your stocks are Echo-compatible first; glycerol
is the usual problem.

The ATC earns its place here as a sealed, lid-heated, precisely held
incubator, not as a cycler. That also controls the evaporation that
otherwise ruins edge wells.

---

## Readout

**split-GFP11 + Twin-Strep at the C-terminus, GGGS linkers** — one tag
gives both this quantification and downstream BLI capture, so nothing is
re-cloned between D1 and D4. GFP1-10 added in excess after expression;
RFU converted against the standard curve.

HiBiT is the alternative if you need luminescence dynamic range. Both
read on the PHERAstar.

---

## Analysis

1. Subtract per-condition NTC background.
2. Convert RFU to µg/mL against the standard curve; reject the fit if
   R² < 0.98.
3. Fit main effects plus estimable two-factor interactions, **with
   temperature arm as a factor** across the four plates.
4. Report effect size and CI per factor. Flag any factor whose CI
   crosses zero as not worth carrying into round 2.
5. Rank conditions by mean yield; report the best and its replicate SD.

---

## D1 — does it express?

| | |
|---|---|
| **pass** | at least one condition **≥ 5 µg/mL** in ≥3 of 4 replicates |
| **fail** | no condition reaches 5 µg/mL at any temperature |
| **ambiguous** | clears in exactly 2 of 4 replicates, or only at one edge temperature |

**pass** → fix the condition, go to `express.cfps.production96`
**fail** → log the route failure as training data, try `express.ecoli.autoinduction96`
**ambiguous** → round 2, Bayesian optimisation around the best region

Decided by: agent.

**Where 5 µg/mL comes from** (set 2026-11-17). The screen is tiered:
NanoBiT first, on crude cell-free with no purification, then HTRF on the
survivors. So D1 does not have to deliver assay-grade mass — it only has
to put the design above NanoBiT's working range. At ~14 kDa, 5 µg/mL is
about 360 nM in the reaction, which still leaves ≥10 nM in the assay well
after a 20× dilution.

The floor is deliberately low. **D1 is the cheap, inclusive gate** and its
failures are training data; the expensive resource is purified protein,
which is D2's problem.

The number that *is* expensive was derived the other way, from what the
full ladder consumes per design at ~14 kDa:

| | |
|---|---|
| D5 dose–response, 12 points 3-fold, top 1 µM, 20 µL, triplicate | 1.26 µg |
| D4 primary, ± target, triplicate at 100 nM | 0.17 µg |
| D6 selectivity, hotspot mutant + 3 homologs | 0.34 µg |
| D2 QC | 0.20 µg |
| D4 promiscuity panel, 3 proteins in triplicate | 0.25 µg |
| **purified protein per design** | **~2.25 µg** |
| crude needed, at 50% bead recovery | ~4.5 µg |

**That 2 µg is D2's floor, and it is stated as a mass rather than a
concentration on purpose** — so it does not depend on the production
reaction volume. When `express.cfps.production96` picks a volume, the
conversion follows: 100 µL/well needs 45 µg/mL, 50 µL needs 90, 200 µL
needs 22.

---

## Consumables per plate

Lysate CFPS kit (2 lots) · template DNA · GFP1-10 reagent · GFP11
standard · 96-well PCR plate ×4 · seals ×4 · Echo source plate · tips.
Four plates per round, one per temperature arm.

## Scaling

**Settled.** RAC 2 holds **3 × 96-well + 1 × 384-well ATCs**, four units in
one cart (Ginkgo Q&A, confirmed 2026-11-03). So this design runs as written
on three of the four temperature arms, and the fourth arm is the 384 block.

That matters for the matrix above, not just for throughput. Thermo's own
figures: the **96-well block takes 10–100 µL** for full-skirted plates, and
the **384-well block takes 5–20 µL** (0.02 mL block). The Volume factor here
has levels of **5 µL and 15 µL**, so both sit inside the 384 block's range
and the design runs unchanged on any of the four arms. Give the 384 arm the
5 µL runs if you are choosing. All four blocks share the same thermal
performance — ±0.25 °C accuracy from 35–99.9 °C, under 0.5 °C uniformity
twenty seconds after reaching 95 °C, 2.8 °C/s block ramp — so the arms are
comparable by specification, not by assumption.

**The 4× is still available, and the decision is open.** The recommendation on
record is to swap a second 96 block for a 384 — still four units, so close to
price-neutral against the quoted ATC line — and push retrieval PCR to 384 via
the Echo. For a 1,152-design set that is 3 plates instead of 12 and cycler
time from 10 h to 6 h. Keep at least two 96-well blocks whatever happens:
Golden Gate at 30 µL, heat lysis at 95 °C and held-temperature steps all need
the 10–100 µL range the 384 block does not have.

**What this costs the day.** Nothing on the Bravo. The Echo builds the
matrix (~3 min a plate, 12 min for the four arms) and the PHERAstar reads it
(~8 min a plate, 32 min for four) — so one round is about 3% of a 20-hour
day, and the reader is what limits it. Building the same matrix with a
96-channel head instead would cost **32 min of Bravo time per 384-well
plate**, four offset quadrant transfers each, against the Bravo's ceiling of
~75 two-plate protocols a day. That ratio is the reason step 1 below is an
Echo step and not a Bravo one.
