---
title: Pricing Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: active
audience: internal
maturity: approved
confidence: inferred
covers: [web/src/*, web/src/design-system/*]
verified-against: 02d21a1926f6
chunk: ch-localtokenomics-web-src
approved-by: human
approved-at: '2026-11-19T07:31:30+00:00'
---

# Pricing Screen

The Models and pricing view (web/src/Pricing.tsx): estimated models, the rate table, the provider multipliers and the unpriced models. Its map is [[Pricing Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `items.length === 0` empty section | Hides the estimated panel when every model has its own row. | - | empty: `items.length === 0` | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:428-428` |
| 2 | `<Badge` rate age | Badge that says how old the rate table is. | - | shown only while the rates are old | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:342-342` |
| 3 | `<Table` rates | Rate table with one row per model, priced rows first. | `visibleRows` | - | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:352-366` |
| 4 | `<button` details | Expands the detail row of a model; disabled when there is no detail. | `onToggle` | - | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:277-279` |
| 5 | `<TagBadge` tags | Tag badges such as unverified. | - | - | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:289-289` |
| 6 | `<RowDetail` detail row | Detail of a rate row: source, bands, peak window and dated prices. | - | - | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:401-401` |
| 7 | `<Button` Show more rates | Reveals the next batch of unused rates. | `setRevealed` | shown only while unused rates are hidden | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:413-416` |
| 8 | `providersPresent.length === 0` empty section | Shows an empty state when no provider has priced activity. | - | empty: `providersPresent.length === 0` | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:492-492` |
| 9 | `<ProviderMultipliers` per provider | Cache and batch multipliers of one provider. | - | - | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:497-497` |
| 10 | `listed.length === 0 && unknown.length === 0 && idle.length === 0` empty section | Hides the unpriced panel when nothing is unpriced. | - | empty: `listed.length === 0 && unknown.length === 0 && idle.length === 0` | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:543-543` |
| 11 | `<UnpricedBadge` status | Badge that marks a model as no list price or watchlist. | - | - | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:569-569` |
| 12 | `<CodeBlock` rates.json snippet | A ready rate row to copy for the first unknown model. | - | - | [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:597-597` |

### Conditional sections

- empty: `items.length === 0`, callout 1, [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:428-428`
- empty: `providersPresent.length === 0`, callout 8, [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:492-492`
- empty: `listed.length === 0 && unknown.length === 0 && idle.length === 0`, callout 10, [[web/src/Pricing.tsx]] `web/src/Pricing.tsx:543-543`

## Diagnosis

The reader browses rates, expands details and copies a rate row; the view writes nothing back. The fix it suggests is to add a row to rates.json `web/src/Pricing.tsx:448` `web/src/Pricing.tsx:594-597`.

What can go wrong:

- A provider with priced activity but no multiplier rules renders nothing, without a note `web/src/Pricing.tsx:495-498`.
- An empty rate table renders a table with headers only, with no empty state `web/src/Pricing.tsx:352-409`.

States not handled: the reveal button only adds rows; there is no way to hide them again `web/src/Pricing.tsx:416`.
