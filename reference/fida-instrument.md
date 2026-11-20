# The FIDA instrument

What it is, what it does, and what it would mean on this deck. Specs are
from the vendor's own Fida Neo brochure, the Fida 1 specification sheet
(Jan 2022) and the current fidabio.com product page, read 2026-11-16.
**Vendor material — the performance claims are theirs, not measured here.**

---

## First: there are three generations, and the paper used the middle one

| | **Fida 1** | **Fida Neo** | **Fida Evolve** |
|---|---|---|---|
| Status | superseded | what the DTU paper used | **current product** |
| Size accuracy | not stated | 5% change detectable | **1% change** |
| Detector | multiple wavelengths | 3 swappable LED modules | click-on, integrated, smaller footprint |
| Autosampler temp | 4–55 °C (both chambers) | 5–50 °C | **5–95 °C, ±1 °C per tray** |
| Capillary chamber | — | 15–45 °C | 15–55 °C |
| Pressure | 1–3500 mbar | 1–3500 mbar | **1–4000 mbar** |
| Minimum sample | 10 µL | 10 µL | **2 µL** |
| Capillary swap | manual | manual | click-on cartridge, semi-automated |
| Automation | — | not stated | **an API with a built-in SiLA driver** |

Detector modules are listed inconsistently by the vendor: the specification
page gives **280 nm (UV, label-free), 480, 530 and 640 nm**; the product page
lists only UV, 480 and 640. Size range is given as 0.5–500 nm in one place and
0.3–500 nm in another. Small discrepancies, but confirm before quoting.

**Do not quote Neo numbers in a 2026 purchase case.** The Evolve claims
five times the size resolution and, far more importantly here, ships an
API. More on that below.

---

## The principle

![How FIDA measures size](images/fida-principle.svg)

It is **Taylor dispersion**, measured by fluorescence.

A plug of fluorescent sample is pushed through a narrow fused-silica
capillary under pressure. Flow is laminar, so liquid at the centre moves
faster than liquid at the walls and the plug smears into a parabola. At
the same time molecules diffuse sideways, sampling fast and slow
streamlines and averaging the smearing out.

**How much averaging happens depends on how fast the molecule diffuses,
which depends on its size.** A small molecule diffuses quickly across the
bore, averages the velocity profile well, and arrives at the detector as a
narrow Gaussian. A large one diffuses slowly, samples the profile poorly,
and arrives broader. Fit the Gaussian, get the diffusion coefficient, get
the **hydrodynamic radius in nanometres — absolutely, with no calibration
standard.** The vendor calls this "first principle"; the physics is
genuinely standard.

Binding makes the fluorescent partner bigger. Titrate, watch Rh rise,
fit the curve, get K_D. Change the pressure programme so the complex has
less time to re-equilibrate inside the capillary, and the shifted curve
gives you k_on and k_off.

**That last move is the clever one.** The same prepared samples give both
the equilibrium curve and the kinetic curve — you re-run the plate under a
different pressure programme rather than preparing anything new.

---

## Specifications — Fida Neo

| | |
|---|---|
| Detection | fluorescence; **UV label-free, 480 nm, 640 nm** LED modules, swappable by the user |
| Limit of detection | 100 pM FITC in PBS at SNR > 30 (480 module); 1 nM Cy5 (640 module) |
| Signal-to-noise | > 30; claimed 3× the previous generation |
| **Size range** | **Rh 0.5 – 500 nm** |
| Size accuracy | 5% change detectable |
| **Affinity range** | **pM – mM** |
| Kinetics range | seconds to hours |
| Sample capacity | **up to 2 × 96 per run** |
| Sample consumption | **as little as 4 µL analyte, 40 nL indicator per data point** |
| Assay length | ~4 min |
| Pressure | 1 – 3500 mbar |
| Autosampler | 5 – 50 °C |
| Capillary chamber | 15 – 45 °C |
| Capillary | fused silica, dynamic or permanent coating |
| Power | 120–240 VAC, 50/60 Hz |
| Control | Windows, proprietary Fidabio suite; PDF and .txt export |

From the **Fida 1** sheet, which states some things the Neo brochure does
not: molecular weight range **100 Da to ~10⁶ Da**, indicator detection
limit ~0.1 nM, and throughput of **24 data points in under 30 minutes**,
or **8 binding curves × 8 points in triplicate — 192 points — in 4 hours
unattended.**

---

## Physical — it is a benchtop box, and it is published after all

From Fida's knowledge base, *"How much bench space do I need?"*:

| Model | Footprint (W × D) | Height |
|---|---|---|
| **Fida Evolve** | **500 × 610 mm** | **497 mm** |
| Fida Neo | 520 × 610 mm | 490 mm |
| Fida 1 | 430 × 670 mm | 480 mm |

**Plus space for a PC**, which the vendor notes but does not size. One
environmental requirement is stated: **cooling the trays to 5 °C assumes a
room at 22 °C or below** — fine for a Mission Bay lab, worth checking against
the heat load of fifteen RACs in one room.

Half a metre square and half a metre tall puts it in the same class as a
plate reader. **So the size is not the obstacle. Plate access is.**

**Still not published anywhere:** weight, power draw or circuit requirement,
required clearance or ventilation, heat output, bench load rating, **how
plates are loaded** (door, drawer, open deck), the sample-tray format, and
**price**. Pricing is quote-only through a configurator. A comparison-table
PDF exists on their CDN and may hold weight and power; it has not been read.

---

## What it measures, per sample, in one run

This is the part that makes it interesting rather than just another
affinity instrument. The vendor claims **8 QC parameters on every
measurement**, free:

| Readout | What it tells you |
|---|---|
| **Hydrodynamic radius** | absolute size in nm, no calibration |
| **Binding affinity** | K_D from a titration |
| **Kinetics** | k_on and k_off from the same samples, different pressure programme |
| **Aggregation** | aggregates are resolved and quantified while the core signal stays usable |
| **Polydispersity index** | sample heterogeneity |
| **Stickiness** | peak shape reveals adsorption of your protein or complex |
| **Viscosity** | measured every run, and compensated for |
| **Labelling efficiency** | free versus conjugated fluorophore, up to 3 species |
| **Quantity** | concentration, pM–mM |
| **Sample loss** | how much material never made it |

For a foundry whose whole problem is *standardised per-design data*, a
single measurement that returns size, aggregation state, concentration and
affinity together is a better match than any of these readouts separately.

---

## PHERAstar FSX vs FIDA Evolve

One is quoted and on the rack. The other is not in the quote.

| | **PHERAstar FSX** | **FIDA Evolve** |
|---|---|---|
| **Price** | in the Ginkgo quote | not quoted; Fida publishes no list price. Figure held in the internal repo |
| **Relative** | 1 | **1.3 ×** |
| **In the the third-party instrument total instrument line** | yes | no — would add ~9.5% |
| **What that price includes** | High-End TRF/HTRF module, TR-FRET laser (a priced option), HTS AlphaScreen laser (a priced option), AS-680-570 + AS-680-615, TRF-337-665-620, FP-485-520-S20 | 3 detectors (280 / 480 / 640 nm); software free, not a line item |
| **Not in that price** | — | capillary cartridge cost and lifetime, service contract, PC, Ginkgo integration |
| **Reads** | 6 to 3,456 wells, whole plate at once | 2 × 96 positions, one well at a time |
| **Throughput** | a 384 plate in minutes | ~24 data points / 30 min; ~58 designs / day |
| **Needs purified protein** | usually | **no — crude lysate** |
| **Needs immobilisation** | no | no |
| **Needs a detection reagent** | yes | no |
| **Sample consumed** | the whole well | **~40 nL**, from a 2 µL fill |
| **Consumable per sample** | detection reagent | none — one shared capillary, washed |
| **Parameters per sample** | 1 | **~10** |
| **k_on / k_off** | no | **yes** |
| **Absolute size (nm)** | no | **yes, uncalibrated** |
| **Aggregation state** | no | yes |
| **Temperature** | incubator tops out at 45 °C | autosampler 5 – 50 °C, capillary 15 – 45 °C *(Neo figures)* |
| **Footprint** | benchtop | 500 × 610 × 497 mm + a PC |
| **On the RAC** | quoted and integrated | never integrated by Ginkgo; new devices take months |
| **Role** | primary screen, hundreds | second-tier, on the dozens that survive |

Sources: Ginkgo draft quote (PHERAstar line and option prices); public
procurement awards (Aarhus University 2026, DTU 2023) for the FIDA price,
recorded in the internal repo; Fida Biosystems Evolve datasheet for
everything non-price. Rows marked *(Neo figures)* are not Evolve-confirmed.

---

## How the sample actually gets in

**You never pipette into the instrument.** You fill a plate, the plate goes
into a temperature-controlled autosampler, and the capillary sips from the
well.

In the DTU run that meant 1 µL of crude cell-free into 99 µL of buffer in a
FIDABIO 96-well plate — the well holds ~100 µL and **the measurement
consumes about 40 nL of it.** The vendor's floor for the Evolve is a 2 µL
fill. Everything else is pressure.

One cycle, as they ran it:

| | Step | Pressure |
|---|---|---|
| 1 | wash the capillary with 0.1% phosphoric acid | 3500 mbar |
| 2 | pre-equilibrate with buffer | 3500 mbar |
| 3 | draw the analyte | 3500 mbar |
| 4 | **inject the indicator plug** — this is the ~40 nL | 50 mbar |
| 5 | mobilise past the detector and record | 400 mbar |

The capillary is fused silica, **75 µm inner diameter, 1 m long with 84 cm
to the detector**, permanently coated. It is shared across every sample in
the run and washed between each.

**That is the structural difference worth understanding.** BLI burns a
biosensor tip per sample. A plate reader commits the whole well. FIDA takes
a droplet and reuses one capillary — so per-sample consumable cost is close
to zero and **your sample survives the measurement**, which matters when it
is 20 µL of cell-free reaction you cannot easily make more of.

Changing the pressure programme on the same filled plate is what turns an
equilibrium titration into a kinetics run. **No new samples, no new plate.**

---

## The automation question, which is the one that decides it

### What the vendor actually says

Two sentences, on the product page and in the knowledge base, both about
the Evolve only: it *"allows for easy raw metadata export"*, and its
*"rest API software with built-in SiLA driver enables lab automation,
while connecting to existing LIMS and digital lab infrastructure."*

That is the entire public statement. **There is no public API
documentation** — no endpoints, no schema, no SiLA version, no auth model.

### Why that sentence needs unpicking

**"REST API with a built-in SiLA driver" names two different things.**
SiLA 2 does not run on REST: it runs over HTTP/2 with Protocol Buffers.
So either the instrument exposes both and one wraps the other, or the
marketing copy is loose. **Which it is changes the integration story
completely**, because the deck's SiLA path and a REST path are different
pieces of work.

This matters here specifically: **the ATC on RAC 2 is integrated into
Catalyst over SiLA.** The rack already speaks that protocol. An instrument
with a real SiLA 2 server is a candidate for genuine orchestration rather
than a box someone walks plates to.

### Has Ginkgo ever integrated one?

**No public record of it — I looked and found nothing** connecting Ginkgo
Bioworks and Fida Biosystems. No press release, no case study, no mention
either way.

That is not fatal. RACs are explicitly vendor-agnostic — a robotic arm, a
plate transport track and standard connection points, designed so
instruments from different vendors can be arranged as needed. But it does
mean **this would be a first integration, not a catalogue item**, and
first integrations cost time and sit on someone's critical path. Ask
Ginkgo directly rather than assuming the RAC's generality covers it.

### The one thing nobody publishes

**Nothing on any Fida page says a robot can load the instrument.** It
takes 2 × 96 sample positions and the tray format is not described. If
plates seat by hand, the instrument is an offline station regardless of
how good its API is — which is still useful, but it is a different
purchase.

---

## Limits, stated and implied

- **It needs a size change to see anything.** Neo detects 5%, Evolve
  claims 1%. A small binder onto a large target is the favourable
  geometry; **a small target onto an FP-fusion binder is the bad one** —
  which is exactly the DTU configuration, and exactly why their construct
  carries a whole fluorescent protein that dominates the radius.
- **It is serial.** 2 × 96 is autosampler capacity, not parallelism.
- **One fluorescent partner.** Something must carry the fluorophore, or
  you use the UV label-free module and accept its sensitivity.
- **Single vendor, single supplier.** Capillaries, consumables and
  software all come from one company in Søborg. The DTU paper has a Fida
  Biosystems author, so read its performance figures accordingly.
- No published footprint, no published price.

---

## If this goes into a purchase case

Ask **Fida** for:

1. **Can a plate robot load it?** The question that decides everything else.
2. Sample-tray format and the loading mechanism — door, drawer or open deck.
3. **Is it SiLA 2, REST, or both** — and which commands does the API expose?
   Is there documentation, and is API access licensed separately?
4. Weight and power draw, which are not published.
5. List price for an Evolve with the UV and 480 modules.
6. Capillary cartridge lifetime and cost per cartridge.
7. Service contract cost.

Ask **Ginkgo** for: whether they have integrated a Fida instrument on any
RAC, and what a first integration of a SiLA instrument of this class costs
in time and money.

Compare against a Gator BLI at the same budget line. The honest framing
is not *FIDA versus BLI for kinetics* — it is **FIDA buys kinetics on
unpurified material, which removes a purification step the deck cannot do
at scale anyway.** That is the argument, and it is a good one if the
numbers come back sane.

See `reference/fida-pipeline.md` for the campaign that used it.
