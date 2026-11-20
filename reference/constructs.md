# What goes in

The input side of every workflow in `capabilities.md` §4 — what you order,
what it costs you in sequence budget, and which bead or reagent it commits
you to downstream. Vendor specifics are dated November 2026 and marked where
they need re-checking.

---

## 1. The standing cassette

One construct layout for the whole foundry. Everything else is a variant.

```
T7 promoter — 5' UTR / RBS — [design] — GGGS — split-GFP11 — GGGS — Twin-Strep — T7 term
```

| Element | Sequence or spec | What it buys |
|---|---|---|
| T7 promoter | `TAATACGACTCACTATAG` | works in lysate CFPS, PURE and BL21(DE3) — one promoter for all three routes |
| RBS / 5' UTR | strong, defined | the one element worth tuning per host |
| GGGS linkers | `GGCGGAGGCAGC` | keeps the tag from folding back onto a 50–65 aa design |
| split-GFP11 | `RDHMVLHEYVNAAGIT` | expression quantification with GFP1-10 added after the fact |
| Twin-Strep | `WSHPQFEKGGGSGGGSGGSAWSHPQFEK` | capture on Strep-Tactin XT, mild biotin elution |
| T7 terminator | standard | reduces read-through on linear template |

**Why both tags.** Split-GFP11 answers *how much*, Twin-Strep answers *get it
out*, and neither needs the construct re-cloned between D1 and D4. This is
Adaptyv's pattern and it is worth copying exactly.

**The alternative: a whole fluorescent protein.** `[design] — linker — FP —
protease site — Strep-tag II` reads expression with nothing added at all, and
normalises every downstream number by that same fluorescence. It costs ~27 kDa
against split-GFP11's 16 aa, which is irrelevant for a plate assay and fatal
for a size-based one. Pick by readout — see `reference/fida-pipeline.md`.

**The variant that breaks the pattern:** a CF2H construct is
`promoter — RBS — CI(1–92) — GGSx5 — [design]`, with no C-terminal tag, and
its sfGFP reporter collides with a split-GFP readout. Pick the readout at
order time; see `protocols/bind.cf2h.screen.md`.

---

## 2. The three DNA inputs

| | **Gene fragments** | **Oligo pool** | **Plasmid** |
|---|---|---|---|
| Product | IDT eBlocks, Twist Gene Fragments | Twist / IDT oPools | cloned, **or circularised in vitro — see 4.13** |
| Length | ~300 bp–1.5 kb | **20–350 nt** | any |
| Delivered | one tube or well per design | one tube, everything mixed | one well per clone |
| Cost shape | per construct | per pool, ~10× cheaper per member | per clone, dearest |
| Sequence known? | yes, per design | yes as a list, no per molecule | yes, verified |
| QC | gel + fluorimetric quant | needs NGS to know what is in it | Sanger / whole-plasmid |
| Goes into | arrayed CFPS, arrayed *E. coli* | Golden Gate → pooled library | anything, especially structure |

Twist states 20–350 nt for pools on its own FAQ pages, though its pricing
tiers are written inconsistently (251–300 nt in one place, 251–350 in
another). **Treat 300 nt as the planning number and 350 as the stretch.**

---

## 3. Oligo pool design, in detail

### The length budget

This is the arithmetic that decides whether a design fits at all.

```
  300 nt  ordered length (plan at 300, not 350)
−  40 nt  5' and 3' amplification adapters (20 each)
−  22 nt  two BsaI sites + 4 nt overhangs + spacers
−  12 nt  barcode (optional, see below)
= 226 nt  coding budget  →  75 aa
```

**So: ~75 amino acids per oligo, 85 if you drop the barcode, ~60 if you want
comfortable primer design.** Minibinders at 50–65 aa fit. A 100 aa design
does not — that needs two oligos with an internal junction, or an eBlock.

### Adapters and subpools

Both ends carry a constant 20 nt amplification adapter. Design them to:

- have no internal BsaI/BsmBI site,
- share a Tm within ~2 °C,
- be absent from the *E. coli* genome and from your backbone.

**Use different adapter pairs to split one physical pool into subpools.**
One synthesis order, several independently amplifiable libraries — this is
how you put four targets' designs in one pool and still assemble them into
four separate backbones.

### Type IIS and overhang choice

**BsaI** is the default. **BsmBI** is the second enzyme when a construct has
to survive two rounds. Strip both recognition sites from every coding region
before ordering — a single internal site destroys that member silently, and
you will not know which one failed without NGS.

Overhangs are not free to choose. Four-base overhangs mis-ligate at rates
that depend on the specific set, profiled exhaustively for T4 ligase by
Potapov et al. (2018, *ACS Synth Biol*). Use NEB's tools rather than
intuition:

| Tool | Use |
|---|---|
| **NEBridge GetSet** | generate a high-fidelity overhang set of N junctions |
| **NEBridge SplitSet** | split a given sequence into fragments at high-fidelity junctions (Lite handles ≤20 fragments) |
| **Ligase Fidelity Viewer** | score an overhang set you already have |

At `ligasefidelity.neb.com`. For a two-part assembly (one insert, one
backbone) almost any set works; the tools earn their keep at 4+ parts.

### Codon and sequence rules

- **Codon-optimise for *E. coli***, but the thing that actually matters is
  mRNA secondary structure over roughly the first 30 codons. A strong hairpin
  across the RBS is the commonest silent expression failure.
- Avoid homopolymer runs >6 and GC <30% or >65% in any 50 nt window — both
  are synthesis-failure modes, not biology.
- Keep every member the same length where you can. Unequal lengths skew pool
  amplification toward the short ones.

### Barcodes

12 nt, Hamming distance ≥3 between any pair, no homopolymers. Only worth the
sequence budget **if NGS is settled** — without sequencing they cost you four
amino acids and buy nothing.

### NNK for affinity maturation

`NNK` = N(any) N(any) K(G or T). 32 codons, all 20 amino acids, **one stop
(TAG) instead of three.** Randomise 4–6 positions around a confirmed
interface; 6 positions is 32⁶ ≈ 10⁹ DNA sequences, which is far past what
this foundry can screen, so **choose positions, do not scan**.

Twist and IDT both accept degenerate bases in pools — confirm the per-order
limit, as it is capped.

---

## 4. Backbones

| Backbone | Use | Selection | Notes |
|---|---|---|---|
| **pET21b(+)** | C-terminal His, *E. coli* expression | Amp | BindCraft's own validation used pET21b/pET11 |
| **pET29b(+)** | same, Kan | Kan | prefer Kan for anything grown unattended overnight |
| **pET22b(+)** | periplasmic via PelB | Amp | the VHH route — disulfide-containing binders need it |
| **pET28a(+)** | N-term His + thrombin | Kan | what CF2H used for its purified binders |
| **pSB4k5** | low-copy, for the CF2H pRM reporter | Kan | low copy matters — a high-copy reporter titrates CI |
| **pALiCE01** | eukaryotic CFPS (tobacco BY-2 lysate, LenioBio) | — | the base for a *circularising* Golden Gate vector: no transformation at all |
| **pETCON3** | yeast display | Trp | **do not build toward it.** It only pays off with FACS, which the deck does not have |

**One decision worth making once:** standardise on kanamycin for everything
that incubates unattended. Ampicillin degrades over a long incubation and
satellite growth follows.

### Transformation works on the machine, so every row above stands

**Heat shock is a capability of this deck.** The **Bravo** carries two
temperature-controlled deck positions held at **4 °C and 42 °C** —
QInstruments Peltier blocks, −20 °C to 99.9 °C, 12 K/min. The 45-second
pulse is a plate move between them.

Two fixed positions rather than one ramping block is what makes the timing
real: a single block takes about three minutes to go from 4 °C to 42 °C at
12 K/min, and a thermal cycler in another RAC cannot time a 45-second step
at all. Two plates, both multi-temperature, one move.

**Transformation, plating and *E. coli* expression are all in scope on the
RAC.** Colony picking is not, so plating is for titre and QC and nothing
returns a clone to liquid — which is why §2's cassette is designed to be
recovered by PCR rather than by picking.

So the plasmid rows above — **pET21b, pET29b, pET22b, pET28a** and
**pSB4k5** — are specified as written, Route C is a live route alongside
cell-free, and pSB4k5 carries the CF2H pRM reporter.

**One practical note.** The coldest position on the system is the **4 °C
SteriStore** (4–100 °C, 98% RH, CO₂-ready, 216 standard + 50 deep-well).
Competent cells arrive cold on the day and are held there in-run.

---

## 5. Tags, and what each one commits you to

| Tag | Partner reagent | Elution | Watch |
|---|---|---|---|
| **His6 / His10** | Ni-NTA or Co-IMAC mag beads | imidazole gradient | **dies on EDTA and DTT** — see §6 |
| **Twin-Strep** | MagStrep Strep-Tactin XT | biotin (Buffer BXT), mild | **biotin elution poisons any downstream streptavidin step** |
| **split-GFP11** | GFP1-10 added in excess | n/a, it is a readout | irreversible, so it over-reports weak signal |
| **HiBiT** | LgBiT + furimazine | n/a, readout | luminescent, widest dynamic range, works in crude lysate |
| **AviTag** | biotin ligase BirA | n/a | this is how you make your *target* biotinylated for CF2H format 3 |

**The biotin collision is real and it is easy to walk into.** If you elute a
Twin-Strep protein with biotin and then try to tetramerise a biotinylated
target on streptavidin in the same assay, free biotin from the elution
saturates the streptavidin. Either buffer-exchange, or use a His tag on the
binder when the target is the biotinylated partner.

---

## 6. Magnetic beads

This is the part that quietly decides whether workflow 4.5 works at all.

### For His tags

| Product | Support | Size | EDTA / DTT | Plate format |
|---|---|---|---|---|
| **NEBExpress Ni-NTA Magnetic Beads** | magnetic agarose | — | no | published 96-well protocol, 50 µL slurry/well, 96-well magnet rack |
| **Thermo HisPur Ni-NTA Magnetic Beads** | magnetic agarose | — | no | KingFisher 96 deep-well protocol; do not dry, freeze or centrifuge |
| **Pierce Ni-NTA Magnetic Agarose** | agarose | ~10–40 µm | no | the Opentrons note runs 96 samples in 57 min |
| **Pierce Ni-NTA Magnetic Beads** | polymer | ~1 µm | no | small beads, slow to collect on a weak magnet |
| **Pierce High-Capacity Ni-IMAC MagBeads** | — | ~100 µm | **EDTA-compatible** | large, collects fast |
| **PureCube Ni-INDIGO MagBeads** (Cube) | agarose-coated ferrimagnetic | — | **up to 20 mM EDTA and 20 mM DTT** | round-bottom 96-well recommended; pre-filled plates sold |

**The DTT problem.** Cell-free reaction buffers routinely carry DTT, and most
lysate recipes include it. Plain Ni-NTA strips nickel in the presence of DTT
and chelators, so **purifying a His-tagged protein straight out of a CFPS
reaction on ordinary Ni-NTA will underperform or fail.** Two ways out:

1. use an EDTA/DTT-tolerant bead — PureCube Ni-INDIGO tolerates 20 mM of
   each, Pierce High-Capacity Ni-IMAC is EDTA-compatible; or
2. **use the Twin-Strep tag instead**, which does not care about either.

Given the standing cassette already carries Twin-Strep, option 2 is free.

### For Twin-Strep

**MagStrep Strep-Tactin XT beads** (IBA Lifesciences, 2-5090-002 for 2 mL,
2-5090-010 for 10 mL). Magnetic 6 % agarose, binds both Strep-tag II and
Twin-Strep, works in reaction tubes or 96-well plates with a magnetic
separator instead of a spin. Elution is biotin in Buffer BXT under mild
conditions, or boiling in SDS buffer if you only need a gel.

Binding capacity is quoted as **1.1 nmol per µL of beads** on the IBA
datasheet; a Cube Biotech listing gives 42.5 mg/mL, which is a different
figure in different units. **Re-read the datasheet before scaling** — this is
the one number here I would not trust second-hand.

Store at 2–8 °C. Do not freeze.

### For DNA cleanup

SPRI / AMPure-class carboxylate paramagnetic beads, on the same Bravo magnet.
Ratio sets the size cut: 1.8× keeps nearly everything, 0.8× drops fragments
below ~200 bp, 0.6× below ~500 bp. **Use a ratio, not a kit's default** — it
is the only size selection the deck has.

### Bead size versus the deck

Agarose beads are 10–100 µm, polymer beads can be 1 µm. Small beads need
longer on the magnet and are the usual cause of a workflow that works by hand
and fails on the Bravo. If a bead is new to the deck, **time the collection
step before trusting it in a protocol**, and never centrifuge or let agarose
beads run dry.

---

## 7. Assay reagents by format

| Format | What you buy | Per-well cost shape | Needs a tag? |
|---|---|---|---|
| **NanoBiT / split-luc** | LgBiT + SmBiT constructs, furimazine substrate | substrate dominates | engineered in |
| **HTRF** | Tb or Eu cryptate anti-tag donor, d2/XL665 acceptor | antibody dominates | anti-His / anti-Strep |
| **AlphaScreen** | donor + acceptor beads | beads dominate | anti-tag |
| **FP** | fluorescein or TAMRA tracer peptide | cheapest, one tracer | none |
| **CF2H** | extract, buffer, pRM reporter plasmid | €0.10/reaction homemade | CI fusion |

Anti-tag HTRF reagents against His and Strep are catalogue items; an
anti-tag pair is almost always cheaper and faster than raising something
target-specific.

---

## 8. What each workflow actually needs

| Workflow | Inputs |
|---|---|
| **4.1** clonal array | gene fragments, one per design; nuclease-free water |
| **4.2** pooled library | oligo pool with adapters; BsaI-HFv2 + T4 ligase; linearised backbone; SPRI beads; competent cells; recovery medium |
| **4.3** cell-free arrayed | lysate or PURE kit (2 lots); Mg/K-glutamate stocks; template; GFP1-10 reagent; GFP11 standard |
| **4.4** *E. coli* arrayed | plasmid or fragment; BL21(DE3); autoinduction medium (ZYM-5052); lysis reagent |
| **4.5** bead purification | **MagStrep Strep-Tactin XT** (or an EDTA/DTT-tolerant IMAC bead); wash buffer; Buffer BXT |
| **4.6** protein QC | GFP1-10 or LgBiT + furimazine; UV-transparent plate for A260/A280; FP tracer |
| **4.7** assay ladder | per §7, by format; purified or crude protein; target |
| **4.8** counter-screen | counter-target; **hotspot point-mutant of your own target**; non-binder control |
| **4.9** dose–response | one Echo source plate of titrant |
| **4.10** thermal challenge | the binding assay's reagents, plus sealed plates for the ladder |
| **4.11** crystallisation | protein at ≥10 mg/mL from offline; commercial screens; SwissCI plates; DMSO compound stocks |
| **4.12** compound screening | compound plates in DMSO; the 4.7 reagents |
| **CF2H** | ΔRecBCD extract; CF2H buffer; pRM/OR3\*–sfGFP reporter plasmid; CI-fusion fragments; FITC standard; biotinylated target + streptavidin for format 3 |
| **4.14** heat-shock transformation | chemically competent cells, delivered cold on the day; assembled DNA held at 4 °C; SOC or recovery medium; agar plates for titre and QC, lidded on the a4s |

---

## 9. Still to verify

- Twist's top oligo-pool tier: 300 or 350 nt. Their own pages disagree.
- IDT oPools maximum length, from IDT's page rather than an aggregator.
- MagStrep XT binding capacity, from the IBA datasheet directly.
- Degenerate-base limits per pool order, both vendors.
- Whether the Bravo magnet collects 1 µm beads in a sensible time, or whether
  the deck is agarose-only in practice.
