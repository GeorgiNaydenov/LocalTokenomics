---
title: Risks and Open Questions
aliases: []
tags: [generated, open-question, risks, spec]
area: operations
status: generated
audience: internal
maturity: draft
confidence: confirmed
covers: [src/ai_usage_cost/aggregate.py, src/ai_usage_cost/api.py, src/ai_usage_cost/cli.py,
  src/ai_usage_cost/collect.py, src/ai_usage_cost/models.py, src/ai_usage_cost/pipeline.py,
  src/ai_usage_cost/pricing.py, src/ai_usage_cost/privacy.py, src/ai_usage_cost/store.py,
  web/src/App.tsx, web/src/Header.tsx, web/src/SessionWorkspace.tsx, web/src/Sessions.tsx,
  web/src/TraceTab.tsx, web/src/api.ts, web/src/components/chart-time.tsx, web/src/components/columns.tsx,
  web/src/components/metric-info.tsx, web/src/components/rank.test.ts, web/src/components/states.tsx,
  web/src/components/ui/chart.tsx, web/src/format.ts, web/src/main.tsx, web/src/prototype/Prototype.tsx]
generated: true
anchors: true
---

# Risks and Open Questions

> [!info] What this is
> What could go wrong and what is not yet known, each with the code that raises it.

## RSK-01 Prototype looks live but is staged

Filters, the rescan button and the scanned 2 min ago text suggest real behaviour but do nothing, so a reader may take the prototype for working product.

Notes state the staged parts; the migration guide marks the folder read only.


## RSK-02 Design system README and migration guide are out of date

The README says the shipped dashboard still runs on the old src/ds CSS system, but the shipped entry point already imports the new theme and the ds folder is absent.

Open question for the owner of the web folder; this chunk does not edit those files.


## RSK-03 No tests cover the prototype

No test file imports or lives inside the prototype folder, so a change to a reference screen is unchecked except by typecheck and lint.

Accepted: the folder is read only reference code.


## RSK-04 Mypy is a manual pre-commit stage, so type errors in the Pyt

Mypy is a manual pre-commit stage, so type errors in the Python package are caught only by the workflow or a deliberate local run.

The Python workflow runs mypy on src for every pull request.

- **Impact:** low, likelihood medium
Source:
- `.pre-commit-config.yaml`: `stages: [manual]`

## RSK-05 Bandit security scanning skips the web folder, so dashboard

Bandit security scanning skips the web folder, so dashboard code gets security analysis only from CodeQL.

The CodeQL workflow scans JavaScript and TypeScript on every pull request and weekly.

- **Impact:** low, likelihood low
Source:
- [[pyproject.toml|pyproject.toml]]: `exclude_dirs = ["tests", ".venv", "web"]`

## RSK-06 Risk 1꞉ The dashboard client can write to the

The dashboard client can write to the server with PUT for outcomes and DELETE for sessions, although it mainly reads usage.

Confirm in the server chunk that delete only removes derived trace data; see [[web/src/api.ts|web/src/api.ts:593]].


## RSK-07 Risk 2꞉ Most files in this chunk have no

Most files in this chunk have no test importing them, only the pure helper modules are tested.

Add component tests for the views if they change often; the tested helpers include [[web/src/format.ts|web/src/format.ts:20]].


## RSK-08 Most shared components have no tests

Only the info popover, the ranking helpers and the sparkline geometry have tests. The stat cards, the daily chart, the filters, the column chooser and the session and trace views are untested, so a change can break a figure shown to the reader unnoticed. [[web/src/components/rank.test.ts|web/src/components/rank.test.ts:4]]

Add tests for the display rules recorded in this chunk, starting with the unavailable marker and the twelve series limit.

- **Impact:** medium, likelihood medium

## RSK-09 Popover timing depends on a polling interval

The info popover decides to open and close from a 100 ms poll of the pointer position, so it can lag on a slow machine. [[web/src/components/metric-info.tsx|web/src/components/metric-info.tsx:11]]

The popover also opens on focus and click, so it is reachable without the poll. [[web/src/components/metric-info.tsx|web/src/components/metric-info.tsx:143]]

- **Impact:** low, likelihood low

## RSK-10 Primitives have no tests of their own

No test file lives in this folder, so a change to a shared primitive is exercised only through the screens that import it.

Cover primitives through the screens that use them, or add tests beside the primitives.


## RSK-11 Cline family token semantics unverified

Cline family token semantics are unverified: it is not known whether input tokens include cache buckets, so cost may be off.

The policy is held per source in one table and the module header says to flip it when a real log shows otherwise.


## RSK-12 Copilot CLI and Muse Code unchecked against real logs

Copilot CLI and Muse Code were built without a real log to check against, so their totals may be wrong.

Both are flagged experimental and shown with a badge.


## RSK-13 Render layer has no tests of its own

No test file imports or lives inside the render folder, so output format changes are not caught here.

Add tests for the headline text, the 30 row cut and the empty project panel.

- **Impact:** medium, likelihood medium
Source:
- `render`: `def render(`

## RSK-14 Silent row truncation in terminal tables

Only 30 rows are printed and nothing tells the user that more exist.

Print a note when buckets are cut.

- **Impact:** low, likelihood medium
Source:
- `_bucket_table`: `for bucket in rows[:30]:`

## RSK-15 HTTP routes have no authentication

No route checks a caller [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:198]].

The default host is the loopback address [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:110]] and metadata only is on by default [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:53]].

- **Impact:** Anyone who can reach the port can read costs and, with the content route, span text if metadata only is off, and can forget sessions, likelihood low while the host stays on loopback

## RSK-16 Daily series uses the UTC date

Buckets by day use the local day [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:704]] while the series uses [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:544]].

Not found in the code. See the open question on the series day.

- **Impact:** The by day buckets and the series can place the same event on different days near midnight, likelihood medium

## RSK-17 Secret patterns are a fixed list

Redaction relies on nine patterns [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:14]].

Content is off by default [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:53]] and text is cut to a byte limit [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:11]].

- **Impact:** A secret in a form the patterns do not match is returned in released text, likelihood low, and only when metadata only is off

## RSK-18 A privacy typo silently resets the settings

An invalid file is replaced by defaults without a message [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:67]].

Not found in the code.

- **Impact:** A person who mistypes config.json believes a project is excluded but the defaults apply, likelihood medium

## RSK-19 Content retention is accepted but does nothing

The setting is read but no content is stored [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:242]].

The pipeline adds a warning when it is set.

- **Impact:** A person may expect text to expire, likelihood low

## RSK-20 Prices drift from the vendors

The table carries an as of date and warns only after a fixed age [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:179]].

Estimated, unpriced and tier gaps are warned about each scan.

- **Impact:** Cost figures can be wrong without any warning until the table is 30 days old, likelihood medium

## RSK-21 A mistyped settings file silently drops the project exclusions

One wrong value in the settings file, for example text where a number belongs, makes the whole file fall back to defaults. A project named in exclude_projects is then no longer excluded at ingest, and nothing tells the user.

Raise a warning when the file exists but fails to load or validate, or validate each key on its own so one bad key cannot discard the others.

- **Impact:** medium, likelihood low
Source:
- [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py]]: `except ValidationError:`
- [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py]]: `exclude_projects=config.exclude_projects,`

## RSK-22 Bandit is configured but no workflow or hook runs it

The package file holds a bandit section and the dev extras install bandit, but the Python workflow steps and the pre-commit hooks never call it. The security lint therefore never gates a change; only CodeQL does.

Add a bandit step to the Python workflow, or remove the unused section and extra so the files do not suggest a check that does not run.

- **Impact:** low, likelihood high
Source:
- [[pyproject.toml|pyproject.toml]]: `[tool.bandit]`
- [[pyproject.toml|pyproject.toml]]: `"bandit>=1.7",`
- `.github/workflows/python.yml`: `run: uv run --no-sync pytest -q`

## RSK-23 Export writes a chart for a report with no events

The scan command refuses an empty report with a hint and exit code 1, but the export command has no such check, so a png export of an empty report writes a figure with a zero cost title and empty axes and then prints that it wrote the file.

Share the empty report check between the two commands, or print a warning before the picture is written.

Source:
- [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py]]: `if not report.totals.events:`
- [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py]]: `write_png(report, out)`
- [[src/ai_usage_cost/render/png.py|src/ai_usage_cost/render/png.py]]: `fig.suptitle(`

## RSK-24 A missing timestamp is stamped with the scan time

Copilot Chat, Dyad and Ollama call parse_timestamp without a fallback file. When the stored time is missing or unreadable the helper returns the current time, so the event lands on the day of the scan and moves each time the file is rebuilt.

Pass the file path as the fallback, as the other readers do, or skip the row and add a warning.

- **Impact:** low, likelihood low
Source:
- [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py]]: `return datetime.now(tz=UTC)`
- [[src/ai_usage_cost/sources/copilot_chat.py|src/ai_usage_cost/sources/copilot_chat.py]]: `timestamp=parse_timestamp(timestamp),`
- [[src/ai_usage_cost/sources/dyad.py|src/ai_usage_cost/sources/dyad.py]]: `timestamp=parse_timestamp(created_at),`
- [[src/ai_usage_cost/sources/ollama_app.py|src/ai_usage_cost/sources/ollama_app.py]]: `timestamp=parse_timestamp(created_at),`

## RSK-25 One broken reader module stops the registry

The registry imports every module of the package with no guard, so an import error in a single reader raises out of the registry call and no reader can be used until the module is fixed.

Catch the import error per module, skip that reader and report a warning naming it.

- **Impact:** medium, likelihood low
Source:
- [[src/ai_usage_cost/sources/__init__.py|src/ai_usage_cost/sources/__init__.py]]: `module = importlib.import_module(f"{__name__}.{info.name}")`

## RSK-26 Two readers import a private name from the Cline module

Roo Code and Kilo Code legacy import _TOKENS_IN_INCLUSIVE, a name that starts with an underscore, from the Cline module, so a rename inside Cline breaks them without a public contract saying so.

Expose the table under a public name or pass the flag through Spec.

- **Impact:** low, likelihood low
Source:
- [[src/ai_usage_cost/sources/roo_code.py|src/ai_usage_cost/sources/roo_code.py]]: `from .cline import _TOKENS_IN_INCLUSIVE, Spec, make_source, task_roots`
- [[src/ai_usage_cost/sources/kilo_legacy.py|src/ai_usage_cost/sources/kilo_legacy.py]]: `from .cline import _TOKENS_IN_INCLUSIVE, Spec, make_source, task_roots`

## RSK-27 Forgetting a session keeps its cost

Forgetting deletes only the session's spans and rating [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:597]], and ingest checks exclusions only for spans [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:273]], so its requests are kept and stored again.

Not found in the code. See the open question on forgetting requests.

- **Impact:** A forgotten session still counts in totals and its raw records stay in the store, while its routes answer 404, likelihood high whenever a session is forgotten

## RSK-28 Project exclusion and retention skip requests

Requests are inserted without the exclusion test [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:270]] and retention deletes only trace rows [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:302]].

Not found in the code.

- **Impact:** Requests of an excluded or expired project keep their project, working directory and raw record in the store and in reports, likelihood medium

## RSK-29 Truncation runs before redaction

Released text is truncated first and redacted after [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:97]] [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:98]].

Content is off by default [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:53]].

- **Impact:** A secret cut at the byte limit can fall below a pattern's minimum length and be returned unredacted, likelihood low, and only when metadata only is off

## RSK-30 A bad date option ends in a raw error

Dates are parsed with no guard [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:45]].

Not found in the code.

- **Impact:** A mistyped since or until value shows a Python error instead of a usage message, likelihood medium

## RSK-31 An invalid rate file stops every command

Loading validates the whole file with no handler [[src/ai_usage_cost/pricing.py|src/ai_usage_cost/pricing.py:287]].

The model validators reject duplicate keys and overlapping periods at load, so a bad file fails loudly rather than pricing quietly.

- **Impact:** One malformed rates.json row stops scan, serve, export, alert and tui with a validation error, likelihood low for the bundled file, medium for a file passed with --rates

## RSK-32 Chart style text is built from config keys without escaping

The chart style element is filled by putting each config key and colour into a template string and passing it as HTML. The time chart builds its config keys from row data, so a key that holds a closing brace or a closing style tag would change the style rules or end the element. The data comes from local logs, so the exposure is small, but nothing validates the key. [[web/src/components/ui/chart.tsx|web/src/components/ui/chart.tsx:102]] [[web/src/components/ui/chart.tsx|web/src/components/ui/chart.tsx:92]] [[web/src/components/chart-time.tsx|web/src/components/chart-time.tsx:65]]

Map keys to safe indexed names such as series-1 before they enter the style text, and keep the readable name only in the label.

- **Impact:** medium, likelihood low
Source:
- `ChartStyle`

## RSK-33 A chart part outside its container throws with no error boundary above it

The chart hook throws a plain error when no container is above it, and the app is mounted with one render call and no error boundary, so the error would leave the page blank. [[web/src/components/ui/chart.tsx|web/src/components/ui/chart.tsx:33]] [[web/src/main.tsx|web/src/main.tsx:7]]

Add one error boundary around the app that shows the existing error card with a retry button.

- **Impact:** medium, likelihood low

## RSK-34 A chart legend label is empty for a series with no config entry

The legend content prints only the config label, with no fallback to the series name, so a series missing from the config shows a colour square and no text, while the tooltip falls back to the raw name. [[web/src/components/ui/chart.tsx|web/src/components/ui/chart.tsx:319]] [[web/src/components/ui/chart.tsx|web/src/components/ui/chart.tsx:249]]

Fall back to the series name in the legend as the tooltip does.

- **Impact:** low, likelihood low

## RSK-35 Hidden columns and shown columns can disagree

When a reader unchecks every column, the table guard returns the full column list, so the table still shows every column while the chooser shows every box unchecked. [[web/src/components/columns.tsx|web/src/components/columns.tsx:59]] [[web/src/components/columns.tsx|web/src/components/columns.tsx:85]]

Either keep the last column checked and disabled in the chooser, or show an explanation when the guard applies.

- **Impact:** low, likelihood medium

## RSK-36 A failed copy of the start command gives no feedback

The offline card swallows a rejected clipboard write, so on a browser that blocks clipboard access the button stays at Copy command and the reader is not told that nothing was copied. [[web/src/components/states.tsx|web/src/components/states.tsx:300]]

Show a short failure label or select the command text so the reader can copy it by hand.

- **Impact:** low, likelihood medium

## RSK-37 Empty warnings and empty charts draw nothing

The warnings list, the time chart, the sparkline and the context bars return an empty area or nothing when they have no data, and the component gives no message, so a page that forgets its own empty card shows a blank space. [[web/src/components/chart-time.tsx|web/src/components/chart-time.tsx:95]] [[web/src/components/states.tsx|web/src/components/states.tsx:272]]

Pages already pass an empty card in most places; add the same in every place that renders these parts, or give the parts an empty message prop.

- **Impact:** low, likelihood medium

## RSK-38 Every info box keeps a timer and one global pointer listener

Each info box starts its own 100 ms interval for its whole lifetime, and one pointer listener is added to the window at load and never removed, so a table with many badges runs many timers. [[web/src/components/metric-info.tsx|web/src/components/metric-info.tsx:79]] [[web/src/components/metric-info.tsx|web/src/components/metric-info.tsx:37]]

Start the timer only while the pointer is near or the box is open.

- **Impact:** low, likelihood medium

## RSK-39 A test title says the opposite of what it checks

The rank test named picks measured as the best expects the result derived, which is the worst of the two inputs, so the title misleads a reader of the test list. [[web/src/components/rank.test.ts|web/src/components/rank.test.ts:28]]

Rename the test to say that the worse of measured and derived wins.

- **Impact:** low, likelihood low

## RSK-40 Sessions footer asks the user to narrow filters that do nothing

The footer note says to narrow the filters to see the rest of the sessions, but the screen receives no filter value, so the advice cannot work. A port that copies the text would promise a control the data layer does not apply.

Pass the filter state into the screen when porting, or drop the sentence from the reference.

Source:
- [[web/src/prototype/SessionsScreen.tsx|web/src/prototype/SessionsScreen.tsx]]: `Narrow the filters to see the rest.`

## RSK-41 Session rows can be opened by mouse only

The table row has a click handler and a pointer cursor but no key handler and no tab stop, so a keyboard user cannot open a session. Only the error count has a tab stop. A screen meant as the reference for the real one should not carry this gap.

Make the row focusable and open it on Enter, or put a button in the id cell, in the shipped screen.

Source:
- [[web/src/prototype/SessionsScreen.tsx|web/src/prototype/SessionsScreen.tsx]]: `className="cursor-pointer"`

## RSK-42 Cache prices of providers without rules are defaults, not published prices

The pricing screen derives cache prices from the provider rules and falls back to 0.1 for reads and 1.25 for writes when the provider has none. The rule table lists three providers while the rate table also has deepseek, moonshot and mistral rows, so their cache columns show the default. The note beside the multipliers says discounts differ by provider.

Show a dash, or mark the figure as a default, for providers without a rule.

Source:
- [[web/src/prototype/PricingScreen.tsx|web/src/prototype/PricingScreen.tsx]]: `const rules = PROVIDER_RULES[rate.provider]`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `export const PROVIDER_RULES: Record<string, ProviderRules> = {`

## RSK-43 Overview panels read the first item of a list without a guard

The cost by model panel reads the first ranked model and the project panel reads the first project to write its title. With real data and an empty list both would fail. Averages and shares also divide by totals without a zero check.

Add an empty state for each panel before the layout is ported.

Source:
- [[web/src/prototype/OverviewScreen.tsx|web/src/prototype/OverviewScreen.tsx]]: `const top = ranked[0]`
- [[web/src/prototype/OverviewScreen.tsx|web/src/prototype/OverviewScreen.tsx]]: `const averagePerSession = TOTALS.cost / TOTALS.sessions`

## RSK-44 Sample figures are stored twice and can drift

The spend of each model is written once in the model list and once in the rate table, for example the figure of the top model, with no link between them. An edit to one copy leaves the other stale, and the overview and pricing screens would disagree.

Derive one list from the other, or add a test that compares them.

Source:
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `cost: 1489.22,`
- [[web/src/prototype/data.ts|web/src/prototype/data.ts]]: `spend: 1489.22`

## RSK-45 Risk 5꞉ Sessions are identified by session id alone in the table and when opened

The sessions table keys its rows and opens the workspace by session id only, and the shell looks the row up by that id alone, so two sources that share a session id collide and the first match opens. [[web/src/Sessions.tsx|web/src/Sessions.tsx:354]] [[web/src/App.tsx|web/src/App.tsx:285]]

Pass the source with the session id, as the workspace key already does. [[web/src/App.tsx|web/src/App.tsx:344]]

- **Impact:** medium, likelihood low

## RSK-46 Risk 6꞉ One failed report refetch hides the whole dashboard

A failed report request after the first load sets the shared error, and the shell then replaces every view with an error card that has no retry action. [[web/src/App.tsx|web/src/App.tsx:193]] [[web/src/App.tsx|web/src/App.tsx:274]]

Keep the last report on screen with an inline error and a retry, or pass a retry handler to the error card.

- **Impact:** medium, likelihood medium

## RSK-47 Risk 7꞉ Outcome saves are not sequenced

A rating pick and a notes or tags blur each start a save while another may still run, and the toggle stays enabled during a save, so answers can arrive out of order and the older one can win. [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:274]] [[web/src/SessionWorkspace.tsx|web/src/SessionWorkspace.tsx:312]]

Queue saves or ignore answers of superseded saves.

- **Impact:** low, likelihood low

## RSK-48 Risk 8꞉ A missing span text is recognised by message wording

The trace tab treats an error as not found when its message contains 404, which depends on the wording of the API helper rather than on a status field. [[web/src/TraceTab.tsx|web/src/TraceTab.tsx:60]] [[web/src/api.ts|web/src/api.ts:497]]

Carry the HTTP status on the error object and test it.

- **Impact:** low, likelihood low

## RSK-49 Risk 9꞉ Rescan can be started twice

The Rescan logs button stays enabled while a scan runs, only its label changes, so a second press sends a second refresh. [[web/src/Header.tsx|web/src/Header.tsx:128]] [[web/src/App.tsx|web/src/App.tsx:211]]

Disable the button while rescanning is true.

- **Impact:** low, likelihood medium

## RSK-50 Risk 10꞉ Session rows cannot be opened from the keyboard

A sessions table row opens the workspace on click only, with no tab stop or key handler, while the turn rows of the trace tab do have both. [[web/src/Sessions.tsx|web/src/Sessions.tsx:355]] [[web/src/TraceTab.tsx|web/src/TraceTab.tsx:686]]

Give the row a tab stop and an Enter handler, or put a button in the session cell.

- **Impact:** medium, likelihood high

## OQ-01 Is the prototype still wanted once every screen is ported？

The migration guide treats the folder as a working reference during the port. Should it be deleted or kept after the port, and should the README and guide be updated to say the port is done? Checked web/src/design-system/MIGRATION.md and README.md.


## OQ-02 Is Node 20 tested for the dashboard build

The README asks for Node.js 20 or newer to rebuild the dashboard, but the web workflow only runs Node 22. Is Node 20 meant to be tested?


## OQ-03 Question 3꞉ Does the DELETE session endpoint remove the

Does the DELETE session endpoint remove the user's own log files or only the derived trace store? The client only reports a deleted span count, see web/src/api.ts.


## OQ-04 Question 4꞉ Is deleteSession reachable from any screen in

Is deleteSession reachable from any screen in this chunk? No caller was found in the pages read, only its definition in web/src/api.ts.


## OQ-05 Why the Other series limit is twelve

Is twelve series a design choice or the number of colours defined in the theme? The code only shows the constant in web/src/components/series.ts.


## OQ-06 Which primitives are unused

Dialog, Alert, Accordion and Progress are imported only by the component gallery. Should they stay in the layer or be removed?


## OQ-07 Experimental readers verified？

Which experimental readers have been verified against a real session since their module headers were written?


## OQ-08 Muse Code cache write tokens

Does Muse Code cache_write_tokens sit inside input_tokens? The module marks it unverified.


## OQ-09 Where is the dashboard data produced

The brief for this chunk mentions data for the local dashboard, but the render folder holds only terminal.py and png.py. The dashboard reads the report from the HTTP route in src/ai_usage_cost/api.py. Is the dashboard payload meant to belong to another chunk?


## OQ-10 Does the PNG chart need a group by option

write_png always charts model, project, day and token mix and ignores the grouping the user chose in scan. Is that intended?


## OQ-11 Should the series use the local day

The series groups by the UTC date of an event [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:544]] while every other day view uses the local day [[src/ai_usage_cost/models.py|src/ai_usage_cost/models.py:146]]. Is that intended?

- **Status:** open

## OQ-12 Who may use the HTTP interface

The code has no caller check [[src/ai_usage_cost/api.py|src/ai_usage_cost/api.py:198]]. Is loopback binding the intended only control, and is a non loopback host a supported setup?

- **Status:** open

## OQ-13 Will content capture be built

Metadata only and content retention exist [[src/ai_usage_cost/privacy.py|src/ai_usage_cost/privacy.py:57]] but the pipeline says no content is persisted [[src/ai_usage_cost/pipeline.py|src/ai_usage_cost/pipeline.py:242]]. Is persisted content planned?

- **Status:** open

## OQ-14 Why 30 days for stale rates

The stale rate threshold is a constant [[src/ai_usage_cost/aggregate.py|src/ai_usage_cost/aggregate.py:179]]. What is the reason for the value?

- **Status:** open

## OQ-15 Should the README list content_retention_days

The settings model has a fifth setting, content_retention_days, that is accepted but inert and only produces a warning. The README lists four settings. Is the omission intended?


## OQ-16 Should local checks and the workflow lint the same folders

The README tells contributors to run ruff on src, tests and scripts, while the Python workflow runs ruff on the whole repository root. Which scope is the rule?


## OQ-17 Should the four chart colours keep one meaning across panels？

Colours are assigned by position in each chart, so a reader can take indigo for a client in one panel and for the top model in another. Checked src/ai_usage_cost/render/png.py. Is a fixed colour per client or per model wanted?


## OQ-18 Is the scan helper in the shared module still needed

The shared module has a scan function that loops over roots, files and parse, but the real ingest loop in the store does its own looping with skip and resume logic. Only a test file calls the helper. Should it be removed or reused by the store?

Source:
- [[src/ai_usage_cost/sources/base.py|src/ai_usage_cost/sources/base.py]]: `def scan(`
- [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py]]: `for path in source.files(root):`

## OQ-19 Should forgetting a session remove its requests

Forgetting removes spans and the rating but keeps requests [[src/ai_usage_cost/store.py|src/ai_usage_cost/store.py:595]]. Should the session's cost and raw records also go, and should project exclusion apply to requests?

- **Status:** open

## OQ-20 Sampler error message omits rocm-smi

The sampler supports rocm-smi [[src/ai_usage_cost/collect.py|src/ai_usage_cost/collect.py:88]] but the error names only nvidia-smi and PowerShell [[src/ai_usage_cost/cli.py|src/ai_usage_cost/cli.py:214]]. Is the message stale?

- **Status:** open

## OQ-21 Should the toast host ship in the main app

In the web source only the prototype page mounts the toast host, and the shipped dashboard entry mounts only the tooltip provider. Is the toast primitive meant for a later screen or is it dead code in the shipped app? [[web/src/prototype/Prototype.tsx|web/src/prototype/Prototype.tsx:109]] [[web/src/main.tsx|web/src/main.tsx:9]]


## OQ-22 Are the chart legend parts still needed

The wrapper exports a legend and a legend content part, but the time chart draws its own key list instead. Does any screen plan to use these two, or can they go? [[web/src/components/ui/chart.tsx|web/src/components/ui/chart.tsx:270]] [[web/src/components/chart-time.tsx|web/src/components/chart-time.tsx:174]]


## OQ-23 Should a retry on the offline card show progress

The Retry connection button only bumps a counter in the page and the card shows no pending or failed state, so pressing it twice sends two reloads. Is that intended?


## OQ-24 Is the offline card matched by message text on purpose

The app decides that the reader is offline by looking for a fixed sentence in the error text before it draws the offline card, so a reworded message would show the plain error card instead. Should the failure carry a typed marker? [[web/src/App.tsx|web/src/App.tsx:251]]


## OQ-25 Does the shared token cell clamp a negative bar fraction？

A session without token counts has a token total of minus one, and the table divides it by the largest total to get the bar fraction, which is then negative. The prototype does not clamp it. Checked web/src/prototype/SessionsScreen.tsx; the answer is in the shared session component, which belongs to another chunk.


## OQ-26 Which sort keys does the sort menu offer compared with the column headers？

The column headers can sort by client, model, id and outcome, but the option list of the sort menu has no entry for them, so the menu value after a header press has no matching option. Checked web/src/prototype/SessionsScreen.tsx and web/src/prototype/data.ts; how the menu shows an unknown value is decided in the shared component.


## OQ-27 Question 11꞉ Should filters stay reachable on a large screen while a session is open？

On a large screen the filter rail is hidden while a workspace is open and the Filters button is hidden at that breakpoint, so the filters cannot be reached until the workspace closes. Is that intended? See web/src/App.tsx (docked), web/src/FilterRail.tsx (aside) and web/src/Header.tsx (Filters button).


## OQ-28 Question 12꞉ Which warnings should the Flagged figure count？

The Flagged figure of the overview counts the warning summary of the last scan, while the Sources view lists the warning groups of the current report. Should both use the same set? See web/src/Overview.tsx (FlaggedStat) and web/src/Sources.tsx (Scan warnings panel).


## OQ-29 Question 13꞉ Should failed tabs and span texts offer a retry？

A workspace tab whose endpoint failed and a span text that failed both keep the error with no retry until the session is reopened. Is a retry wanted? See web/src/SessionWorkspace.tsx (LoadableTab) and web/src/TraceTab.tsx (toggleContent).


## OQ-30 Question 14꞉ Should the heaviest sessions on the overview open their session？

The rows of the heaviest sessions panel show a session but have no click handler, unlike the sessions table. Is opening a session from the overview wanted? See web/src/Overview.tsx (HeavyRow).
