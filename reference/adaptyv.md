# Adaptyv Bio — pipelines, read 2026-11-15

A cloud lab running design→data on submitted sequences. The closest
working analogue to what the foundry is building, and the parts worth
copying are marked **⇒**.

## The platform

Submit sequences via portal or API. Experiment types: Expression,
Expression Scale-Up (purified protein returned), Binding,
Thermostability (nanoDSF), Enzyme Activity. Turnaround quoted as 21
days in one place and 3–4 weeks in another, plus a separate "waiting
for materials, 5–10 days" stage.

## Expression

**Fully reconstituted PURE-type *E. coli* system** — ribosomes, tRNAs
and synthetases, transcription/translation factors, T7 RNAP,
nucleotides, amino acids, energy, **DsbC + oxidised/reduced
glutathione** for disulfides. Yeast cell-free offered as a fallback
when a design expresses poorly. CHO/mammalian in development.

**⇒ Template is full-length linear dsDNA ordered from an outside
vendor. No plasmid, no cloning.** PURE systems lack nucleases, so
linear DNA survives. Internal pipeline codon-optimises for cell-free
usage, mRNA secondary structure and synthesisability, adding 5′/3′
non-coding regions.

Protein within a few hours; max yield at 4–6 h; 2–3 h often enough for
screening. Typical yield 50–300 µg/mL for scFvs, 50–600 µg/mL for small
de novo proteins. Reaction volume, temperature and plate format are
**not stated**.

**Constraints:** ~8–700 aa. No intact IgG (Fc does not express) —
submit scFv or Fab. VHH most common. Non-canonical aa and cyclic
peptides need custom protocols. Risk factors they name for poor
expression: hydrophobic patches, mRNA secondary structure, repetitive
sequence, unusual composition, >50 kDa.

**⇒ Expression readout is split-GFP, not a gel.** A C-terminal
**split-GFP11 (RDHMVLHEYVNAAGIT) + Twin-Strep-tag**, joined by GGGS
linkers, is appended to every design. GFP1-10 reagent added in excess
after expression; RFU converted to concentration against a standard
curve (y = 130.1x + 261, R² = 0.994, linear 2.5–25 µM). The tag is not
cleaved before binding.

**⇒ They run no SDS-PAGE, SEC or A280 on designs at all.** Designs go
straight from the split-GFP number into the binding assay. This is the
precedent for skipping per-well purity: quantify, gate, proceed.

Claimed expression success >90%, thousands of proteins/month. "Success"
is not defined on the page. In the EGFR competition, <0.02 µg/mL was
the exclusion threshold, with 2–4 expression batches per sequence.

## Binding

**Gator Bio Pro for BLI; Carterra for SPR.** Design is the ligand,
captured on the tip through its Twin-Strep-tag; target flows as
analyte. Records wavelength shift at 5 Hz, fits 1:1, globally across
the concentration series.

Two modes: **screening** at 2 concentrations + zero blank, and
**affinity characterisation** at 4–7 (sources disagree) + blank.
Duplicate by default; the lab adds replicates when a first pass is
borderline. Competition conditions: 316.2 → 10 nM, PBS-T + 0.02% BSA,
25 °C, baseline-corrected, each replicate fitted independently.

**⇒ The classification scheme — this is the decision layer, in
production:**

| | |
|---|---|
| **True** | clear binder above controls |
| **False** | expresses, but at or below control signal |
| **Unknown** | no/low expression, or marginal signal |

Strength buckets: **Strong <50 nM · Medium 50 nM–1 µM · Weak >1 µM**.
Yield reported as **Low / Medium / High** (thresholds not published).
Usable KD range ~0.1 nM–10 µM, accuracy dropping at both ends.

**⇒ "Unknown" is a first-class outcome, separate from "False".** A
design that did not express is not a non-binder. This is exactly the
three-outcome rule in `gates.yml`, and they ship it.

## Controls

No positive control needed for expression (internal calibration). For
binding, a positive control is *recommended and supplied by the
customer*, flagged with a `Control` boolean in the CSV — and **it
counts against your sequence minimum**. For new targets they hold no
validated control binder, so a feasibility step may be required.
Zero-concentration blank on every run.

## Order rules worth knowing

24 sequences minimum per target for binding; 20 for expression,
thermostability, epitope binning; 30 for enzyme activity. Above 384,
custom quote. **Design total must be ≤90 or ≥120 to fit controls on a
plate.** Pricing disagrees across pages: "from $99/protein" header vs
"$169/sequence" in the configurator. 20% discount for publishing
results on Proteinbase.

## Data package

`kinetics/` PNG sensorgrams per sample+replicate · `raw_data/` CSVs
`<name>_<replicate>_<conc>.csv` with `t` (s) and `y` (nm) · `fit_data/`
modelled traces for approved fits · `aux/replicate_info.csv` with
`name, replicate, method, MAE, rel_MAE, rmax_estimate`.

**⇒ `rel_MAE` (fit error ÷ max signal) is a clean machine-readable fit
quality flag** — worth copying into D5.

## EGFR competition

Metrics: `PAE_interaction` (ColabFold, 2 models, 5 recycles, no
templates, top model's PAE averaged over target–binder pairs),
`pLDDT` (binder chain only), `similarity_check` (identity × coverage vs
SwissProt, THPdb, USPTO, Cao 2022), expression, and BLI KD/kon/koff.
**Only designs >10 aa from any known binder counted** — a novelty gate
worth adopting. Data ODbL, code Apache 2.0.

## Four things to take

1. **Linear dsDNA straight into PURE** — removes assembly,
   transformation and the colony-picker problem from the screening arm.
2. **Split-GFP11 + Twin-Strep as a standing construct tag** — one
   readout gives expression quantification and capture chemistry.
3. **True / False / Unknown, never binary** — and yield as a band, not
   a number.
4. **Novelty distance as a scored gate** on every design set.

## Not yet read

`/wiki/technologies/construct-tag-design` (full tag sequence),
`/wiki/methods/bli-methods`, SPR and nanoDSF pages, the API reference,
and the competition results CSVs themselves.
