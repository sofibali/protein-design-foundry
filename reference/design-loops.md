# Binder design tools — what exists, and what the publications claim

_Compiled 2026-11-23. A catalogue of published tools and their cited
capabilities. It recommends nothing._

The foundry screens designed binders. This file is the survey of the
computational tools that produce them — what each one does, what its
publication reports it achieved, how that was measured, and whether the code
is available and maintained.

**It makes no judgement about which tool this lab should use.** Where a
paper reports a number, the number is here as the paper states it. Where a
claim is computational only, it is marked as such. Nothing here is this
lab's own experience and no campaign data of any kind appears.

---

## Verification standard used throughout

Every DOI below was resolved **live against the Crossref REST API** on
2026-11-23 and returned the title, first author and year claimed here.
Identifiers Crossref could not confirm were re-resolved against **PubMed**
or the **arXiv API**, and the corrected identifier is what appears. Every
repository was queried through the **GitHub API** the same day for its
licence, its last push and whether it is archived; those are the figures in
§7, not claims from the papers.

Three consequences, which are findings rather than method:

1. **Every reported number in §2–§5 is quoted from the abstract of the
   primary source**, which was read directly. Where a figure exists only in
   a paper's body and the body was not accessible, this file says the
   abstract does not give it rather than reproducing a number second-hand.
2. **Tools surfaced by search, not by prior listing.** The starting point
   was a list of names; everything retained was independently found through
   PubMed, bioRxiv, Crossref, arXiv or web search and then verified at the
   primary source. §8 names what was dropped for failing that test.
3. **"Success rate" is not one quantity.** Each paper defines it
   differently — binding above a control threshold, nanomolar affinity,
   at least one hit per target. The definitions are given beside the
   numbers in §2.3 and the numbers are **not comparable across rows**.

---

## 1. Scope — the path before a sequence is ordered

| Stage | What it produces | §|
|---|---|---|
| **Generation** | a binder backbone, or backbone + sequence, against a target | §2 |
| **Sequence design** | an amino-acid sequence for a given backbone | §3 |
| **Structure prediction** | a predicted model of the design, alone and in complex | §4 |
| **Filtering and affinity estimation** | a shortlist, and a predicted strength | §5 |

Everything downstream of ordering — synthesis, expression, assay, gating —
is the deck's half and is documented in `reference/capabilities.md` and
`_data/gates.yml`.

---

## 2. Generation

### 2.1 General protein binders

| Tool | Approach | Code |
|---|---|---|
| **Rosetta, target structure alone** [1] | large-scale binding-mode search, then intensification | — |
| **RFdiffusion** [2] | RoseTTAFold fine-tuned as a backbone denoising diffusion model | open |
| **BindCraft** [3] | backpropagation through AlphaFold2 weights; no known site required | open |
| **AlphaProteo** [4] | generative family from Google DeepMind | **closed** |
| **BoltzDesign1** [5] | inverts Boltz-1; optimises on the distogram, no finetuning | open, **no licence file** |
| **BoltzGen** [6] | all-atom generative model; one model for design and folding | open |

### 2.2 Antibody, nanobody and macrocycle formats

| Tool | Format | Code |
|---|---|---|
| **RFantibody** [7] | VHH, scFv, full antibody; RFdiffusion fine-tuned, with yeast display | open |
| **Germinal** [8] | de novo CDRs onto a user-specified framework | open |
| **Chai-2** [9] | antibodies, nanobodies and miniproteins | **closed** |
| **RFpeptides** [10] | macrocyclic peptide binders | no repository found — §8 |

### 2.3 What each publication reports it achieved

Quoted from the abstract of each primary source. **Definitions differ, so
the rows do not compare.**

| Tool | Reported experimental outcome | n tested, as stated |
|---|---|---:|
| Rosetta, structure alone [1] | binders to **12 targets**, all < 65 aa, "nanomolar to picomolar affinities" *following experimental optimisation*; 5 crystal structures "closely match" the design models | "nearly half a million computational designs" |
| AF2/RoseTTAFold as a filter [11] | "increases design success rates **nearly 10-fold**" | not stated in abstract |
| RFdiffusion [2] | "hundreds of designed symmetric assemblies, metal-binding proteins and protein binders" characterised; cryo-EM of a designed binder–haemagglutinin complex "nearly identical to the design model" | **no per-target hit rate in the abstract** |
| BindCraft [3] | "experimental success rates of **10–100%**", nanomolar affinity "without the need for high-throughput screening or experimental optimization" | not stated in abstract |
| AlphaProteo [4] | "**3- to 300-fold** better binding affinities and higher experimental success rates than the best existing methods" | **7 target proteins** |
| RFantibody [7] | VHH binders to **4 disease-relevant epitopes**; cryo-EM confirms binding pose; initial designs "exhibit modest affinity (tens to hundreds of nanomolar K_d_)", single-digit nM only **after** OrthoRep affinity maturation | not stated in abstract |
| Germinal [8] | "functional antibodies across all targets and binder formats", nanomolar affinity | **43–101 designs per antigen**, 4 targets |
| Chai-2 [9] | "**16%** hit rate in fully de novo antibody design … over 100-fold improvement"; "at least one successful hit for **50% of targets**"; "**68%** wet-lab success rate in miniprotein design" | **≤ 20 designs** to each of **52 targets** |
| BoltzGen [6] | "eight diverse design campaigns with functional and affinity readouts" | **26 targets** |
| BoltzDesign1 [5] | "outstanding **in silico** success rates and diversity" — **computational only** | — |
| RFpeptides [10] | title claims "accurate de novo design of high-affinity protein-binding macrocycles"; abstract not retrieved for this audit | — |
| RFdiffusion, independent test [12] | 2 of 5 Strep-Tag II binders "outperformed streptavidin in Western blot assays", none matched the anti-tag antibody; binders to the other five targets "failed due to low expression, nonspecific binding, or undetectable affinity" | **5 designs each, 6 targets** |

**Three things this table says plainly.**

The highest reported rates come from the **smallest and most recent tests**
and from **closed models** — Chai-2's 16% and 68% are company-reported on a
preprint, and AlphaProteo's advantage is reported by its developers against
their own comparator set. The lowest reported rate [12] comes from an
**independent group testing five designs per target**, which is also the
smallest n in the table.

Several entries report affinity **after** an optimisation or maturation step
that is not part of the design method — [1] says "following experimental
optimization" and [7] reaches single-digit nM only through OrthoRep. The
as-designed affinity and the post-maturation affinity are different claims.

**n is small nearly everywhere.** The largest per-target number in the table
is 101 [8]; most are 5–32. The one large-n dataset in this file is the
meta-analysis at §5.2, and it is an aggregate of other people's campaigns.

---

## 3. Sequence design

| Tool | What it does | Reported result | Code |
|---|---|---|---|
| **ProteinMPNN** [13] | fixed-backbone sequence design | **52.4%** native sequence recovery vs **32.9%** for Rosetta; X-ray, cryo-EM and functional validation; rescued designs that Rosetta and AlphaFold had failed | open, MIT |
| **LigandMPNN** [14] | sequence design with small molecules, nucleotides and metals in context; outputs side-chain conformations | **>100** experimentally validated small-molecule and DNA-binding proteins, **4 X-ray structures**; redesign of Rosetta binders raised affinity "by as much as 100-fold" | open, MIT |

Sequence recovery, by contact type, as [14] reports it:

| Residues contacting | LigandMPNN | ProteinMPNN | Rosetta |
|---|---:|---:|---:|
| Small molecules | `63.3%` | `50.5%` | `50.4%` |
| Nucleotides | `50.5%` | `34.0%` | `35.2%` |
| Metals | `77.5%` | `40.6%` | `36.0%` |

Native-sequence recovery is a computational benchmark on backbones the model
did not design. The experimental validation in the same papers is the
separate claim.

---

## 4. Structure and complex prediction

These are not design tools. They are what a design is checked against, and
their published validation is against **experimental structures**, not
against design outcomes.

| Tool | Reported scope | Code and weights |
|---|---|---|
| **AlphaFold 2** [15] | "highly accurate" monomer structure prediction | open, Apache-2.0 |
| **AlphaFold 3** [16] | proteins, nucleic acids, small molecules, ions, modified residues; reports "far greater accuracy for protein–ligand interactions compared with state-of-the-art docking tools" and "substantially higher antibody–antigen prediction accuracy compared with AlphaFold-Multimer v2.3" | code Apache-2.0; **weights restricted — §7** |
| **Boltz-1** [17] | open reproduction of AlphaFold 3 | open, MIT |
| **Chai-1** [18] | open complex prediction | open, Apache-2.0 |
| **ESMFold** [19] | single-sequence folding, no MSA | open |

---

## 5. Filtering and affinity estimation

### 5.1 The metrics, and what they are

| Metric | What it is |
|---|---|
| **pLDDT** | per-residue confidence in the predicted monomer |
| **pAE / ipAE** | expected positional error between residue pairs, across the interface |
| **ipTM** | predicted TM-score of the interface |
| **ipSAE** [20] | interface-restricted recomputation of ipTM, proposed because ipTM is reported to be miscalibrated for small interfaces |
| **Rosetta ΔG/ΔSASA, shape complementarity** | physicochemical interface descriptors |

### 5.2 The one large-n test of these metrics

A 2025 meta-analysis re-predicted **3,766 experimentally tested binders
across 15 structurally diverse targets** with AF2 (initial guess and
ColabFold), AF3 and Boltz-1, extracting over 200 features per design [21].
What it reports:

| Finding, as stated | |
|---|---|
| AF3-derived **ipSAE** outperforms ipAE and ipTM | "a significant **1.4-fold** increase in average precision compared to ipAE" |
| Adding orthogonal physicochemical descriptors | "improves predictive performance" |
| Generalisation | "simple linear models trained on a small number of AF3-derived features generalize well across datasets" |
| Caveat the authors state | "overall performance varies by target" |

The dataset is released as a community resource [21]. **This is the only
entry in this file where a filtering metric has been tested against
experimental outcome at n in the thousands**, and it is the reason a
ranking claim is worth separating from a filtering claim: the paper
measures *average precision*, a prioritisation quantity, not a pass/fail
gate.

### 5.3 Affinity estimation

| Tool | Reported scope | Important limit |
|---|---|---|
| **Boltz-2** [22] | "first AI model to approach the performance of free-energy perturbation (FEP) methods in estimating **small molecule–protein** binding affinity", "at least 1000× more computationally efficient than FEP" | the affinity claim is **small molecule–protein**. The abstract makes no protein–protein affinity claim |

No tool found by this audit reports a validated **protein–protein** binding
affinity predictor. That is an absence established by search, not a tested
negative.

---

## 6. Evidence summary

Counting the 22 catalogued sources by what kind of validation each one
reports:

| Kind of validation reported | Count | Which |
|---|---:|---|
| **Experimental, with designs made and assayed** | `11` | Rosetta structure-alone [1], RFdiffusion [2], BindCraft [3], AlphaProteo [4], BoltzGen [6], RFantibody [7], Germinal [8], Chai-2 [9], AF2-as-filter [11], ProteinMPNN [13], LigandMPNN [14] |
| **Experimental, by independent group** | `2` | Jiang et al. [12], Overath et al. meta-analysis [21] |
| **Computational only** | `1` | BoltzDesign1 [5] |
| **Benchmarked against experimental structures**, not design outcomes | `5` | AlphaFold 2 [15], AlphaFold 3 [16], Boltz-1 [17], Chai-1 [18], ESMFold [19] |
| **Metric proposals**, validated computationally | `2` | ipSAE [20], Boltz-2 affinity head [22] |
| **Not retrieved for this audit** | `1` | RFpeptides [10] |

| | |
|---|---:|
| Tools whose own paper reports bench validation | **11 of 22** |
| Of those, validated by someone **other than** the developers | **0** |
| Independent evaluations found, of any tool | **2** |
| Peer-reviewed journal articles vs preprints and reports | **11 / 11** |
| Catalogued work with no public code or weights found | **3** — AlphaProteo [4], Chai-2 [9], RFpeptides [10] |

**The single most useful thing in this table is the second row.** Every
headline success rate in §2.3 was reported by the group that built the tool.
The two independent evaluations found [12][21] are both smaller in ambition
than the claims they bear on: one tests five designs per target, the other
re-scores other people's designs rather than making new ones.

---

## 7. Code, licence and maintenance

Queried through the GitHub API on 2026-11-23. "Last push" is the repository's
most recent commit to any branch, which is the only maintenance signal the
API gives directly.

| Tool | Repository | Licence | Last push |
|---|---|---|---|
| RFdiffusion | `RosettaCommons/RFdiffusion` | BSD, stated to cover code **and weights** | `2026-10-28` |
| RFdiffusion2 | `RosettaCommons/RFdiffusion2` | BSD-3-Clause | `2026-10-22` |
| RFantibody | `RosettaCommons/RFantibody` | custom — GitHub reports no standard SPDX id | `2026-11-19` |
| BindCraft | `martinpacesa/BindCraft` | MIT | `2026-09-21` |
| BoltzDesign1 | `yehlincho/BoltzDesign1` | **no licence file** | `2026-11-14` |
| BoltzGen | `HannesStark/boltzgen` | MIT | `2026-11-01` |
| Germinal | `SantiagoMille/germinal` | Apache-2.0 | `2026-04-24` |
| ProteinMPNN | `dauparas/ProteinMPNN` | MIT | `2024-08-14` |
| LigandMPNN | `dauparas/LigandMPNN` | MIT | `2025-02-06` |
| AlphaFold 3 | `google-deepmind/alphafold3` | Apache-2.0 code; **weights restricted** | `2026-11-19` |
| Boltz (1 and 2) | `jwohlwend/boltz` | MIT | `2026-05-29` |
| Chai-1 | `chaidiscovery/chai-lab` | Apache-2.0 | `2026-11-19` |
| AF2 binder pipeline | `nrbennet/dl_binder_design` | MIT | `2024-08-07` |
| ipSAE | `DunbrackLab/IPSAE` | MIT | `2026-01-03` |
| Binder-scoring dataset [21] | `DigBioLab/de_novo_binder_scoring` | MIT | `2026-04-30` |
| AlphaProteo | — | **no public code or weights found** | — |
| Chai-2 | — | **no public code or weights found** | — |
| RFpeptides | — | **no official repository found** — §8 | — |

None of the repositories above is archived. The Rosetta pipeline behind [1]
is distributed through RosettaCommons rather than as one of these
repositories and was not checked for this audit.

**Three licence facts worth having in one place.**

**AlphaFold 3's weights are the one hard restriction.** Per
`WEIGHTS_TERMS_OF_USE.md` in the repository (last modified 2024-11-09, read
live 2026-11-23): the parameters are free "for certain non-commercial uses",
available "**only** … for non-commercial use by, or on behalf of,
non-commercial organizations", must not be used "in connection with any
commercial activities, including research on behalf of commercial
organizations", must not be published or shared outside the organisation,
and their output must not be used "to train machine learning models …
for biomolecular structure prediction similar to AlphaFold 3". Output may
be published and adapted under separate terms.

**BoltzDesign1 carries no licence file.** The GitHub API returns no licence
for it. Absent one, default copyright applies.

**RFantibody's licence is non-standard.** GitHub reports no SPDX identifier
for it; the Institute for Protein Design's announcement describes the
software as shared for academic, personal and commercial use. The licence
file itself is what to read before relying on either statement.

---

## 8. What this audit did not confirm

Recorded so the next session does not spend the time again.

**RFD4-Proteina.** Named in a working document as a current Baker Lab /
NVIDIA scaffold generator. Its DOI resolves at Crossref, but **an
independent search did not surface it** — PubMed returns nothing, and a web
search for it returned no relevant result at all. It is therefore left out
of this catalogue rather than carried across on a single reference.

**RFpeptides' repository.** The paper is real and verified [10]. Searching
GitHub returns only third-party reimplementations and MCP wrappers, no
official repository; one project page states code "will be released upon
publication". Nothing is claimed here about the pipeline's availability.

**The field review at [23] could not be read.** `cell.com` returned HTTP 403.
Its metadata is verified through Crossref and it is listed as further
reading, but **no figure in this file comes from it**.

**Per-target hit rates from paper bodies.** Several papers report hit rates
in figures or supplementary tables rather than abstracts. Where the abstract
does not state a number, §2.3 says so instead of quoting a secondary
summary. A reader who needs those figures should read the papers directly.

**Two DOIs that circulate widely are wrong by one character**, found while
checking: RFdiffusion is `10.1038/s41586-023-06415-8`, **not** `-9`, and
AlphaFold 3 is `10.1038/s41586-024-07487-w`, **not** `-6`. Crossref returns
404 for both wrong forms; PubMed gave the correct ones. Neither wrong form
appears anywhere in this repository.

---

## 9. Sources

All resolved live 2026-11-23: Crossref first, PubMed or the arXiv API where
Crossref could not confirm.

| # | Citation | Identifier |
|---|---|---|
| 1 | Cao et al., *Nature* 2022 — Design of protein-binding proteins from the target structure alone | [10.1038/s41586-022-04654-9](https://doi.org/10.1038/s41586-022-04654-9) |
| 2 | Watson et al., *Nature* 2023 — De novo design of protein structure and function with RFdiffusion | [10.1038/s41586-023-06415-8](https://doi.org/10.1038/s41586-023-06415-8) |
| 3 | Pacesa et al., *Nature* 2025 — One-shot design of functional protein binders with BindCraft | [10.1038/s41586-025-09429-6](https://doi.org/10.1038/s41586-025-09429-6) |
| 4 | Google DeepMind, arXiv 2024 — De novo design of high-affinity protein binders with AlphaProteo. **Technical report, not peer reviewed** | [arXiv:2409.08022](https://arxiv.org/abs/2409.08022) |
| 5 | Cho et al., bioRxiv 2025 — BoltzDesign1: inverting all-atom structure prediction model for generalized biomolecular binder design. **Preprint; in-silico results only** | [10.1101/2025.04.06.647261](https://doi.org/10.1101/2025.04.06.647261) |
| 6 | Stark et al., bioRxiv 2025 — BoltzGen: toward universal binder design. **Preprint** | [10.1101/2025.11.20.689494](https://doi.org/10.1101/2025.11.20.689494) |
| 7 | Bennett et al., *Nature* 2025 — Atomically accurate de novo design of antibodies with RFdiffusion | [10.1038/s41586-025-09721-5](https://doi.org/10.1038/s41586-025-09721-5) |
| 8 | Mille-Fragoso et al., bioRxiv 2025 — Efficient generation of epitope-targeted de novo antibodies with Germinal. **Preprint** | [10.1101/2025.09.19.677421](https://doi.org/10.1101/2025.09.19.677421) |
| 9 | Chai Discovery Team, bioRxiv 2025 — Zero-shot antibody design in a 24-well plate. **Preprint; company-reported** | [10.1101/2025.07.05.663018](https://doi.org/10.1101/2025.07.05.663018) |
| 10 | Rettie et al., *Nature Chemical Biology* 2025 — Accurate de novo design of high-affinity protein-binding macrocycles using deep learning | [10.1038/s41589-025-01929-w](https://doi.org/10.1038/s41589-025-01929-w) |
| 11 | Bennett et al., *Nat Commun* 2023 — Improving de novo protein binder design with deep learning | [10.1038/s41467-023-38328-5](https://doi.org/10.1038/s41467-023-38328-5) |
| 12 | Jiang et al., bioRxiv 2025 — RFdiffusion exhibits low success rate in de novo design of functional protein binders for biochemical detection. **Preprint; independent of the tool's authors** | [10.1101/2025.02.07.636769](https://doi.org/10.1101/2025.02.07.636769) |
| 13 | Dauparas et al., *Science* 2022 — Robust deep learning-based protein sequence design using ProteinMPNN | [10.1126/science.add2187](https://doi.org/10.1126/science.add2187) |
| 14 | Dauparas et al., *Nature Methods* 2025 — Atomic context-conditioned protein sequence design using LigandMPNN | [10.1038/s41592-025-02626-1](https://doi.org/10.1038/s41592-025-02626-1) |
| 15 | Jumper et al., *Nature* 2021 — Highly accurate protein structure prediction with AlphaFold | [10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2) |
| 16 | Abramson et al., *Nature* 2024 — Accurate structure prediction of biomolecular interactions with AlphaFold 3 | [10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w) |
| 17 | Wohlwend et al., bioRxiv 2024 — Boltz-1: democratizing biomolecular interaction modeling. **Preprint** | [10.1101/2024.11.19.624167](https://doi.org/10.1101/2024.11.19.624167) |
| 18 | Chai Discovery, bioRxiv 2024 — Chai-1: decoding the molecular interactions of life. **Preprint** | [10.1101/2024.10.10.615955](https://doi.org/10.1101/2024.10.10.615955) |
| 19 | Lin et al., *Science* 2023 — Evolutionary-scale prediction of atomic-level protein structure with a language model | [10.1126/science.ade2574](https://doi.org/10.1126/science.ade2574) |
| 20 | Dunbrack, bioRxiv 2025 — *Res ipSAE loquuntur*: what's wrong with AlphaFold's ipTM. **Preprint** | [10.1101/2025.02.10.637595](https://doi.org/10.1101/2025.02.10.637595) |
| 21 | Overath et al., bioRxiv 2025 — Predicting experimental success in de novo binder design: a meta-analysis of 3,766 experimentally characterised binders. **Preprint** | [10.1101/2025.08.14.670059](https://doi.org/10.1101/2025.08.14.670059) |
| 22 | Passaro et al., bioRxiv 2025 — Boltz-2: towards accurate and efficient binding affinity prediction. **Preprint; affinity claims are small molecule–protein** | [10.1101/2025.06.14.659707](https://doi.org/10.1101/2025.06.14.659707) |
| 23 | Fox et al., *Structure* 2025 — Code to complex: AI-driven de novo binder design. **Further reading. Metadata verified; the article itself returned HTTP 403 and nothing in this file is drawn from it** | [10.1016/j.str.2025.08.007](https://doi.org/10.1016/j.str.2025.08.007) |

Also catalogued but outside binder design, and listed only because they
share the RFdiffusion lineage: **RFdiffusion2**, atom-level enzyme active
site scaffolding, Ahern et al., *Nature Methods* 2025,
[10.1038/s41592-025-02975-x](https://doi.org/10.1038/s41592-025-02975-x).
