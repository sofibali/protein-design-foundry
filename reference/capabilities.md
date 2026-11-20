# What the foundry can run

A map of workflows against the deck, drawn from Adaptyv's production
pipeline and the Baker lab's published campaigns. Styles and capabilities,
not thresholds.

---

## 0. What kind of foundry this is

Four facts about the deck decide everything below.

**It is a plate-reader foundry, not a biosensor foundry.** Adaptyv runs
BLI on a Gator; BindCraft validated PD-1 designs by BLI; the Baker lab
leans on BLI and SPR throughout. There is no BLI or SPR on the RAC. The
PHERAstar does **homogeneous mix-and-read** chemistry — HTRF,
AlphaScreen, fluorescence polarisation, luminescence, absorbance. No
wash, no immobilisation, no regeneration, no sensor tips.

That is a real constraint and a real advantage. You cannot get kon/koff.
You can read 1,536 wells in minutes, from crude reactions, with no
consumable per sample beyond reagent.

**It is a cloning-light foundry.** No colony picker means no clonal
isolation. Nothing on this deck can take a transformed plate, pick a
colony, and return it to liquid. Every workflow below either avoids
clones or recovers them by PCR.

**It is arrayed first, pooled second.** Pooled selection needs NGS and a
physical selection step. The Baker pipeline's selection step is FACS on
yeast display — the deck has neither. Arrayed screening needs neither.

**It has a ceiling, and the ceiling is the Bravo.** ~75 two-plate protocols
per 20-hour day, tied with the PHERAstar. Everything in §4 is priced against
that in §4.0 below. The short version: **a 384-well plate costs the Bravo
four times a 96-well plate**, because a 96-channel head has to make four
offset quadrant transfers to fill one. Push the dispensing to the Echo and
384 costs the same as 96.

---

## 1. The three DNA routes

Everything starts with one of these.

### Route A — linear dsDNA, one design per well, no cloning

Adaptyv's route. Order full-length linear dsDNA (eBlocks, gBlocks,
Gene Fragments), one design per well, straight into cell-free. No
plasmid, no transformation, no colonies, no minipreps.

**Why it works:** reconstituted PURE systems carry no nucleases, so
linear template survives. In *lysate*-based CFPS, RecBCD chews linear
DNA. Three fixes, cheapest last: add **GamS**, buy a lysate that ships
with it, or make extract from a **ΔRecBCD strain** — which is what CF2H
does (§8), and it removes the additive from every reaction forever.

Note that CF2H PCR-amplifies the ordered fragment before use rather than
pipetting it neat. That costs one thermocycler step and buys template
mass, a gel check and a Qubit number per design.

**On deck:** Echo transfers template → MultiFlo adds the CFPS mix →
PlateLoc seals → ATC holds temperature → XPeel → read. Four unit ops,
no overnight step, same day.

**Scale:** 96–384 designs per campaign comfortably. Cost per design is
the synthesis cost, which is the ceiling.

### Route B — oligo pool → Golden Gate → pooled library

The Baker route, minus the yeast. Order a pool of 200–300 nt oligos,
amplify, assemble into a backbone by Type IIS digestion-ligation.

**On deck:** this is genuinely well suited to the Echo — Golden Gate at
nanolitre scale, BsaI-HFv2 plus T4 ligase, cycled 37 °C/16 °C on the
ATC. Oligo-pool cloning runs roughly tenfold cheaper per construct than
ordering dsDNA.

**The catch:** a pool is only useful if you can select from it and read
out what survived. Selection needs a physical enrichment step; readout
needs NGS. Neither is on the deck. **Until the NGS path is decided,
Route B builds libraries the foundry cannot interrogate.**

### Route C — clonal plasmid array

Order designs as sequence-verified plasmids, one per well. Expensive per
construct, but no assembly, no QC, no ambiguity — and compatible with
*E. coli* expression where cell-free fails.

**Use it for:** the handful of designs going to structure, where you need
milligrams and certainty rather than hundreds and speed.

| | Route A linear | Route B pool | Route C plasmid |
|---|---|---|---|
| Cloning | none | Golden Gate | none |
| Designs | 96–384 | 10⁴–10⁶ | 1–96 |
| Turnaround | days | weeks | weeks |
| Needs NGS | no | **yes** | no |
| Needs selection | no | **yes** | no |
| Protein scale | µg | n/a | mg |
| Ready today | **yes** | no | yes |

---

## 2. Backbones and the standing construct

**The detail lives in `reference/constructs.md`** — the cassette element by
element, every backbone with its selection marker, the tag table, bead
chemistries, and the oligo-pool length arithmetic. Sections 2 and 3 here are
the summary.

Stop designing a construct per campaign. Pick one cassette and keep it.

**For cell-free linear template (Route A):**

```
T7 promoter — 5' UTR/RBS — [design] — GGGS — split-GFP11 — GGGS — Twin-Strep — T7 terminator
```

Adaptyv's tag, and worth copying wholesale. The C-terminal
**split-GFP11** (RDHMVLHEYVNAAGIT) gives expression quantification with
GFP1-10 reagent added in excess; the **Twin-Strep** gives capture. One
cassette, two jobs, nothing re-cloned between the expression readout and
the binding assay.

Add **HiBiT** instead of, or beside, split-GFP11 if you want luminescence
dynamic range rather than fluorescence.

**For *E. coli* arrayed expression (Route C):** pET21b or pET29b with
C-terminal His6, BL21(DE3) or Codon Plus, IPTG or autoinduction. This is
what BindCraft and most Baker campaigns used.

**Route C is a live route.** Transformation, plating and *E. coli*
expression all run on the RAC: the Bravo carries two temperature-controlled
deck positions at 4 °C and 42 °C, and a 45-second heat shock is a plate move
between them. See §4.14 and `reference/constructs.md` §4.

**pETCON3** is the Baker yeast-display vector. **Do not build toward it** —
it only pays off with FACS.

**Linkers:** GGGS repeats for flexibility, EAAAK for rigidity when you
need to hold two domains apart. Keep the same linker across campaigns so
expression differences are about the design, not the joint.

---

## 3. Oligo and gene design

**Length is the hard constraint.** Oligo pool synthesis tops out around
230–300 nt. Subtract ~40 nt of adapters and Type IIS sites and you have
~190–260 nt of coding — **roughly 60–85 amino acids**. De novo
minibinders sit at 50–65 aa, so they fit. Anything longer needs two
oligos assembled, or eBlocks instead.

**Rules to bake into the design script:**

- Strip internal **BsaI** and **BsmBI** sites, or Golden Gate eats the insert.
- Codon-optimise for the expression system, and separately for **mRNA
  secondary structure** at the 5′ end — Adaptyv optimises for cell-free
  usage, structure and synthesisability together.
- Fixed adapter pairs at both ends for pool amplification.
- For pooled work, a **barcode** per design, long enough to stay unique
  after sequencing error.
- **Novelty distance.** Adaptyv's competition counted only designs more
  than 10 aa from any known binder. Score it, record it, use it — it
  stops a campaign quietly rediscovering cetuximab.

**For affinity maturation:** degenerate **NNK** codons at chosen
positions, which is what the Baker lab uses to build combinatorial
libraries around a confirmed hit. NNK gives all 20 amino acids with one
stop codon instead of three.

**Smarter design, concretely:** order a **hotspot point-mutant of the
target** alongside every campaign. One extra construct. It is the only
plate-reader way to ask whether a binder hit the face you aimed at, and
it is the thing that would have caught the PARP14 result.

---

## 4. The workflows

**This section is also a page.** `data/protocols.yml` holds every workflow
below as a deck sequence, and `dist/workflows.html` renders it — click an
instrument to see everything that needs it. The YAML is the source of
truth; if it and this prose disagree, the prose is stale.

### 4.0 What a workflow costs the day

Every *Scale* and *Time* line below says what a workflow **gives**. None of
them used to say what it **costs**, so two workflows that both read "384
designs" could differ fourfold in machine time and nothing showed it. Each
workflow in `data/protocols.yml` now carries a `cost:` block, and the page
renders it as a share of the day.

**The ceilings**, in the order they bind:

| Instrument | Ceiling, per 20-hour day | Binds |
|---|---|---|
| **Bravo 96** | **~75 two-plate protocols** | everything that pipettes |
| **PHERAstar FSX** | **150** 384-well TR-FRET plates | everything that reads |
| Echo | 400 384-well plates | plate setup, drop setting |
| **Cytomat** | **7 concurrent** culture protocols, 14 deep-well positions | everything that grows |

The Bravo and the PHERAstar are **tied** as the system bottleneck. The
Cytomat is a harder cap but it only applies to the *E. coli* route.

**The rates those ceilings imply**, which is what each `cost:` is built from:

| Step | Minutes | Where it comes from |
|---|---|---|
| Bravo, one **96**-well plate, one transfer | **8** | 1,200 min ÷ 75 protocols ÷ 2 plates |
| Bravo, one **384**-well plate, one transfer | **32** | **four offset quadrant transfers** with a 96-channel head |
| Echo, one plate | 3 | 400 plates per 20 h at 384 |
| PHERAstar, one 384 TR-FRET or FI read | 8 | 150 plates per 20 h |
| PHERAstar, one luminescence read | 3 | the scheduler model |

**The 4× is the whole point.** It is why 4.1, 4.3, 4.7, 4.9 and 4.12 put the
Echo in the chain and keep the Bravo out of it entirely, and why **CF2H**,
which dispenses a cold master mix into 384 on the Bravo, spends 32 minutes
of the system bottleneck on a step that would cost 3 on the Echo. If that
master mix can be made acoustic, move it.

**Two things would raise the ceiling**, and both are open: a **384-channel
Bravo head** (price and whether heads swap without re-integration are
unasked — Agilent), and pushing more dispensing to the Echo, which is free
and is already the design of most of §4.

**Treat these as modelled, not measured.** The rates are arithmetic off
Ginkgo's own throughput figures; the per-workflow step counts are read off
the deck sequences. The ratio between two workflows is worth more than the
absolute number on either.

**One assumption underneath all of it now has a source.** ~75 two-plate
protocols a day only materialises if the scheduler interleaves runs rather
than draining them one at a time. Ginkgo's published oligo-pool tech note
states that "multiple, different protocol runs can be interleaved to increase
throughput", with metadata kept for traceability — see
[reference/ginkgo-published.md](reference/ginkgo-published.md) §2, which
collects everything Ginkgo has published that bears on §4.

> Ceilings and rates from the Ginkgo device-set notes (Bravo, Echo and
> PHERAstar lines) and the small-protocol capacity model, both in the
> internal repo.

### 4.1 Build a clonal array (no cloning)

Linear dsDNA arrives plated. Echo normalises concentration into a
destination plate. That is the whole build.

*Deck:* Echo → (nothing else) · *Waits in:* AmbiStore
*Gives:* a template plate ready for any expression route
*Scale:* 384/plate · *Time:* one hour · *Costs:* 3 min of Echo, nothing of
the Bravo — the cheapest thing on the deck

### 4.2 Build a pooled library

Pool amplification by PCR, Type IIS digestion-ligation into a linearised
backbone, cleanup on magnetic beads, transformation, outgrowth as a
pool — never plated for colonies.

*Deck:* Echo sets up pool PCR → **ATC 384** cycles → Bravo + magnet cleans
up → **Magniflex** delivers the enzyme master mixes → Echo sets up nL Golden
Gate → **ATC 96** cycles 37/16 °C → Bravo + magnet cleans up → **Bravo
heat-shocks between its 4 °C and 42 °C nests** → MultiFlo adds SOC → Cytomat
recovers · *Waits in:* AmbiStore, SteriStore 4 °C, MicroServe
*Gives:* a library in liquid culture
*Costs:* 24 min Bravo, 6 min Echo — but the real cost is a Cytomat shaking
position for the night, and there are only 14
*Blocked on:* NGS to know what is in it

**Two lines corrected.** An earlier draft had the ATC doing the heat shock
and the SteriStore doing the outgrowth. The pulse happens between the Bravo's
two temperature-controlled nests (§4.14), and outgrowth needs shaking, which
only the Cytomat has — the 4 °C SteriStore holds the *grown* blocks after.
The **Magniflex** carries the enzyme master mixes because BsaI-HFv2 and T4
ligase ship in glycerol and the Echo will not transfer them.

### 4.3 Cell-free expression, arrayed

The foundry's bread and butter. Echo builds the condition matrix from
concentrated stocks, MultiFlo adds the common mix, ATC holds temperature
4–6 h, GFP1-10 reagent in, PHERAstar reads.

*Deck:* Echo → MultiFlo → PlateLoc → **ATC 96 ×3 + ATC 384** → XPeel →
MultiFlo → PHERAstar · *Waits in:* SteriStore 37 °C, AmbiStore
*Gives:* µg/mL per well against a standard curve
*Scale:* 384/plate, four plates in parallel across four ATCs
*Costs:* 12 min Echo, 32 min reader, **nothing on the Bravo** — one round is
about 3% of a 20-hour day and the reader is what limits it
*Note:* use the four ATCs as four temperature arms — the only way to
treat temperature as a real factor rather than a plate-level confound.
The four are **3 × 96-well + 1 × 384-well** and all four run independent
programs at once. The 384 block takes **5–20 µL** against the 96 block's
**10–100 µL**, so both of the DOE's volume levels fit it; give the 384 arm
the 5 µL runs. At production scale the arms stop being the point and the
**37 °C SteriStore** is: 288 standard positions of static incubation, at up
to 98% RH, against four cycler blocks.

### 4.4 *E. coli* expression, arrayed

For designs cell-free will not make. Autoinduction avoids timed IPTG and
suits unattended overnight running.

*Deck:* MultiFlo inoculates → **a4s** applies the gas-permeable seal →
**Cytomat 2** shakes and incubates overnight → HiG 3 pellets → MultiFlo
lyses → HiG 3 clears · *Waits in:* SteriStore
4 °C (grown blocks), SteriStore 37 °C (static recovery), AmbiStore
*Gives:* lysate ready for purification
*Costs:* nothing on the Bravo, Echo or reader. It is limited by the
**Cytomat** — 14 deep-well positions, **7 concurrent** culture protocols,
and that is the hard cap on the whole *E. coli* route
*Note:* a foil seal off the PlateLoc takes a 20 h deep-well culture
anaerobic, which is the whole reason the system carries **two sealers** —
the a4s holds the gas-permeable roll while the PlateLoc holds foil, and
neither needs a manual change mid-run. Growth goes on the **Cytomat**, which
shakes and incubates. The Bravo deck nests hold fixed temperatures and do not
aerate, so they are not the growth position.
*Yeast is already in range.* The C-LiN series runs to 50 °C (70 °C on the
C470) and the unit has to reach 37 °C for *E. coli* anyway, so **30 °C costs
no hardware** and a third expression route in Aim 1 is a scheduling change,
not a purchase. What is worth a growth curve first is the **orbit**: 1–3 mm
at 100–1200 rpm is a mammalian-suspension spec, and published deep-well
microbial protocols run 25 mm. The Selector variant offers it.

### 4.5 Magnetic bead purification

His-tag on Ni-NTA or IMAC magnetic beads, on the Bravo magnet.

*Deck:* Bravo + magnet, three washes, elute, with the **BioShake**
resuspending beads between washes without the plate leaving the deck ·
*Waits in:* MicroServe, SteriStore 4 °C, AmbiStore
*Gives:* **micrograms**, which is plenty for plate assays
*Costs:* **60 min of Bravo time per 96-well plate** — Ginkgo's own figure is
96 lysates an hour. This is the single most expensive hour on the system: a
full 14-plate *E. coli* round is a **14 h serial step**. **Heat lysis** at
95 °C in a 96-well ATC block removes it outright, 14 h → 2.1 h, which is the
strongest argument in §4 for adopting it.
*And not the Magniflex.* Despite the name, a Tecan **Cavro Magni Flex** is
an OEM pipetting framework — 2, 4 or 8 independent channels, tip spacing
variable from 9 to 445 mm, Cavro Pulssar PBC piston pumps over 5–1,000 µL —
with no magnet in it. Bead separation is the Bravo's. What the Magniflex is
genuinely the only thing on the system for is **positive-displacement
transfer from tubes at variable spacing**: glycerol-based enzyme master
mixes, viscous reagents, and anything the Echo refuses.
*Not:* milligrams. Crystallography protein cannot come from here.

### 4.6 Protein QC without a gel

Concentration from **GFP11 complementation**, on the same standard curve
as D1; aggregation from a **fluorescence-polarisation** read on the
complemented species. Both on the PHERAstar, one plate, two reads, no new
hardware. Purity as band identity still needs a gel on a subset, offline.

*Not A280, and this was tested rather than assumed.* At D2's 2 µg floor in
a 50 µL eluate, a typical ProteinMPNN mini-binder — 1 Trp, 2 Tyr, ε280
≈ 8,730 — gives **A280 = 0.012 against about 0.005 AU of reader noise**.
Eluting into 10 µL rescues it (0.062) but only for designs with enough
aromatics, and ε280 varies several-fold across designs, which would make
them incomparable. GFP11 reads identically for every design. A280 is
recorded alongside as a cross-check wherever the design's own computed
ε280 puts it above roughly 0.05 AU.

*And no A260/A280.* It is a ratio of two near-noise numbers at this
concentration, and residual nucleic acid does not interfere with NanoBiT
or HTRF. The check belongs on the structure path, where it matters.

*The FP window is narrow, and that is physics.* GFP's ~3 ns lifetime on a
~41 kDa complemented species sits close to the limiting anisotropy: Perrin
gives **427 mP for the monomer against a 490 mP ceiling** — dimer +29,
trimer +40, gross aggregate +63. Against ±3–5 mP of reader precision a
dimer is still 6σ, so the read works; it just detects aggregation rather
than oligomer-level change. Read it knowing that.

*Deck:* MultiFlo → PHERAstar ×3 reads → **Lynx LM900 VVP** ·
*Waits in:* MicroServe, AmbiStore
*Costs:* 24 min of reader — three reads of the same plate
*Then normalise.* The **Lynx** is the only variable-volume channel on the
system and its job in the Q&A is exactly this: **concentration
normalisation before assay**. 1 µL minimum, **2 µL at 2% CV**. Run it off
these numbers and D3's concentration series starts from a flat plate instead
of from whatever each well happened to express.
*Why the Lynx and not the Bravo.* **Volume Verified Pipetting** puts an
in-line flow sensor on every channel and measures what was actually
aspirated and dispensed, per channel, in real time. A normalised plate is
therefore *measured*, not nominal, and the per-well correction can be logged
against the design — which is what makes D3's concentration series
comparable between campaigns. 96-channel and 8-channel VVP heads, three tip
types (35 / 300 / 1200 µL, filter tips included), tip detection per channel.
*And there is a precedent.* Ginkgo's HiBiT application note ran ~10,000
samples on a RAC carrying **a PHERAstar FSX** — our RAC 13 — with 7,680
quantified unattended, and reported machine-normalised concentrations
averaging **2% from the prior semi-automated protocol**. That is the claim
this step rests on, measured by the vendor on our reader. See
[reference/ginkgo-published.md](reference/ginkgo-published.md) §3.

### 4.7 Binding — the assay ladder

Four homogeneous formats, in the order you should reach for them.

**NanoBiT / split luciferase.** LgBiT on the target, SmBiT on the
design; interaction reconstitutes luciferase. Luminescence, enormous
dynamic range, no antibody, cheap, and **it reads straight out of a
crude cell-free reaction** — no purification at all. This is the deck's
natural first screen.

**HTRF.** Tb or Eu cryptate donor on an anti-tag antibody, d2/XL665
acceptor. Ratiometric at 665/620, which cancels most well-to-well
optical variation, and tolerant of crude matrix. The PHERAstar has the
high-end TRF module. This is the workhorse for the PARP14 campaign, and
protocols already exist at low throughput.

**AlphaScreen.** Donor and acceptor beads, singlet-oxygen transfer over
~200 nm. The most sensitive of the four and the laser is already in the
PHERAstar quote. Light-sensitive, bead-dependent, and shows a hook
effect at high concentration — read it knowing that.

**Fluorescence polarisation.** A small labelled tracer tumbles fast and
depolarises; bound to something large it slows and polarisation rises.
Needs roughly a tenfold mass ratio, so it is for peptides and small
molecules, not protein–protein pairs of similar size. Doubles as the
aggregation readout in 4.6.

*Deck for all four:* Echo dispenses protein and titrant → MultiFlo adds
detection reagent → PlateLoc → short incubation → PHERAstar

All four need protein in hand. **CF2H (§8) sits below the ladder**: it
makes both proteins and reads the interaction in the same well, with no
purified material at all, at the cost of giving a rank rather than a
number.
*Scale:* 384 routine, 1,536 reachable — the PHERAstar covers 6 to 3,456
wells and the Echo handles 1,536
*Costs, and this is the same for 4.8 and 4.9:* 3 min of Echo, 8 min of
reader, **nothing on the Bravo**. Tipless in, one read out. This is the
cheapest thing the foundry does per design, and it is why the ceiling that
actually binds the Test stage is the reader's 150 plates a day, not the
Bravo's 75. 4.8 is three extra columns on 4.7's plate, so in practice it
costs nothing new at all.

### 4.8 Counter-screen and competition

Same plate, same chemistry, extra columns: the counter-target, the
non-binder control, the **hotspot mutant of your own target**, and the
**standing promiscuity panel** — lysozyme, ubiquitin and MBP, unchanged
between campaigns, which is what makes a specificity index comparable
across targets and across labs. See
[reference/design-quality-invariants.md](reference/design-quality-invariants.md).
Competition format — unlabelled competitor titrated against a fixed
tracer — gives IC50 and tests epitope access without a second assay
platform. Both halves of this are now validated in a plate-reader
format: see §8, where single-residue mutants rank by ΔΔG and a tight
small molecule displaces a designed binder.

### 4.9 Dose–response

Echo builds the dilution series acoustically in the destination plate.
No serial pipetting, no tip-to-tip carryover, arbitrary non-linear
spacing if you want it. This is the single thing the Echo is best at.

### 4.10 Thermal stability

**Not available as DSF.** Neither the Applied Biosystems ATC (96 or 384)
nor the common on-deck alternative has optical detection, so melt curves
have nowhere to be read. Options: nanoDSF as a separate instrument (what
Adaptyv uses for its thermostability product), or a thermal-challenge
assay — incubate aliquots at a temperature ladder on the four ATCs, then
read residual binding on the PHERAstar. The second needs no new hardware
and is a genuine stability readout, just not a Tm.

*Costs:* 32 min of reader — four plates, four rungs. The fourth rung is the
**384-well** block, which caps at ~30 µL; keep the ladder's fill volume
inside that or run three rungs.

### 4.11 Crystallisation screening

**The RAC does not make crystallography protein — it screens it.**
Purified protein at milligram scale and 10+ mg/mL comes in from
offline expression. The deck then does what it is extremely good at:
nanolitre drop setting with the Echo into SwissCI plates, condition
matrices, co-crystallisation against soaking, and fragment screening
from DMSO stocks.

*Deck:* offline → Echo dispenses → offline · *Waits in:* AmbiStore
*Costs:* ~9 min of Echo a tray — 80 trays is 11.5 h on-system, against
48.9 h once imaging is done by hand
*Needs:* the Echo 6XX, not the 525 — the 525 cannot do DMSO, 1536, or
the drop volumes crystallography needs. Imagers and automated scoring
are still unquoted; Fraser lab instruments cover the interim.
*How a wet tray is closed:* with a **lid**, not a seal. Both sealers on the
system are thermal — PlateLoc 30–200 °C, a4s 100–195 °C — and a 200 nL drop
has no thermal mass to survive either. Trays live in the **AmbiStore**,
which is why that unit is configured with 216 standard positions: 100–150
rotating crystallography trays plus ≥50 deep-well of bulk precipitant. It is
a random-access carousel with up to six transfer nests that returns a plate
in as little as 12 seconds, which is exactly the access pattern a rotating
tray library wants.

### 4.12 Compound and fragment screening

The same Echo-plus-PHERAstar spine, with compound plates instead of
design plates. Essentially free once 4.7 works, and it is what makes the
foundry useful to labs that are not designing proteins at all. Compound
source plates sit in the **AmbiStore** between runs.

*Costs:* 3 min Echo, 8 min reader — the same plate cost as 4.7 for four
times the wells, which is the whole argument for 1536.

### 4.14 Heat-shock transformation

**The deck does heat shock.** The **Bravo** carries two temperature-controlled
deck positions held at **4 °C and 42 °C** — QInstruments Peltier blocks,
−20 °C to 99.9 °C, 12 K/min — and the 45-second pulse is a plate move between
them.

Two fixed positions rather than one ramping block is the whole trick. A
single block takes about three minutes to go from 4 °C to 42 °C at 12 K/min,
and a thermal cycler in another RAC cannot time a 45-second step at all. Two
plates, both multi-temperature, one move.

*Deck:* Echo doses DNA into cold cells on the 4 °C nest → Bravo moves the
plate to the 42 °C nest, 45 s, and back → MultiFlo adds SOC → BioShake mixes
→ Cytomat recovers, 1 h at 37 °C shaking → a4s lids agar plates → offline ·
*Waits in:* SteriStore 4 °C, MicroServe, AmbiStore
*Gives:* transformants in liquid — a pool, or one well per design
*Costs:* 24 min of Bravo per 96-well plate. The pulse is a deck move, so the
whole transformation is Bravo time and it comes off the same ~75 protocols a
day as everything else.
*Scope:* transformation **and plating** are in, and so is *E. coli*
expression (§4.4). **Colony picking is out**, so plating is for titre and QC
and nothing returns a clone to liquid — which is why §2's cassette is built
to be recovered by PCR.

**What this makes possible.** The `pET21b/29b/22b/28a` and `pSB4k5`
backbones in `reference/constructs.md`, Route C as a live route alongside
cell-free, and pooled library builds that need to amplify through cells
(§4.2). Competent cells arrive cold on the day and are held in the **4 °C
SteriStore**, which is the coldest position on the system.

---

## 5. The loops

**This section is also on the page.** `data/protocols.yml` carries each loop
as steps coloured by where they run, and `dist/workflows.html` draws them.

Five, nested, each returning something different.

**Expression loop.** Fractional-factorial screen → effect sizes →
Bayesian optimisation around the best region → fixed condition. Closes
in days. Feeds a model that assigns each *new* target an expression
route — which is Aim 1's real product, not the condition itself.

**Binder loop.** Design → express → screen → confirm → counter-screen →
retrain on every measured design, failures included. Closes in weeks.
A design that did not express is not a non-binder: keep **three**
outcomes, the way Adaptyv does with True / False / Unknown.

**Affinity-maturation loop.** NNK library around a confirmed hit → same
assay → ranked variants. Closes in weeks. This one genuinely wants
pooled handling and is the strongest argument for settling NGS.

**Structure loop.** Hits → offline scale-up → crystallisation screen →
diffraction → solved interface compared to the design model → filters
promoted or demoted. Closes in months, and it is the only loop that
tells you whether the models are right about *where*.

**Compound loop.** Fragment or compound screen → hits → co-crystallise →
structure → chemistry → rescreen. Not your programme, but it is what
makes the foundry a service rather than a project.

---

## 6. What the foundry cannot do

Worth stating plainly, because every one of these appears somewhere in
the Baker or Adaptyv pipelines you would otherwise copy.

- **FACS, and therefore yeast-display selection.** The entire Baker
  screening route depends on it. Their library sizes (10⁶–10⁹) are
  unreachable here.
- **Kinetics.** No BLI or SPR. You get endpoint and equilibrium, not
  kon/koff. Hits that need kinetics go offline. CF2H does not change
  this — it ranks, it does not measure. The one instrument that would
  fill this gap *from crude lysate* is a FIDA, which returns K_D, k_on
  and k_off per design off 1 µL of unpurified cell-free. It is an
  off-rack purchase, not a deck change — see §9.1.
- **NGS.** Undecided, and it gates every pooled workflow — but less of it
  than this list implies. Ginkgo has published Illumina DNA Prep miniaturised
  100-fold and run end-to-end on RACs, upstream microbial lysis included, so
  **library prep on the deck is a solved workflow**. What is actually open is
  the *sequencer*: in-lab Nanopore or a campus core.
- **Chromatography.** No FPLC, no SEC, no SEC-MALS. Oligomeric state and
  aggregate fraction are offline questions.
- **Colony picking**, and so clonal isolation from any transformation. Not
  permanent, though: Ginkgo's yeast transformation note puts colony picking
  out of scope "and can be onboarded with further expansion of the RAC
  system", so this is a cart we have not bought rather than a thing the
  platform cannot do.
- **Milligram protein.** Mag beads from 96-well give micrograms.
- **Mammalian and CHO**, which rules out the Fc-fusion format BindCraft
  used for its PD-1 validation.
- **Nothing, as far as shaking incubation goes** — that was wrong in an
  earlier draft. The Cytomat 2 shakes and incubates, and it is the growth
  position. The open question is only its temperature range.
- **Frozen storage, as configured.** The coldest position on the rack is the
  **4 °C SteriStore**, so competent cells and enzyme stocks arrive cold on the
  day. Worth knowing: the AmbiStore chassis is also specified down to
  **−20 °C**, so frozen storage is a configuration away rather than a new
  instrument, if it is ever wanted.
- **More than ~75 two-plate protocols in a day** (§4.0). That is the Bravo,
  and it is tied with the PHERAstar's 150 plate reads. It is not a gap in
  capability but it is a hard limit on how much of §4 runs in parallel, and
  every `cost:` in `data/protocols.yml` is quoted against it.

---

## 7. What unlocks what

| Add | Unlocks |
|---|---|
| **NGS path** — the *sequencer*, since Ginkgo has published library prep on RACs | all of Route B, pooled screening, affinity maturation at scale |
| **Echo 6XX** instead of 525 | Aim 3 entirely, plus 1536 and DMSO work |
| **nanoDSF** | thermostability as a product, the way Adaptyv sells it |
| **FIDA Evolve**, off-rack (§9.1) | kinetics and aggregation state from crude cell-free, no purification or immobilisation — but serial, ~58 designs/day, single vendor, and not in the quote |
| *(done)* **the Cytomat reaches 30 °C** — the C-LiN series runs to 50 °C | yeast expression as a third route in Aim 1, at no hardware cost. What is left is the 1–3 mm orbit, not the temperature |
| *(done)* **two temperature-controlled Bravo nests** at 4 °C and 42 °C | heat-shock transformation (§4.14), Route C and every plasmid backbone — a capability the deck has, not a decision outstanding |
| **A second 384-well ATC** — a swap, not an extra unit, so probably price-neutral | retrieval PCR at 384 off the Echo: 3 plates instead of 12 for 1,152 designs, cycler time 10 h → 6 h. Keep two 96 blocks: the 384 block takes 5–20 µL and Golden Gate, heat lysis and held-temperature steps need 10–100 µL |
| **A 384-channel Bravo head** | removes the 4× cost of 384 format on the bottleneck instrument, which is the ceiling in §4.0 |
| **Heat lysis at 95 °C** in a 96-well ATC block | deletes 4.5's 14 h bead step from the *E. coli* route, 14 h → 2.1 h. Costs nothing and is already on the deck |
| **Plate-scale CE** (LabChip class) | purity per well, rather than on a subset |
| **Crystal imager + scoring** | Aim 3 unattended, 24-hour |
| **ΔRecBCD extract + a CI/pRM reporter plasmid** | CF2H (§8): expression and binding in one well, no purified protein, no purified target |
| **FACS** | the Baker route — probably not worth it; it is a different foundry |

---

## 8. CF2H — read in full, and worth building

Delauriere et al., *CF2H: a cell-free two-hybrid platform for rapid
protein binder screening*, Nat Commun 2026.
<https://doi.org/10.1038/s41467-026-69741-1> (via PubMed Central,
PMC13103306). Read in full on 2026-11-16 — everything below is from the
paper, not the abstract.

It is the closest published match to this deck of anything surveyed
here, and the reason is one sentence from their discussion: *the setup
requires a set of pipettes and a microplate reader.*

### What it is

Lambda phage CI is a transcriptional activator that only works as a
dimer. Its DNA-binding domain (residues 1–92) is monomeric and inert on
its own. Fuse that DBD to a bait and to a prey through a flexible
GGSx5 linker; if bait and prey interact, the two DBDs are brought
together, the pair binds the OR1 and OR2 operators of the pRM promoter,
and contacts σ to fire transcription. A reporter plasmid in the same
tube carries sfGFP behind pRM, with the third operator (OR3) knocked
out so the promoter is not repressed at high CI. Binding becomes green
light.

Everything happens in one pot: both proteins are translated from linear
DNA in the same cell-free reaction that reads them out. There is no
purification, no immobilisation, no antibody, no bead, no labelling
chemistry, and no wash step.

### How it actually runs

- **Lysate**, not PURE. *E. coli* BL21 Rosetta 2 **ΔRecBCD**, homemade
  S30 extract. The strain deletion is what makes linear DNA survive, so
  no GamS is needed. Their buffer optimum: **15 mM Mg-glutamate,
  100 mM K-glutamate** — inside the bracket of the D1 screen.
- **DNA**: eBlocks (IDT) or Gene Fragments (Twist), PCR-amplified with a
  high-fidelity polymerase, checked on a gel, quantified by Qubit,
  normalised to 50 nM. Never cloned. Never sequenced.
- **Reaction**: 22 µL assembled on ice — ⅓ extract, 5/12 buffer, ¼ DNA
  and additives. Reporter plasmid at 5 nM, each linear fragment at
  2.5–5 nM.
- **Plate**: **5 µL per well** into a 384-well black-wall /
  clear-bottom low-binding plate, sealed with a *transparent* adhesive
  film.
- **Read**: 37 °C, Ex 485 / Em 528. Signal is detectable in under 2 h
  and plateaus by 8 h. Fluorescence converted to FITC mean-equivalent
  units against a FITC standard curve so numbers survive a change of
  reader.
- **Cost**: €0.10 per reaction on homemade extract — under €10 for a
  whole binder screen — or €5–10 per reaction if you buy lysate.

**Deck sequence:** Echo dispenses the two linear DNAs, the reporter
plasmid and any competitor compound → MultiFlo adds the cold
extract/buffer master mix → PlateLoc seals with a **clear** seal →
PHERAstar holds 37 °C and reads the kinetic. No ATC, no XPeel, no
MicroServe round trip. Four unit operations and one instrument doing the
work. The 5 µL volume is why it fits: acoustic transfer plus one bulk
dispense is the whole liquid-handling problem.

**One scheduling catch:** an 8 h kinetic read occupies the PHERAstar for
the day. A 4 h endpoint recovers most of the discrimination and frees
the reader — worth deciding before this goes on a shared schedule.

### The call

A design counts as a binder at **more than twofold signal over the same
design run without its target.** That control is per design, not per
plate, and the reason is in the limits below.

### What the benchmark actually showed

They re-screened 48 designs from Watson et al. — 36 aimed at human Mdm2
plus **12 designed against an unrelated target (IL-7Ra) as decoys.**

- 17 of the 24 that single-point BLI called binders were confirmed.
- 6 of the 12 that BLI called *non*-binders scored as binders here.
- **0 of the 12 decoys gave signal.**
- Mean signal-to-noise 5.1, against 7.8 for single-point BLI.

Several of the misses were traced to systematic DNA synthesis errors,
not to the assay.

Then a real campaign: 100 BindCraft designs against murine PD-L1, top 36
by i_pTM screened, **7 hits**, two confirmed by SPR at 6.85 nM and
**0.78 nM**, and the best one blocked PD-1/PD-L1 in a cell assay at
28 nM IC50. That is a ~19% hit rate from one-shot AF2 design, found on a
plate reader.

### Three formats, in order of how hard the target is

1. **CI–target + CI–binder.** Simplest. Works for most targets.
2. **CF2H-multimer.** For a target that aggregates: drop the CI fusion
   on the target and fuse it instead to a multimerisation domain, with
   CI only on the binder. The p53 tetramerisation domain and a hexameric
   coiled-coil gave ~3× the signal of the CI–target format. A GCN4
   dimer did not work — valency above two is what matters.
3. **Streptavidin-templated.** Do not express the target at all. Buy it
   biotinylated, pre-mix 1:1 with streptavidin at 150 nM, spike the
   tetramer into the reaction. Best signal-to-noise of the three, and it
   removes target expression from the problem entirely.

Format 3 is the one to notice. Commercial biotinylated ectodomains are
catalogue items, and this turns "can I express my target?" into "can I
buy it?".

### Limits, stated plainly

- **Upper limit ~100 nM.** Interactions weaker than that are not
  reliably detected. This is a high-affinity filter, not an affinity
  assay. It inherits the constraint from CI itself, whose own
  interactions sit in the low-nanomolar range.
- **It saturates at the bottom.** Sub-nanomolar binders cannot be ranked
  against each other.
- **Signal is not affinity.** Expression, solubility and stability all
  feed the same number. The authors argue that is a feature for
  prioritisation, and it is — but it means the output is a rank, not a
  measurement, and it must never be fitted as one.
- **Self-activation is real.** Designs that homodimerise or aggregate
  fire the reporter with no target present. One of 36 Mdm2 designs and
  two of 36 PD-L1 designs did this; both PD-L1 offenders were
  beta-rich. Hence the per-design no-target control — and note that this
  failure mode is itself a free readout of self-association.
- **Linear DNA is unsequenced.** Synthesis error shows up as a false
  negative with no warning.

### What it maps onto here

- **It collapses expression and binding into one well.** D1 and D4
  answered by the same measurement, same day.
- **Alanine scanning works.** Single-residue mutants of a binder gave
  ΔActivation values that tracked ΔΔG measured by SPR, and ranked
  mutants by affinity correctly. That is the hotspot question — *did it
  bind where it was designed to?* — answered on a plate reader, which is
  exactly what the PARP14 MD1 campaign lacked.
- **Competition works when the competitor is tighter.** Venetoclax
  displaced a designed BCL2 binder with an IC50 of ~202 nM. The Mdm2
  inhibitor, at comparable affinity to the binders, only displaced the
  weakest of three. For MD1, a known macrodomain-site ligand would give
  an orthogonal site test with no mutant construct at all — but only if
  it is substantially tighter than the binder.

### What it would cost to stand up

No hardware. The build is: a pRM/OR3\*–sfGFP reporter plasmid, a CI(1–92)
DBD cassette with the GGSx5 linker, and either a homemade ΔRecBCD
extract or a commercial lysate with GamS. All cloning and extract work,
all offline, all cheap.

**But it is not free in machine time**, and it is the one exception in the
Bind phase. CF2H needs the cold master mix pipetted into a 384-well plate on
the **Bravo** — four offset quadrant transfers, **32 minutes of the system
bottleneck per plate**, against 3 minutes for the Echo-built plates in 4.7,
4.8, 4.9 and 4.12 (§4.0). At 36 designs a plate in triplicate that is an
expensive ratio. The ordering constraint is real — every DNA component goes
in before the cold mix — but if the mix itself can be made Echo-compatible,
moving it is worth more than any other change to this protocol.

One construct note: a CI fusion is about 700 bp with promoter and RBS,
so it still fits in a single eBlock — order the fusion, do not try to
append the DBD by PCR. But a CF2H construct is **not** the standing
split-GFP11 / Twin-Strep cassette from §2, and the sfGFP reporter would
collide with a split-GFP expression readout anyway. Pick the readout at
order time, per campaign.

---

## 9. Future plans — expanded capability, off the rack

The rack is fixed at install. Everything in this section sits **beside**
it: an instrument on its own bench, fed by a plate a person carries over,
returning numbers that come back into the per-design table by file. That
is the honest model for anything bought after April 2027, and it is not a
compromise — §4's `offline` workflows already end this way, in a sample
prepared for something off the rack.

### 9.1 FIDA — the kinetics gap, filled from crude lysate

**What it is.** Flow-induced dispersion analysis. A fluorescent sample is
drawn into a 75 µm capillary and pushed past a detector; how much the plug
spreads gives the hydrodynamic radius in nm, with no calibration, no
immobilisation and no wash. Binding makes the species bigger. Full detail,
including the Ginkgo-quote comparison, is in
[reference/fida-instrument.md](reference/fida-instrument.md); the
published pipeline it comes from is in
[reference/fida-pipeline.md](reference/fida-pipeline.md).

**Why it is the one worth adding.** §6 says the foundry has no kinetics —
no BLI, no SPR, endpoint and equilibrium only. FIDA is the only instrument
found so far that closes that from **unpurified cell-free reaction**,
1 µL into 99 µL of buffer, and returns K_D, k_on, k_off, absolute size,
aggregation state and expression level from the same wells. In gate terms
it is **D5 and most of D2 in one pass**, on the designs that already
cleared D4.

**Why it is off-rack, not on it.** Three reasons, and only the first is
about the instrument:

1. It is **serial**. ~24 data points per 30 minutes, about 58 designs a
   day. Nothing is gained by feeding it from a scheduler that can deliver
   a 384 plate every few minutes.
2. There is **no public record of Ginkgo integrating a Fida instrument**.
   RACs are vendor-agnostic, but this would be a first, and Ginkgo's own
   note is that new device integrations take months.
3. The sample is **not consumed**. ~40 nL out of a 2 µL fill, through a
   shared capillary that is washed between samples. A plate can be
   carried over, run, and carried back.

**What it costs.** Fida publishes no list price; the working figure is
held in the internal repo. Against the quoted PHERAstar FSX it is
about 1.3x, and about 9.5% of the third-party
instrument line. **It is not in the Ginkgo quote and should not be added
to it** — buying it separately is what keeps it off the rack.

**The one thing that could sink it.** FIDA sees binding as a change in
radius. Below about 5% change the signal is hard to call. A small binder
on a large target is the good case; a small target on an FP-fusion binder
is the bad one. Several foundry campaigns are the bad one.

### TODO before this becomes a purchase case

- [ ] **Ask Ginkgo directly**: has any RAC ever carried a Fida instrument,
      and what would integration cost in months and dollars? Goes on the
      standing question list.
- [ ] **Resolve the API sentence.** Fida advertise "REST API with built-in
      SiLA driver". SiLA 2 runs on HTTP/2 and protocol buffers, not REST,
      so that names two different things. Ask which Catalyst would speak.
- [ ] **Get a real quote** for an Evolve: detector configuration, capillary
      cartridge price *and lifetime*, service contract, the PC. None of
      those are published and all four are recurring.
- [ ] **Confirm the Evolve specs.** Everything currently recorded for
      temperature range, throughput and minimum fill is a **Fida Neo**
      figure carried forward. Do not put Neo numbers in a 2027 purchase
      case.
- [ ] **Run a demo on our own material** before committing: one real
      binder–target pair from a foundry campaign, in crude cell-free, to
      see whether ΔR_h clears the ~5% floor on a target we actually care
      about.
- [ ] **Decide the fusion at campaign level.** FIDA reads crude lysate
      because the construct carries a *whole* fluorescent protein. The
      standing cassette in §2 is split-GFP11, which is the right choice
      for a plate assay and the wrong one here. This is an order-time
      decision, not a cassette change.
- [ ] **Decide bench and room.** 500 × 610 × 497 mm plus a PC, and tray
      cooling to 5 °C assumes a room at 22 °C or below. Check against the
      499 Illinois floor plan.
- [ ] **Decide how results return.** Which plate format travels, who
      carries it, and how a FIDA output file joins the per-design table
      without a human retyping anything.
- [ ] **Add the workflow** to `data/protocols.yml` as an `offline` entry
      once an instrument exists — not before, or it renders as a deck chip
      for hardware nobody owns.
- [ ] Still unfetched: the Fida comparison-table PDF (may carry weight and
      power draw) and the Evolve webinar.

### 9.2 Everything else on the list

§7 holds the full unlocks table. Of those, the ones that would also be
off-rack purchases rather than deck changes are **nanoDSF**,
**plate-scale CE**, and any **chromatography**. The ones that are not
hardware at all — the NGS path decision, confirming the Cytomat
temperature range — should be settled first, because they are free and
they gate more.
