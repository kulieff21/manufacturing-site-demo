# Kəsim — demo manufacturing site

A static site for a fictional Azerbaijani sheet-metal manufacturer, built as a
portfolio piece and sales demo. The company, address, production records and
prices are fictional; the forms send and store nothing, and the site says so.

**Live:** https://twenion.github.io/manufacturing-site-demo/

13 pages · live quote calculator · sheet-nesting diagram · no framework · no
runtime build · no CDN · no cookies

## The demo set

Four sales demos for Azerbaijani small businesses. They share one technical bar,
but each has a different commercial argument and page shape.

| Demo | Business | Product shape |
| --- | --- | --- |
| [`cargo-site-demo`](https://github.com/twenion/cargo-site-demo) | Courier | Tracking, tariffs and an order form |
| [`ecommerce-site-demo`](https://github.com/twenion/ecommerce-site-demo) | Skincare retail | A 24-product catalogue and cart |
| [`hotel-site-demo`](https://github.com/twenion/hotel-site-demo) | Guesthouse | 365 visible nightly prices and booking |
| `manufacturing-site-demo` **← you are here** | Metal fabrication | A specification bench and measurable quote |

## The commercial argument

Manufacturing sites often list machine names but omit the numbers an engineer
needs before sending a drawing: supported material and thickness, bed size,
tolerance, minimum order, lead time and even an indicative price. The result is a
long email exchange before either side knows whether the part is a fit.

Kəsim starts with the opposite assumption. A photo-led production scene establishes
the workshop, and the working quote bench sits directly beneath it instead of being
buried behind a generic contact CTA. Enter a rectangular part's material, thickness,
dimensions, quantity and follow-up operations; the page immediately publishes:

- the best row-and-column layout on a 1500 × 3000 mm sheet;
- sheet count, material use and offcut percentage;
- finished material weight and estimated lead time; and
- an indicative price range with its limits stated beside it.

The detailed request form then collects the information that actually changes a
production quote: drawing, material, quantity, finish, critical dimensions and
required date. It validates in the browser and clearly states that the demo sends
nothing.

## The signature: the sheet is the interface

The live nesting map is both the site's visual identity and a useful explanation
of its calculation. Change the part dimensions and the SVG redraws the layout,
including rotation when it fits more parts. The same values drive the utilization,
offcut, weight and price results — the diagram cannot disagree with the number
beside it.

This creates a manufacturing-shaped page rather than a generic corporate site
with different copy. Its structure borrows from a job traveller: specification
fields, process abbreviations, dimensional marks and an inspection ledger. The
photo rail, animated nesting map and pointer-reactive process cards show the work
at three scales: factory, machine and finished part.

## What is included

- Four process pages: fiber laser cutting, CNC bending, MIG/TIG welding and powder
  coating, each with actual dimensional and acceptance limits.
- A material table covering S235JR, AISI 304 and EN AW-5754, including stocked
  thicknesses, sheet format, density and the calculation basis.
- A sample first-article inspection report with nominal dimension, tolerance,
  measured result, instrument and disposition in the same row.
- A detailed RFQ form and a separate technical-contact form. Both validate and
  then explicitly confirm that this demo sent no data.
- Useful output with JavaScript disabled: every limit, material, process and
  contact fallback remains ordinary HTML.
- Responsive layouts down to 390 px, keyboard focus, 44 px controls and reduced
  motion support.

## The bar it is held to

`tools/audit.py` checks every generated page against the same faults used in a
client audit:

| Check | Requirement |
| --- | --- |
| Language | `<html lang="az">` on every page |
| Heading | exactly one non-empty, subject-specific `<h1>` |
| Search metadata | sensible, unique title and description |
| Sharing | complete Open Graph text fields and URL |
| Canonical | one exact GitHub Pages URL per page |
| Structured data | valid, filled JSON-LD; Service schema on process pages |
| Links and assets | every local target exists; no runtime third-party request |
| Protocols | valid `mailto:` and `tel:` links |
| Images | meaningful `alt`, or `alt=""` plus `aria-hidden` for decoration |
| Placeholders | no TODO, lorem ipsum or scaffold copy |
| Discovery | `robots.txt` and a sitemap containing exactly the public pages |

The self-test copies the site to a temporary directory, breaks it nine different
ways and proves that each fault is caught. That includes an invalid language,
missing H1, `mail:` typo, broken internal link, remote script, placeholder copy,
invalid JSON-LD, wrong canonical and missing description.

```bash
python tools/build_pages.py
python tools/audit.py
python tools/audit_selftest.py
```

## Technical decisions

- **Static HTML, CSS and vanilla JavaScript.** The site can be handed to a client
  as a folder and hosted without a framework, package install or build service.
- **No CDN.** All authored assets are in the repository, so rendering does not
  depend on a third party. The audit rejects remote runtime assets.
- **System drafting typography.** Bahnschrift/DIN-style condensed headings make
  the page read like an engineering work surface; plain system sans keeps forms
  and tables practical. There is no font download.
- **Project-owned photography.** Two original industrial images were created for
  this fictional brand and optimized locally; there is no stock-photo hotlink or
  third-party image request at runtime.
- **Motion follows intent.** One orchestrated hero entrance, pointer-positioned
  gallery light, restrained card depth and responsive button feedback add energy;
  `prefers-reduced-motion` removes the non-essential movement.
- **Fiction stays labelled.** Zeroed phone numbers, a reserved `.example` email,
  explicit demo notices and no invented clients, certificates or awards.

## Licence

Code is MIT licensed. The fictional brand and demo content are provided as a
portfolio example, not as claims about a real manufacturer.
