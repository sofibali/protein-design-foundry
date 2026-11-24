# Consolidated first-pass inventory

_Compiled 2026-11-23 from the fifteen STAR Methods documents in this
directory, which in turn derive from `_data/protocols.yml` (`workflows:`),
`protocols/*.md` and `reference/*.md`._

**What this is.** The union of every Key Resources Table in this directory,
deduplicated, with the protocols that need each item. Its job is to make the
**shape** of the reagent need visible before anyone prices anything, so
completeness of the list matters more than precision about any one line.

**What this deliberately is not.**

- **No catalogue numbers.** A guessed part number is worse than a blank.
  Where a vendor appears it is because the method determines it, not because
  a part was chosen.
- **No prices, no quotes, no currency figures of any kind.** This
  repository is public. Anything that acquires a price belongs in
  `protein-design-foundry-internal`.
- **No quantities**, except where a protocol states one (plates per round,
  wells per plate, control well counts). Per-run consumption cannot be
  derived without a campaign size, and inventing one would make the list
  look more settled than it is.
- **No instruments.** The device set lives in `_data/protocols.yml` under
  `racs:` and is a different list with a different owner. Instrument
  *consumables* — tips, cassettes, seals — are here; the instruments
  themselves are not.

**Marks.** **[inferred]** — not stated in the repository; derived from the
instrument a step runs on, from the plate format, or from a named reagent's
requirements. **[to build]** — does not exist yet and must be made or
sourced before its protocol can run. **[⚠]** — carries a flagged
inconsistency; see the note at the end.

**Totals.** 95 distinct items across 12 groups. 32 rows carry an
**[inferred]** mark for at least one of the protocols that needs them —
several items are stated in one protocol and inferred in another, and the
mark is applied per protocol rather than per item. 3 rows are marked **[to
build]**, all three of them CF2H's.

---

## 1. Strains, extracts and expression systems

| Item | Needed by | Notes |
|---|---|---|
| *E. coli* BL21(DE3), chemically competent | 4.4, 4.14 | Chemically competent is sufficient; no colony is picked either way |
| *E. coli*, electrocompetent **[⚠]** | 4.2 | The `inputs:` block says electrocompetent; the transformation step describes an on-deck heat shock. One of the two is wrong |
| *E. coli* BL21 Rosetta 2 ΔRecBCD, homemade S30 extract **[to build]** | CF2H | The RecBCD deletion is what lets linear DNA survive, so no GamS is needed in any reaction |
| Lysate-based cell-free expression kit, **two lots** | 4.3, 4.13, CF2H (fallback) | Lot is a factor in the 4.3 design matrix, not a constant — two lots are a requirement, not a convenience |
| PURE reconstituted cell-free system | 4.3, 4.13 | The alternative to lysate. Linear template needs no GamS in PURE |

## 2. Media, antibiotics and agar

| Item | Needed by | Notes |
|---|---|---|
| ZYM-5052 autoinduction medium | 4.4 | Studier 2005 formulation. Avoids timed IPTG, which is what makes an unattended overnight possible |
| SOC or recovery medium | 4.2, 4.14 | Bulk-dispensed immediately after the pulse |
| Outgrowth medium **[inferred]** | 4.2, 4.14 | An outgrowth follows recovery in both; the medium is not named |
| Kanamycin | 4.2 **[inferred]**, 4.4 | Named by marker, not by concentration. Studier 2005 specifies 100 µg/mL rather than 30 in high-phosphate media |
| Selection antibiotic, backbone-dependent **[inferred]** | 4.14 | For the agar plates and outgrowth; no agent or concentration stated |
| Agar plates | 4.14 | Plating is in scope for titre and QC only — nothing picks a colony |

## 3. Enzymes, polymerases and kits

| Item | Needed by | Notes |
|---|---|---|
| BsaI-HFv2 | 4.2, 4.13 | New England Biolabs. Ships in glycerol, so it moves by positive-displacement channel and never acoustically |
| T4 DNA ligase | 4.2, 4.13 | Same glycerol constraint |
| Platinum SuperFi II 2× PCR master mix | 4.13 | Thermo Fisher — the source paper's choice, 30 µL / 30 cycles |
| High-fidelity PCR polymerase or master mix, unspecified **[inferred for 4.2]** | 4.2, CF2H | CF2H states one is required; 4.2 specifies a PCR without naming the enzyme |
| SPRI paramagnetic beads | 4.2, 4.13, CF2H | The only size selection the deck has. 0.8× for size selection, 1.8× for cleanup |
| Detergent-based lysis reagent, plate-compatible | 4.4 | There is no sonicator on the deck, so lysis is chemical |
| GamS | 4.3 (linear template in lysate), CF2H (commercial-lysate fallback only) | Not needed with a ΔRecBCD extract, which is the point of building one |

## 4. Affinity resins and capture reagents

| Item | Needed by | Notes |
|---|---|---|
| MagStrep Strep-Tactin XT magnetic beads | 4.5 | IBA Lifesciences. Magnetic 6% agarose, binds Twin-Strep, 96-well compatible |
| Chelator-tolerant IMAC magnetic bead (PureCube Ni-INDIGO or Pierce High-Capacity Ni-IMAC) | 4.5 | His route only. Tolerates 20 mM EDTA/DTT — plain Ni-NTA strips in a cell-free reaction |
| Streptavidin | CF2H | Format 3 only: pre-mixed 1:1 with biotinylated target at 150 nM |

## 5. Buffers, salts and solvents

| Item | Needed by | Notes |
|---|---|---|
| Magnesium glutamate | 4.3, CF2H | A 4.3 factor at 8 and 16 mM. CF2H's published optimum is 15 mM — re-derive per extract lot, do not inherit |
| Potassium glutamate | 4.3, CF2H | A 4.3 factor at 80 and 180 mM. CF2H's optimum is 100 mM |
| Cell-free energy solution | 4.3 | A factor at 1× and 1.5× |
| Buffer BXT, biotin elution | 4.5 | IBA. Mild, but it poisons any downstream streptavidin step — buffer-exchange after it or use a His tag |
| Imidazole elution buffer **[inferred]** | 4.5 | Implied by the IMAC route; no composition stated |
| Bead wash buffer **[inferred]** | 4.5 | Wash steps are specified; the buffer is not. Determined by the bead chemistry |
| Assay buffer, format-dependent **[inferred]** | 4.7, 4.8, 4.9, 4.10, 4.12 | None is named anywhere in the repository for any of the four binding formats |
| Backfill solution to constant volume **[inferred]** | 4.9 | Assay buffer in the ordinary case |
| Nuclease-free water | 4.1, 4.13 **[inferred]** | Resuspension at the vendor's stated concentration; elution and backfill |
| DMSO, as the compound-stock solvent | 4.11, 4.12 | The reason both protocols need an Echo 6XX: the 525 cannot transfer DMSO |

## 6. Detection reagents, dyes and labels

| Item | Needed by | Notes |
|---|---|---|
| GFP1-10 complementation reagent | 4.3, 4.6 | Added in excess after expression, ~30 min to complement |
| GFP11 standard protein | 4.3, 4.6 **[inferred]** | 8 points in duplicate, carried on every plate, so RFU converts to µg/mL |
| LgBiT protein | 4.6, 4.7 **[inferred]** | The HiBiT/NanoBiT route |
| SmBiT peptide or SmBiT fusion partner **[inferred]** | 4.7 | Implied by the NanoBiT format; the repository names only the substrate |
| Furimazine substrate | 4.6, 4.7 | Promega. The luminescent read is ~3 min a plate against ~8 for TR-FRET |
| Terbium or europium cryptate anti-tag donor antibody | 4.7, and 4.8–4.10 / 4.12 via the shared spine | The tag on the target must match the donor — a construct-design constraint set at order time |
| d2 or equivalent acceptor conjugate | 4.7, and 4.8–4.10 / 4.12 via the shared spine | Ratiometric 665/620 |
| AlphaScreen donor and acceptor bead pair | 4.7, and 4.8–4.10 / 4.12 via the shared spine | The most sensitive of the four formats, but bead-dependent and shows a hook effect |
| Fluorescently labelled tracer peptide, FP format | 4.7, and 4.8–4.10 / 4.12 via the shared spine | Needs a ~10× mass ratio, so peptides and small molecules only |
| FP tracer for the aggregation flag — fluorescein or TAMRA | 4.6 | Listed separately from the FP binding tracer because it is used as an aggregation readout, not a binding one |
| dsDNA-binding dye + DNA standard | CF2H | Quantification of each fragment before normalisation to 50 nM |
| FITC standard | CF2H | 16 wells, 8 points in duplicate, pipetted directly and never assembled. Converts RFU to mean-equivalent units so numbers survive a change of reader |

## 7. Nucleic acids, constructs and libraries

| Item | Needed by | Notes |
|---|---|---|
| Gene fragments, linear dsDNA, one per design (~300 bp–1.5 kb) | 4.1, 4.13, CF2H | IDT eBlocks at 10 ng/µL or Twist Gene Fragments at 0.5 ng/µL, delivered plated |
| Oligo pool, 20–350 nt | 4.2 | Coding budget ~75 aa. Subpool adapters split one order into several libraries |
| Subpool retrieval primers **[inferred]** | 4.2 | A subpool PCR is specified; the primers are not named |
| Linearised backbone, low copy, Kan | 4.2 | Kan because ampicillin satellites over a long unattended outgrowth |
| Circularising CFPS vector, pALiCE01-derived | 4.13 | Carries an FP fusion, a protease site and an affinity tag; closes on itself in the Golden Gate |
| Expression plasmid, pET29b backbone | 4.4 | Kan, because this incubates unattended overnight |
| Assembled DNA — Golden Gate product or plasmid | 4.14 | Held at 4 °C. Supports the pET21b/29b/22b/28a and pSB4k5 backbones in `reference/constructs.md` |
| Template DNA, linear dsDNA **and** plasmid forms | 4.3 | Template form is a factor in the design matrix, so both are required |
| pRM / OR3* sfGFP reporter plasmid **[to build]** | CF2H | Low copy — a high-copy reporter titrates CI. 5 nM final |
| CI(1–92) + GGSx5 cassette **[to build]** | CF2H | Ordered as one eBlock, ~700 bp with a 200 bp insert. CI(1–76) does not work; the linker is not optional |
| Compound library plates in DMSO | 4.11, 4.12 | Held as source plates in ambient storage between runs. No library is named |
| Commercial sparse-matrix crystallisation screens | 4.11 | Standard kits, loaded as Echo source plates |

## 8. Proteins, targets and on-plate controls

| Item | Needed by | Notes |
|---|---|---|
| Designed protein, purified | 4.7, 4.8, 4.9, 4.10, 4.12 | Crude cell-free is enough for NanoBiT only; the other three formats need protein in hand |
| Target protein, tagged to match the donor | 4.7, 4.8, 4.9, 4.10, 4.12 | |
| Purified protein at ≥10 mg/mL | 4.11 | From offline expression. Bead purification cannot reach this |
| Biotinylated target protein | CF2H | Format 3 only |
| Multimerisation-domain fusion — p53 tetramerisation domain or a hexameric coiled-coil | CF2H | Format 2 only. A GCN4 homodimer gave nothing: valency above two is the requirement |
| Counter-target homolog | 4.8 | Mac1 against MD1 in the worked example |
| Hotspot point-mutant of the designed target | 4.8 | One extra construct per target. The only control of the three that catches a wrong-face binder |
| Non-binder control design, unrelated target | 4.8 | |
| Decoy designs, 4–6 per plate | CF2H | The only on-plate evidence the screen is specific. Any decoy above threshold invalidates the plate |
| Single-alanine interface mutants, 4–6 per hit | CF2H (gate D6), 4.8 by analogy | Δactivation against wild-type tracked ΔΔG by SPR in the published work |
| Known binder pair, ± target | CF2H | The positive PPI control |
| Positive-control expression construct | 4.3 | 8 wells on every plate, carried forever, so plate-to-plate drift stays visible |
| Monomer control protein | 4.6 | The aggregation flag is a polarisation rise *against* this control |
| Standard-curve protein for the concentration read **[inferred]** | 4.6 | The GFP11 standard where the split-GFP route is used |
| Competitor / titrant | 4.8, 4.9 | One source plate; the whole series is built acoustically in the destination |
| Known site ligand, orthogonal site test | CF2H, 4.8 **[inferred]** | Only displaces a binder it substantially out-competes — check the affinity gap first |

## 9. Plates and plasticware

| Item | Needed by | Notes |
|---|---|---|
| Echo-qualified acoustic source plate, 384-well | 4.1 **[inf]**, 4.2 **[inf]**, 4.3, 4.7 **[inf]**, 4.8, 4.9, 4.10 **[inf]**, 4.11 **[inf]**, 4.12 **[inf]**, 4.13 **[inf]**, 4.14 **[inf]**, CF2H | Stated outright in only three protocols, required by eleven. The most widely needed single consumable in the set |
| 384-well destination / template plate | 4.1 | The stated output of 4.1 |
| 96-well PCR plate | 4.2 **[inf]**, 4.3 (×4 per round), 4.10 (×3), 4.13, CF2H (assembly, 22 µL) | The 96 block takes 10–100 µL |
| 384-well PCR plate | 4.2 **[inf]**, 4.3, 4.10 (×1), 4.13 (Armadillo) | The 384 block takes 5–20 µL — Golden Gate at 30 µL does not fit it |
| 96-well deep-well culture block | 4.4, 4.2 **[inferred]** | Fourteen deep-well Cytomat positions is the cap on everything that grows |
| 384-well assay plate | 4.6 **[inf]**, 4.7, 4.9, 4.10 | |
| 1536-well assay plate | 4.7, 4.12 **[inferred format]** | Reachable because the Echo builds the plate; 1536 costs the same deck time as 96 |
| 384-well black-wall / clear-bottom, low-binding | CF2H | 234 reaction wells + 16 FITC standard wells = 250 of 384 |
| UV-transparent microplate | 4.6 | A260/A280 for nucleic-acid carryover |
| 96-well plate compatible with the deck magnet **[inferred]** | 4.5 | |
| Elution plate **[inferred]** | 4.5 | |
| 96-well plate rated for the 4 °C and 42 °C deck nests **[inferred]** | 4.14 | It sits on a cold nest and is moved to a hot one |
| SwissCI sitting-drop crystallisation plate | 4.11 | Echo-addressable |
| Plate lids | 4.1 **[inf]**, 4.11, 4.14 | For crystallisation trays a **lid and never a seal**: both sealers are thermal and a 200 nL drop has no thermal mass to survive either |

## 10. Seals and films

| Item | Needed by | Notes |
|---|---|---|
| Thermal foil seal | 4.2 **[inf]**, 4.3 (×4 per round), 4.7, 4.9, 4.10 (×4), 4.12, 4.13 **[inf]** | Applied on the PlateLoc at 30–200 °C |
| Gas-permeable (breathable) membrane seal | 4.4, 4.2 **[inferred]** | Carried on the second sealer so both seal types stay resident without a manual roll change. A foil seal would take a 20 h deep-well culture anaerobic |
| Transparent adhesive film seal | CF2H | Not foil — the plate is read through it. **PlateLoc compatibility is unconfirmed** and is an open item before the first run |
| XPeel peel-off tape or waste consumable **[inferred]** | 4.3, 4.10 | A peeler is in both chains at up to 200 seals an hour; its own consumable is not named anywhere |

## 11. Tips and dispenser consumables

| Item | Needed by | Notes |
|---|---|---|
| Bravo 96-channel pipette tips | 4.2 **[inf]**, 4.5 **[inf]**, 4.13 **[inf]**, 4.14 **[inf]**, CF2H | Every SPRI cleanup, every bead wash, and CF2H's four offset quadrant transfers |
| Positive-displacement tips for the Cavro Magni Flex **[inferred]** | 4.2, 4.13 | The glycerol-based enzyme mixes, delivered from the tube |
| Lynx pipette tips **[inferred]** | 4.6 | The volume-verified normalisation pass |
| MultiFlo dispense cassette, including the 1 µL cassette | 4.3, 4.4 **[inf]**, 4.6 **[inf]**, 4.14, CF2H **[inf]** | The 1 µL cassette is named in 4.14 and covers anything down to 1 µL a well |
| Bench pipette tips, offline | 4.1, 4.3 | For the off-deck resuspension and the protocol's own stated consumables line |

## 12. Software and design tools

| Item | Needed by | Notes |
|---|---|---|
| NEBridge GetSet overhang-set selection | 4.2 | The repository is explicit: the overhang set comes from GetSet, "not from intuition" |

---

## What this list makes visible

**Eleven of fifteen protocols need an Echo-qualified source plate** and only
three say so. If one line item in this inventory is wrong by a factor of
ten, it is that one.

**Four binding protocols share one reagent set.** 4.8, 4.9, 4.10 and 4.12 all
run 4.7's spine with one thing added — three control columns, a titrant, a
heat step, a compound plate. The detection reagents are therefore bought
once for five protocols, not five times, and the format choice made in 4.7
determines the purchase for all of them.

**No assay buffer is named anywhere.** Four homogeneous formats, five
protocols, and the repository names no buffer for any of them. This is the
largest genuine gap in the list rather than an oversight in this document.

**Two items do not exist yet** — the pRM/OR3* reporter plasmid and the
CI(1–92)+GGSx5 cassette — and a third, the ΔRecBCD extract, must be made or
substituted. All three are CF2H's, all three are offline builds, and the
protocol cannot run until they exist.

**Two protocols are gated on an instrument that is not quoted.** 4.11 and
4.12 both need the Echo 6XX rather than the 525, for DMSO and for 1536.
Every compound and crystallisation line in this inventory is contingent on
that.

## Flagged inconsistency

**4.2 — electrocompetent cells against an on-deck heat shock.** The
`inputs:` block specifies electrocompetent *E. coli*; the transformation
step specifies the pulse as a plate move between the Bravo's two
temperature-controlled nests, which is heat shock and does not work on
electrocompetent cells. Both readings are carried in `4.2.md` rather than
one being silently chosen. Whichever is right changes the cell line item in
group 1 and may add an electroporation consumable that is not currently in
this list.
