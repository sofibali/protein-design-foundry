---
layout: page
title: Foundational test projects
standfirst: Each project is a claim about a capability. It earns its place by exercising instruments end to end and telling us something we did not already know.
---

Failures are written up with the same care as successes. A test project that
found a limit has done its job.

<table class="wide">
<thead><tr><th>Status</th><th>Project</th><th>Lead</th><th>Scale</th></tr></thead>
<tbody>
{%- for p in site.projects -%}
<tr>
  <td>{% include status.html s=p.status %}</td>
  <td><strong><a href="{{ p.url | relative_url }}">{{ p.title }}</a></strong><br>
      <span class="muted">{{ p.summary }}</span></td>
  <td>{{ p.lead }}</td>
  <td>{{ p.scale }}</td>
</tr>
{%- endfor -%}
</tbody></table>
