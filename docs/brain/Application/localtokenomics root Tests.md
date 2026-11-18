---
title: localtokenomics root Tests
aliases: []
tags: [tests]
area: application
status: draft
audience: internal
maturity: draft
confidence: inferred
covers: [web/*]
verified-against: e5313fbd7062
chunk: ch-localtokenomics-root
---

# localtokenomics root Tests

The tests that cover the localtokenomics root chunk and what they check.

## How it works

188 tests exercise this chunk. 64 of its 75 files are not imported by any test.

## What the tests cover

The tests are Vitest files beside the dashboard code. Vitest runs them in a jsdom browser stand-in, and a shared setup file removes rendered components after every test so one test cannot leak into the next. `web/vite.config.ts:27-30` `web/src/test-setup.ts:6-8` The command is npm test, which maps to vitest run. `web/package.json:12`

The tests check dashboard logic that turns raw numbers into labels, rather than screens. The pricing tests check that spend is summed over every bucket matched to one rate row and that buckets matched to another row are ignored. `web/src/Pricing.test.ts:96-113` Two rows that share a display label must not mix their spend. `web/src/Pricing.test.ts:115-125`

The trace tests check how a span's time window is derived. The end comes from the logged end time, or from the start plus the duration, and stays unknown when neither is logged. `web/src/TraceTab.test.ts:64-79` An unparsable start timestamp leaves the start unknown instead of guessing one. `web/src/TraceTab.test.ts:81-84`

The Python side has its own tests under the tests folder; pyproject.toml points pytest there. `pyproject.toml:51-52` Those belong to the chunks of the Python package.

## What a reader must know

The count above comes from the generated table, which includes every test under the web folder. Most dashboard files have no test of their own, and the quality gate for them is the type check and lint step of the web workflow. `.github/workflows/web.yml:36-43`

## Reference

%% generated:chunk-tests start (do not edit; run brain docs generate) %%
| Test | Scenario | File | Code |
|---|---|---|---|
| `rateUnavailableHint` | Rate unavailable hint | `web/src/EconomicsTab.test.ts` | [[web/src/EconomicsTab.test.ts]] `web/src/EconomicsTab.test.ts:16` |
| `names the missing timing capability instead of claiming no source anywhere logs it` | Names the missing timing capability instead of claiming no source anywhere logs it | `web/src/EconomicsTab.test.ts` | [[web/src/EconomicsTab.test.ts]] `web/src/EconomicsTab.test.ts:17` |
| `names the missing token capability when latency is fine but tokens are not` | Names the missing token capability when latency is fine but tokens are not | `web/src/EconomicsTab.test.ts` | [[web/src/EconomicsTab.test.ts]] `web/src/EconomicsTab.test.ts:21` |
| `falls back to a generic reason when both capabilities are present but this row lacks one` | Falls back to a generic reason when both capabilities are present but this row lacks one | `web/src/EconomicsTab.test.ts` | [[web/src/EconomicsTab.test.ts]] `web/src/EconomicsTab.test.ts:25` |
| `falls back to a generic reason when capability data was not supplied` | Falls back to a generic reason when capability data was not supplied | `web/src/EconomicsTab.test.ts` | [[web/src/EconomicsTab.test.ts]] `web/src/EconomicsTab.test.ts:29` |
| `buildRow spend join by model key` | Build row spend join by model key | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:96` |
| `sums every bucket matched to this row` | Sums every bucket matched to this row | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:97` |
| `ignores buckets matched to another row` | Ignores buckets matched to another row | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:106` |
| `does not collide when two rows share a display label` | Does not collide when two rows share a display label | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:115` |
| `does not credit an estimated bucket to the parent, and lists it separately` | Does not credit an estimated bucket to the parent, and lists it separately | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:127` |
| `reports unused with zero spend when nothing matches` | Reports unused with zero spend when nothing matches | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:140` |
| `estimatedModels` | Estimated models | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:148` |
| `only returns estimated matches, biggest cost first` | Only returns estimated matches, biggest cost first | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:149` |
| `buildRow cache columns` | Build row cache columns | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:160` |
| `derives cache prices from the provider rules` | Derives cache prices from the provider rules | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:161` |
| `prefers absolute prices the row publishes` | Prefers absolute prices the row publishes | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:167` |
| `mixes absolute and derived per field` | Mixes absolute and derived per field | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:173` |
| `keeps provider fields when cache_rules is partial` | Keeps provider fields when cache rules is partial | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:180` |
| `is unavailable (null) with no provider block and no absolute price` | Is unavailable (null) with no provider block and no absolute price | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:189` |
| `shows free for a free provider` | Shows free for a free provider | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:197` |
| `buildRow metadata` | Build row metadata | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:207` |
| `formats the context window` | Formats the context window | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:208` |
| `lists variants with prices` | Lists variants with prices | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:213` |
| `carries band, peak and period detail strings` | Carries band, peak and period detail strings | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:224` |
| `tags preview, retired and unverified rows` | Tags preview, retired and unverified rows | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:239` |
| `splitUnpriced` | Split unpriced | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:245` |
| `matches the longest prefix and separates truly unknown models` | Matches the longest prefix and separates truly unknown models | `web/src/Pricing.test.ts` | [[web/src/Pricing.test.ts]] `web/src/Pricing.test.ts:252` |
| `spanWindow` | Span window | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:64` |
| `uses the logged end time when present` | Uses the logged end time when present | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:65` |
| `derives the end from start plus duration when no end time is logged` | Derives the end from start plus duration when no end time is logged | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:71` |
| `leaves the end unknown when neither an end time nor a duration is logged` | Leaves the end unknown when neither an end time nor a duration is logged | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:76` |
| `leaves the start unknown for an unparsable timestamp` | Leaves the start unknown for an unparsable timestamp | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:81` |
| `resolveInsightTurn` | Resolve insight turn | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:87` |
| `uses the span own turn_id directly when set` | Uses the span own turn id directly when set | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:88` |
| `walks the parent_id chain to find an ancestor turn span` | Walks the parent id chain to find an ancestor turn span | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:97` |
| `numbers turns in seq order across multiple turns` | Numbers turns in seq order across multiple turns | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:107` |
| `returns null when the span has no resolvable turn` | Returns null when the span has no resolvable turn | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:117` |
| `returns null for an unknown span id` | Returns null for an unknown span id | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:126` |
| `stops at the depth cap instead of looping on a cyclical parent chain` | Stops at the depth cap instead of looping on a cyclical parent chain | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:130` |
| `summarizeInsightTurns` | Summarize insight turns | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:139` |
| `returns null when the session has no turns at all` | Returns null when the session has no turns at all | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:140` |
| `reports every turn carrying an insight when spread evenly` | Reports every turn carrying an insight when spread evenly | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:144` |
| `names the dominant turns once they pass half the weighted total` | Names the dominant turns once they pass half the weighted total | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:161` |
| `stays under the threshold when the top turns hold half or less` | Stays under the threshold when the top turns hold half or less | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:174` |
| `says nothing could be tied to a turn when every insight is unresolvable` | Says nothing could be tied to a turn when every insight is unresolvable | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:187` |
| `groupSpansByTurn` | Group spans by turn | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:195` |
| `groups spans under the turn span sharing their turn_id, excluding it from the breakdown` | Groups spans under the turn span sharing their turn id, excluding it from the breakdown | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:196` |
| `orders turns chronologically by the turn span started_at` | Orders turns chronologically by the turn span started at | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:212` |
| `falls back to the earliest child span start when the turn span itself is missing` | Falls back to the earliest child span start when the turn span itself is missing | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:222` |
| `uses the turn span's own duration directly and never sums children` | Uses the turn span's own duration directly and never sums children | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:232` |
| `marks duration unavailable when the turn span carries none, even though children do` | Marks duration unavailable when the turn span carries none, even though children do | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:264` |
| `sums input and output tokens across the turn's model_call spans` | Sums input and output tokens across the turn's model call spans | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:281` |
| `marks tokens unavailable when any contributing model_call span has none, rather than treating it as zero` | Marks tokens unavailable when any contributing model call span has none, rather than treating it as zero | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:306` |
| `collects spans with no turn_id into an "Outside any turn" group placed last` | Collects spans with no turn id into an "outside any turn" group placed last | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:324` |
| `counts a failed tool call once, not twice for the call and its paired result` | Counts a failed tool call once, not twice for the call and its paired result | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:337` |
| `still counts a failed tool call with no paired result` | Still counts a failed tool call with no paired result | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:354` |
| `collects the distinct models used by the turn's model_call spans` | Collects the distinct models used by the turn's model call spans | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:363` |
| `reads is_sidechain from the turn span` | Reads is sidechain from the turn span | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:374` |
| `returns nothing for an empty trace` | Returns nothing for an empty trace | `web/src/TraceTab.test.ts` | [[web/src/TraceTab.test.ts]] `web/src/TraceTab.test.ts:380` |
| `MetricInfo` | Metric info | `web/src/components/metric-info.test.tsx` | [[web/src/components/metric-info.test.tsx]] `web/src/components/metric-info.test.tsx:6` |
| `opens on click and shows the simple content` | Opens on click and shows the simple content | `web/src/components/metric-info.test.tsx` | [[web/src/components/metric-info.test.tsx]] `web/src/components/metric-info.test.tsx:7` |
| `closes on a second click and does not return focus to the trigger` | Closes on a second click and does not return focus to the trigger | `web/src/components/metric-info.test.tsx` | [[web/src/components/metric-info.test.tsx]] `web/src/components/metric-info.test.tsx:17` |
| `renders the rich metric content with meaning, formula and computed value` | Renders the rich metric content with meaning, formula and computed value | `web/src/components/metric-info.test.tsx` | [[web/src/components/metric-info.test.tsx]] `web/src/components/metric-info.test.tsx:43` |
| `worstState` | Worst state | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:4` |
| `picks unavailable over unpriced, free and priced` | Picks unavailable over unpriced, free and priced | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:5` |
| `picks unpriced over free and priced` | Picks unpriced over free and priced | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:9` |
| `returns unavailable for an empty list` | Returns unavailable for an empty list | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:13` |
| `is order-independent` | Is order-independent | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:17` |
| `worstProvenance` | Worst provenance | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:23` |
| `picks unavailable as the worst` | Picks unavailable as the worst | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:24` |
| `picks measured as the best when nothing worse is present` | Picks measured as the best when nothing worse is present | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:28` |
| `returns unavailable for an empty list` | Returns unavailable for an empty list | `web/src/components/rank.test.ts` | [[web/src/components/rank.test.ts]] `web/src/components/rank.test.ts:32` |
| `geometry` | Geometry | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:4` |
| `scales a series that peaks below 1 to the real max instead of flattening it` | Scales a series that peaks below 1 to the real max instead of flattening it | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:5` |
| `keeps every y coordinate inside the viewBox height for a series with negative dips` | Keeps every y coordinate inside the view box height for a series with negative dips | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:10` |
| `falls back to a flat line without dividing by zero when every value is identical` | Falls back to a flat line without dividing by zero when every value is identical | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:19` |
| `draws the highest value nearest the top of the box` | Draws the highest value nearest the top of the box | `web/src/components/sparkline.test.ts` | [[web/src/components/sparkline.test.ts]] `web/src/components/sparkline.test.ts:24` |
| `formatMoney` | Format money | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:20` |
| `formats whole dollars with two decimal places` | Formats whole dollars with two decimal places | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:21` |
| `formatMoneyExact` | Format money exact | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:26` |
| `keeps four decimal places for a sub-cent value instead of collapsing to $0.00` | Keeps four decimal places for a sub-cent value instead of collapsing to $0.00 | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:27` |
| `falls back to two decimal places once a cent is reached` | Falls back to two decimal places once a cent is reached | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:31` |
| `renders exactly zero as $0.00, not four decimal places` | Renders exactly zero as $0.00, not four decimal places | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:35` |
| `formatTokens` | Format tokens | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:40` |
| `abbreviates millions` | Abbreviates millions | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:41` |
| `renders small counts as-is` | Renders small counts as-is | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:45` |
| `rolls 999,999 tokens up to the next unit instead of "1000K"` | Rolls 999,999 tokens up to the next unit instead of "1000k" | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:49` |
| `rolls 999,999,999 tokens up to the next unit instead of "1000M"` | Rolls 999,999,999 tokens up to the next unit instead of "1000m" | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:53` |
| `does not promote a value that legitimately rounds within its unit` | Does not promote a value that legitimately rounds within its unit | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:57` |
| `handles negative values with the sign in front` | Handles negative values with the sign in front | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:61` |
| `formats zero as a plain count` | Formats zero as a plain count | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:65` |
| `formatMoneyShort` | Format money short | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:70` |
| `gains a millions branch instead of stopping at K` | Gains a millions branch instead of stopping at k | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:71` |
| `places a negative sign before the dollar sign, not after` | Places a negative sign before the dollar sign, not after | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:75` |
| `rounds a negative two-digit value to a whole number` | Rounds a negative two-digit value to a whole number | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:79` |
| `promotes a value that rounds up to a whole ten-thousands figure` | Promotes a value that rounds up to a whole ten-thousands figure | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:83` |
| `keeps a whole dollar amount unscaled` | Keeps a whole dollar amount unscaled | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:87` |
| `keeps a fractional amount under $10 in cents` | Keeps a fractional amount under $10 in cents | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:91` |
| `formatDuration` | Format duration | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:96` |
| `renders sub-second durations in ms` | Renders sub-second durations in ms | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:97` |
| `returns a placeholder for invalid input` | Returns a placeholder for invalid input | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:101` |
| `formatPercent` | Format percent | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:107` |
| `formats a ratio as a whole-number percentage by default` | Formats a ratio as a whole-number percentage by default | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:108` |
| `honors the requested digit count` | Honors the requested digit count | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:112` |
| `plural` | Plural | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:117` |
| `keeps the singular form for a count of one` | Keeps the singular form for a count of one | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:118` |
| `adds an s for every other count` | Adds an s for every other count | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:122` |
| `formats the count with thousands separators` | Formats the count with thousands separators | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:127` |
| `logSpanMs` | Log span ms | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:136` |
| `returns the gap between the first and last record` | Returns the gap between the first and last record | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:137` |
| `returns zero when the end is not after the start` | Returns zero when the end is not after the start | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:142` |
| `returns zero for an unparsable timestamp instead of NaN` | Returns zero for an unparsable timestamp instead of na n | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:147` |
| `today` | Today | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:153` |
| `returns an ISO date string in the local calendar` | Returns an iso date string in the local calendar | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:154` |
| `formatDay` | Format day | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:161` |
| `parses the ISO day as a plain date, never shifted by the viewer's time zone` | Parses the iso day as a plain date, never shifted by the viewer's time zone | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:162` |
| `can omit the year` | Can omit the year | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:166` |
| `shiftDays` | Shift days | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:171` |
| `moves forward across a month boundary using UTC arithmetic` | Moves forward across a month boundary using utc arithmetic | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:172` |
| `moves backward across a year boundary` | Moves backward across a year boundary | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:176` |
| `formatTimestamp and formatClock` | Format timestamp and format clock | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:181` |
| `both return a placeholder for an unparsable timestamp` | Both return a placeholder for an unparsable timestamp | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:182` |
| `formatTimestamp returns a placeholder for a null input` | Format timestamp returns a placeholder for a null input | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:187` |
| `daySpan` | Day span | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:192` |
| `lists every day inclusive of both ends` | Lists every day inclusive of both ends | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:193` |
| `returns a single day when from equals to` | Returns a single day when from equals to | `web/src/format.test.ts` | [[web/src/format.test.ts]] `web/src/format.test.ts:197` |
| `providerLabel` | Provider label | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:12` |
| `maps known providers` | Maps known providers | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:13` |
| `capitalises unknown providers` | Capitalises unknown providers | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:20` |
| `formatContextWindow` | Format context window | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:25` |
| `formats K and M` | Formats k and m | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:26` |
| `is null when unknown` | Is null when unknown | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:33` |
| `peakWindowText` | Peak window text | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:38` |
| `compresses weekday runs and lists hour ranges in UTC` | Compresses weekday runs and lists hour ranges in utc | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:39` |
| `handles split weekday sets` | Handles split weekday sets | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:52` |
| `stalenessBadge` | Staleness badge | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:59` |
| `has thresholds at 30 and 90 days` | Has thresholds at 30 and 90 days | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:60` |
| `matchUnpriced` | Match unpriced | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:69` |
| `prefers the longest prefix, case-insensitively` | Prefers the longest prefix, case-insensitively | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:75` |
| `returns null with no prefix match` | Returns null with no prefix match | `web/src/pricing-format.test.ts` | [[web/src/pricing-format.test.ts]] `web/src/pricing-format.test.ts:80` |
| `ratesAgeNotice` | Rates age notice | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:11` |
| `is silent when fresh or unknown` | Is silent when fresh or unknown | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:12` |
| `is info from 30 days` | Is info from 30 days | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:16` |
| `is caution from 90 days` | Is caution from 90 days | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:23` |
| `reportedDiverges` | Reported diverges | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:29` |
| `ignores differences within 5% or one cent` | Ignores differences within 5% or one cent | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:30` |
| `flags larger differences` | Flags larger differences | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:34` |
| `reportedNote` | Reported note | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:40` |
| `returns null when no reported cost` | Returns null when no reported cost | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:41` |
| `formats the line without a note when close` | Formats the line without a note when close | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:45` |
| `adds the note when divergent` | Adds the note when divergent | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:48` |
| `isEstimatedPriced` | Is estimated priced | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:54` |
| `requires priced state and estimated cost` | Requires priced state and estimated cost | `web/src/pricing-notes.test.ts` | [[web/src/pricing-notes.test.ts]] `web/src/pricing-notes.test.ts:56` |
| `truncateLabel` | Truncate label | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:56` |
| `leaves a short label untouched` | Leaves a short label untouched | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:57` |
| `cuts a long label to the limit and appends an ellipsis` | Cuts a long label to the limit and appends an ellipsis | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:61` |
| `never appends an ellipsis when the label exactly fits` | Never appends an ellipsis when the label exactly fits | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:67` |
| `turnLabel` | Turn label | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:72` |
| `formats an ordinal with a quoted, truncated snippet` | Formats an ordinal with a quoted, truncated snippet | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:73` |
| `falls back to just the ordinal when the label is null, never an empty quoted string` | Falls back to just the ordinal when the label is null, never an empty quoted string | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:79` |
| `shows the unattributed row label unchanged, not an ordinal` | Shows the unattributed row label unchanged, not an ordinal | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:83` |
| `realTurns` | Real turns | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:90` |
| `excludes the unattributed row` | Excludes the unattributed row | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:91` |
| `sortRealTurns` | Sort real turns | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:97` |
| `excludes the unattributed row from ordinal sorting entirely, not just ranks it last` | Excludes the unattributed row from ordinal sorting entirely, not just ranks it last | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:104` |
| `sorts by cost descending` | Sorts by cost descending | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:109` |
| `sorts by duration ascending` | Sorts by duration ascending | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:113` |
| `sorts by errors descending` | Sorts by errors descending | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:117` |
| `costConcentration` | Cost concentration | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:122` |
| `is null when no turn carries a priced cost` | Is null when no turn carries a priced cost | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:123` |
| `computes the top-N share against the sum of turn cost, not the unattributed row` | Computes the top-n share against the sum of turn cost, not the unattributed row | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:127` |
| `longestTurn` | Longest turn | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:143` |
| `picks the turn with the largest known duration, ignoring turns with no duration` | Picks the turn with the largest known duration, ignoring turns with no duration | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:144` |
| `is null when no turn has a known duration` | Is null when no turn has a known duration | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:153` |
| `errorOrRetryTurns` | Error or retry turns | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:158` |
| `counts turns with an error or a retry and finds the worst by errors first` | Counts turns with an error or a retry and finds the worst by errors first | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:159` |
| `is empty when nothing has an error or a retry` | Is empty when nothing has an error or a retry | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:171` |
| `toolHeaviestTurn` | Tool heaviest turn | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:176` |
| `picks the turn with the most tool calls` | Picks the turn with the most tool calls | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:177` |
| `is null when no turn made a tool call` | Is null when no turn made a tool call | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:182` |
| `halfCostTrend` | Half cost trend | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:187` |
| `is null with fewer than two turns` | Is null with fewer than two turns | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:188` |
| `splits by ordinal into two halves and sums each half separately` | Splits by ordinal into two halves and sums each half separately | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:192` |
| `leaves changeFraction null when the first half has no cost to compare against` | Leaves change fraction null when the first half has no cost to compare against | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:207` |
| `unattributedCostShare` | Unattributed cost share | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:213` |
| `is null when there is no unattributed row` | Is null when there is no unattributed row | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:214` |
| `is null when the unattributed row carries no cost` | Is null when the unattributed row carries no cost | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:218` |
| `shares against turn cost plus its own, matching costConcentration's denominator` | Shares against turn cost plus its own, matching cost concentration's denominator | `web/src/turn-insights.test.ts` | [[web/src/turn-insights.test.ts]] `web/src/turn-insights.test.ts:222` |
%% generated:chunk-tests end %%
