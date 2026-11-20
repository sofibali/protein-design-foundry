# Galen's pattern (gcorrey/ginkgo-crystal, private — read 2026-11-15)

His side is Aim 3 (crystallography). The architecture is reusable as-is
for Aims 1–2, and it is already the thing I was describing in the abstract.

## Take these

**`build.py` — one self-contained HTML file.** Inlines the JS and
base64-embeds every referenced PNG, so `dist/ginkgo_rac.html` works with
no server: email it, drop it in Slack, open it offline. ~60 lines.
Take almost verbatim.

**Data split from page.** `workflows.js` holds `PLATES`, `INSTRUMENTS`,
`WORKFLOWS`, `GROUPS`, `LOOP`, `EXTRA_COSTS` as plain objects; the HTML
only renders them. This is the "pages render facts, never restate them"
rule, already working.

**Decision state on each instrument.** Every device carries
`details: {CAD status, API status, Risk, Open questions}` plus
`cost: {quote}` or `cost: {note, options:[…]}`. That is a live
procurement tracker inside the figure — it is what the open Ginkgo
answers need, and Echo 655 is already in there.

**`offRac: true`.** Flags diffraction, structures and make-on-demand
chemistry as happening off the machine. Same distinction as the teal/grey
split in the loop diagram — adopt his flag name, not a second vocabulary.

**`style_options.js` + `style_picker.html`.** Candidate palettes, each
with a written blurb about what it fixes for colour blindness, switchable
by URL (`?palette=…&arrows=…`). Includes **Okabe–Ito**, which is also
the palette in the printable-protocol skill. House palette: settled.

## Watch for

- Light mode only; no dark-mode variables.
- `svg#schematic { min-width: 760px }` — does not work on a phone.
- Palette hexes are literal, not CSS variables, so theming means
  regenerating rather than restyling.

## The point

He has already built the living-page architecture: data files, a
renderer, a bundler, a palette system, and decision state attached to
real objects. Adopt it rather than invent a second one. His workflow
data is crystallography; ours is expression and binding. Same page,
different `WORKFLOWS` entries.
