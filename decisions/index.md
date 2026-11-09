---
layout: page
title: Open decisions
standfirst: A facility under construction has unsettled questions. Hiding them wastes the time of anyone trying to plan work here.
---

{% assign d = site.data.decisions.decisions %}
**{{ d | where: "status", "open" | size }} open**,
{{ d | where: "status", "pending" | size }} pending an answer,
{{ d | where: "status", "settled" | size }} settled, and
{{ d | where: "status", "dropped" | size }} considered and dropped.

A decision marked dropped stays on this list on purpose, so nobody re-opens it
without knowing it was already weighed.

{% include decision-table.html %}

<p class="muted">Rendered from <code>_data/decisions.yml</code>.</p>
