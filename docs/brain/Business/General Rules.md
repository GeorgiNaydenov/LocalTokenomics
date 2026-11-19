---
title: General Rules
aliases: []
tags: [business, generated, rules, spec]
area: business
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [pyproject.toml, src/ai_usage_cost/privacy.py, src/ai_usage_cost/render/png.py,
  src/ai_usage_cost/sources/__init__.py, src/ai_usage_cost/sources/base.py, src/ai_usage_cost/sources/claude_code.py,
  src/ai_usage_cost/sources/codex.py, src/ai_usage_cost/sources/muse_code.py, web/eslint.config.js,
  web/package.json, web/src/App.tsx, web/src/Pricing.tsx, web/src/SessionWorkspace.tsx,
  web/src/Sessions.tsx, web/src/Sources.tsx, web/src/TraceTab.tsx, web/src/design-system/MIGRATION.md,
  web/src/format.ts, web/src/pricing-format.ts, web/src/pricing-notes.ts, web/src/prototype/Prototype.tsx,
  web/src/prototype/Screens.tsx, web/src/prototype/SessionsScreen.tsx, web/src/prototype/data.ts,
  web/src/turn-insights.ts, web/vite.config.ts]
generated: true
anchors: true
---

# General Rules

> [!info] What this is
> Business rules that belong to no single subdomain. Each rule is a heading, so a use case links straight to it, and each names the line of code that enforces it.

## BR-01 The prototype is excluded from the production build

The production build writes to the Python package folder from a single page, and the repository guide states the prototype page is deliberately left out of it.

- **Used in:** [[UC-02 Rebuild the dashboard bundle]], [[UC-03 Develop the dashboard against live data]]

Source:
- [[web/vite.config.ts|web/vite.config.ts]]: `outDir: '../src/ai_usage_cost/web/dist',`
- [[web/src/design-system/MIGRATION.md|web/src/design-system/MIGRATION.md]]

## BR-02 Prototype filters do not filter the screens

The filter rail in the prototype changes its own state and chips, but the screens are rendered without any filter value, so the figures on screen never change.

- **Used in:** [[UC-01 Compare a dashboard screen with its reference]], [[UC-28 Sort the session list and open one session in the prototype]]

Source:
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `const [filters, setFilters] = useState<FilterState>(INITIAL_FILTERS)`
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `<SessionsScreen onOpen={setActive} />`

## BR-03 Prototype session table shows at most 120 rows

The prototype sorts all sessions and then displays only the first 120.

- **Used in:** [[UC-28 Sort the session list and open one session in the prototype]]

Source:
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `export const SESSION_LIMIT = 120`
- [[web/src/prototype/SessionsScreen.tsx|web/src/prototype/SessionsScreen.tsx]]: `const shown = sorted.slice(0, SESSION_LIMIT)`

## BR-04 Prototype splits session cost across token buckets by fixed weights

The session drawer apportions a session's cost across the four token buckets with constant weights, not with real rates.

- **Used in:** [[UC-01 Compare a dashboard screen with its reference]], [[UC-28 Sort the session list and open one session in the prototype]]

Source:
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `const BUCKET_WEIGHT: Record<string, number> = {`
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `total > 0 ? (weighted[index] / total) * session.cost! : 0,`

## BR-05 Prototype rescan is staged

The Rescan logs button only shows a scanning state for 900 milliseconds and reads no logs.

- **Used in:** [[UC-01 Compare a dashboard screen with its reference]], [[UC-28 Sort the session list and open one session in the prototype]]

Source:
- [[web/src/prototype/Prototype.tsx|web/src/prototype/Prototype.tsx]]: `setTimeout(() => setScanning(false), 900)`

## BR-06 Prototype figures are invented

The headline totals are literal numbers and the session list is generated from a few seed sessions.


Source:
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `cost: 3_431.96,`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `for (let index = 0; generated.length + seeded.length < 184; index++) {`

## BR-07 Do not import from the prototype folder

The migration guide tells porters to copy the composition of a prototype screen and never to import from the prototype folder.


Source:
- [[web/src/design-system/MIGRATION.md|web/src/design-system/MIGRATION.md]]

## BR-08 A type error stops the dashboard build

The web build script runs the TypeScript check before Vite, so a type error prevents a bundle from being written.

- **Category:** quality
- **Used in:** [[UC-02 Rebuild the dashboard bundle]], [[UC-03 Develop the dashboard against live data]]

Source:
- [[web/package.json|web/package.json]]: `"build": "tsc --noEmit && vite build",`

## BR-09 A production build replaces the committed bundle

Every production build empties the output folder inside the Python package before writing the new bundle.

- **Category:** build
- **Used in:** [[UC-02 Rebuild the dashboard bundle]], [[UC-03 Develop the dashboard against live data]]

Source:
- [[web/vite.config.ts|web/vite.config.ts]]: `emptyOutDir: true,`

## BR-10 Lint skips build output

ESLint ignores the local dist folder and the bundle inside the Python package.

- **Category:** quality

Source:
- [[web/eslint.config.js|web/eslint.config.js]]: `{ ignores: ['dist', '../src/ai_usage_cost/web/dist'] },`

## BR-100 _valid_window refuses when any((not 0 ‹= day ‹= 6 for day in self.weekdays))

In _valid_window, when any((not 0 <= day <= 6 for day in self.weekdays)): the code raises ValueError, message "peak weekdays must be 0 (Monday) to 6 (Sunday)". Located at src/ai_usage_cost/pricing.py lines 55-56.

- **Category:** guard

Source:
- `_valid_window`: `if any(not 0 <= day <= 6 for day in self.weekdays):`

## BR-101 _valid_window refuses when any((not 0 ‹= start ‹ end ‹= 24 for start, end in self

In _valid_window, when any((not 0 <= start < end <= 24 for start, end in self.utc_hours)): the code raises ValueError, message "peak utc_hours ranges must satisfy 0 <= start < end <= 24". Located at src/ai_usage_cost/pricing.py lines 58-59.

- **Category:** guard

Source:
- `_valid_window`: `if any(not 0 <= start < end <= 24 for start, end in self.utc_hours):`

## BR-102 _ordered validates the model

In _ordered, the model: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 90-93.

- **Category:** validator

Source:
- `_ordered`: `def _ordered(self) -> Period:`

## BR-103 _ordered refuses when self.from_ is not None and self.until is not None and (

In _ordered, when self.from_ is not None and self.until is not None and (self.from_ >= self.until): the code raises ValueError, message "period `from` must be earlier than `until`". Located at src/ai_usage_cost/pricing.py lines 91-92.

- **Category:** guard

Source:
- `_ordered`: `if self.from_ is not None and self.until is not None and self.from_ >= self.until:`

## BR-104 _sorted_bands validates bands

In _sorted_bands, bands: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 149-150.

- **Category:** validator

Source:
- `_sorted_bands`: `def _sorted_bands(cls, bands: list[Band]) -> list[Band]:`

## BR-105 _disjoint_periods validates the model

In _disjoint_periods, the model: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 153-160.

- **Category:** validator

Source:
- `_disjoint_periods`: `def _disjoint_periods(self) -> ModelRate:`

## BR-106 _disjoint_periods refuses when earlier.until is None or (later.from_ or date.min) ‹ ea

In _disjoint_periods, when earlier.until is None or (later.from_ or date.min) < earlier.until: the code raises ValueError. Located at src/ai_usage_cost/pricing.py lines 158-159.

- **Category:** guard

Source:
- `_disjoint_periods`: `if earlier.until is None or (later.from_ or date.min) < earlier.until:`

## BR-107 _consistent validates the model

In _consistent, the model: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 272-283.

- **Category:** validator

Source:
- `_consistent`: `def _consistent(self) -> RateTable:`

## BR-108 _consistent refuses when duplicates

In _consistent, when duplicates: the code raises ValueError. Located at src/ai_usage_cost/pricing.py lines 275-276.

- **Category:** guard

Source:
- `_consistent`: `if duplicates:`

## BR-109 _consistent refuses when missing

In _consistent, when missing: the code raises ValueError. Located at src/ai_usage_cost/pricing.py lines 281-282.

- **Category:** guard

Source:
- `_consistent`: `if missing:`

## BR-11 Python code must keep a pylint score of 9.0

Both the Python workflow and the pre-commit hook fail when pylint scores below 9.0.

- **Category:** quality

Source:
- [[pyproject.toml|pyproject.toml]]: `fail-under = 9.0`
- `.github/workflows/python.yml`: `run: uv run --no-sync pylint src tests --fail-under=9.0`

## BR-110 read_content refuses when config.metadata_only or span.content_path is None

In read_content, when config.metadata_only or span.content_path is None: the code raises ContentUnavailable. Located at src/ai_usage_cost/privacy.py lines 87-88.

- **Category:** guard

Source:
- `read_content`: `if config.metadata_only or span.content_path is None:`

## BR-111 resolve_path refuses when index ›= len(current)

In resolve_path, when index >= len(current): the code raises ContentUnavailable. Located at src/ai_usage_cost/privacy.py lines 109-110.

- **Category:** guard

Source:
- `resolve_path`: `if index >= len(current):`

## BR-112 _values_match_provenance validates the model

In _values_match_provenance, the model: the code validates before accepting the value. Located at src/ai_usage_cost/trace.py lines 89-101.

- **Category:** validator

Source:
- `_values_match_provenance`: `def _values_match_provenance(self) -> Span:`

## BR-113 _values_match_provenance refuses when (value is None) != (provenance == 'unavailable')

In _values_match_provenance, when (value is None) != (provenance == 'unavailable'): the code raises ValueError. Located at src/ai_usage_cost/trace.py lines 96-100.

- **Category:** guard

Source:
- `_values_match_provenance`: `if (value is None) != (provenance == "unavailable"):`

## BR-114 A settings file that cannot be loaded is ignored as a whole

When the optional settings file is missing, unreadable, not valid JSON or fails validation, every setting takes its default at once, not only the faulty one, and no warning is raised.

- **Category:** privacy

Source:
- [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py]]: `except (OSError, ValueError):`
- [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py]]: `except ValidationError:`

## BR-115 Chart colours follow position, not meaning

The picture writer takes colours from one seven colour list by position. In the cost per day chart a colour is a client, in the model chart a rank, and in the token mix chart a token bucket, so the same colour means a different thing in each panel.

- **Used in:** [[UC-16 Export a usage and cost chart as a PNG image]]

Source:
- [[src/ai_usage_cost/render/png.py|src/ai_usage_cost/render/png.py]]: `color=PALETTE[index % len(PALETTE)],`
- [[src/ai_usage_cost/render/png.py|src/ai_usage_cost/render/png.py]]: `color=[PALETTE[i % len(PALETTE)] for i in range(len(buckets))],`
- [[src/ai_usage_cost/render/png.py|src/ai_usage_cost/render/png.py]]: `ax.barh(labels, values, left=left, label=name, color=PALETTE[index % len(PALETTE)])`

## BR-12 Web dependencies are installed from the lockfile

The web workflow installs with npm ci, which installs exactly what package-lock.json records.

- **Category:** build

Source:
- `.github/workflows/web.yml`: `run: npm ci`

## BR-122 Drawer trace blocks show the same sample data for every traced session

The context window, trace, insights and capability blocks of the session drawer are read from fixed sample arrays and are not derived from the chosen session, so they are identical for every session whose traced flag is true.

- **Used in:** [[UC-01 Compare a dashboard screen with its reference]], [[UC-28 Sort the session list and open one session in the prototype]]

Source:
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `spans={TRACE_SPANS.map((span) => ({`
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `points={CONTEXT_SNAPSHOTS}`

## BR-123 Screens stay mounted across the four screen tabs but not across the gallery

The Screens component owns the filter state and the active session. It stays mounted while the tab moves between the four screens, and it is replaced by the gallery for the design system tab, so a visit to the gallery resets the filters.

- **Used in:** [[UC-01 Compare a dashboard screen with its reference]], [[UC-28 Sort the session list and open one session in the prototype]]

Source:
- [[web/src/prototype/Prototype.tsx|web/src/prototype/Prototype.tsx]]: `{tab === 'gallery' ? (`
- [[web/src/prototype/Screens.tsx|web/src/prototype/Screens.tsx]]: `const [filters, setFilters] = useState<FilterState>(INITIAL_FILTERS)`

## BR-124 A workspace tab loads its data only when first opened

The Trace, Economics and Context tabs of a session fetch from the server only after the reader has selected them once; the Summary tab needs no request. [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:472]]

- **Category:** behaviour
- **Used in:** [[UC-06 Inspect one session]], [[UC-07 Rate a session outcome]]

Source:
- `useLazyResource`: `if (!enabled) return`

## BR-125 Span text is fetched once per span

The text of a trace span is requested the first time the reader opens it and the stored result, content or error, is reused afterwards. [[web/src/TraceTab.tsx|web/src/TraceTab.tsx:791]]

- **Category:** behaviour

Source:
- `toggleContent`: `if (alreadyOpen || contents[span.span_id]) return`

## BR-13 getJson refuses when !response.ok

In getJson, when !response.ok: the code throws ApiError, message "${path} responded ${response.status} ${response.statusText}". Located at web/src/api.ts lines 496-497.

- **Category:** guard

Source:
- `getJson`: `if (!response.ok) {`

## BR-14 useChart refuses when !context

In useChart, when !context: the code throws Error, message "useChart must be used within a <ChartContainer />". Located at web/src/components/ui/chart.tsx lines 32-33.

- **Category:** guard

Source:
- `useChart`: `if (!context) {`

## BR-15 Unavailable is never shown as zero

When a log does not carry a value, the dashboard shows it as unavailable instead of a zero or a guess.

- **Used in:** [[UC-06 Inspect one session]], [[UC-07 Rate a session outcome]]

Source:
- [[web/src/Sources.tsx|web/src/Sources.tsx]]: `unavailable: 'the log does not carry it',`
- [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx]]: `return 'This client logs no token counts, so cost is left blank instead of guessed.'`

## BR-16 Unpriced cost stays out of totals

A session whose model matches no rate entry shows its tokens but its cost is kept out of totals.

- **Used in:** [[UC-06 Inspect one session]], [[UC-07 Rate a session outcome]]

Source:
- [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx]]: `return 'Tokens are counted, no rate entry matches this model, so cost stays out of totals.'`

## BR-17 Reported cost divergence threshold

The tool's own cost is flagged as different when it differs from the computed cost by more than five percent or one cent, whichever is larger.


Source:
- [[web/src/pricing-notes.ts|web/src/pricing-notes.ts]]: `return Math.abs(computed - reported) > Math.max(0.05 * Math.abs(computed), 0.01)`

## BR-18 Rate age notice thresholds

A notice about old prices appears from 30 days and becomes a caution from 90 days. Unknown age shows nothing.


Source:
- [[web/src/pricing-notes.ts|web/src/pricing-notes.ts]]: `if (days < STALE_INFO_DAYS) return null`
- [[web/src/pricing-notes.ts|web/src/pricing-notes.ts]]: `severity: days >= STALE_CAUTION_DAYS ? 'caution' : 'info',`

## BR-19 Cache price derivation

A cache price is the published figure when present, otherwise the input price times the provider ratio, otherwise it is not shown.


Source:
- [[web/src/pricing-format.ts|web/src/pricing-format.ts]]: `return rate.input * rules[field]`

## BR-20 Rate row state

A rate row is free when its rules say free, priced when matched buckets carry spend, and unused otherwise.

- **Used in:** [[UC-08 Check list prices]]

Source:
- [[web/src/Pricing.tsx|web/src/Pricing.tsx]]: `const state: RateState = isFree ? 'free' : spendValue > 0 ? 'priced' : 'unused'`

## BR-21 Sub cent money keeps four decimals

A nonzero amount under one cent is shown with up to four decimals so it never reads as zero dollars.


Source:
- [[web/src/format.ts|web/src/format.ts]]: `return value !== 0 && Math.abs(value) < 0.01 ? moneyPrecise.format(value) : money.format(value)`

## BR-22 Unattributed turn is excluded from rankings

Turn rankings and insights ignore the row for spend outside any turn.


Source:
- [[web/src/turn-insights.ts|web/src/turn-insights.ts]]: `return rows.filter((row) => row.key !== UNATTRIBUTED_TURN_KEY)`

## BR-23 Session table row limit

The sessions table shows at most 120 rows of the sorted list.


Source:
- [[web/src/Sessions.tsx|web/src/Sessions.tsx]]: `const SHOWN_LIMIT = 120`

## BR-24 Outcome notes are saved only when changed

Notes and tags are sent to the server on blur only when the text differs from the saved value.

- **Used in:** [[UC-06 Inspect one session]], [[UC-07 Rate a session outcome]]

Source:
- [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx]]: `if (current.notes === persisted.notes && current.tagsText === persisted.tagsText) return`

## BR-25 Automatic rescan every five minutes

While the tab is visible the dashboard asks the server to rescan logs every five minutes.

- **Used in:** [[UC-05 Read usage and cost for a period]], [[UC-06 Inspect one session]], [[UC-08 Check list prices]]

Source:
- [[web/src/App.tsx|web/src/App.tsx]]: `const FIVE_MINUTES = 5 * 60 * 1000`
- [[web/src/App.tsx|web/src/App.tsx]]: `if (interval === null) interval = setInterval(doRefresh, FIVE_MINUTES)`

## BR-26 A missing value is shown as unavailable, never as zero

Meters, bucket bars, comparison bars, token cells and session cards show the unavailable marker when a value is null or a total is not positive, and draw no bar.

- **Category:** display

Source:
- `Meter`: `if (value === null) {`
- `BucketBar`: `if (total <= 0) {`
- `TokenCell`: `if (label === null) {`

## BR-27 A rollup shows its least trustworthy cost state and provenance

When several rows are combined, the worst cost state (unavailable over unpriced over free over priced) and the worst provenance are shown. An empty list gives unavailable.

- **Category:** calculation

Source:
- `worstState`: `return [...states].sort((a, b) => STATE_RANK[b] - STATE_RANK[a])[0] ?? 'unavailable'`
- `worstProvenance`: `return [...values].sort((a, b) => PROVENANCE_RANK[b] - PROVENANCE_RANK[a])[0] ?? 'unavailable'`

## BR-28 An estimated price is marked next to the cost state

A priced row that used a sibling model's rate gets an Estimated badge in a purple hue, so it is not mistaken for an unpriced row, which is left out of totals.

- **Category:** display

Source:
- `CostBadges`: `{isEstimatedPriced(state, cost) ? <EstimatedBadge className={className} /> : null}`

## BR-29 The daily chart names at most twelve series

The stacked daily cost chart gives its twelve largest series their own colour and legend entry, and groups all others under Other with a count.

- **Category:** display

Source:
- `TimeChart`: `const overflowKeys = keys.slice(LEGEND_LIMIT)`
- `SERIES_SLOTS`: `export const SERIES_SLOTS = 12`

## BR-30 A table always keeps at least one column

If the reader hides every column, all columns are shown again.

- **Category:** display

Source:
- `visibleColumns`: `return shown.length > 0 ? shown : columns`

## BR-31 The date range cannot cross itself

The from date cannot be later than the to date, and the to date cannot be earlier than the from date.

- **Category:** validation

Source:
- `DateRange`: `max={until ?? max}`
- `DateRange`: `min={since ?? min}`

## BR-32 The side panel width is bounded

The workspace side panel is at least 360 pixels wide and at most 900 pixels or 90 percent of the window, whichever is smaller.

- **Category:** validation

Source:
- `clampWidth`: `return Math.min(bound, Math.max(MIN_WIDTH, width))`

## BR-33 An explanation popover does not take focus back on close

Closing the metric explanation popover does not return focus to its trigger, because focusing the trigger opens the popover again.

- **Category:** behaviour

Source:
- `MetricInfo`: `onCloseAutoFocus={(event) => event.preventDefault()}`

## BR-34 Caller class names override primitive defaults

Every primitive merges its default Tailwind classes with the caller className through cn, so a caller override replaces a conflicting default instead of stacking with it.

- **Category:** design system

Source:
- `cn`: `return twMerge(clsx(inputs))`

## BR-35 Toggle group settings win over item settings

A toggle group passes its variant, size and spacing to its items through a context, and an item uses its own variant or size only when the group sets none.

- **Category:** design system

Source:
- `ToggleGroupItem`: `data-variant={context.variant || variant}`

## BR-36 Chart parts require a chart container

The chart tooltip and legend content read the chart config through a context, and using them outside a chart container throws an error.

- **Category:** design system

Source:
- `useChart`: `throw new Error("useChart must be used within a <ChartContainer />")`

## BR-37 Sheet opens from the right by default

A sheet slides in from the right unless a side of top, bottom or left is given, and both sheet and dialog show a close button unless showCloseButton is false.

- **Category:** design system

Source:
- `SheetContent`: `side = "right",`
- `DialogContent`: `showCloseButton = true,`

## BR-38 Tooltip provider default delay is zero

The tooltip provider shows tooltips without a hover delay unless the app gives a delayDuration, and the dashboard roots give 200 milliseconds.

- **Category:** design system

Source:
- `TooltipProvider`: `delayDuration = 0,`

## BR-39 Readers only read

A SQLite store is opened through a read only URI and a database error becomes a warning, so a reader never changes the file it measures.

- **Category:** privacy
- **Used in:** [[UC-13 Discover AI tool usage from local files]]

Source:
- [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py]]: `uri = f"file:{path.as_posix()}?mode=ro"`

## BR-40 A reader is found by its SOURCE value

The registry keeps the SOURCE of every module in the readers package except the base module, so adding a reader needs no list edit.

- **Used in:** [[UC-13 Discover AI tool usage from local files]]

Source:
- [[src/ai_usage_cost/sources/__init__.py|src/ai_usage_cost/sources/__init__.py]]: `source = getattr(module, "SOURCE", None)`

## BR-41 Unparsable lines are skipped and counted

A JSON Lines reader skips lines that are not valid JSON and adds one warning per file with the count.

- **Used in:** [[UC-13 Discover AI tool usage from local files]]

Source:
- [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py]]: `warnings.append(f"{path.name}: skipped {bad} unparsable lines")`

## BR-42 Synthetic Claude Code records are not usage

A Claude Code assistant record with no model or a synthetic model is skipped.


Source:
- [[src/ai_usage_cost/sources/claude_code.py|src/ai_usage_cost/sources/claude_code.py]]: `if not model or model in SYNTHETIC_MODELS:`

## BR-43 Repeated Codex token totals are not counted twice

A Codex token_count record whose total is unchanged is skipped, because Codex repeats it on rate limit updates.


Source:
- [[src/ai_usage_cost/sources/codex.py|src/ai_usage_cost/sources/codex.py]]: `if total == previous_total_snapshot:`

## BR-44 Muse Code control folders are skipped

The Muse Code reader skips the view and model catalog folders when it lists session files.


Source:
- [[src/ai_usage_cost/sources/muse_code.py|src/ai_usage_cost/sources/muse_code.py]]: `_SKIP_DIRS = frozenset({".msp-view-v1", "model-catalog"})`

## BR-45 Experimental readers carry a flag

A reader whose parser has not been checked against a real session sets experimental to true.

- **Used in:** [[UC-13 Discover AI tool usage from local files]]

Source:
- [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py]]: `experimental: bool = False`

## BR-46 Terminal table shows at most 30 rows

The terminal breakdown table prints only the first 30 buckets, with no notice that rows were cut.


Source:
- `_bucket_table`: `for bucket in rows[:30]:`

## BR-47 Day breakdown is listed oldest first

Only the day grouping is sorted ascending by key; every other grouping keeps the order of the report.


Source:
- `render`: `ascending=group_by == "day"`

## BR-48 Unknown grouping falls back to model

A grouping name that is not model, client, provider, project or day is treated as model.


Source:
- `render`: `tables.get(group_by, tables["model"])`

## BR-49 Warnings are summarised unless verbose

Without the verbose flag the terminal shows only the number of warnings.


Source:
- `render`: `elif report.warnings:`

## BR-50 Unpriced models are shown but not totalled

Models without a rate appear in their own table and are described as excluded from totals.


Source:
- `render`: `Unpriced models (excluded from totals)`

## BR-51 PNG charts are limited to the top buckets

The model cost chart and project cost chart show at most 10 buckets and the token mix chart at most 8 models.


Source:
- `_cost_by_model`: `buckets = report.by_model[:10][::-1]`
- `_token_mix`: `buckets = report.by_model[:8][::-1]`

## BR-52 Empty project panel is left blank

When the report has no project buckets the project chart panel is switched off instead of drawn.


Source:
- `_cost_by_project`: `ax.set_axis_off()`

## BR-53 Export accepts only json and png

The export command refuses any other extension with exit code 2.


Source:
- `export`: `raise typer.Exit(code=2)`

## BR-87 create_app refuses when path is None

In create_app, when path is None: the code raises HTTPException with status 503, message "this analysis was built without a store". Located at src/ai_usage_cost/api.py lines 222-223.

- **Category:** guard

Source:
- `create_app`: `if path is None:`

## BR-88 opened refuses when path is None

In opened, when path is None: the code raises HTTPException with status 503, message "this analysis was built without a store". Located at src/ai_usage_cost/api.py lines 222-223.

- **Category:** guard

Source:
- `opened`: `if path is None:`

## BR-89 create_app refuses when not store.session_exists(conn, source, session_id)

In create_app, when not store.session_exists(conn, source, session_id): the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 235-236.

- **Category:** guard

Source:
- `create_app`: `if not store.session_exists(conn, source, session_id):`

## BR-90 session_spans refuses when not store.session_exists(conn, source, session_id)

In session_spans, when not store.session_exists(conn, source, session_id): the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 235-236.

- **Category:** guard

Source:
- `session_spans`: `if not store.session_exists(conn, source, session_id):`

## BR-91 create_app refuses when not store.session_exists(conn, source, session_id) (line 364)

In create_app, when not store.session_exists(conn, source, session_id): the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 364-365.

- **Category:** guard

Source:
- `create_app`: `if not store.session_exists(conn, source, session_id):`

## BR-92 forget_session refuses when not store.session_exists(conn, source, session_id)

In forget_session, when not store.session_exists(conn, source, session_id): the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 364-365.

- **Category:** guard

Source:
- `forget_session`: `if not store.session_exists(conn, source, session_id):`

## BR-93 create_app refuses when span is None

In create_app, when span is None: the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 377-378.

- **Category:** guard

Source:
- `create_app`: `if span is None:`

## BR-94 span_content refuses when span is None

In span_content, when span is None: the code raises HTTPException with status 404. Located at src/ai_usage_cost/api.py lines 377-378.

- **Category:** guard

Source:
- `span_content`: `if span is None:`

## BR-95 _roots refuses when not path

In _roots, when not path: the code raises typer.BadParameter. Located at src/ai_usage_cost/cli.py lines 65-66.

- **Category:** guard

Source:
- `_roots`: `if not path:`

## BR-96 alert refuses when days ‹ 1

In alert, when days < 1: the code raises typer.BadParameter, message "--days must be at least 1". Located at src/ai_usage_cost/cli.py lines 320-321.

- **Category:** guard

Source:
- `alert`: `if days < 1:`

## BR-97 alert refuses when over is not None and rise_over is not None

In alert, when over is not None and rise_over is not None: the code raises typer.BadParameter, message "pass --over or --rise-over, not both". Located at src/ai_usage_cost/cli.py lines 322-323.

- **Category:** guard

Source:
- `alert`: `if over is not None and rise_over is not None:`

## BR-98 alert refuses when threshold is None

In alert, when threshold is None: the code raises typer.BadParameter, message "pass --over (window total) or --rise-over (rise vs before)". Located at src/ai_usage_cost/cli.py lines 325-326.

- **Category:** guard

Source:
- `alert`: `if threshold is None:`

## BR-99 _valid_window validates the model

In _valid_window, the model: the code validates before accepting the value. Located at src/ai_usage_cost/pricing.py lines 54-60.

- **Category:** validator

Source:
- `_valid_window`: `def _valid_window(self) -> Peak:`
