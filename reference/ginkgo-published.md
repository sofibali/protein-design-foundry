# What Ginkgo has published — read 2026-11-19

Ginkgo runs RACs itself and writes up some of what it runs. Four of those
write-ups are workflows we have already specified, on the hardware we are
buying, which makes this the one reference in here that is not an analogue
but a precedent. Parts worth taking are marked **⇒**.

**The caveat first, because it applies to nearly everything below.** All of
it is vendor-authored except the preprint in §1, and that is a preprint, not
a peer-reviewed paper. There is no SLAS or other journal article on the RAC
platform that I could find. Treat the throughput and hands-on-time numbers
as vendor claims — they are useful as existence proofs ("this ran") and weak
as benchmarks ("this is what you will get").

**And the strategic one.** The public notes below are a sample. The
**Automated Protocol Library** is a customer entitlement, not a public
archive: Ginkgo says it shares protocols refined over years of running RAC
systems, alongside protocol code review and paired protocol writing. So what
follows is the shop window, and four of the items in it are workflows we
would otherwise write from scratch. That bears directly on the Foundation
vs Apex decision — Foundation carries no third-party instrument support, and
this is the other half of what the tier buys.

---

## 1. The cell-free optimisation loop — the one that matters

**Smith et al., *Using a GPT-5-driven autonomous lab to optimize the cost and
titer of cell-free protein synthesis*.** bioRxiv 2026-02-05,
[10.64898/2026.02.05.703998](https://www.biorxiv.org/content/10.64898/2026.02.05.703998v1),
**CC-BY**. Corresponding author Reshma Shetty, Ginkgo Bioworks. ~45 authors.

This is Aim 1's expression loop, already run end to end on our platform.

| | |
|---|---|
| Scale | **six iterative rounds**, ~36,000 reaction compositions (a ResearchGate copy says **29,000 unique** — pick the denominator deliberately) |
| Result | **−40% specific cost**, $698 → **$422 per gram** sfGFP; **+27% titer** (g/L) |
| Execution | designs → **Catalyst** programmatic multi-instrument workflows → **RACs** |
| In the loop | experimental design, execution, data capture, analysis, interpretation, next hypothesis |
| Out of the loop | "human intervention **largely limited to reagent and consumables preparation, loading and unloading**" |
| Interface | GPT-5 ↔ cloud lab, with a **Pydantic schema** validating that AI-designed experiments were properly specified. Ginkgo said the schema would be open-sourced |

**⇒ That last row is the number to have.** It is a vendor statement of the
unattended fraction of a cell-free loop on this exact hardware, and it is the
closest thing we have to evidence for the "a run ends in a verdict" premise
being mechanically achievable rather than aspirational.

**⇒ The Pydantic-schema-as-contract pattern is directly reusable.** We have
an agent deciding gates against `gates.yml`; they have an LLM proposing
reaction compositions against a schema that rejects malformed designs before
anything is pipetted. Same problem, and theirs is published.

**⇒ Read their factor set before we fix ours.** `express.cfps.doe` picks six
factors at two levels on a 2^(6-2) resolution IV design. Six rounds of 29,000
compositions is a different instrument entirely, but what they varied, and
what moved cost rather than titer, is the best available prior for our level
choices.

**Limits, stated plainly.** One protein (sfGFP), one CFPS system. Cost per
gram is not our objective function — D1 is a yield floor for a binding assay,
and theirs is $/g at scale. The 40% is against a stated state of the art we
have not independently checked.

---

## 2. Tech notes — short, protocol-level, on RACs

Four exist. Three are ours.

### [Magnetic bead protein purification on RACs](https://www.ginkgo.bio/tech-notes/magnetic-bead-protein-purification-on-racs)
→ our **4.5**, which at 96 lysates an hour is the most expensive hour on the
system.

A configurable protocol supporting different bind, wash and elute schemes
through Catalyst, with **no hands-on involvement during runtime**. One
summary describes it as a tip-based workflow — worth reading against our
Bravo-magnet assumption before we commit the protocol, since tip-based and
magnet-based bead handling have different plate-time costs.

### [Gene synthesis from oligo pools on the RAC platform](https://www.ginkgo.bio/tech-notes/gene-synthesis-from-oligo-pools-on-the-ginkgos-reconfigurable-automation-cart-rac-platform)
→ our **4.2**, and the most structurally similar of the four.

Multiplexed PCR → magnetic bead cleanup → gene-length "finishing" PCR,
**96 gene-sized fragments**, and it explicitly exists to feed *their*
downstream high-throughput **cell-free protein synthesis screening
pipeline**. That is our Route A/B spine, built by the vendor, feeding the
same place ours feeds.

**⇒ "Multiple, different protocol runs can be interleaved to increase
throughput"**, with metadata kept for traceability. This is the scheduler
behaviour our machine-time model in `capabilities.md` §4.0 assumes but does
not evidence — the ~75 two-plate protocols a day only materialises if
interleaving works, and here is Ginkgo saying it does.

### [Yeast heat shock transformation on a RAC](https://www.ginkgo.bio/tech-notes/yeast-heat-shock-transformation-on-a-flexible-reconfigurable-automation-cart-rac-system)
→ our **4.14**. Already cited in the internal notes; this is the public copy.

Each step written as a **separate Catalyst protocol, run in sequence** —
which is an argument for how to decompose ours. Note the scope line:
**colony picking was out of scope "and can be onboarded with further
expansion of the RAC system."** Our spec says colony picking is out; Ginkgo
says it is an expansion, not an impossibility. Worth knowing before anyone
treats §6 as permanent.

### [Chemical transfection of mammalian cells using RACs](https://www.ginkgo.bio/tech-notes/chemical-transfection-of-mammalian-cells-using-racs)
Not ours — CHO and mammalian are out of scope. Recorded for completeness:
Expi293F, 93% mean transfection efficiency, 80% hands-on reduction.

---

## 3. Application notes

### [High-throughput screening of HiBiT-tagged proteins](https://www.ginkgo.bio/app-notes/high-throughput-screening-of-hibit-tagged-proteins)
→ our **4.6**, and **it is on our reader.**

The note describes adding **one additional RAC containing the BMG LABTECH
PHERAstar FSX** to an existing system. That is RAC 13 in our 15-cart list.

| | |
|---|---|
| Scale | ~10,000 samples; **7,680 quantified with no in-person monitoring** |
| Agreement | normalised concentrations averaged **2% from the prior semi-automated protocol** |
| Data | output flowed to their LIMS automatically via an Event Processing Pipeline |
| Origin | the system was built for qPCR and NGS prep, then **extended to plate reading** |

**⇒ The 2% figure is the precedent for the Lynx normalisation step in 4.6.**
It says a machine-normalised plate agrees with a careful semi-automated one,
which is exactly the claim that step rests on.

**⇒ "Extended to plate reading" is the shape of our phase-2 argument.** They
added a reader cart to a DNA system and got an assay platform. We are
proposing to add an imager cart and get crystallography.

### [NGS library preparation on RACs](https://www.ginkgo.bio/app-notes/next-generation-sequencing-ngs-library-preparation-on-racs)
([white paper version](https://cms.ginkgo.bio/assets/automation/application-notes/ginkgo-automation-white-paper-high-throughput-miniaturized-next-generation-sequencing-library-preparation-on-the-ginkgo-reconfigurable-automation-cart-platform.pdf))

Illumina DNA Prep **miniaturised 100-fold** and executed end to end on RACs,
**including upstream microbial cell lysis**. Claimed: 30–40% less hands-on
time, 33% less headcount, 10× reagent saving.

**⇒ This narrows the open NGS item usefully.** Library prep on the deck is a
solved workflow with a published precedent. What is actually undecided is the
*sequencer* — in-lab Nanopore versus a campus core — not whether the deck can
prepare the library. Route B and affinity maturation are blocked on less than
`stages.yml` currently implies.

### The rest
- [Cell-based assays at Octant Bio](https://www.ginkgo.bio/app-notes/accelerating-drug-discovery-at-octant-bio-using-racs-for-cell-based-assays) — 7× throughput over manual. Relevant as a customer case study: the closest published example of this hardware running a real assay programme.
- [Chemical transfection on RACs](https://cms.ginkgo.bio/assets/automation/application-notes/application-note-chemical-transfection-on-racs.pdf)
- [qPCR AAV titering on RACs](https://cms.ginkgo.bio/assets/automation/application-notes/application-note-qpcr-aav-titering-on-racs.pdf)
- [Miniaturised cell-based assays white paper](https://cms.ginkgo.bio/assets/automation/application-notes/ginkgo-automation-white-paper-accelerating-drug-discovery-with-miniaturized-cell-based-assays-on-ginkgos-flexible-reconfigurable-automation-cart-rac-system_0241010.pdf)
- [Control and data plane integration for high-throughput modular automation](https://cms.ginkgo.bio/assets/automation/application-notes/application-note-control-and-data-plane-integration-for-high-throughput-modular-automation.pdf) — the architecture note. Describes Catalyst's Configuration Center for reconfiguring a system online, and **separating protocol logic from automation programming so individual steps can be validated**. That separation is the same one `data/protocols.yml` makes between a workflow and its deck sequence.

---

## 4. System blueprints

Published RAC system layouts with their unit operations — the public analogue
of our 15-cart list.

- **[DNA Assembly & Microbial Strain Engineering RAC System](https://automation.ginkgo.bio/applications/dna-assembly-microbial-engineering-blueprint)** — described as a validated starting point for planning. Unit operations include DNA amplification, colony PCR, non-contact acoustic cherry-picking, plate reading, and colony picking (optional).
- **High-Throughput Mammalian Biology RAC System** — not ours.

**⇒ Compare the DNA blueprint against our cart list before the layout is
frozen.** Ours was assembled from a quote and a meeting; theirs is a
configuration they have built repeatedly. Any unit operation on their list
that has no home on ours is worth a deliberate answer.

**The blueprint PDFs are gated** behind a name-and-work-email form, so what is
public is the landing page, the summary of contents, and the schematic image.
That is enough: the schematic carries the whole grammar.

**What a blueprint is, from the three schematics.** A closed track — the
MagneMover rail — with one tile per cart sitting on it, labelled **by unit
operation rather than by instrument model**; optional or not-yet-bought carts
drawn with a dashed border; small I/O badges on the track where material enters
or leaves by hand. No model numbers, no prices, no vendor names anywhere on the
sheet. Counts: DNA assembly **13 carts**, mammalian biology **14**, small
molecule **11**.

**⇒ Done, 2026-11-19.** `data/protocols.yml` now carries a `racs:` block and
`build.py` renders `dist/blueprint.html` in this grammar — 15 carts at install
plus the 4 the floor plan reserves, every unit-operation name taken from
Ginkgo's vocabulary where they have one for something we have. It is generated
from the same YAML as the workflow page, so the two cannot drift, and the build
refuses an instrument that is on the capability map and on no cart. The one
thing a static JPEG cannot do, and ours does: click a cart and it lists what is
on it and which workflows run through it.

---

## 5. What this changes, concretely

1. **`capabilities.md` §4.0's interleaving assumption now has a source** —
   the oligo-pool note states it directly.
2. **4.6's normalisation step has a precedent at 2% agreement** on the same
   reader.
3. **The NGS open item is narrower than written** — prep is solved, the
   sequencer is the decision.
4. **Colony picking is an expansion, not a wall** — Ginkgo's own words.
5. **The Foundation/Apex tier decision gains a second axis.** It is not only
   third-party instrument support; it is whether we get the library these
   four notes are drawn from.

## Not yet read

The full PDFs of the bead-purification and oligo-pool tech notes (both
summarised here from page text, not read end to end); the CFPS preprint's
methods section; the SLAS 2025 Ginkgo Automation handout; and
`automation.ginkgo.bio/product/support`, which lists what the Automated
Protocol Library entitlement actually includes.
