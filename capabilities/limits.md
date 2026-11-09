---
layout: page
title: Limits
standfirst: Real constraints we have hit or expect to hit, listed so you can plan around them rather than discover them.
---

## Hard limits

**No frozen storage on the system.** Nothing at −20 or −80. Anything that must
be frozen leaves the enclosure, which breaks the unattended run.

**No size exclusion and no concentrator.** Bead purification gives micrograms at
screening purity. There is no route from a 0.3–0.5 mg/mL eluate to the
10–20 mg/mL a crystallisation screen needs, so that protein is made off-system.

**No colony picking.** Plating is in scope but nothing returns a clone from agar
to liquid, so well position does not carry identity unless sequencing supplies
it. This is the unsolved step in the binder pipeline, not a detail.

**No crystal imaging.** Trays are stored on the system but imaged by hand. A
campaign of 80 trays at 7 timepoints is 560 imaging events, roughly **37 hours
of human time** against 9 hours of robot time on an imaging cart.

**Centrifugation is not refrigerated** and tops out at 5,000 g, below what
detergent-based lysis needs to clear. Turbid lysate defeats AlphaScreen and
fluorescence polarisation, so lysis chemistry is constrained by the centrifuge.

**Shaking capacity is 14 deep-well plates.** That is the ceiling on in-cell
expression, and no amount of scheduling moves it.

## Instrument caveats

{% assign noted = site.data.instruments.instruments | where: "status", "quoted" %}
<table class="wide">
<thead><tr><th>Instrument</th><th>What to know before you plan around it</th></tr></thead>
<tbody>
{%- for i in noted -%}{%- if i.note -%}
<tr><td><strong>{{ i.name }}</strong></td><td>{{ i.note }}</td></tr>
{%- endif -%}{%- endfor -%}
</tbody></table>

## Capability gaps

Named but not specified. A gap is not a plan, it is an admission.

{% assign gaps = site.data.instruments.instruments | where: "status", "gap" %}
{% assign later = site.data.instruments.instruments | where: "status", "phase2" %}
<table class="wide">
<thead><tr><th>Status</th><th>Capability</th><th>Why it matters</th></tr></thead>
<tbody>
{%- for i in gaps -%}<tr><td>{% include status.html s=i.status %}</td><td><strong>{{ i.name }}</strong></td><td>{{ i.note }}</td></tr>{%- endfor -%}
{%- for i in later -%}<tr><td>{% include status.html s=i.status %}</td><td><strong>{{ i.name }}</strong></td><td>{{ i.note | default: i.role }}</td></tr>{%- endfor -%}
</tbody></table>
