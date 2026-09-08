# Instrument — the AI Usage Tracking design system

Cool neutral ramp, one indigo accent, hairline borders, no shadows. Built for a dense,
data-first dashboard where nothing should compete with the numbers.

Everything the dashboard renders resolves to a token in [`theme.css`](theme.css), defined
in both themes. There are no hard-coded colours in components.

## What it is made of

| Layer | Lives in | Source |
|---|---|---|
| Tokens, fonts, base | `design-system/theme.css` | written for this product |
| Primitives (27) | `components/ui/*.tsx` | [shadcn/ui](https://ui.shadcn.com) registry, on [Radix](https://www.radix-ui.com) |
| Domain components | `components/*.tsx` | written for this product, on the primitives |
| Charts | `components/ui/chart.tsx` | shadcn's chart layer over [Recharts](https://recharts.org) |

Primitives are **copied into the repository, not imported from a package**. They are ours to
edit. `radix-ui` (a single tree-shakeable package) supplies the accessible behaviour
underneath — focus management, dismissal, ARIA wiring, keyboard interaction.

### Why these sources

The brief named shadcn/ui, Base UI, Radix, ReUI, 21st.dev, Magic UI and Aceternity. What
each actually contributed:

- **shadcn/ui on Radix** — the whole primitive layer. Chosen over Base UI because every
  other source listed publishes against it, so nothing needed porting.
- **ReUI** (MIT, all core components free) — reference for the chart and data-grid
  patterns. Its charts are Recharts-based too, so adopting its ideas cost no dependency.
- **Magic UI** — the number-ticker pattern behind `NumberTicker` in `components/stat.tsx`.
  Reimplemented in ~25 lines on `requestAnimationFrame` rather than pulling in
  `framer-motion` for a single effect.
- **Aceternity** — reviewed and largely declined. It is a decoration library (backgrounds,
  spotlights, 3D cards); roughly three of its ~90 components suit a dense dashboard, and
  none survived the "restrained, functional only" bar.
- **21st.dev** — pattern reference only. Its free tier caps you at two component copies per
  day, so it is not a viable build source.
- **Base UI** — not used. Adopting it alongside Radix would mean two headless dependency
  trees for one system.

## Tokens

Names follow shadcn/ui so registry components drop in unmodified. Domain tokens extend that
vocabulary for this product.

| Group | Tokens |
|---|---|
| Surfaces | `background` `card` `popover` `muted` `accent` `secondary` |
| Ink | `foreground` `card-foreground` `muted-foreground` … |
| Emphasis | `primary` `primary-foreground` `primary-subtle` |
| Lines | `border` `input` `ring` |
| Semantic | `destructive` `success` `warning` (+ `-subtle` fills) |
| Charts | `chart-1` … `chart-8`, `chart-other`, `chart-grid`, `chart-axis` |
| Cost state | `state-priced` `state-free` `state-unpriced` `state-unavailable` |
| Provenance | `provenance-measured` `-derived` `-estimated` `-inferred` `-unavailable` |
| Token buckets | `bucket-uncached-input` `-cache-read` `-cache-write` `-output` |
| Geometry | `radius` (6px; controls 4px via `radius-sm`) |
| Density | `text-ui` 14px · `control-height` 36px · `row-height` 44px · `card-padding` 24px |

Two rules the palette encodes:

- **Chart series keep their slot.** Eight well-separated hues in fixed order. A series is
  assigned a slot by stable identity, so filtering the data never repaints a surviving
  series.
- **`unavailable` is deliberately colourless.** When a log carries no token counts, no cost
  is implied — not even visually.

## Theming

Dark mode is driven by `data-theme` on `<html>`, set before first paint by the inline
script in the page head and thereafter by `src/theme.ts`. Tailwind's `dark:` variant is
repointed at that attribute in `theme.css`, so it never falls back to the media query and
disagrees with an explicit user choice. Default is to follow the OS; an override persists
in `localStorage`.

Every token is defined in both themes. A colour that exists in only one is a bug.

## Motion

Functional only. Values count up on mount (`NumberTicker`), skeletons mirror the shape of
what is arriving, panels and meters transition on change. Nothing decorative, and nothing
that carries meaning which is lost when it is switched off — `prefers-reduced-motion` cuts
every animation to ~0ms in `theme.css`.

## Fonts

Inter (UI) and Geist Mono (every numeral), self-hosted as variable woff2 under `fonts/`.
The tool is offline by design and makes no network requests. Licences and attribution are
in [`fonts/LICENSE.md`](fonts/LICENSE.md). Numerals are tabular everywhere so columns align.

## Working on it

Add a primitive from the registry:

```bash
npx shadcn@latest add <component>
```

**One quirk to know.** The CLI rewrites the `utils` alias in generated imports and collapses
`@/design-system/cn` to a bare `cn`, which then resolves to an unrelated npm package. After
any `add`, run:

```bash
sed -i 's|from "cn"|from "@/design-system/cn"|' src/components/ui/*.tsx
```

Then check `package.json` for a stray `cn` dependency and remove it.

## Domain components

Built on the primitives, in `src/components/`:

| File | Holds |
|---|---|
| `panel.tsx` | `Panel`, `PanelHeader` (eyebrow / title / hint / actions), `PanelBody`, `PanelNote` |
| `stat.tsx` | `Stat` (hero and default), `StatGrid`, `StatLabel`, `NumberTicker` |
| `status.tsx` | `CostStateBadge`, `ProvenanceBadge`, `OutcomeBadge`, `Meter`, `MeterRow`, `ComparisonMeter`, `BucketBar`, `Legend` |
| `chart-time.tsx` | `TimeChart` — stacked daily bars with the slice mean and the peak callout |
| `sparkline.tsx` | `Sparkline` — plain SVG, no chart library; interactive when given `labels` + `format` |
| `chart-hover.tsx` | `HoverFrame` — pointer tracking, arrow-key stepping and a live region for continuous charts |
| `series.ts` | `seriesColor(index)`, `TOKEN_BUCKETS` |
| `filters.tsx` | `SearchField`, `FacetGroup`, `ChipRow`, `DateRange`, `SortSelect`, `FilterChips` |
| `session.tsx` | `TokenCell`, `SessionCard` (the phone layout) |
| `source-card.tsx` | `SourceCard`, `SourceDetail` |
| `detail.tsx` | `Section`, `MetaGrid`, `CodeBlock`, `PathList` |
| `states.tsx` | `SortButton`, `EmptyState`, `ErrorState`, `OfflineCard`, `DisclosurePanel`, `WarningsList`, skeletons |
| `trace.tsx` | `ContextOccupancy`, `SpanTimeline`, `InsightList`, `CapabilityGrid`, `SPAN_KIND_GLYPH` |
| `use-media-query.ts` | `useMediaQuery` — drives the phone session cards and the rail drawer |

Charts are Recharts under shadcn's chart layer; sparklines are hand-written SVG, because
several render per screen and Recharts is heavy for a 96×26 line.

Every visualization is inspectable. Continuous series use `HoverFrame` — one tab stop per
chart, arrow keys to step, a polite live region for screen readers. Discrete elements use
the Radix tooltip. The native `title` attribute is never used for a value that matters: it
waits a second, cannot be styled, and never fires for keyboard or touch. `Tooltip` needs a
`TooltipProvider` ancestor at the app root.

## Where it is used

The design system backs the **prototype** at `web/prototype.html` (`src/prototype/`), which
renders all four dashboard screens panel-for-panel against mock data, plus a component
gallery.

The shipping dashboard still runs on the older `src/ds/` CSS system.
[`MIGRATION.md`](MIGRATION.md) maps every component the app renders today to its
Instrument equivalent, in a suggested porting order.
