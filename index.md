---
layout: page
title: Protein Design Foundry
standfirst: An automated protein design facility at UCSF Mission Bay. It is being built, and is not open for general submissions yet.
---


<div class="note" markdown="1">
### [Start here: what the foundry is for &rarr;]({{ '/static/pages/foundry.html' | relative_url }})

What the system is, how a campaign runs, the kinds of project it takes, and
whether yours is one of them. One page, mostly pictures.
</div>

Everything else on this site is the detail behind that page.

<div class="cards" markdown="0">
  <div class="card"><h3><a href="{{ '/static/pages/workflows.html' | relative_url }}">Sample protocols</a></h3>
    <p>Every protocol drawn: what happens on the deck, what the readout looks like, what
    goes in and what comes back. Chain them into a campaign at the foot of the page.</p></div>
  <div class="card"><h3><a href="{{ '/static/pages/blueprint.html' | relative_url }}">System blueprint</a></h3>
    <p>{% assign on_track = site.data.instruments.racs | where: "status", "installed" %}
    {% assign reserved = site.data.instruments.racs | where: "status", "phase2" %}
    {{ on_track | size }} carts on the track{% if reserved.size > 0 %}, {{ reserved | size }} more
    reserved{% endif %}. Each one drawn: what the cart does to a plate, what is inside it, and the
    protocols that run through it.</p></div>
  <div class="card"><h3><a href="{{ '/static/pages/intake.html' | relative_url }}">Propose a campaign</a></h3>
    <p>What to send, and how to shape a binder question so it comes back with an
    interpretable answer.</p></div>
  <div class="card"><h3><a href="{{ '/capabilities/' | relative_url }}">Capabilities</a></h3>
    <p>What the system does, at what scale, and where it stops.</p></div>
  <div class="card"><h3><a href="{{ '/projects/' | relative_url }}">Projects</a></h3>
    <p>Foundational test projects. Each is a claim about a capability.</p></div>
  <div class="card"><h3><a href="{{ '/inventory/' | relative_url }}">Inventory</a></h3>
    <p>{{ site.data.instruments.instruments | where: "status", "quoted" | size }} instruments across {{ site.data.instruments.racs | size }} carts.</p></div>
</div>

<details markdown="1">
<summary markdown="span">How this stays accurate</summary>

The inventory lives in `_data/` and every table is rendered from it at build
time. A number changes in one place. Figures taken from somewhere else say
where they came from, and figures that are arithmetic rather than measurement
say that too.

</details>
