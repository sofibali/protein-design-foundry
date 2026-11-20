# What fails across every campaign — the in vitro equivalent of ipAE

The question: **in silico you have ipAE, pTM, ipSAE and pLDDT — generic
numbers computed the same way for every design against every target. What
is the experimental equivalent?** If the limiting factor is screening large
numbers of designs, the measurements worth standardising are the ones that
mean the same thing whatever the target is.

Written 2026-11-17.

---

## First, the honest split

Design failures fall into two classes, and they are not the same size.

**Class 1 — it does not behave as a protein.** Does not express, expresses
and aggregates, gets cleaved, sticks to everything. **Target-independent:
measurable with no target present at all.**

**Class 2 — it behaves perfectly and does not bind.** Folds, is soluble,
is monomeric, and has no affinity for the thing it was designed against.
**Target-specific.**

What the published numbers say about the split:

| | |
|---|---|
| DTU, hGH, 32 designs | **30/32 expressed (94%)**, then **11/30 bound (37%)** |
| Adaptyv, across customers | claimed **>90% expression success** |
| Pacesa 2025, cited in the aims | experimental success **~10–100% per target** |

So after in-silico filtering, roughly **6% fail class 1 and 59% of the
survivors fail class 2.** Class 1 is the minority.

**But that is partly an artefact of the filtering**, and it is the key
subtlety. DTU kept only designs at ipAE < 8 Å and pLDDT > 80 before
ordering. Those metrics are, among other things, **implicit expressibility
predictors** — a design the model cannot fold confidently is also a design
that tends not to express. The in-silico filter has already removed most
class-1 failures before anything reaches a plate.

**The consequence for the foundry is uncomfortable and worth stating.** The
target-independent measurements are cheap, transferable and worth
collecting on every design — and they will not be the main discriminator.
The main discriminator is class 2, and **there is no known
target-independent in vitro predictor of it.** That is precisely why a
large measured-failure dataset is worth building: it is the only way the
question gets answered.

---

## What the deck can measure with no target present

Everything at D1 and D2 is already target-free. These are the candidates,
and most are already being collected:

| Descriptor | Where | Measured today? |
|---|---|---|
| **Expression yield**, µg/mL | D1 | yes, every design, every route |
| **Oligomeric / aggregation state** | D2, FP | yes |
| **Integrity** — is the design still attached to its tag | D2, FP low side | **no — see below** |
| **Decoy promiscuity** — how many decoys a design fires on | D4 | measured, then **discarded** |
| **Thermal robustness** — residual binding after a temperature ladder | 4.10 | not yet; needs no new hardware |
| **Stickiness** — adsorption, from peak shape | FIDA only | no instrument |
| **Hydrodynamic radius**, absolute | FIDA only | no instrument |

Two of these are free and currently thrown away.

---

## The one that is a real hole: integrity

The standing cassette is `[design] — GGGS — GFP11 — GGGS — Twin-Strep`, so
**both the reporter and the purification tag sit C-terminal to the design.**

If the design is proteolysed off, what survives is a GFP11–Strep peptide.
It still complements GFP1-10, so **D1 passes.** It still binds the beads,
so **D2's concentration read passes.** The campaign then carries a well
that contains no design at all and is labelled as 2 µg of one.

DTU excluded two of their thirty designs for exactly this, by gel.

**FP catches it, and D2 is currently blind to it because the window is
one-sided:**

| species | size | FP |
|---|---|---|
| GFP1-10 + free GFP11 peptide (**cleaved**) | 27 kDa | **400 mP** |
| GFP1-10 + design–GFP11 (intact) | 41 kDa | 427 mP |
| intact dimer | 82 kDa | 456 mP |
| aggregate | — | 490 mP |

Cleavage sits **27 mP below** the intact monomer, against **+29 mP** for a
dimer. At ±4 mP reader precision both are about 6σ. The same read already
being taken catches both failure modes — the gate just has to look down as
well as up.

---

## Stickiness needs a standing panel, and the repo does not have one

**Correction to an earlier draft of this document.** It claimed the decoys
already on every D4 plate give a per-design stickiness score. They do not.
In this repo a **decoy is a design** — one generated against an unrelated
target and placed inside the 36 as a plate control, where *"any decoy above
threshold invalidates the plate"*. A design is never read against decoys,
so there is no decoy-fire fraction per design to retain.

The counter-target is per-design, but it is a **campaign-specific homolog**
— MD2 and MD3 for PARP14. That measures selectivity within a family, which
is useful and is not transferable: a specificity number against MD2 means
nothing to a lab working on a kinase.

**A transferable stickiness score needs a standing panel of unrelated
targets, identical in every campaign and every lab.** That is the thing
that makes it an experimental ipAE: the same measurement, computed the same
way, on every design anyone in the foundry ever makes.

### The panel

Three proteins, spanning charge and size, because nonspecific binding is
mostly electrostatic and mostly surface area:

| | Size | pI | Why |
|---|---|---|---|
| **Lysozyme** | 14 kDa | ~11 | small and strongly basic — catches acidic designs |
| **Ubiquitin** | 8.5 kDa | ~6.8 | tiny and extremely stable — a low-surface-area baseline |
| **MBP** | 43 kDa | ~5 | large and acidic — catches basic designs, and large surface |

Not BSA, which is already a blocking agent in these buffers, and not GFP,
which collides with the split-GFP readout. Each is expressed once with the
assay's tag (LgBiT for NanoBiT) and used in every campaign thereafter. **The
panel must never change**, or the numbers stop being comparable, which is
the entire point.

### The score

Read each design against all three at the same concentration as its target,
in triplicate — 9 wells, **0.25 µg per design**.

| | |
|---|---|
| **panel fold** | the design's fold-activation on each member |
| **specificity index** | target fold / **max** panel fold — the headline number |
| **panel-fire fraction** | members at fold ≥ 2.0, out of 3 |

Max rather than mean, because one strong nonspecific interaction is the
thing worth knowing about.

**It records, it does not gate.** A promiscuous design still goes to D5 —
D6 does the real specificity work, and cross-reactivity is a measurement.
Gating on it here would discard data for the sake of a cleaner funnel.

### What it costs

0.25 µg per design, which takes the budget from 1.97 µg to 2.22 µg and so
**raises D2's floor from 2 µg to 2.25 µg**. Triplicate costs the same floor
as duplicate once rounded, so there is no reason to economise.

---

## Why the target-independent block is the valuable dataset

Year 1 is four labs; year 2 is twelve. **Binding data from different
targets does not pool** — a K_D against PARP14 MD1 and a K_D against
someone else's kinase are not comparable observations, and a model trained
across them is learning target identity as much as design quality.

**The target-free block does pool.** "Does this sequence express, stay
monomeric, stay intact and stay unsticky" is the same question for every
design in every lab, and the answer is a property of the sequence. Pooled
across twelve labs that is a dataset nobody else has, and it is the one
thing the foundry can produce that a single well-run lab cannot.

It also feeds Aim 1 directly. The expression model that assigns a route to
each new target is trained on exactly this.

---

## What to do about it

1. **Make D2's FP window two-sided.** Catches cleavage at no cost on a read
   already being taken. This is a correctness fix, not an enhancement.
2. **Build the standing promiscuity panel** and record a specificity index
   per design. This is the experimental ipAE analogue, and the repo has no
   equivalent today.
3. **Record the target-free block as a per-design vector** — yield,
   FP deviation, specificity index, route — alongside the campaign-specific
   result, so it is poolable later even if nothing uses it in year 1.
4. **Add the thermal ladder (4.10)** once there is spare reader time. It
   needs no hardware and it is the one major class-1 descriptor the deck
   cannot currently produce.
5. **Do not expect any of this to predict binding.** On the published
   evidence it will explain a minority of failures. Collect it because it
   is nearly free and because it is the part that transfers — and let the
   class-2 dataset accumulate to answer the harder question honestly.
