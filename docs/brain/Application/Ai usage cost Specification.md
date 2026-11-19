---
title: Ai usage cost Specification
aliases: []
tags: [generated, index, reference]
area: application
status: generated
audience: internal
maturity: approved
confidence: confirmed
covers: []
generated: true
---

# Ai usage cost Specification

The specification entities reverse-engineered from the Ai usage cost module.

%% generated:spec-links start (do not edit; run brain docs generate) %%
| Kind | Notes | Count |
|---|---|---|
| actor | [[AI coding tool logs]], [[Notification target]], [[Person using the tool]], [[User of Ai usage cost]] | 4 |
| data-store | [[Data of Ai usage cost]], [[Privacy configuration file]], [[Rate table file]], [[Usage store]] | 4 |
| event | [[Conflicting records warning]], [[Estimated price warning]], [[Reported cost divergence warning]], [[Session forgotten]], [[Session rated]], [[Spend alert sent]], [[Stale rates warning]], [[Tier unpriced warning]], [[Unpriced model warning]] | 9 |
| glossary-term | [[Amplification]], [[Bucket]], [[Cache read]], [[Cache write]], [[Cost state]], [[Estimated price]], [[Fingerprint]], [[Metadata only]], [[Outcome]], [[Parser version]], [[Peak window]], [[Price band]], [[Price period]], [[Provenance]], [[Rate table]], [[Redaction]], [[Request]], [[Service tier]], [[Session]], [[Sidechain]], [[Source]], [[Span]], [[Unpriced model]] | 23 |
| model | [[AlertDecision]], [[Analysis]], [[Bucket]], [[Capabilities]], [[ClientInfo]], [[Config]], [[ContextSnapshot]], [[CostBreakdown]], [[EconRow]], [[Economics]], [[Facets]], [[IngestSummary]], [[Insight]], [[Meta]], [[ModelMatch]], [[ModelRate]], [[Outcome]], [[OutcomeSignals]], [[OutcomeUpdate]], [[PartialRules]], [[Period]], [[Prefix]], [[PriceSet]], [[PricedEvent]], [[ProviderRules]], [[RateTable]], [[Report]], [[Sample]], [[SeriesPoint]], [[SessionRow]], [[Source]], [[SourceInfo]], [[Span]], [[SpanContent]], [[Spec]], [[TokenUsage]], [[Totals]], [[Trace]], [[UnknownModel]], [[UnpricedModel]], [[UsageEvent]], [[WarningGroup]], [[WarningInstance]], [[WarningSummary]], [[apps]], [[chats]], [[files]], [[messages]], [[outcomes]], [[requests]], [[samples]], [[session_exclusions]], [[trace_events]] | 53 |
| nfr | [[GPU sampler command timeouts]], [[Incremental ingest]], [[Rate lookup is cached]], [[Released text size limit]], [[Server binds to loopback by default]], [[Store uses write ahead logging]] | 6 |
| open-question | [[Should the series use the local day]], [[Who may use the HTTP interface]], [[Why 30 days for stale rates]], [[Will content capture be built]] | 4 |
| risk | [[A privacy typo silently resets the settings]], [[Content retention is accepted but does nothing]], [[Daily series uses the UTC date]], [[HTTP routes have no authentication]], [[Prices drift from the vendors]], [[Secret patterns are a fixed list]] | 6 |
| rule | [[A bad configuration file gives the defaults]], [[A forgotten session is not stored again]], [[A free provider costs zero]], [[A grown file resumes only when its earlier bytes are unchanged]], [[A known unpriced model beats a guess]], [[A model without a rate row is unpriced]], [[A prefix match is an estimate]], [[A reported cost that differs is flagged]], [[A request is stored once per fingerprint]], [[A row must name a defined provider]], [[A session shows its worst cost state]], [[A session title prefers the tool, then the latest]], [[An alert needs exactly one threshold]], [[An excluded project drops its spans]], [[An unchanged file is not parsed again]], [[An unknown session answers 404]], [[An unpriced tier is billed standard and flagged]], [[Cache prices fall back in a fixed order]], [[Content retention is inert]], [[Duplicate rate keys are rejected]], [[Missing token counts mean unavailable]], [[Old rates raise a warning]], [[Only listed suffixes count as the same model]], [[Peak windows must not wrap midnight]], [[Price periods must not overlap]], [[Records that disagree on input tokens keep the first]], [[Released text is cut and then redacted]], [[Source databases are opened read only]], [[Span text is refused in metadata only mode]], [[The first covering period replaces the row prices]], [[The largest band at or under the request size applies]], [[The local calendar day decides the day of an event]], [[The longest matching row wins]], [[_consistent refuses when duplicates]], [[_consistent refuses when missing]], [[_consistent validates the model]], [[_disjoint_periods refuses when earlier.until is None or (later.from_ or date.min) < ea]], [[_disjoint_periods validates the model]], [[_ordered refuses when self.from_ is not None and self.until is not None and (]], [[_ordered validates the model]], [[_roots refuses when not path]], [[_sorted_bands validates bands]], [[_valid_window refuses when any((not 0 <= day <= 6 for day in self.weekdays))]], [[_valid_window refuses when any((not 0 <= start < end <= 24 for start, end in self.]], [[_valid_window validates the model]], [[_values_match_provenance refuses when (value is None) != (provenance == 'unavailable')]], [[_values_match_provenance validates the model]], [[alert refuses when days < 1]], [[alert refuses when over is not None and rise_over is not None]], [[alert refuses when threshold is None]], [[create_app refuses when not store.session_exists(conn, source, session_id)]], [[create_app refuses when not store.session_exists(conn, source, session_id) (line 364)]], [[create_app refuses when path is None]], [[create_app refuses when span is None]], [[forget_session refuses when not store.session_exists(conn, source, session_id)]], [[opened refuses when path is None]], [[read_content refuses when config.metadata_only or span.content_path is None]], [[resolve_path refuses when index >= len(current)]], [[session_spans refuses when not store.session_exists(conn, source, session_id)]], [[span_content refuses when span is None]] | 60 |
| state-machine | [[CostState lifecycle]], [[MatchKind lifecycle]], [[Request cost state]], [[RowStatus lifecycle]], [[SpanKind lifecycle]], [[SpanStatus lifecycle]] | 6 |
| subdomain | [[Cost pricing]], [[Privacy and retention]], [[Spend reporting]], [[Usage collection]] | 4 |
| use-case | [[Be alerted when spend rises]], [[Browse sessions in the terminal]], [[Explore spend in the dashboard]], [[Export a report as a file]], [[Forget a session]], [[Inspect and rate one session]], [[Query the store with SQL]], [[Read the text of one span]], [[Sample GPU use for local models]], [[See what my AI usage would cost]], [[Try the tool with demo data]] | 11 |

These notes are drafts until the chunk ch-localtokenomics-src-ai-usage-cost is approved. They are written to the spec graph and cite the code they describe.
%% generated:spec-links end %%
