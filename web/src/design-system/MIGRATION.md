# UI refactor: porting the dashboard onto Instrument

**Audience:** an agent doing the port. This file is the entry point. It tells you what to
read, in what order, which component replaces which, and what to verify.

**Task:** the shipping dashboard renders through the old CSS system in `web/src/ds/`.
Port it onto Instrument.

> **Port against `claude/instrument-port`, not this branch.**
> Instrument was built on `experimentation` @ `393c421`. That branch then advanced six
> commits while the design system was being written, and the app was rebuilt into an agent
> observability tool underneath it. `claude/instrument-port` is `experimentation` @ `eb88e4c`
> with the six Instrument commits replayed on top; it is the only tree where the design
> system and the real app coexist.
>
> Consequences you must not miss, all verified against `experimentation`:
> - The session drawer is gone. `SessionDrawer.tsx` was replaced by `SessionWorkspace.tsx`
>   plus `TraceTab.tsx`, `EconomicsTab.tsx` and `ContextTab.tsx`, about 1,700 lines together.
> - **Economics and SpanContent are built, shipping and tested.** Do not redesign them.
> - **`chart.ts` has no callers left.** `timeChart()`, `contextBars()` and `spark()` are all
>   dead; the occupancy geometry now lives in `ContextOccupancy`.
> - The API has 12 routes, not 5. `rates.json` carries a context window on all 80 of its
>   models, so context occupancy renders real values rather than "unavailable".
> - Sources renders a 9-reader x 5-capability matrix, one row per reader in
>   `src/ai_usage_cost/sources/`.
>
> `SpanTimeline`, `InsightList` and `ContextOccupancy` have all met a real API response:
> `TraceTab.tsx` drives the first two, `ContextTab.tsx` the third. `CapabilityGrid` is still
> prototype-only — the app renders capabilities as a row of `ProvenanceBadge`s in `TraceTab`
> and as the Sources matrix instead.

**Ground rules**

- Work one screen per commit. Each screen is independently verifiable.
- `npx tsc --noEmit` and `npm run build` must pass before every commit (run from `web/`).
- Follow `CLAUDE.md` at the repo root. Most relevant here: no comments in `.tsx`, smallest
  coherent diff, no unrelated refactors, no new dependencies.
- The prototype in `web/src/prototype/` is a working reference implementation of every
  screen. Read the prototype file beside the app file you are changing. Do not import
  from `prototype/` — it is mock data; copy the composition, not the module.

## Read these first

In this order. Stop when you have enough to start the screen you are on.

| Order | File | Why |
|---|---|---|
| 1 | `web/src/design-system/README.md` | the token vocabulary and what each component file holds |
| 2 | `web/src/design-system/theme.css` | every colour, radius, density and motion token, both themes |
| 3 | this file | the component-by-component mapping |
| 4 | `web/src/prototype/<Screen>.tsx` | the reference implementation of the screen you are porting |
| 5 | `web/src/<Screen>.tsx` | the app file you are changing |
| 6 | `web/src/api.ts` | the real data shapes; the prototype's `data.ts` mirrors a subset |

## Repo map

| Path | Holds | Status |
|---|---|---|
| `web/src/design-system/theme.css` | tokens, fonts, base layer | **use** |
| `web/src/design-system/cn.ts` | `cn()` class merge | **use** |
| `web/src/components/ui/*.tsx` | 28 shadcn primitives on Radix | **use** |
| `web/src/components/*.tsx` | domain components (table below) | **use** |
| `web/src/prototype/*` | reference screens + mock data | **read only** |
| `web/src/ds/**` | old CSS design system | **delete at the end** |
| `web/src/chart.ts` | old chart geometry | **delete at the end** |
| `web/src/index.css` | old app-local classes | **delete at the end** |
| `web/src/api.ts`, `web/src/format.ts`, `web/src/theme.ts` | data, formatting, theme store | **keep** |

`web/src/theme.ts` keeps its `useTheme` store — it already drives `data-theme`, which is
what `theme.css` keys its dark block on. Only the colour constants in it move (see
Constants below); delete those and leave the store.

## Order of work

| Step | Change | Reference | Note |
|---|---|---|---|
| 1 | `web/src/main.tsx` imports `@/design-system/theme.css` instead of `./index.css`, **and `App.tsx` wraps its whole returned tree in `TooltipProvider`** | `web/src/prototype/main.tsx`, `prototype/Prototype.tsx` | the whole app restyles at once; own commit. The provider must sit **above the early returns** or `OfflineCard` and `ErrorState` fall outside it |
| 2 | `web/src/Sources.tsx` | `web/src/prototype/SourcesScreen.tsx` | smallest screen, 3 components, no interaction |
| 3 | `web/src/Pricing.tsx` | `web/src/prototype/PricingScreen.tsx` | tables and meters, one piece of local state |
| 4 | `web/src/Sessions.tsx` | `web/src/prototype/SessionsScreen.tsx` | keep the 120-row cap, see Behaviour to preserve |
| 5 | `web/src/SessionWorkspace.tsx` + `TraceTab.tsx` + `EconomicsTab.tsx` + `ContextTab.tsx` | `SessionDrawer` in `web/src/prototype/Screens.tsx` is a **partial** reference only | a `Sheet` + `Tabs` shell over four lazily loaded tabs, about 1,700 lines together; `SheetContent` caps at `sm:max-w-sm` and there is no outcome editor in the design system. Extend, do not swap |
| 6 | `web/src/FilterRail.tsx` | `web/src/prototype/Rail.tsx` | largest surface; the mobile drawer depends on it |
| 7 | `web/src/Header.tsx`, `web/src/App.tsx` | header + `Screens` in `web/src/prototype/Prototype.tsx` | shell, chips, offline and loading states |
| 8 | `web/src/Overview.tsx` | `web/src/prototype/OverviewScreen.tsx` | 7 panels, the only real chart work |
| 9 | delete `ds/`, `chart.ts`, `index.css`; drop colour constants from `theme.ts` | — | nothing should import them by now |

Step 1 before anything else: until `theme.css` is loaded, none of the Instrument
components have tokens to resolve against, and until `TooltipProvider` is mounted every
tooltip introduced in steps 2 to 6 fails **silently, with no type error**.

## Component index

Every domain component, where it lives, what it replaces, and which primitives it sits on.

| Component | File | Replaces | Built on |
|---|---|---|---|
| `Panel` `PanelHeader` `PanelBody` `PanelNote` | `components/panel.tsx` | `.panel`, `.panel__head`, `.panel__title`, `.lbl` eyebrow, `.panel__note` | — |
| `Stat` `StatGrid` `StatLabel` `NumberTicker` | `components/stat.tsx` | `.kpi`, `.kpi--wide`, `StatTile`, `.lbl` | — |
| `CostStateBadge` | `components/status.tsx` | `STATE_BADGE` + state dot markup | — |
| `ProvenanceBadge` | `components/status.tsx` | `PROVENANCE_BADGE` (had no renderer) | — |
| `OutcomeBadge` | `components/status.tsx` | nothing — `SessionRow.outcome` had no renderer | — |
| `Meter` | `components/status.tsx` | `.meter` / `.meter__fill` | — |
| `MeterRow` | `components/status.tsx` | `ModelRow`, `ProjectRow`, `ProviderMultipliers` rows | — |
| `ComparisonMeter` | `components/status.tsx` | `CacheSavingsPanel`'s two tall meters | — |
| `BucketBar` `Legend` | `components/status.tsx` | `TokenMixRow` bar, `TokenBucketsSection` bar | — |
| `TimeChart` | `components/chart-time.tsx` | `chart.ts timeChart()` + the SVG in `TimeChartPanel` | `ui/chart`, recharts |
| `Sparkline` | `components/sparkline.tsx` | `chart.ts spark()` | `HoverFrame` when given `labels` + `format` |
| `HoverFrame` | `components/chart-hover.tsx` | nothing — hover/keyboard layer for continuous charts | — |
| `seriesColor` `TOKEN_BUCKETS` | `components/series.ts` | `theme.ts SERIES`, `theme.ts BUCKETS` | — |
| `SearchField` | `components/filters.tsx` | `.search-field` | `ui/input` |
| `FacetGroup` | `components/filters.tsx` | `FacetOptionButton` | `ui/checkbox`, `ui/label` |
| `ChipRow` | `components/filters.tsx` | saved-view and range-preset `.chip` rows | — |
| `DateRange` | `components/filters.tsx` | the `.date-input` pair | `ui/input` |
| `SortSelect` | `components/filters.tsx` | `.sort-select` | `ui/select` |
| `FilterChips` | `components/filters.tsx` | `App.tsx buildActiveChips` markup | `ui/badge` |
| `TokenCell` | `components/session.tsx` | `TokensCell` | — |
| `SessionCard` | `components/session.tsx` | `SessionCard` (phone layout) | — |
| `SourceCard` `SourceDetail` | `components/source-card.tsx` | `Overview SourceCard`, `Sources SourceDetail` | `ui/badge` |
| `Section` `MetaGrid` `CodeBlock` `PathList` | `components/detail.tsx` | `.detail-section__title`, `.detail-meta-grid`, `<pre>`, raw-file list | — |
| `SortButton` | `components/states.tsx` | `.sortbtn` header buttons | — |
| `EmptyState` `ErrorState` | `components/states.tsx` | `.empty-state` | `ui/button` |
| `OfflineCard` | `components/states.tsx` | `App.tsx OfflineCard` | `ui/button`, `CodeBlock` |
| `DisclosurePanel` | `components/states.tsx` | `UndetectedSection`, rail's undetected block | `ui/collapsible` |
| `WarningsList` | `components/states.tsx` | `ScanWarningsPanel` `<ul>` | — |
| `PanelSkeleton` `StatSkeleton` | `components/states.tsx` | the centred "Loading…" label | `ui/skeleton` |
| `ContextOccupancy` | `components/trace.tsx` | `chart.ts contextBars()` | — |
| `SpanTimeline` | `components/trace.tsx` | nothing — `Trace.spans` had no renderer | — |
| `InsightList` | `components/trace.tsx` | nothing — `Trace.insights` had no renderer | — |
| `CapabilityGrid` | `components/trace.tsx` | nothing — `Trace.capabilities` had no renderer | — |
| `useMediaQuery` | `components/use-media-query.ts` | `Sessions.tsx useIsPhone` | — |

### Interaction contract

Two patterns, and which to reach for:

| Shape | Pattern | How |
|---|---|---|
| Continuous series (sparkline, occupancy) | `HoverFrame` | one tab stop per chart; pointer tracking, arrow keys, Home/End, Escape, polite live region |
| Discrete elements (bucket segment, meter row, token cell, span glyph) | `ui/tooltip` | one `Tooltip` per element, `tabIndex={0}` on the trigger |
| Cartesian chart | Recharts `ChartTooltip` | already wired in `TimeChart` |

**`Sparkline` is inert until you pass `labels` and `format`.** Without them it draws a
line and nothing more — that is the escape hatch for decorative use, but on any screen
where the number matters, pass both plus `seriesLabel`.

**`Tooltip` needs a `TooltipProvider` ancestor.** `components/ui/tooltip.tsx` does not
self-provide. The prototype wraps everything in one inside `prototype/Prototype.tsx`; when
you port the shell, wrap the app root the same way or every discrete tooltip silently
does nothing.

Never use the native `title` attribute for a value a user needs: it waits about a second,
cannot be styled, and never appears for keyboard or touch. All of them have been removed.

## Per-screen mapping

### Sources — `web/src/Sources.tsx`

The screen opens on a capability matrix, not on the reader cards. One row per reader in
`src/ai_usage_cost/sources/` — nine of them, detected or not — and one column per field of
`Capabilities` in `src/ai_usage_cost/trace.py`: trace, tokens, cost, context, latency. Every
cell is a `ProvenanceBadge` carrying that reader's provenance for that capability, so the
matrix answers "what can this reader tell me, and how does it know" in one grid. A reader
with no logs on this machine keeps its row and is marked "not detected" rather than
dropped, since its capabilities are a property of the reader, not of this machine. The
panel note spells out what each provenance word means and why Cursor is listed with
everything `unavailable`.

The reader cards follow, then the undetected readers, then the scan warnings.

| Today | Use |
|---|---|
| capability matrix | `Panel` + `ui/table` + `ProvenanceBadge` |
| `SourceDetail` | `SourceDetail` from `components/source-card.tsx` |
| `Stat` (local) | the `stats` prop on `SourceDetail` |
| `spark()` | `SourceDetail` renders its own `Sparkline` from the `trend` prop |
| `UndetectedSection` | `DisclosurePanel` + `StatLabel` |
| `ScanWarningsPanel` | `Panel` + `WarningsList` |

### Models and pricing — `web/src/Pricing.tsx`

| Today | Use |
|---|---|
| `RateTablePanel` table | `ui/table` |
| `inherited` and state badges | `ui/badge` |
| "Show N more rates" | `ui/button` + local `revealed` state, unchanged logic |
| `ProviderMultipliers` rows | `MeterRow` with `labelWidth={140}` |
| `UnpricedPanel` `<pre>` | `CodeBlock` |
| `.panel` accent border | `<Panel className="border-l-2 border-l-primary">` |

### Sessions — `web/src/Sessions.tsx`

| Today | Use |
|---|---|
| `.data-table` | `ui/table` |
| `.sortbtn` headers | `SortButton` |
| `SORT_OPTIONS` `<select>` | `SortSelect` |
| `TokensCell` | `TokenCell` |
| `SessionCard` | `SessionCard` |
| `useIsPhone` | `useMediaQuery('(max-width: 639px)')` |
| state dot + label | `CostStateBadge` |
| — | an Outcome column: `OutcomeBadge` on `row.outcome`, plus `TracedDot` and `ErrorCount` |

`SessionRow` carries `outcome`, `traced` and `error_count` from the API and the table
renders all three: an Outcome column of `OutcomeBadge`, a `TracedDot` beside the cost
state, and an `ErrorCount` that reads muted at zero and destructive above it.

### Session workspace — `SessionWorkspace.tsx`, `TraceTab.tsx`, `EconomicsTab.tsx`, `ContextTab.tsx`

`SessionDrawer.tsx` no longer exists. `SessionWorkspace.tsx` is a `Sheet` holding a `Tabs`
shell: a header carrying the session id, a one-line subtitle and the outcome control, then
a tab strip over Summary, Trace, Economics and Context. The sheet is
`sm:w-[95vw] sm:max-w-[1180px]`, well past `SheetContent`'s own `sm:max-w-sm`, and the tab
panels scroll inside it rather than moving the page.

Only Summary renders from the report row already in memory. The other three fetch on first
selection and never again — `SessionWorkspace` tracks which tabs have been asked for and
`useLazyResource` starts one aborted-on-unmount request per tab. Opening the workspace on
Summary issues no trace, economics or context call at all. Each lazy tab shows a loading
line, then either its content or the endpoint's error message; none of them ever renders
blank.

| Region | Built on |
|---|---|
| the panel itself | `ui/sheet` (`SheetContent` ships its own close button) |
| tab strip and panels | `ui/tabs`, `TabsList variant="line"` |
| outcome control | `ui/toggle-group` over the five `OutcomeLabel`s, plus `ui/textarea` and `ui/input` behind a "Notes and tags" toggle |
| Summary's section headings | `Section` from `components/detail.tsx` |
| Summary's token buckets | `BucketBar` + `TOKEN_BUCKETS` |
| Summary's origin block | `MetaGrid` from `components/detail.tsx` |
| Summary's raw log file list | `PathList` |
| cost and outcome badges | `CostStateBadge`, `OutcomeBadge` |
| every missing figure | `Unavailable` from `components/status.tsx` |

The tabs pull their own data. `web/src/api.ts` has every call:

| Need | Call | Returns |
|---|---|---|
| span timeline, insights, capabilities | `fetchTrace(source, sessionId, signal)` | `Trace` |
| context occupancy | `fetchContext(source, sessionId, signal)` | `ContextSnapshot[]` |
| per-turn economics | `fetchEconomics(source, sessionId, signal)` | `Economics` |
| outcome + notes + tags | `fetchOutcome` / `putOutcome` | `Outcome` |
| one span's text | `fetchSpanContent(source, sessionId, spanId, signal)` | `SpanContent` |

`Trace` carries `spans`, `insights`, `capabilities` and `outcome` together, so `TraceTab`
needs one `fetchTrace` and nothing else. `fetchSpanContent` is the exception to the
per-tab rule: `TraceTab` calls it per span, when a row's "Text" button is pressed.

The three tabs interlock. `ContextTab` renders a button per contributing span; pressing one
selects the Trace tab and scrolls that span into view. `TraceTab`'s insight list does the
same within its own tab. Both go through the workspace's `focusSpanId`, so a span selected
from Context survives the tab switch.

### Filter rail — `web/src/FilterRail.tsx`

| Today | Use |
|---|---|
| whole component | split like `web/src/prototype/Rail.tsx`: `RailContent` + `FilterRail` |
| `.search-field` | `SearchField` |
| saved views | `ChipRow` |
| range presets | `ChipRow` |
| `.date-input` pair | `DateRange` |
| `FacetOptionButton` | `FacetGroup` |
| sidechain checkbox | `ui/switch` + `ui/label` |
| "Clear all filters" | `ui/button` `variant="outline"` |
| undetected block | `DisclosurePanel` |
| mobile copy of the rail in `.detail-panel-overlay` | `Sheet side="left"` |
| — | an Outcome facet from `report.facets.outcomes`, and switches for `query.traced` / `query.hasErrors` |

`Query` has `outcomes`, `traced` and `hasErrors`, `Facets` has `outcomes`, and
`buildQueryParams` in `api.ts` serialises all three. The rail exposes each of them: an
Outcome `FacetGroup`, a `ui/switch` row apiece for the two booleans, and a "Sessions with
errors" saved view that sets `hasErrors` in one press.

### Shell — `web/src/Header.tsx`, `web/src/App.tsx`

| Today | Use |
|---|---|
| `.app-header` | header markup in `web/src/prototype/Prototype.tsx` |
| `.tab-btn` nav | buttons with `aria-current="page"` |
| `.theme-toggle` knob | `ui/button` `variant="ghost" size="icon"` + lucide icons |
| `OfflineCard` | `OfflineCard` from `components/states.tsx` |
| loading screen | `PanelSkeleton` / `StatSkeleton` |
| `buildActiveChips` markup | `FilterChips` (keep the builder, replace the rendering) |
| `.app`, `.app-rail`, `.app-main` | Tailwind utilities, see `Screens` in `prototype/Screens.tsx` |

### Overview — `web/src/Overview.tsx`

| Today | Use |
|---|---|
| `DetectedSourcesPanel` + local `SourceCard` | `SourceCard` from `components/source-card.tsx` |
| `KpiRow` + `StatTile` | `Stat` + `StatGrid`, with `Sparkline` as children |
| `TimeChartPanel` + `timeChart()` | `TimeChart` |
| stack-by / metric `.chip` groups | `ui/toggle-group` |
| `CostByModelPanel` + `ModelRow` | `MeterRow` |
| `TokenMixPanel` + `TokenMixRow` | `BucketBar` + `Legend` + `TOKEN_BUCKETS` |
| `CacheSavingsPanel` | `ComparisonMeter` × 2 |
| `ByProjectPanel` + `ProjectRow` | `MeterRow` |

`TimeChart` takes the same `{day, key, label, value}` rows `TimeChartPanel` already builds,
so that construction ports unchanged. The pivot, key ordering by descending total, the mean
and the peak all move inside the component. Delete the `ResizeObserver` — `ChartContainer`
handles sizing.

## Constants

| Today | Use |
|---|---|
| `theme.ts SERIES` | `seriesColor(index)` from `components/series.ts` |
| `theme.ts STATE_COLOR` / `STATE_BADGE` | `COST_STATE_META` / `CostStateBadge` |
| `theme.ts BUCKETS` | `TOKEN_BUCKETS` from `components/series.ts` |
| `theme.ts PROVENANCE_COLOR` / `PROVENANCE_BADGE` | `PROVENANCE_META` / `ProvenanceBadge` |
| `theme.ts SPAN_KIND_GLYPH` | `SPAN_KIND_GLYPH` from `components/trace.tsx` |
| `.num` | `.tabular` |
| `.lbl` | `StatLabel` |
| `var(--fg-strong)` / `--fg-muted` / `--fg-faint` | `text-foreground` / `text-muted-foreground` |
| `var(--bg-panel)` / `--bg-muted` | `bg-card` / `bg-muted` |
| `var(--accent)` | `text-primary` / `bg-primary` |
| `var(--rose)` | `text-destructive` |

## Behaviour to preserve

Not design decisions. Carry these across unchanged:

- **Sessions caps at 120 rows** (`SHOWN_LIMIT`) with the "Showing the first N of M
  sessions" note. The prototype keeps it as `SESSION_LIMIT`.
- **`maxTokens` for the token bar is computed over the shown rows**, not all rows.
- **Facets hide zero-count options** unless currently selected, and sort by count
  descending (`buildFacetEntries`).
- **The 5-minute auto-rescan** and its `visibilitychange` handling in `App.tsx`.
- **Cost is never fabricated.** `n/a` and `—` where state is `unavailable`; a model is
  never shown at `$0.00` unless it is genuinely free.
- **`TokenCell`'s bar is relative to the largest row currently shown**, so it rescales on
  sort and filter. That is intended; its tooltip now says so.

## Deliberate changes

Each is a decision, not an oversight. Revisit if you disagree:

- The time chart gains tooltips, a keyboard-reachable legend and axis semantics from
  Recharts. The `<title>` tooltips and absolutely-positioned tick labels go.
- The peak callout is a `ReferenceLine` label and no longer flips its anchor near the
  right edge, because Recharts keeps it inside the plot.
- The theme toggle is a plain icon button, not the sliding knob.
- Facets are real Radix checkboxes, so they announce state and respond to the space bar.
- Density rises: 14px base against ~12.5px, 44px rows against ~30px.
- Every visualization is inspectable. The old dashboard exposed values through native
  `title` attributes on some SVG rects and nothing at all on the sparklines; the new one
  gives each chart a tooltip and a keyboard path.
- Cost by model no longer prints `unpriced` / `free` inside the empty bar track. The state
  is already in the row meta; the bar does not repeat it.

## What renders each API type

Every type the API returns now has a renderer. Where the app and the prototype disagree,
the app is the reference:

| API | Rendered by | Through |
|---|---|---|
| `SessionRow.outcome`, `Facets.outcomes`, `Query.outcomes` | `Sessions.tsx`, `FilterRail.tsx` | `OutcomeBadge`, `FacetGroup` |
| `SessionRow.traced`, `Query.traced` | `Sessions.tsx`, `FilterRail.tsx` | `TracedDot`, a `ui/switch` row |
| `SessionRow.error_count`, `Query.hasErrors` | `Sessions.tsx`, `FilterRail.tsx` | `ErrorCount`, a `ui/switch` row and the "Sessions with errors" saved view |
| `ContextSnapshot[]` | `ContextTab.tsx` | `ContextOccupancy` over the whole session, then one card per call with a `ComparisonMeter` |
| `Trace.spans` | `TraceTab.tsx` | `SpanTimeline` |
| `Trace.insights` | `TraceTab.tsx` | `InsightList`, with `spanId` and `onSelectSpan` wired to the row scroll |
| `Trace.capabilities` | `TraceTab.tsx`, `Sources.tsx` | a `ProvenanceBadge` row, and the Sources matrix; `CapabilityGrid` stays prototype-only |
| `Economics` | `EconomicsTab.tsx` | `StatGrid` + `ui/table` |
| `SpanContent` | `TraceTab.tsx` | `CodeBlock` inside an expanded span row |

### Economics

A KPI row of eight `Stat`s — tokens, cost, duration, calls, retries, amplification, cache
hit ratio, tokens per second — then three tables: by turn in the order they ran, by model
heaviest first, by tool most-called first. The three share one `Column[]` shape and one
`EconPanel`, so a column is a cell function and a label and nothing more. Each table holds
its own reveal state and shows 40 rows at a time; each collapses to a stack of cards under
`(max-width: 639px)`, first column as the card title and the rest as label-value rows.

Every cell that can be absent is absent rather than zero. A null duration, cost, retry
count, amplification, cache ratio or token rate renders `Unavailable` with a hint saying
which log does not carry it, and a duration that is present carries a `ProvenanceBadge` for
where it came from. A row whose cost covers only some of its model calls is marked
`partial`.

### Span content

Each span row with a `content_path` gets a "Text" button that calls `fetchSpanContent` for
that span alone. The result renders as a `CodeBlock` followed by one line of provenance:
whether the text was truncated at the configured byte limit, and how many secrets were
redacted before display — or "Nothing matched a redaction pattern" when none were.
`src/ai_usage_cost/privacy.py` does both, matching against nine patterns and rewriting each
hit to `[REDACTED:<name>]` before the text leaves the process.

The endpoint answers 404 when content capture is off, which is the default
(`Config.metadata_only` is `True`). The tab reads that as a state rather than an error and
says so: content capture is off, nothing is read back until `metadata_only: false` is set
in `~/.ai-usage-cost/config.json`. The same answer covers a record whose file has moved
since the scan, and the message says that too.

### Remaining Instrument gaps

- `ui/alert-dialog` is **not** installed. `deleteSession` in `api.ts` has no caller yet;
  it is destructive, so wire it up only together with a confirmation. Add the primitive
  with `npx shadcn@latest add alert-dialog`, then re-run the `cn` import fix in
  `web/src/design-system/README.md`.
- Five `index.css` classes are now dead rather than unported: `.workspace`,
  `.workspace .tab-strip`, `.workspace__panel`, `.workspace__outcome`,
  `.workspace__disclosure`. They go with the rest of the file in step 9.

## Verify

From `web/`:

```bash
npx tsc --noEmit
npm run build
npm run dev        # app at /, prototype at /prototype.html
```

`npm run build` writes into `src/ai_usage_cost/web/dist/`, which is committed and ships
inside the Python wheel. It must stay working. `prototype.html` is deliberately excluded
from the production build; do not add it to `rollupOptions.input`.

Check both themes on every screen you touch — the header's toggle is the fastest way, and
a token defined in only one theme is a bug.
