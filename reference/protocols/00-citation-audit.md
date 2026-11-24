# Citation audit — the fifteen sample protocols

_Compiled 2026-11-23. Covers every entry under `workflows:` in
`_data/protocols.yml` (ids 4.1–4.14 and CF2H), as rendered at
`pages/workflows.html`._

Companion documents: one STAR Methods file per protocol in this directory
(`4.1.md` … `CF2H.md`), and the consolidated first-pass inventory in
`99-inventory.md`.

---

## Verification standard used throughout

Every DOI asserted below was resolved **live against the Crossref REST API**
on 2026-11-23 and confirmed to return the title, first author and journal
claimed here. PMC and PubMed identifiers were resolved live against the NCBI
ID converter. Nothing in this file is cited from memory.

Three things follow from that standard and are worth stating, because they
are the findings rather than the method:

1. **A citation is only asserted where the repository already names a
   method, a paper, a medium or a branded reagent that _is_ a published
   method.** Where a protocol is ordinary bench practice, this file says so
   instead of attaching a plausible-looking paper to it. Reaching for a
   reference that nobody actually worked from is the failure mode this audit
   exists to avoid, not a gap in it.
2. **Protocol source and component source are kept apart.** "Autoinduction
   medium ZYM-5052 is Studier 2005" is a statement about one reagent in 4.4;
   it is not a statement that 4.4 as a whole derives from that paper. The
   two are in separate columns below and should stay separate anywhere they
   are rendered.
3. **Candidate sources are labelled as candidates.** Where a protocol cites
   nothing but a canonical published origin exists and would be defensible
   to adopt, it is listed as a candidate and marked as not currently cited
   by the repository. Adopting one is an editorial decision for whoever owns
   `workflows:`, not something this audit has already done.

---

## Headline finding

`_data/protocols.yml` contains **no DOI, no PMID and no author name** — a
grep for `doi`, `pmid`, `biorxiv`, `et al` and a bare DOI prefix across the
whole file returns one incidental line about a flow sensor. Every citation
that exists for these protocols lives somewhere else in the repository:
`protocols/bind.cf2h.screen.md`, `reference/fida-pipeline.md` and
`reference/capabilities.md`.

| | Count |
|---|---|
| Protocols deriving from a specific published method, **cited somewhere in the repo** | **2** (4.13, CF2H) |
| Protocols deriving from a specific published method, **not cited anywhere** | **0** |
| Protocols whose **core method is ordinary bench practice** with a canonical published origin that could be cited | **3** (4.4, 4.11, 4.14) |
| Protocols that are **standard practice, vendor method or this facility's own design**, with no single source to cite | **10** |
| **Total** | **15** |

So the honest summary is: two protocols have a paper behind them, thirteen
do not, and of those thirteen only three have a canonical origin that it
would even make sense to cite. The remaining ten are either this deck's own
arrangement of standard operations or a vendor's method.

---

## Errata found during the audit

**1. The CF2H paper's first author is wrong in two public files.**
`protocols/bind.cf2h.screen.md` and `reference/capabilities.md` both
attribute DOI `10.1038/s41467-026-69741-1` to *"Delauriere et al."*
Crossref returns the author list **Capin, Mayonove, DeVisch, Becher, Ngo,
Courbet** for that DOI. The DOI itself, the journal (*Nature
Communications*), the year (2026) and the PMC identifier (PMC13103306,
PMID 41807394) in those files are all correct — only the name is wrong.
`notes/binder_literature_record.md` in the private repository already has it
as **Capin et al.**, so the two repositories currently disagree. This is a
one-word fix in each file; it has deliberately **not** been made here,
because both files belong to other lanes.

**2. The 4.13 citation is two files away from the protocol.** The
`workflows:` entry for 4.13 ends "From reference/fida-pipeline.md" and that
file carries the full citation and DOI. A reader on the workflows page has
no way to reach it. This is the strongest case in the set for a `refs:`
field (see the proposal at the end of this file).

---

## Per-protocol findings

### 4.1 — Build a clonal array

| | |
|---|---|
| **Repo states a source** | No |
| **Verdict** | **No published source.** Vendor resuspension instructions plus this facility's own acoustic normalisation step. |

Resuspending plated gene fragments at the vendor's stated concentration is a
vendor instruction (IDT eBlocks, Twist Gene Fragments), not a method from the
literature, and the repo quotes the vendor concentrations directly. The one
non-trivial idea here — normalising by transferred mass on an acoustic
dispenser rather than by volume — is a deck design decision.

*Candidate component source, not currently cited:* acoustic droplet ejection
as a transfer mechanism, Ellson et al., *JALA* 2003,
[10.1016/s1535-5535(03)00011-x](https://doi.org/10.1016/s1535-5535(03)00011-x)
— "Transfer of Low Nanoliter Volumes between Microplates Using Focused
Acoustics" (verified; note that Crossref holds two DOI variants for this
article, `…(03)00011-x` and `…-03-00011-x`, both resolving to the same
paper).

### 4.2 — Build a pooled library

| | |
|---|---|
| **Repo states a source** | No |
| **Verdict** | **No single source.** A composite of four published components and one architectural choice that is standard in the display literature. |

The architecture — amplify a subpool, size-select, Type IIS assembly into a
linearised backbone, transform, outgrow as a pool and never plate — is the
ordinary pooled-library route, not one lab's protocol.

Component sources, all verified, none currently cited:

| Component as named in the repo | Published source |
|---|---|
| Type IIS digestion–ligation ("Golden Gate") | Engler, Kandzia & Marillonnet, *PLoS ONE* 2008, [10.1371/journal.pone.0003647](https://doi.org/10.1371/journal.pone.0003647) |
| "overhang set from NEBridge GetSet, not from intuition" | Potapov et al., *ACS Synth Biol* 2018, [10.1021/acssynbio.8b00333](https://doi.org/10.1021/acssynbio.8b00333) — the four-base overhang ligation-fidelity profiling the GetSet tool is built on |
| SPRI beads | DeAngelis, Wang & Hawkins, *Nucleic Acids Res* 1995, [10.1093/nar/23.22.4742](https://doi.org/10.1093/nar/23.22.4742) |
| "0.8× drops anything under ~200 bp" | ratio-based SPRI size selection as characterised by Rohland & Reich, *Genome Res* 2012, [10.1101/gr.128124.111](https://doi.org/10.1101/gr.128124.111) |

The private repository's `notes/binder_literature_record.md` §1.1 holds the
pooled-display archetype papers (Chevalier 2017, Cao 2022) that this
protocol's shape comes from. They are context for the route, not a method
source for these steps, and are not asserted here as 4.2's citation.

### 4.3 — Cell-free expression, arrayed

| | |
|---|---|
| **Repo states a source** | No — `protocols/express.cfps.doe.md` states **"Evidence: none yet"** explicitly, and says the factor levels are "literature starting ranges for lysate-based CFPS — confirm against your kit's recommendation before the first run" without naming which literature. |
| **Verdict** | **This facility's own design of experiments**, run on a standard lysate or PURE cell-free platform. |

The 2^(6−2) resolution IV matrix, the use of four independently programmed
cycler blocks as four temperature arms, and the randomisation seed are all
this facility's. They are not from a paper and the repo does not claim they
are.

*Candidate component sources, not currently cited:*

- The split-GFP readout the protocol specifies (GFP1-10 reagent plus a
  GFP11 tag, read against a standard curve): Cabantous, Terwilliger & Waldo,
  *Nat Biotechnol* 2005, [10.1038/nbt1044](https://doi.org/10.1038/nbt1044).
- The Mg-glutamate / K-glutamate factor bracket the matrix scans is the
  standard bracket for *E. coli* lysate TX-TL: Sun et al., *J Vis Exp* 2013,
  [10.3791/50762](https://doi.org/10.3791/50762) — "Protocols for
  Implementing an *Escherichia coli* Based TX-TL Cell-Free Expression
  System". This is offered as the obvious thing to cite **if** the levels are
  ever traced to a source; nobody has yet said they came from here.

### 4.4 — *E. coli* expression, arrayed

| | |
|---|---|
| **Repo states a source** | No, but it names **ZYM-5052**, which is a published medium rather than a catalogue item. |
| **Verdict** | **Standard practice with one canonical published component.** |

Autoinduction in ZYM-5052 is Studier, *Protein Expr Purif* 2005,
[10.1016/j.pep.2005.01.016](https://doi.org/10.1016/j.pep.2005.01.016) —
"Protein production by auto-induction in high-density shaking cultures"
(verified). Naming ZYM-5052 without that citation is the single clearest
case in the set of the repo using a published method by name and not saying
so.

Everything else in 4.4 — deep-well block culture, a gas-permeable seal,
overnight shaking incubation, plate centrifugation, detergent lysis — is
ordinary arrayed-expression bench practice with no single canonical source,
and the detergent lysis reagent is a vendor product chosen because there is
no sonicator on the deck.

Two warnings from Studier that the repo does not currently carry, and that
matter for a protocol that runs unattended overnight on a Kan backbone:
kanamycin is used at 100 µg/mL rather than 30 in high-phosphate media, and
high aeration inhibits induction at low lactose. Both are recorded in the
private repository's literature record.

### 4.5 — Magnetic bead purification

| | |
|---|---|
| **Repo states a source** | No. It names the bead chemistry and the elution buffer by product name. |
| **Verdict** | **Vendor method**, over a published affinity-tag system. |

The protocol as written is the bead manufacturer's binding/wash/elution
cycle (IBA MagStrep Strep-Tactin XT with Buffer BXT; or a chelator-tolerant
IMAC bead for His-tagged constructs). The tag system behind it is published:

- Strep-tag / Strep-Tactin: Schmidt & Skerra, *Nat Protoc* 2007,
  [10.1038/nprot.2007.209](https://doi.org/10.1038/nprot.2007.209).
- Twin-Strep specifically, which is the tag the repo's constructs carry:
  Schmidt et al., *Protein Expr Purif* 2013,
  [10.1016/j.pep.2013.08.021](https://doi.org/10.1016/j.pep.2013.08.021).

Both verified. Neither is cited in the repo.

### 4.6 — Protein QC without a gel

| | |
|---|---|
| **Repo states a source** | No |
| **Verdict** | **This facility's own combination** of three published or standard readouts, assembled to avoid a gel. |

The idea being tested — that concentration, nucleic-acid carryover and
aggregation can be answered on one plate reader, and that band identity
simply cannot — is the foundry's. The three readouts are not:

| Readout | Source |
|---|---|
| Concentration by split-GFP complementation | Cabantous, Terwilliger & Waldo, *Nat Biotechnol* 2005, [10.1038/nbt1044](https://doi.org/10.1038/nbt1044) |
| Concentration by HiBiT, the stated alternative | Schwinn et al., *ACS Chem Biol* 2018, [10.1021/acschembio.7b00549](https://doi.org/10.1021/acschembio.7b00549) (issued online 2017-09-11) |
| A260/A280 for nucleic-acid carryover | Standard spectrophotometry. No canonical source, and none should be invented for it. |
| Aggregation by fluorescence polarisation of a tracer | Fluorescence polarisation in a screening format is reviewed by Lea & Simeonov, *Expert Opin Drug Discov* 2011, [10.1517/17460441.2011.537322](https://doi.org/10.1517/17460441.2011.537322). Using a polarisation rise against a monomer control specifically as an **aggregation flag** is this facility's own use of it, and the repo is already careful to say it detects aggregation rather than a change of oligomer state. |

### 4.7 — Binding, the assay ladder

| | |
|---|---|
| **Repo states a source** | No |
| **Verdict** | **This facility's own ladder** over four established homogeneous assay formats. |

The ladder — which format to reach for first, and why NanoBiT comes before
the three that need protein in hand — is a scheduling and cost argument
about this deck, not a published method. The formats themselves:

| Format | Source |
|---|---|
| NanoBiT split luciferase | Dixon et al., *ACS Chem Biol* 2016, [10.1021/acschembio.5b00753](https://doi.org/10.1021/acschembio.5b00753) (issued online 2015-11-16) |
| HTRF, Tb/Eu cryptate donor with an acceptor dye | Mathis, *Clin Chem* 1993, [10.1093/clinchem/39.9.1953](https://doi.org/10.1093/clinchem/39.9.1953) — rare-earth cryptates in homogeneous fluoroimmunoassay |
| AlphaScreen | Ullman et al., *PNAS* 1994, [10.1073/pnas.91.12.5426](https://doi.org/10.1073/pnas.91.12.5426) — luminescent oxygen channeling, the chemistry AlphaScreen commercialises |
| Fluorescence polarisation | Lea & Simeonov, *Expert Opin Drug Discov* 2011, [10.1517/17460441.2011.537322](https://doi.org/10.1517/17460441.2011.537322) |

All four verified; none cited in the repo. Note that the repo's own caveats
(Alpha's hook effect, FP's ~10× mass-ratio requirement) are properties
documented in those sources, so the citations would be carrying their own
weight rather than decorating the page.

### 4.8 — Counter-screen and competition

| | |
|---|---|
| **Repo states a source** | No, on the workflow. The evidence for the hotspot arm is cited in `protocols/bind.cf2h.screen.md`. |
| **Verdict** | **Standard practice with a canonical origin**, plus one published result the repo relies on and does not cite here. |

Using a point-mutant at a designed interface residue to ask whether a binder
found the face it was designed for is alanine-scanning logic: Cunningham &
Wells, *Science* 1989,
[10.1126/science.2471267](https://doi.org/10.1126/science.2471267) —
"High-Resolution Epitope Mapping of hGH-Receptor Interactions by
Alanine-Scanning Mutagenesis" (verified).

The specific claim the foundry leans on — that Δsignal on a hotspot mutant
tracks ΔΔG and ranks mutants correctly by affinity — is from the CF2H paper
(Capin et al. 2026, below), where it was shown against SPR. It is stated in
`protocols/bind.cf2h.screen.md` under "The hotspot arm" and is not attached
to 4.8, which is where a reader of the workflows page meets the idea.

### 4.9 — Dose-response

| | |
|---|---|
| **Repo states a source** | No |
| **Verdict** | **Standard practice.** Dilution series, four-parameter fit, report K_D or IC50. The acoustic implementation is this facility's own. |

What is distinctive here is building the series in the destination plate
from one titrant source rather than serially, which removes tip-to-tip
carryover and allows non-linear spacing. That is a property of acoustic
transfer (Ellson et al. 2003, above), applied by this deck; it is not a
published assay method, and nothing should be cited as though it were.

### 4.10 — Thermal stability

| | |
|---|---|
| **Repo states a source** | No |
| **Verdict** | **This facility's own**, and deliberately not a published method. |

The protocol is 4.7 run after a heat step at four temperatures, reporting
residual binding. The repo is explicit that this is a challenge rather than
a melt, and that a T_m has nowhere to be read because neither cycler has
optical detection. Citing the DSF or nanoDSF literature here would imply a
measurement this protocol does not make. Nothing to cite.

### 4.11 — Crystallisation screening

| | |
|---|---|
| **Repo states a source** | No |
| **Verdict** | **Two published methods, neither cited.** |

| Element | Source |
|---|---|
| Commercial sparse-matrix screens — the entire premise of "condition matrices" | Jancarik & Kim, *J Appl Crystallogr* 1991, [10.1107/S0021889891004430](https://doi.org/10.1107/S0021889891004430) — "Sparse matrix sampling: a screening method for crystallization of proteins" |
| Acoustic drop setting and acoustic *in situ* co-crystallisation with fragment libraries | Yin et al., *Acta Crystallogr D* 2014, [10.1107/S1399004713034603](https://doi.org/10.1107/S1399004713034603) |

Both verified. The Yin paper is the closest published precedent for what
4.11 and 4.12 together propose — acoustic dispensing of protein against
condition and against a fragment library — and is the one citation in this
audit that would most change what a reader thinks the protocol is.

The protocol's own hard limits (needs ≥10 mg/mL from offline expression;
needs the Echo 6XX for DMSO and 1536; imaging and scoring unquoted) are
facility facts, not literature.

### 4.12 — Compound and fragment screening

| | |
|---|---|
| **Repo states a source** | No |
| **Verdict** | **This facility's own**, built entirely on the 4.7 spine with a compound source plate substituted. |

There is no separate method here to cite: the assay is 4.7's, the transfer
is acoustic DMSO transfer (Ellson 2003), and the hit metric — percent effect
against the plate's own controls — is ordinary screening practice. Yin et
al. 2014 (above) is the relevant precedent if this is ever run as *in situ*
co-crystallisation rather than as a plate assay.

### 4.13 — In-vitro assembly to expression

| | |
|---|---|
| **Repo states a source** | **Yes, indirectly.** The `workflows:` note ends "From reference/fida-pipeline.md"; that file carries the citation. |
| **Verdict** | **Published method, cited.** |

**Ruiz Espi, Avelar Molina, Sonne Buch, Heyd, Unger, Winther Gormsen et
al.**, "A rapid, automation-friendly, cell-free and purification-free
pipeline for binding and kinetic characterisation of de novo designed
binders with high quality standardised per-design data", **bioRxiv**, posted
2026-10-20, [10.64898/2026.10.19.759856](https://doi.org/10.64898/2026.10.19.759856).

Verified live: Crossref returns that title, those authors and type
`posted-content` with that posted date. **It is a preprint and has not been
peer reviewed**, which `reference/fida-pipeline.md` states along with the
funding and competing-interest position of its authors. Anything 4.13
inherits from it inherits that status too.

What 4.13 takes from the paper: PCR off a linear fragment, SPRI, Golden Gate
into a **circularising** CFPS vector, SPRI, straight into the cell-free
reaction — no transformation, outgrowth, colony or miniprep. What 4.13
changes: the insert is normalised against vector **by mass on the Echo**,
where the source paper added a fixed volume and let the molar ratio drift.
The repo already says this; it is the right way round and worth keeping.

The named reagents in the `inputs:` block (pALiCE01-derived circularising
vector, Platinum SuperFi II 2× master mix, BsaI-HFv2 + T4 ligase with the
30 × 37 °C/16 °C cycling and 60 °C hold, Armadillo 384 PCR plate) are the
source paper's, not independent choices, and are recorded as such in the
STAR Methods file for 4.13.

Underlying method: Golden Gate, Engler et al. 2008 (above).

### 4.14 — Heat-shock transformation

| | |
|---|---|
| **Repo states a source** | No |
| **Verdict** | **Standard practice with a canonical origin.** |

Chemical transformation with a ~45 s pulse at 42 °C is Hanahan, *J Mol Biol*
1983, [10.1016/s0022-2836(83)80284-8](https://doi.org/10.1016/s0022-2836(83)80284-8)
— "Studies on transformation of *Escherichia coli* with plasmids"
(verified). It is textbook, and citing it is optional in a way that citing
Studier for ZYM-5052 is not.

What is genuinely this facility's is the implementation: two
temperature-controlled deck nests at 4 °C and 42 °C with the pulse as a
plate move between them, because a single block ramping at ~12 K/min would
take about three minutes to cross. That argument is the protocol's real
content and it is not from any paper.

### CF2H — Cell-free two-hybrid screen

| | |
|---|---|
| **Repo states a source** | **Yes**, in `protocols/bind.cf2h.screen.md` and `reference/capabilities.md` — with the first author's name wrong in both. |
| **Verdict** | **Published method, cited, one erratum.** |

**Capin, Mayonove, DeVisch, Becher, Ngo, Courbet et al.**, "CF2H: a
cell-free two-hybrid platform for rapid protein binder screening", *Nature
Communications*, 2026-03-10,
[10.1038/s41467-026-69741-1](https://doi.org/10.1038/s41467-026-69741-1).
PMC13103306, PMID 41807394. All four identifiers verified live; the DOI,
journal, year and PMC id in the repo are correct and the author name
("Delauriere et al.") is not. See **Errata**, above.

Everything numeric in the CF2H protocol that is attributed to the paper is
the paper's: CI(1–92) as the DNA-binding domain and the finding that CI(1–76)
gives no activation, the GGSx5 linker, BL21 Rosetta 2 ΔRecBCD S30 extract
and why no GamS is needed, 15 mM Mg-glutamate / 100 mM K-glutamate as
**their** optimum to be re-derived per lot, the reporter plasmid at 5 nM and
fragments at 2.5–5 nM, 22 µL assembled on ice, 5 µL into a 384-well
black-wall/clear-bottom low-binding plate under a transparent film, 37 °C
with Ex 485 / Em 528, signal under 2 h and plateau by 8 h, FITC
mean-equivalent conversion, the three target formats and the PD-L1
self-activation result, and the hotspot-arm result that Δactivation tracks
ΔΔG. The protocol file is already careful to separate these from the deck
mapping, which is the foundry's and unvalidated.

---

## Proposal: how a `refs:` field would attach

**Not implemented here.** `_data/protocols.yml` belongs to the schematics
lane and was deliberately not edited in this pass. This is a proposal for
whoever picks it up.

A `refs:` list on each `workflows:` entry, sibling to `inputs:` and `gates:`,
would carry what this audit established without putting a citation on the
page itself — which is what `CLAUDE.md` asks for under "Findable is not the
same as visible":

```yaml
  - id: '4.13'
    name: In-vitro assembly to expression
    # ...
    refs:
      - kind: protocol          # this workflow derives from this paper
        cite: "Ruiz Espi et al., bioRxiv 2026"
        doi: 10.64898/2026.10.19.759856
        preprint: true
        note: "circularising-vector Golden Gate into CFPS; insert normalised by mass here, by volume there"
      - kind: component         # one named reagent or step, not the workflow
        for: "BsaI-HFv2 + T4 DNA ligase"
        cite: "Engler, Kandzia & Marillonnet, PLoS ONE 2008"
        doi: 10.1371/journal.pone.0003647
```

Three properties worth keeping whatever the shape:

- **`kind:` distinguishes a protocol source from a component source.** Ten
  of the fifteen protocols have component sources and no protocol source;
  flattening the two would turn this audit's main finding into noise.
- **A protocol with no source carries `refs: []`**, explicitly, the way
  `gates: []` already works. An empty list is a statement that somebody
  looked; a missing key is not.
- **`preprint: true` travels with the citation**, because 4.13's source is a
  preprint and anything the site says on its authority inherits that.

A renderer could then put a small "sources" disclosure inside the protocol
card, shut by default, or leave it unrendered entirely and still have the
data one `grep` away. Either satisfies the convention; the second needs no
page change at all.

---

## Sources cited in this audit

All resolved live against Crossref on 2026-11-23; PMC and PMID against the
NCBI ID converter the same day.

| Short form | DOI |
|---|---|
| Capin et al., *Nat Commun* 2026 — CF2H | [10.1038/s41467-026-69741-1](https://doi.org/10.1038/s41467-026-69741-1) (PMC13103306, PMID 41807394) |
| Ruiz Espi et al., bioRxiv 2026 — cell-free purification-free pipeline **(preprint)** | [10.64898/2026.10.19.759856](https://doi.org/10.64898/2026.10.19.759856) |
| Studier, *Protein Expr Purif* 2005 — autoinduction, ZYM-5052 | [10.1016/j.pep.2005.01.016](https://doi.org/10.1016/j.pep.2005.01.016) |
| Cabantous, Terwilliger & Waldo, *Nat Biotechnol* 2005 — split GFP | [10.1038/nbt1044](https://doi.org/10.1038/nbt1044) |
| Schwinn et al., *ACS Chem Biol* 2018 — HiBiT | [10.1021/acschembio.7b00549](https://doi.org/10.1021/acschembio.7b00549) |
| Dixon et al., *ACS Chem Biol* 2016 — NanoBiT | [10.1021/acschembio.5b00753](https://doi.org/10.1021/acschembio.5b00753) |
| Mathis, *Clin Chem* 1993 — rare-earth cryptates (HTRF) | [10.1093/clinchem/39.9.1953](https://doi.org/10.1093/clinchem/39.9.1953) |
| Ullman et al., *PNAS* 1994 — luminescent oxygen channeling (AlphaScreen) | [10.1073/pnas.91.12.5426](https://doi.org/10.1073/pnas.91.12.5426) |
| Lea & Simeonov, *Expert Opin Drug Discov* 2011 — fluorescence polarisation | [10.1517/17460441.2011.537322](https://doi.org/10.1517/17460441.2011.537322) |
| Engler, Kandzia & Marillonnet, *PLoS ONE* 2008 — Golden Gate | [10.1371/journal.pone.0003647](https://doi.org/10.1371/journal.pone.0003647) |
| Potapov et al., *ACS Synth Biol* 2018 — overhang ligation fidelity | [10.1021/acssynbio.8b00333](https://doi.org/10.1021/acssynbio.8b00333) |
| DeAngelis, Wang & Hawkins, *Nucleic Acids Res* 1995 — SPRI | [10.1093/nar/23.22.4742](https://doi.org/10.1093/nar/23.22.4742) |
| Rohland & Reich, *Genome Res* 2012 — SPRI ratio size selection | [10.1101/gr.128124.111](https://doi.org/10.1101/gr.128124.111) |
| Sun et al., *J Vis Exp* 2013 — *E. coli* TX-TL protocols | [10.3791/50762](https://doi.org/10.3791/50762) |
| Hanahan, *J Mol Biol* 1983 — chemical transformation | [10.1016/s0022-2836(83)80284-8](https://doi.org/10.1016/s0022-2836(83)80284-8) |
| Schmidt & Skerra, *Nat Protoc* 2007 — Strep-tag system | [10.1038/nprot.2007.209](https://doi.org/10.1038/nprot.2007.209) |
| Schmidt et al., *Protein Expr Purif* 2013 — Twin-Strep | [10.1016/j.pep.2013.08.021](https://doi.org/10.1016/j.pep.2013.08.021) |
| Cunningham & Wells, *Science* 1989 — alanine-scanning | [10.1126/science.2471267](https://doi.org/10.1126/science.2471267) |
| Jancarik & Kim, *J Appl Crystallogr* 1991 — sparse matrix sampling | [10.1107/S0021889891004430](https://doi.org/10.1107/S0021889891004430) |
| Yin et al., *Acta Crystallogr D* 2014 — acoustic *in situ* co-crystallisation | [10.1107/S1399004713034603](https://doi.org/10.1107/S1399004713034603) |
| Ellson et al., *JALA* 2003 — acoustic droplet ejection | [10.1016/s1535-5535(03)00011-x](https://doi.org/10.1016/s1535-5535(03)00011-x) |
