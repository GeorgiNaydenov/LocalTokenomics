from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

from ai_usage_cost import store
from ai_usage_cost.models import RawScalar, TokenUsage, UsageEvent
from ai_usage_cost.sources.base import Source
from ai_usage_cost.trace import OutcomeUpdate, Span, SpanKind

_UNSET = TokenUsage(uncached_input=100, output=50)


def _event(
    *,
    source: str = "fake",
    client: str = "fake-client",
    session_id: str = "s1",
    request_id: str | None = "req-1",
    model: str = "m1",
    minute: int = 0,
    tokens: TokenUsage | None = _UNSET,
    source_file: str = "",
) -> UsageEvent:
    return UsageEvent(
        source=source,
        client=client,
        provider="unknown",
        model=model,
        timestamp=datetime(2026, 8, 20, 10, minute, 0, tzinfo=UTC),
        session_id=session_id,
        request_id=request_id,
        tokens=tokens,
        machine="test-machine",
        source_file=source_file,
    )


def _span(
    *,
    span_id: str = "sp-1",
    source: str = "fake",
    session_id: str = "s1",
    kind: SpanKind = "turn",
    seq: int = 0,
    agent_id: str | None = None,
    started_at: datetime | None = None,
    source_file: str = "",
    detail: dict[str, RawScalar] | None = None,
    tokens: TokenUsage | None = None,
) -> Span:
    return Span(
        span_id=span_id,
        source=source,
        session_id=session_id,
        seq=seq,
        kind=kind,
        agent_id=agent_id,
        started_at=started_at or datetime(2026, 8, 20, 10, 0, 0, tzinfo=UTC),
        source_file=source_file,
        record_offset=0,
        record_length=12,
        detail=detail or {},
        tokens=tokens,
        tokens_provenance="measured" if tokens is not None else "unavailable",
    )


def _source(
    id_: str,
    events_by_file: dict[Path, list[UsageEvent]],
    spans_by_file: dict[Path, list[Span]] | None = None,
) -> Source:
    def default_roots() -> list[Path]:
        return []

    def files(root: Path) -> list[Path]:
        return [p for p in events_by_file if p.exists() and (p.parent == root or p == root)]

    def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
        yield from events_by_file.get(path, [])

    def spans(path: Path, warnings: list[str]) -> Iterator[Span]:
        yield from (spans_by_file or {}).get(path, [])

    return Source(
        id=id_,
        label=id_,
        clients={"fake-client": "Fake"},
        default_roots=default_roots,
        files=files,
        parse=parse,
        token_data="full",
        display_path="fake path",
        spans=spans if spans_by_file is not None else None,
    )


def test_fresh_store_reaches_the_latest_migration(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    assert conn.execute("PRAGMA user_version").fetchone()[0] == len(store.MIGRATIONS)
    assert {"requests", "files", "trace_events", "outcomes", "session_exclusions"} <= {
        row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    assert "parser_version" in {row[1] for row in conn.execute("PRAGMA table_info(files)")}


def test_reopening_an_up_to_date_store_is_a_no_op(tmp_path: Path) -> None:
    path = tmp_path / "usage.db"
    store.open_store(path).close()
    conn = store.open_store(path)
    assert conn.execute("PRAGMA user_version").fetchone()[0] == len(store.MIGRATIONS)


def test_ingest_twice_is_idempotent(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    log = root / "a.jsonl"
    log.write_text("{}")
    source = _source("fake", {log: [_event(source_file=str(log))]})

    first = store.ingest(conn, [source], {"fake": [root]})
    assert first.files_parsed == 1
    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1

    second = store.ingest(conn, [source], {"fake": [root]})
    assert second.files_parsed == 0
    assert second.files_skipped == 1
    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1


def test_a_grown_file_is_reparsed_and_replaces_its_rows(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    log = root / "a.jsonl"
    log.write_text("{}")
    events = [_event(request_id="req-1", source_file=str(log))]
    source = _source("fake", {log: events})
    store.ingest(conn, [source], {"fake": [root]})

    log.write_text("{}\n{}\n")
    events.append(_event(request_id="req-2", source_file=str(log)))
    store.ingest(conn, [source], {"fake": [root]})

    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 2


def test_a_deleted_file_keeps_its_rows(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    log = root / "a.jsonl"
    log.write_text("{}")
    source = _source("fake", {log: [_event(source_file=str(log))]})
    store.ingest(conn, [source], {"fake": [root]})

    log.unlink()
    store.ingest(conn, [source], {"fake": [root]})

    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1


def test_rebuild_empties_both_tables_before_reingesting(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    log = root / "a.jsonl"
    log.write_text("{}")
    source = _source("fake", {log: [_event(source_file=str(log))]})
    store.ingest(conn, [source], {"fake": [root]})

    summary = store.ingest(conn, [source], {"fake": [root]}, rebuild=True)
    assert summary.files_parsed == 1
    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1


def test_ingest_collects_per_file_warnings(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    log = root / "a.jsonl"
    log.write_text("{}")

    def parse(path: Path, warnings: list[str]) -> Iterator[UsageEvent]:
        warnings.append("something looked odd")
        yield _event(source_file=str(path))

    source = Source(
        id="fake",
        label="fake",
        clients={"fake-client": "Fake"},
        default_roots=list,
        files=lambda root: [log],
        parse=parse,
        token_data="full",
        display_path="fake path",
    )
    store.ingest(conn, [source], {"fake": [root]})
    _, _, warnings = store.load(conn)
    assert "something looked odd" in warnings


def test_fingerprint_uses_request_id_when_present() -> None:
    a = _event(request_id="shared")
    b = _event(request_id="shared", session_id="different-session")
    assert store.fingerprint_of(a) == store.fingerprint_of(b)


def test_fingerprint_falls_back_when_no_request_id() -> None:
    a = _event(request_id=None, minute=0)
    b = _event(request_id=None, minute=1)
    assert store.fingerprint_of(a) != store.fingerprint_of(b)


def test_a_message_split_over_three_records_keeps_the_largest_output(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)

    def event(output: int) -> UsageEvent:
        return _event(
            request_id="split-1",
            tokens=TokenUsage(
                uncached_input=50, cache_read=1_000, output=output, reasoning_output=0
            ),
            source_file=str(log),
        )

    # Streaming order: 10, then 50, then the final, complete 120 -- the last (and largest)
    # record should win, not the first.
    source = _source("fake", {log: [event(10), event(50), event(120)]})
    store.ingest(conn, [source], {"fake": [root]})

    row = conn.execute("SELECT output, uncached_input, cache_read FROM requests").fetchone()
    assert row == (120, 50, 1_000)
    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1


def test_a_smaller_duplicate_record_never_downgrades_the_kept_output(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)

    def event(output: int) -> UsageEvent:
        return _event(
            request_id="split-2",
            tokens=TokenUsage(uncached_input=50, output=output),
            source_file=str(log),
        )

    # Out-of-order arrival: the largest record shows up first, and the store must not let a
    # smaller "duplicate" (e.g. a stray partial) overwrite it afterwards.
    source = _source("fake", {log: [event(120), event(50), event(10)]})
    store.ingest(conn, [source], {"fake": [root]})

    assert conn.execute("SELECT output FROM requests").fetchone()[0] == 120


def test_duplicates_across_two_files_yield_the_max_regardless_of_file_order(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    a, b = root / "a.jsonl", root / "b.jsonl"
    a.write_text("{}")
    b.write_text("{}")
    source = _source(
        "fake",
        {
            a: [
                _event(
                    request_id="cross-1",
                    tokens=TokenUsage(uncached_input=10, output=50),
                    source_file=str(a),
                )
            ],
            b: [
                _event(
                    request_id="cross-1",
                    tokens=TokenUsage(uncached_input=10, output=120),
                    source_file=str(b),
                )
            ],
        },
    )
    store.ingest(conn, [source], {"fake": [root]})
    assert conn.execute("SELECT output FROM requests").fetchone()[0] == 120


def test_a_span_from_a_later_file_with_larger_output_upgrades_the_kept_span(
    tmp_path: Path,
) -> None:
    # The same message.id can appear as a model_call span in two different files (the 155
    # real cross-file-split cases the ground-truth audit found) -- the trace_events table
    # must apply the same last-record-wins rule the requests table already applies, not
    # leave the trace stuck on whichever file's span happened to be ingested first.
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    a, b = root / "a.jsonl", root / "b.jsonl"
    a.write_text("{}")
    b.write_text("{}")
    source = _source(
        "fake",
        {a: [], b: []},
        spans_by_file={
            a: [
                _span(
                    span_id="shared-call",
                    kind="model_call",
                    source_file=str(a),
                    tokens=TokenUsage(uncached_input=10, output=10),
                )
            ],
            b: [
                _span(
                    span_id="shared-call",
                    kind="model_call",
                    source_file=str(b),
                    tokens=TokenUsage(uncached_input=10, output=120),
                )
            ],
        },
    )
    store.ingest(conn, [source], {"fake": [root]})

    spans = store.load_spans(conn, "fake", "s1")
    assert len(spans) == 1
    assert spans[0].tokens is not None
    assert spans[0].tokens.output == 120


def test_duplicates_across_two_files_the_smaller_file_ingested_last_does_not_win(
    tmp_path: Path,
) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    a, b = root / "a.jsonl", root / "b.jsonl"
    a.write_text("{}")
    b.write_text("{}")
    source = _source(
        "fake",
        {
            a: [
                _event(
                    request_id="cross-2",
                    tokens=TokenUsage(uncached_input=10, output=120),
                    source_file=str(a),
                )
            ],
            b: [
                _event(
                    request_id="cross-2",
                    tokens=TokenUsage(uncached_input=10, output=50),
                    source_file=str(b),
                )
            ],
        },
    )
    store.ingest(conn, [source], {"fake": [root]})
    assert conn.execute("SELECT output FROM requests").fetchone()[0] == 120


def test_disagreeing_input_fields_keep_the_first_record_and_warn(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)
    first = _event(
        request_id="collide", tokens=TokenUsage(uncached_input=100, output=10), source_file=str(log)
    )
    second = _event(
        request_id="collide",
        tokens=TokenUsage(uncached_input=999, output=999),
        source_file=str(log),
    )
    source = _source("fake", {log: [first, second]})

    store.ingest(conn, [source], {"fake": [root]})

    row = conn.execute("SELECT uncached_input, output FROM requests").fetchone()
    assert row == (100, 10)
    warnings = json.loads(conn.execute("SELECT warnings FROM files").fetchone()[0])
    assert any("disagree" in w for w in warnings)


def test_fingerprint_is_namespaced_by_source() -> None:
    a = _event(source="fake-a", request_id="shared")
    b = _event(source="fake-b", request_id="shared")
    assert store.fingerprint_of(a) != store.fingerprint_of(b)


def test_fallback_fingerprint_uses_source_file_and_record_offset_to_disambiguate() -> None:
    a = _event(request_id=None, session_id="s1", minute=0, model="m1", source_file="a.jsonl")
    b = _event(request_id=None, session_id="s1", minute=0, model="m1", source_file="b.jsonl")
    assert store.fingerprint_of(a) != store.fingerprint_of(b)

    c = UsageEvent(
        source="fake",
        client="fake-client",
        provider="unknown",
        model="m1",
        timestamp=datetime(2026, 8, 20, 10, 0, 0, tzinfo=UTC),
        session_id="s1",
        request_id=None,
        tokens=_UNSET,
        machine="test-machine",
        source_file="a.jsonl",
        record_offset=10,
    )
    d = c.model_copy(update={"record_offset": 20})
    assert store.fingerprint_of(c) != store.fingerprint_of(d)


def test_two_files_with_the_same_request_id_dedup_at_ingest(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    a, b = root / "a.jsonl", root / "b.jsonl"
    a.write_text("{}")
    b.write_text("{}")
    source = _source(
        "fake",
        {
            a: [_event(request_id="shared-id", source_file=str(a))],
            b: [_event(request_id="shared-id", source_file=str(b))],
        },
    )
    store.ingest(conn, [source], {"fake": [root]})
    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1


def test_fallback_fingerprint_separates_two_turns_without_ids() -> None:
    a = _event(request_id=None, session_id="s1", minute=0, model="m1")
    b = _event(request_id=None, session_id="s1", minute=0, model="m1")
    assert store.fingerprint_of(a) == store.fingerprint_of(b)
    c = _event(request_id=None, session_id="s1", minute=1, model="m1")
    assert store.fingerprint_of(a) != store.fingerprint_of(c)


def test_load_round_trips_tokens_none(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    log = root / "a.jsonl"
    log.write_text("{}")
    source = _source("fake", {log: [_event(tokens=None, source_file=str(log))]})
    store.ingest(conn, [source], {"fake": [root]})

    events, files, _warnings = store.load(conn)
    assert files == 1
    assert len(events) == 1
    assert events[0].tokens is None


def test_load_orders_events_by_timestamp(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    log = root / "a.jsonl"
    log.write_text("{}")
    source = _source(
        "fake",
        {
            log: [
                _event(request_id="r2", minute=5, source_file=str(log)),
                _event(request_id="r1", minute=1, source_file=str(log)),
            ]
        },
    )
    store.ingest(conn, [source], {"fake": [root]})
    events, _, _ = store.load(conn)
    assert [e.request_id for e in events] == ["r1", "r2"]


def _traced_source(log: Path, spans: list[Span]) -> Source:
    return _source("fake", {log: [_event(source_file=str(log))]}, {log: spans})


def _logs(tmp_path: Path, name: str = "a.jsonl") -> tuple[Path, Path]:
    root = tmp_path / "logs"
    root.mkdir(exist_ok=True)
    log = root / name
    log.write_text("{}")
    return root, log


def test_a_file_left_by_an_older_parser_is_reparsed_and_gains_spans(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)
    source = _traced_source(log, [_span(source_file=str(log))])
    store.ingest(conn, [source], {"fake": [root]})

    conn.execute("DELETE FROM trace_events")
    conn.execute("UPDATE files SET parser_version = 0")
    conn.commit()

    summary = store.ingest(conn, [source], {"fake": [root]})
    assert summary.files_parsed == 1
    assert conn.execute("SELECT COUNT(*) FROM trace_events").fetchone()[0] == 1
    assert conn.execute("SELECT parser_version FROM files").fetchone()[0] == store.PARSER_VERSION


def test_reparsing_a_file_replaces_only_its_own_spans(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, a = _logs(tmp_path, "a.jsonl")
    _, b = _logs(tmp_path, "b.jsonl")
    a_spans = [_span(span_id="sp-a1", source_file=str(a))]
    source = _source(
        "fake",
        {
            a: [_event(request_id="ra", source_file=str(a))],
            b: [_event(request_id="rb", source_file=str(b))],
        },
        {a: a_spans, b: [_span(span_id="sp-b1", source_file=str(b))]},
    )
    store.ingest(conn, [source], {"fake": [root]})

    a.write_text("{}\n{}\n")
    a_spans[:] = [_span(span_id="sp-a2", source_file=str(a))]
    store.ingest(conn, [source], {"fake": [root]})

    assert {row[0] for row in conn.execute("SELECT span_id FROM trace_events")} == {
        "sp-a2",
        "sp-b1",
    }


def test_rebuild_empties_spans_but_keeps_outcomes(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)
    spans = [_span(source_file=str(log))]
    source = _traced_source(log, spans)
    store.ingest(conn, [source], {"fake": [root]})
    store.put_outcome(conn, "fake", "s1", OutcomeUpdate(outcome="successful", notes="fine"))

    spans.clear()
    store.ingest(conn, [source], {"fake": [root]}, rebuild=True)

    assert conn.execute("SELECT COUNT(*) FROM trace_events").fetchone()[0] == 0
    stored = store.get_outcome(conn, "fake", "s1")
    assert stored is not None
    assert stored.outcome == "successful"


def test_delete_session_drops_spans_and_the_exclusion_survives_reingest(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)
    source = _traced_source(log, [_span(source_file=str(log))])
    store.ingest(conn, [source], {"fake": [root]})

    assert store.delete_session(conn, "fake", "s1") == 1
    assert store.session_exists(conn, "fake", "s1") is False

    log.write_text("{}\n{}\n")
    store.ingest(conn, [source], {"fake": [root]})

    assert conn.execute("SELECT COUNT(*) FROM trace_events").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1


def test_an_excluded_project_drops_spans_but_keeps_requests(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)
    source = _traced_source(
        log,
        [
            _span(span_id="sp-1", source_file=str(log), detail={"project": "secret"}),
            _span(
                span_id="sp-2",
                source_file=str(log),
                detail={"working_directory": "/home/user/secret/deep"},
            ),
            _span(span_id="sp-3", source_file=str(log), detail={"project": "public"}),
        ],
    )
    store.ingest(
        conn,
        [source],
        {"fake": [root]},
        exclude_projects=["secret", "/home/user/secret"],
    )

    assert [row[0] for row in conn.execute("SELECT span_id FROM trace_events")] == ["sp-3"]
    assert conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 1


def test_retention_deletes_spans_older_than_the_window(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)
    now = datetime.now(tz=UTC)
    source = _traced_source(
        log,
        [
            _span(span_id="old", source_file=str(log), started_at=now - timedelta(days=40)),
            _span(span_id="new", source_file=str(log), started_at=now - timedelta(hours=1)),
        ],
    )
    store.ingest(conn, [source], {"fake": [root]}, metadata_retention_days=7)

    assert [row[0] for row in conn.execute("SELECT span_id FROM trace_events")] == ["new"]


def test_load_spans_reparents_agent_roots_to_their_subagent_span(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)
    source = _traced_source(
        log,
        [
            _span(span_id="call", kind="subagent", seq=0, agent_id="ag1", source_file=str(log)),
            _span(span_id="agent-turn", kind="turn", seq=1, agent_id="ag1", source_file=str(log)),
        ],
    )
    store.ingest(conn, [source], {"fake": [root]})

    spans = store.load_spans(conn, "fake", "s1")
    by_id = {span.span_id: span for span in spans}
    assert by_id["agent-turn"].parent_id == "call"
    assert by_id["call"].parent_id is None


def test_a_pre_title_store_gets_the_new_columns_and_backfills_folder(tmp_path: Path) -> None:
    # Simulate a store built before the title/title_source migration existed: apply every
    # migration except the last one, insert a row the old way (no title columns at all),
    # then reopen -- the ALTER TABLE migration must run and existing rows must backfill
    # title_source='folder' (title itself has no DEFAULT, so it stays NULL).
    path = tmp_path / "usage.db"
    conn = sqlite3.connect(path)
    for migration in store.MIGRATIONS[:-1]:
        conn.executescript(migration)
    conn.execute(f"PRAGMA user_version = {len(store.MIGRATIONS) - 1}")
    conn.execute(
        "INSERT INTO requests (fingerprint, source, client, provider, model, session_id, "
        "timestamp, request_id, uncached_input, cache_read, cache_write_5m, cache_write_1h, "
        "output, reasoning_output, is_sidechain, tier, project, working_directory, "
        "repository, branch, machine, source_file, raw) VALUES "
        "('fp1', 'fake', 'fake-client', 'unknown', 'm1', 's1', '2026-08-20T10:00:00+00:00', "
        "'req-1', 100, 0, 0, 0, 50, 0, 0, 'standard', NULL, NULL, NULL, NULL, "
        "'test-machine', '', '{}')"
    )
    conn.commit()
    conn.close()

    conn = store.open_store(path)
    assert conn.execute("PRAGMA user_version").fetchone()[0] == len(store.MIGRATIONS)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(requests)")}
    assert {"title", "title_source"} <= columns
    row = conn.execute(
        "SELECT title, title_source FROM requests WHERE fingerprint = 'fp1'"
    ).fetchone()
    assert row == (None, "folder")


def test_title_and_title_source_round_trip_through_load(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root = tmp_path / "logs"
    root.mkdir()
    log = root / "a.jsonl"
    log.write_text("{}")
    event = _event(source_file=str(log)).model_copy(
        update={"title": "Fix login bug", "title_source": "tool"}
    )
    source = _source("fake", {log: [event]})
    store.ingest(conn, [source], {"fake": [root]})

    events, _, _ = store.load(conn)
    assert events[0].title == "Fix login bug"
    assert events[0].title_source == "tool"


def test_session_flags_reports_spans_errors_and_outcome(tmp_path: Path) -> None:
    conn = store.open_store(tmp_path / "usage.db")
    root, log = _logs(tmp_path)
    source = _traced_source(
        log,
        [
            _span(span_id="sp-1", source_file=str(log)),
            _span(span_id="sp-2", kind="error", seq=1, source_file=str(log)),
        ],
    )
    store.ingest(conn, [source], {"fake": [root]})
    store.put_outcome(conn, "fake", "s1", OutcomeUpdate(outcome="partial"))

    assert store.session_flags(conn)[("fake", "s1")] == (True, 1, "partial")
