# STAR Methods — CF2H Cell-free two-hybrid screen

_Working document, 2026-11-23. Derived from `_data/protocols.yml`
(`workflows:`, id `CF2H`), from `protocols/bind.cf2h.screen.md`, from
`reference/capabilities.md` §8, and from the citation audit in
`00-citation-audit.md`. Intended practice; the facility installs April 2027
and the repository marks this protocol **build** — three offline components
do not exist yet._

**Citation status: published method, cited, with one erratum.**

**Capin, Mayonove, DeVisch, Becher, Ngo, Courbet et al.**, "CF2H: a
cell-free two-hybrid platform for rapid protein binder screening", *Nature
Communications*, 2026-03-10,
[10.1038/s41467-026-69741-1](https://doi.org/10.1038/s41467-026-69741-1).
PMC13103306, PMID 41807394. DOI resolved live against Crossref on
2026-11-23; PMC and PMID resolved live against the NCBI ID converter the
same day.

> **Erratum.** `protocols/bind.cf2h.screen.md` and
> `reference/capabilities.md` both attribute this DOI to *"Delauriere et
> al."* Crossref returns **Capin et al.** The DOI, journal, year and PMC id
> in those files are correct; only the author name is wrong. The private
> repository's `notes/binder_literature_record.md` already has it right, so
> the two repositories currently disagree. Not fixed here — both files
> belong to other lanes.

**Everything numeric below that is attributed to the paper is theirs; the
deck mapping is this facility's and is unvalidated.** The repository's own
protocol file is already careful about this split and it is preserved here.

---

## Key resources table

Catalogue numbers deliberately omitted. **[inferred]** marks what is not
stated in the repository. **[to build]** marks a component that does not
exist yet — all three are offline builds and the protocol cannot run until
they do.

| REAGENT OR RESOURCE | SOURCE | NOTES |
|---|---|---|
| **Bacterial strains and cell extracts** | | |
| *E. coli* BL21 Rosetta 2 ΔRecBCD, homemade S30 extract | Capin et al. 2026 | **[to build / to source]** The RecBCD deletion is what lets linear DNA survive, so **no GamS in any reaction, ever** |
| Commercial *E. coli* lysate + GamS, as the fallback | | Re-introduces an additive to every well. The choice must be made **before** the reporter plasmid is built, because the extract lot drives the buffer calibration |
| **Recombinant DNA** | | |
| pRM / OR3* sfGFP reporter plasmid | Capin et al. 2026 design | **[to build]** sfGFP behind the pRM promoter with the OR3 operator knocked out so the promoter is not repressed at high CI. Low copy — **a high-copy reporter titrates CI**. Used at 5 nM final |
| CI(1–92) + GGSx5 cassette | Capin et al. 2026 design | **[to design]** Constitutive promoter · RBS · CI(1–92) · GGSx5 linker · insert. Ordered as one eBlock, ~700 bp with a 200 bp insert. **CI(1–76) gave no activation with any linker or pair tested — do not trim the domain.** The GGSx5 linker is not optional either |
| CI-fusion gene fragments, one per design | IDT (eBlocks) or Twist Bioscience | PCR-amplified before use, gel-checked, normalised to 50 nM. Fragments at 2.5–5 nM in the reaction |
| Multimerisation domain — p53 tetramerisation domain or a hexameric coiled-coil | | Format 2 only. Both gave ~3× the signal of format 1 on Mdm2; **a GCN4 homodimer gave nothing**, so valency above two is the requirement, not multimerisation as such |
| **Proteins and targets** | | |
| Biotinylated target protein | | Format 3 only. Pre-mixed 1:1 with streptavidin at 150 nM and spiked in as the tetramer |
| Streptavidin | | Format 3 only |
| **Buffers and chemicals** | | |
| Magnesium glutamate | | Their optimum 15 mM. **Re-derive per extract lot; do not inherit the number** |
| Potassium glutamate | | Their optimum 100 mM. Calibration order: fix K-glu at 80 mM, titrate Mg, take the optimum, then titrate K-glu at that Mg |
| **Enzymes and kits** | | |
| High-fidelity PCR polymerase or master mix | | The PCR is not optional: it buys template mass plus a concentration number per design |
| SPRI / PCR cleanup beads | | After the fragment PCR |
| dsDNA-binding dye + DNA standard | | Quantification of each fragment before normalisation |
| **Reference materials and controls** | | |
| FITC standard | | 8 points in duplicate, 16 wells, **pipetted directly and never assembled**. Converts raw RFU to mean-equivalent units so numbers survive a change of reader or gain setting |
| Known binder pair, ± target | | The positive PPI control, 2 wells |
| CI–target alone | | Target self-activation control, 1 well. **This is the gating experiment** — if it fires with no binder present the target is aggregating and format 1 is dead for that target |
| Reporter plasmid only, no linear DNA | | Floor, 1 well |
| Constitutive sfGFP from linear DNA | | Extract-alive control and the expression ceiling, 1 well |
| Decoy designs, 4–6 inside the 36 | | Designs against an unrelated target, carried through as if real. **The only on-plate evidence the screen is specific** |
| Single-alanine mutants at designed interface residues, 4–6 per hit | | The hotspot arm (gate D6), second round |
| Known site ligand, for the competition variant | | Only displaces a binder it substantially out-competes — check the affinity gap first |
| **Plasticware and consumables** | | |
| 96-well assembly plate | | 22 µL per well, 36 designs, 78 of 96 wells used |
| 384-well black-wall / clear-bottom, low-binding plate | | 5 µL × 3 per assembly well; 234 reaction wells + 16 FITC wells = 250 of 384 |
| **Transparent** adhesive seal film | | **Not foil.** The plate is read through the seal |
| Echo-qualified source plate | Beckman Coulter | |
| Bravo 96-channel pipette tips | | The 5 µL × 3 transfer into 384 — four offset quadrant transfers |
| MultiFlo dispense cassette **[inferred]** | BioTek | The cold master-mix bulk dispense |
| **Instruments** | | |
| Echo 525, MultiFlo, Bravo, PlateLoc, PHERAstar (37 °C, Ex 485 / Em 528) | | Holding: MicroServe, 4 °C SteriStore, AmbiStore |

## Resource availability

**Lead contact.** As 4.1.

**Materials availability.** Three components must be built or sourced before
the first run and none exists today: the pRM/OR3* sfGFP reporter plasmid,
the CI(1–92)+GGSx5 cassette, and the ΔRecBCD extract. Budget weeks. The
extract decision (homemade versus commercial lysate plus GamS) must be taken
first, because the lot drives the buffer calibration.

**Data and code availability.** Plating position is randomised with **seed
20270401**, the same seed `express.cfps.doe` uses. Record it; never re-roll
between rounds or plates stop being comparable.

## Experimental model and subject details

No living organism and **no purified protein on either side**. Both partners
are translated from linear DNA in the same cell-free reaction that reads
them out. The expression system is an *E. coli* S30 extract from BL21
Rosetta 2 ΔRecBCD.

**Mechanism.** Lambda phage CI is a transcriptional activator that only
works as a dimer; its DNA-binding domain (residues 1–92) is monomeric and
inert alone. Fused to a bait and to a prey through a GGSx5 linker, an
interaction brings the two domains together, the pair binds the OR1 and OR2
operators of pRM, contacts σ, and fires sfGFP transcription. Binding becomes
green light.

**Pick the target format once per target, before any design batch:**

| | Format | When |
|---|---|---|
| 1 | CI–target + CI–binder | Default |
| 2 | Target fused to a multimerisation domain, CI on the binder only | When format 1 self-activates |
| 3 | Biotinylated target pre-mixed 1:1 with streptavidin at 150 nM, tetramer spiked in | Target hard to express, or best signal-to-noise wanted. Gave their best SNR — if a biotinylated ectodomain is a catalogue item for your target, start here |

## Method details

**Scale.** 36 designs per 384-well plate in triplicate, 4–8 h.

**Assembly plate, 96-well:** 72 wells for 36 designs × (+target, −target),
2 for the known binder pair ± target, 1 for CI–target alone, 1 for reporter
only, 1 for constitutive sfGFP. 78 used, 18 spare. Assemble at 22 µL; one
assembly well yields four 5 µL platings, so three replicates leaves dead
volume.

**On deck:**

1. **Dispense every DNA component first** — reporter plasmid at 5 nM final,
   CI-fusion fragments normalised to 50 nM, the streptavidin–target complex
   in format 3, and any competitor. ~3 min per plate on the Echo.
2. **Add the cold extract master mix.** The 96-channel head into 384 — four
   offset quadrant transfers and **32 min of the system bottleneck**. If this
   mix can be made acoustic it drops to three.
3. **Top up to volume** by bulk dispense. In the streptavidin format the
   pre-mixed biotinylated target goes in here at 150 nM.
4. **Seal with transparent film and hold** while expression and binding run
   in the same well, 4–8 h.
5. **Read sfGFP.** ~3 min per plate, converted to FITC mean-equivalent units.

**Order matters and it is doing real work.** Reactions are assembled on ice
in the published method. DNA tolerates ambient on the Echo deck; extract
does not. Dispensing all DNA first and adding the cold master mix last is
what makes an ambient-deck instrument sequence survivable at all.

**The remaining cold-chain risk is the MultiFlo reservoir**, where the
master mix sits at ambient for the length of the run. That — not the Echo,
not the Bravo — is what caps how many plates go in one batch, and it is
worth measuring on the first run rather than assuming.

**Timing.** Signal appears under 2 h and plateaus by 8 h. A full kinetic
read owns the PHERAstar for the day; a 4 h endpoint recovers most of the
discrimination.

## Quantification and statistical analysis

1. Convert raw RFU to **FITC mean-equivalent fluorescence** against the
   on-plate standard curve.
2. Subtract the reporter-only floor.
3. **Classify self-activators first.** Any design whose −target signal sits
   meaningfully above the floor is homodimerising or aggregating and its
   fold-activation is not interpretable. Record the self-association as a
   result — it is free data, and in the published screen it hit 1 of 36
   Mdm2 designs and 2 of 36 PD-L1 designs, both beta-rich.
4. **Fold-activation** = signal(+target) ÷ signal(−target), per design, at a
   fixed timepoint.
5. **Check the decoys.** Any decoy above threshold invalidates the plate; do
   not rescue individual wells.
6. **Rank. Do not fit.**

**Gate D4 — which designs bind?** Pass is **robust z ≥ 3.0 AND
fold-activation ≥ 2.0** in ≥2 of 3 replicates, with −target at floor and all
decoys silent. Fail is below both with −target at floor. Ambiguous is one
criterion but not the other, or 1 of 3 replicates, or an elevated −target,
or any decoy firing.

The reasoning behind that pair, fixed 2026-11-17 and recorded in
`protocols/bind.cf2h.screen.md`: the 2.0 fold is the paper's and on its own
is arbitrary in the same way a fixed BLI cutoff is arbitrary, because it
ignores how noisy the plate was. The **robust z across the plate's own fold
distribution** is what makes it noise-aware, and the AND of the two keeps
the training label clean. Recall is protected by routing ambiguous designs
to a dose-response rather than by loosening the pass line.

Pass → D5 orthogonal confirmation offline. Fail → logged as training data; a
measured negative is the point of keeping failures. Ambiguous → D5 as well,
except where a decoy fired or −target was elevated, which point at synthesis
error: re-synthesise the fragment and repeat.

**Gate D6 — did it bind the designed face?** Order 4–6 single-alanine
mutants at the designed interface residues per hit and run them identically
against the same target. In the paper, Δactivation against wild-type tracked
ΔΔG measured by SPR and ranked mutants correctly by affinity. A design whose
signal is unmoved by mutating its own designed hotspots did not bind where
it was designed to — answered on a plate reader.

## What this protocol does not tell you

- **A K_D.** It produces a rank.
- **Anything weaker than ~100 nM**, which is not reliably detected. This is
  a high-affinity filter.
- **Any discrimination among sub-nanomolar binders** — it saturates.
- Signal confounds affinity with expression, solubility and stability. The
  authors argue that is a feature for prioritisation, and it is — but the
  output must never be fitted as an affinity measurement.
- **Unsequenced DNA is this protocol's main false-negative source.** Several
  benchmark misses traced to systematic synthesis error rather than to the
  assay. A design that fails here once is a candidate for re-synthesis, not
  a dead design.

## Open items before the first run

Recorded in `protocols/bind.cf2h.screen.md`: the reporter plasmid and CI
cassette do not exist; the extract route is undecided; clear-seal
compatibility on the PlateLoc is unconfirmed; PHERAstar occupancy (8 h
kinetic versus 4 h endpoint) is undecided; whether the MultiFlo can hold a
cold master mix for a multi-plate batch is unmeasured; and whether the gel
check can be dropped after the first batch of a design set is open.
