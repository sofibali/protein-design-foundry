# bind.cf2h.screen

**Stage** test · **Gates** D1 + D4, same well · **Status** draft ·
**Evidence** published method, never run here

Screen a batch of designed binders against one target with no purified
protein on either side. Expression and binding are read as one number.

```yaml
in:   {format: 96, contents: linear_dna_pair, conc_nm: [2.5, 5]}
out:  {format: 384, contents: cf2h_reaction, readout: rfu_mef}
gate: D4
duration_h: 8
```

Method from Capin et al., *CF2H: a cell-free two-hybrid platform
for rapid protein binder screening*, Nat Commun 2026,
<https://doi.org/10.1038/s41467-026-69741-1>. Every number below that
is attributed to them is theirs; everything about the deck is ours and
unvalidated.

---

## Part 0 — the one-time build

**None of this is on the RAC.** It is three offline components, and
until all three exist the protocol cannot run. Budget weeks.

| Component | What | Status |
|---|---|---|
| **Reporter plasmid** | sfGFP behind the pRM promoter, OR3 operator knocked out so the promoter is not repressed at high CI. Low-copy backbone. Used at **5 nM final**. | to build |
| **CI cassette** | constitutive promoter · RBS · **CI(1–92)** · **GGSx5** linker · insert. Ordered as one eBlock, ~700 bp with a 200 bp insert. | to design |
| **Extract** | *E. coli* **BL21 Rosetta 2 ΔRecBCD**, S30. The deletion is what lets linear DNA survive — no GamS in any reaction, ever. | to source |

The shortened DBD does not work. CI(1–76) gave no activation with any
linker or any pair they tested, so the 16 residues that do not contact
DNA are structural and must stay. **Do not trim the domain.**

The GGSx5 linker is not optional either — direct fusions worked for some
pairs and failed for others, and the long flexible linker is what made
large globular partners work at all.

**Buying the lysate instead.** A commercial lysate plus GamS is the
fallback and costs €5–10 per reaction against €0.10 homemade. It also
re-introduces an additive to every well. Either is defensible; decide
before the reporter plasmid is built, because the extract lot drives the
buffer calibration below.

### Buffer calibration, per extract lot

Fix K-glutamate at 80 mM, titrate Mg-glutamate, take the optimum, then
titrate K-glutamate at that Mg. Theirs landed at **15 mM Mg-glutamate,
100 mM K-glutamate** — inside the bracket `express.cfps.doe` already
scans, so that screen doubles as this calibration if the same extract is
used. Re-derive per lot. Do not inherit the number.

---

## Part 1 — pick the target format

Run this decision once per target, before any design batch.

| | Format | When |
|---|---|---|
| **1** | CI–target + CI–binder | default |
| **2** | target fused to a multimerisation domain, CI on the binder only | format 1 self-activates |
| **3** | buy the target biotinylated, pre-mix **1:1 with streptavidin at 150 nM**, spike the tetramer in | target is hard to express, or best SNR wanted |

**The gating experiment is CI–target alone.** If it fires the reporter
with no binder present, the target is aggregating and format 1 is dead
for that target. That is exactly what happened to them with PD-L1.

For format 2, use the **p53 tetramerisation domain or a hexameric
coiled-coil** — both gave ~3× the signal of format 1 on Mdm2. A GCN4
homodimer gave nothing, so valency above two is the requirement, not
multimerisation as such.

Format 3 removes target expression from the problem entirely and gave
their best signal-to-noise. If a biotinylated ectodomain is a catalogue
item for your target, start here and skip the decision.

---

## Part 2 — DNA, and how much of it runs on deck

Order each construct as an eBlock or gene fragment. Then:

| | Step | Instrument |
|---|---|---|
| 1 | Set up PCR from the ordered fragment, high-fidelity polymerase | **Echo** + **MultiFlo** |
| 2 | Cycle | **ATC** |
| 3 | Bead cleanup | **Bravo** + magnet |
| 4 | Add dsDNA-binding dye, read against a DNA standard curve | **MultiFlo** → **PHERAstar** |
| 5 | Normalise all fragments to **50 nM** | **Echo** |

Their gel check is the one step with no deck equivalent — run it offline
on the first batch of any new design set and drop it once a design set
is trusted.

**The PCR is not optional.** They amplify before use rather than
pipetting the ordered fragment neat, and it buys template mass plus a
concentration number per design.

**Unsequenced DNA is this protocol's main false-negative source.** They
traced several benchmark misses to systematic synthesis error, not to
the assay. A design that fails here once is a candidate for
re-synthesis, not a dead design.

---

## Part 3 — the plate

Assemble at 22 µL in 96, plate 5 µL × 3 into 384. One assembly well
yields four platings, so three replicates leaves dead volume.

**Assembly plate, 96-well — 36 designs:**

| Wells | Contents |
|---|---|
| 72 | 36 designs × (**+target**, **−target**) |
| 2 | known binder pair, ±target — the positive PPI control |
| 1 | CI–target alone — target self-activation |
| 1 | reporter plasmid only, no linear DNA — floor |
| 1 | constitutive sfGFP from linear DNA — extract is alive, and the expression ceiling |
| **78** | **used; 18 spare** |

**Put 4–6 decoys inside the 36.** Designs generated against an unrelated
target, carried through the whole plate as if real. They are the only
on-plate evidence the screen is specific, and in the published benchmark
all 12 decoys stayed silent while 6 of 12 BLI-negatives scored as
binders — without decoys there is no way to tell those two results
apart.

**Destination, 384-well black wall / clear bottom, low-binding:** 78 × 3
= 234 reaction wells, plus **16 FITC standard wells** (8 points in
duplicate) pipetted directly, never assembled. 250 of 384 used.

Randomise plating position with **seed 20270401**, the same seed
`express.cfps.doe` uses. Record it; never re-roll between rounds or
plates stop being comparable.

---

## Part 4 — on deck

| | Step | Instrument |
|---|---|---|
| 1 | Dispense reporter plasmid, binder DNA, target DNA (or the streptavidin-target complex), any competitor | **Echo** |
| 2 | Bulk-dispense the **cold** extract + buffer master mix to 22 µL | **MultiFlo** |
| 3 | 5 µL × 3 from assembly into the 384 | **Bravo** |
| 4 | Seal — **transparent film, not foil** | **PlateLoc** |
| 5 | 37 °C, Ex 485 / Em 528, read every 10 min | **PHERAstar** |

**Order matters and it is doing real work.** Reactions are assembled on
ice in the published method. DNA tolerates ambient on the Echo deck;
extract does not. Dispensing all DNA first and adding the cold master
mix last is what makes an ambient-deck instrument sequence survivable.

**The remaining cold-chain risk is the MultiFlo reservoir**, where the
master mix sits at ambient for the length of the run. That — not the
Echo, not the Bravo — is what caps how many plates go in one batch.
Worth measuring on the first run rather than assuming.

**Timing.** Signal appears under 2 h and plateaus by 8 h. A full kinetic
read owns the PHERAstar for the day; a 4 h endpoint recovers most of the
discrimination. Decide before this goes on a shared schedule.

---

## Part 5 — readout

Convert raw RFU to **FITC mean-equivalent fluorescence** against the
on-plate standard curve, as they do, so numbers survive a change of
reader or gain setting.

**Fold-activation** = signal(+target) ÷ signal(−target), per design, at
a fixed timepoint.

---

## Part 6 — analysis

1. Convert to MEF.
2. Subtract the reporter-only floor.
3. **Classify self-activators first.** Any design whose −target signal
   sits meaningfully above the floor is homodimerising or aggregating.
   Its fold-activation is not interpretable. Record the self-association
   as a result — it is free data, and in the published screen it hit 1
   of 36 Mdm2 designs and 2 of 36 PD-L1 designs, both beta-rich.
4. Compute fold-activation for the rest.
5. **Check the decoys.** Any decoy above threshold invalidates the
   plate; do not rescue individual wells.
6. Rank. Do not fit.

---

## D4 — which designs bind?

| | |
|---|---|
| **pass** | **robust z ≥ 3.0 AND fold-activation ≥ 2.0** in ≥2 of 3 replicates, −target at floor, all decoys silent |
| **fail** | below both, with −target at floor |
| **ambiguous** | clears one but not the other, or 1 of 3 replicates, or −target elevated, or any decoy fired |

**pass** → D5, orthogonal confirmation offline
**fail** → log as training data; it is a measured negative, which is the
point of keeping failures
**ambiguous** → **D5 as well.** A dose-response costs the same plate time
as repeating the single point and tells you more: a real binder shows dose
dependence, a noise hit does not. The exception is a decoy firing or an
elevated −target, which point at synthesis error — re-synthesise the
fragment and repeat those.

Decided by: agent.

**Fixed 2026-11-17.** The 2.0 fold is theirs and on its own it is arbitrary
in the same way Watson's 0.5 BLI cutoff is arbitrary — it ignores how noisy
the plate was. The **robust z across the plate's own fold distribution** is
what makes it noise-aware, and the AND of the two is what keeps the training
label clean. Recall is protected by the ambiguous route rather than by a
loose threshold: across 1,000 designs the whole z = 2 to z = 4 range differs
by about 21 dose-responses, so there is nothing to buy by being lax at the
pass line.

---

## What this protocol does not tell you

- **A Kd.** It produces a rank.
- **Anything weaker than ~100 nM**, which is not reliably detected at
  all. This is a high-affinity filter.
- **Any discrimination among sub-nanomolar binders** — it saturates.
- **Whether the design bound the face it was designed for.** That is the
  arm below.

Signal confounds affinity with expression, solubility and stability.
They argue that is a feature for prioritisation, and it is — but it
means the output must never be fitted as an affinity measurement.

---

## The hotspot arm — same plate, second round

This is the part worth building the whole system for, and it is the
question the baseline PARP14 work could not answer.

For each hit, order **4–6 single-alanine mutants at the designed
interface residues** and run them exactly as above against the same
target. ΔActivation against wild-type tracked ΔΔG measured by SPR in
their hands, and ranked mutants correctly by affinity.

A design whose signal is unmoved by mutating its own designed hotspots
did not bind where it was designed to. That is **D6**, answered on a
plate reader.

**The competition variant.** Titrate a known site ligand into the
reaction. It only displaces a binder it substantially out-competes —
Venetoclax at ~10 pM displaced a nanomolar designed BCL2 binder with an
IC50 of ~202 nM, while an Mdm2 inhibitor at affinity comparable to its
binders moved only the weakest of three. For MD1, a known macrodomain
site ligand gives an orthogonal site test with no mutant construct at
all, **if** it is much tighter than the binder. Check that first.

---

## Consumables per screen

Extract (or commercial lysate + GamS) · cell-free buffer · reporter
plasmid · 78 PCR-amplified fragments · high-fidelity polymerase ·
cleanup beads · dsDNA dye + standard · FITC standard · 96-well assembly
plate · 384-well black/clear low-binding plate · **transparent** seals ·
Echo source plate · tips.

At their costing, the reactions themselves are under €10 for the screen.
**Synthesis is the entire budget.**

---

## Must be settled before the first run

- The reporter plasmid and CI cassette do not exist yet. Offline build.
- Extract route: homemade ΔRecBCD, or commercial lysate plus GamS.
- **Clear seal on the PlateLoc** — confirm with Jamie, same open
  question as the rest of the read-through-seal workflows.
- PHERAstar occupancy: 8 h kinetic or 4 h endpoint.
- Whether the MultiFlo can hold a cold master mix long enough for a
  multi-plate batch.
- Whether the gel check can be dropped after the first batch of a design
  set, or has to stay.
