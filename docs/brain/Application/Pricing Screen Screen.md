---
title: Pricing Screen Screen
aliases: []
tags: [ui, reference, screen-map]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/src/prototype/**]
verified-against: 5796e68c0471
chunk: ch-localtokenomics-web-src-prototype
---

# Pricing Screen Screen

The Pricing screen (`web/src/prototype/PricingScreen.tsx:208-218`), labelled Models and pricing in the tabs `web/src/prototype/Screens.tsx:43-48`. The map is [[Pricing Screen Screen Map]]; each numbered badge in the image is one row below.

## Screen map

| # | Element | What it does | Handler or target | State it depends on | Citation |
|---|---|---|---|---|---|
| 1 | `<PanelHeader` rate table | Title with the rate date and a hint that cache prices are derived and cost is never stored. | - | `TOTALS.ratesAsOf` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:57-61` |
| 2 | `<Table` rates | Table of rates, priced models first. | - | - | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:63` |
| 3 | `<TableHead` column headers | Eight column headers; unlike the sessions table they are not sortable. | - | `RATE_COLUMNS` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:67-72` |
| 4 | `<TableRow` one row per rate | Row with model, provider, input, derived cache prices, output, state and spend. | - | `rate.match` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:80` |
| 5 | `rate.inherited` conditional section | Inherited marker, drawn only for a rate taken from another model. | - | conditional: `rate.inherited` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:84-88` |
| 6 | `<Badge` inherited | Outlined badge that says the rate is inherited. | - | `rate.inherited` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:85-87` |
| 7 | `<Badge` state | Badge with free, priced or unused, derived from the rate and the spend. | - | `values.state` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:102-104` |
| 8 | `hidden > 0` conditional section | Reveal row, drawn only while unused rates are still hidden. | - | conditional: `hidden > 0` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:115-125` |
| 9 | `<Button` show more rates | Reveals four more unused rates per press; there is no way to hide them again. | `setRevealed` (inline, adds `REVEAL_BATCH`) | `hidden` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:117-123` |
| 10 | `<PanelHeader` multipliers | Title of the per provider multiplier panel. | - | `PROVIDER_RULES` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:135-138` |
| 11 | `<MeterRow` one meter per multiplier | Meter for cache read, cache write 5 minutes, cache write 1 hour and batch, per provider. | - | `item.value` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:152-158` |
| 12 | `UNKNOWN_MODELS.length === 0` empty section | Panel is skipped entirely when no model has tokens without a rate. | - | empty: `UNKNOWN_MODELS.length === 0` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:173` |
| 13 | `<div` one row per unpriced model | Row with the model name, its tokens and its events. | - | `UNKNOWN_MODELS` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:185-193` |
| 14 | `<CodeBlock` rates.json line | Example rate line to add, built from the first unpriced model. | - | `first.model` | [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:200-202` |

### Conditional sections

- conditional: `rate.inherited`, callout 5, [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:84-88`
- conditional: `hidden > 0`, callout 8, [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:115-125`
- empty: `UNKNOWN_MODELS.length === 0`, callout 12, [[web/src/prototype/PricingScreen.tsx]] `web/src/prototype/PricingScreen.tsx:173`

## Diagnosis

**What the user can do.** Read the rate table, with priced models first and unused models folded away `web/src/prototype/PricingScreen.tsx:49-53`. Press the button to reveal four more unused rates at a time `web/src/prototype/PricingScreen.tsx:117-123`. Read the multiplier meters for each provider and the list of models that have tokens and no rate `web/src/prototype/PricingScreen.tsx:130-206`.

**What can go wrong.**

- Cache prices come from the provider rules, with a default of 0.1 for a read and 1.25 for a write when the provider has no rule `web/src/prototype/PricingScreen.tsx:40-41`. The rule table lists only three providers `web/src/prototype/data.ts:604-608`, yet the rate table also holds deepseek, moonshot and mistral rows `web/src/prototype/data.ts:592-594`. Their cache columns therefore show the default, not a published price, while the note under the multiplier panel says discounts differ by provider `web/src/prototype/PricingScreen.tsx:164-167`. A port must not copy the default.
- The reveal button only adds rows. There is no control to fold them again `web/src/prototype/PricingScreen.tsx:115-125`.
- The column headers are plain text, so the table cannot be sorted, unlike the sessions table `web/src/prototype/PricingScreen.tsx:66-73`.
- The unpriced panel shows an example rate line with zero prices `web/src/prototype/PricingScreen.tsx:200-202`. The user must edit the file by hand; the screen offers no form.

**States the code does not handle.**

- No loading and no error state: rates are literal constants `web/src/prototype/PricingScreen.tsx:18-18`.
- An empty rate list draws an empty table with no message `web/src/prototype/PricingScreen.tsx:76-112`.
- When no model lacks a rate the whole unpriced panel disappears without a note saying that every model is priced `web/src/prototype/PricingScreen.tsx:173-173`.
