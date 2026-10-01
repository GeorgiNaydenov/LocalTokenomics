from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_usage_cost.models import UsageEvent
from ai_usage_cost.sources import muse_code, registry
from ai_usage_cost.sources.muse_code import SOURCE, default_roots, parse, session_files
from ai_usage_cost.store import fingerprint_of
from conftest import FIXTURES, analyze_roots

BASIC = FIXTURES / "muse_code" / "basic"
PARENT = "7c1d0000-0000-4000-8000-000000000001"
CHILD = "7c1d0000-0000-4000-8000-0000000000c1"


@dataclass
class Scanned:
    events: list[UsageEvent] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def scan(root: Path) -> Scanned:
    result = Scanned()
    for path in session_files(root):
        result.events.extend(parse(path, result.warnings))
    return result


def meta(stream: str = PARENT, provider: str = "meta") -> dict:
    return {
        "payload_type": "runtime.session.metadata",
        "recorded_at": 1790000000000000,
        "seq": 1,
        "stream": {"id": stream},
        "payload": {"record": {"workspace_root": "/work/demo", "provider_id": provider}},
    }


def completed(
    seq: int | None = 9,
    stream: str | None = PARENT,
    usage: dict | None = None,
    recorded_at: object = 1790000004000000,
    model: str | None = "muse-spark-1.3",
    kind: str = "model_completed",
    payload_type: str = "runtime.session",
) -> dict:
    record: dict = {
        "payload_type": payload_type,
        "recorded_at": recorded_at,
        "payload": {
            "event": {
                "kind": kind,
                "model": model,
                "duration_ms": 10,
                "usage": usage if usage is not None else {"input_tokens": 100, "output_tokens": 10},
            }
        },
    }
    if seq is not None:
        record["seq"] = seq
    if stream is not None:
        record["stream"] = {"id": stream}
    return record


def write(tmp_path: Path, lines: list, session: str = PARENT, sub: str | None = None) -> Path:
    directory = tmp_path / "2026" / "10" / "01" / session
    if sub:
        directory = directory / "subagent" / sub
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "session.jsonl"
    text = "\n".join(line if isinstance(line, str) else json.dumps(line) for line in lines)
    path.write_text(text + "\n", encoding="utf-8")
    return path


@pytest.fixture
def basic() -> Scanned:
    return scan(BASIC)


def by_session(events: list[UsageEvent]) -> dict[tuple[str, int], UsageEvent]:
    return {(e.session_id, e.tokens.output if e.tokens else 0): e for e in events}


def test_basic_fixture_counts_each_step_once(basic: Scanned) -> None:
    # parent: 2 steps; child file: 1; echo session, .msp-view-v1 and mirrored/replayed
    # records add nothing.
    assert len(basic.events) == 3
    assert basic.warnings == []
    assert {e.source for e in basic.events} == {"muse-code"}


def test_token_mapping_and_metadata(basic: Scanned) -> None:
    first = by_session(basic.events)[(PARENT, 410)]
    assert first.tokens is not None
    assert first.tokens.uncached_input == 18200 - 15000
    assert first.tokens.cache_read == 15000
    assert first.tokens.cache_write == 0
    assert first.tokens.output == 410
    assert first.tokens.reasoning_output == 90
    assert first.model == "muse-spark-1.3"
    assert first.provider == "meta"
    assert first.project == "demo"
    assert first.working_directory == "/work/demo"
    assert first.reported_cost is None
    assert first.is_sidechain is False
    assert first.title == "demo_" + PARENT
    assert first.title_source == "folder"
    assert first.raw == {"duration_ms": 3900, "cli_version": "1.4.2"}


def test_cache_write_is_inside_input_by_default(basic: Scanned) -> None:
    tokens = by_session(basic.events)[(PARENT, 50)].tokens
    assert tokens is not None
    assert tokens.cache_write_5m == 200
    assert tokens.uncached_input == 1000 - 200
    assert tokens.input_total == 1000


def test_cache_write_policy_constant_both_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    usage = {"input_tokens": 1000, "output_tokens": 5, "cache_read_tokens": 300}
    usage["cache_write_tokens"] = 200
    path = write(tmp_path, [meta(), completed(usage=usage)])
    monkeypatch.setattr(muse_code, "_CACHE_WRITE_INSIDE_INPUT", True)
    inside = next(parse(path, [])).tokens
    monkeypatch.setattr(muse_code, "_CACHE_WRITE_INSIDE_INPUT", False)
    outside = next(parse(path, [])).tokens
    assert inside is not None and outside is not None
    assert inside.uncached_input == 500 and inside.input_total == 1000
    assert outside.uncached_input == 700 and outside.input_total == 1200


def test_uncached_input_never_negative(tmp_path: Path) -> None:
    usage = {
        "input_tokens": 10,
        "output_tokens": 1,
        "cache_read_tokens": 50,
        "cache_write_tokens": 9,
    }
    path = write(tmp_path, [meta(), completed(usage=usage)])
    tokens = next(parse(path, [])).tokens
    assert tokens is not None
    assert tokens.uncached_input == 0
    assert tokens.cache_read == 50


def test_cached_tokens_alias_used_when_cache_read_absent(tmp_path: Path) -> None:
    usage = {"input_tokens": 100, "output_tokens": 1, "cached_tokens": 40}
    warnings: list[str] = []
    (event,) = parse(write(tmp_path, [meta(), completed(usage=usage)]), warnings)
    tokens = event.tokens
    assert tokens is not None and tokens.cache_read == 40 and tokens.uncached_input == 60
    assert warnings == []


def test_conflicting_cache_aliases_prefer_cache_read_and_warn(tmp_path: Path) -> None:
    usage = {"input_tokens": 100, "output_tokens": 1, "cache_read_tokens": 30, "cached_tokens": 45}
    warnings: list[str] = []
    (event,) = parse(write(tmp_path, [meta(), completed(usage=usage)]), warnings)
    tokens = event.tokens
    assert tokens is not None and tokens.cache_read == 30
    assert len(warnings) == 1 and "cached_tokens" in warnings[0]


# --- the three double-count traps -------------------------------------------------------


def test_trap_goal_usage_attribution_is_not_usage(tmp_path: Path) -> None:
    attribution = completed(seq=10, payload_type="goal_usage_attribution", kind="x")
    sneaky = completed(seq=11, kind="goal_usage_attribution")
    path = write(tmp_path, [meta(), completed(seq=9), attribution, sneaky])
    assert len(list(parse(path, []))) == 1


def test_trap_mirrored_child_stream_in_parent_is_skipped(tmp_path: Path) -> None:
    path = write(tmp_path, [meta(), completed(seq=9), completed(seq=3, stream=CHILD)])
    events = list(parse(path, []))
    assert [e.request_id for e in events] == [f"muse-code:{PARENT}:9"]
    # the child's own file counts its records
    child = write(tmp_path, [meta(CHILD), completed(seq=3, stream=CHILD)], PARENT, CHILD)
    child_events = list(parse(child, []))
    assert len(child_events) == 1
    assert child_events[0].session_id == CHILD
    assert child_events[0].is_sidechain is True


def test_trap_replayed_prefix_dedups_on_stream_seq_and_usage_id(tmp_path: Path) -> None:
    with_id = completed(seq=20, usage={"input_tokens": 5, "output_tokens": 5, "usage_id": "u-7"})
    again = completed(seq=21, usage={"input_tokens": 5, "output_tokens": 5, "usage_id": "u-7"})
    path = write(tmp_path, [meta(), completed(seq=9), completed(seq=9), with_id, again])
    events = list(parse(path, []))
    assert len(events) == 2
    assert {e.request_id for e in events} == {f"muse-code:{PARENT}:9", "muse-code:u-7"}


def test_replay_in_a_second_file_gets_the_same_request_id(tmp_path: Path) -> None:
    first = write(tmp_path, [meta(), completed(seq=9)])
    other = "7c1d0000-0000-4000-8000-0000000000f0"
    fork = write(tmp_path, [meta(PARENT), completed(seq=9)], other)
    a, b = next(parse(first, [])), next(parse(fork, []))
    assert fingerprint_of(a) == fingerprint_of(b)


# --- envelope tolerance, timestamps ----------------------------------------------------


def test_recorded_at_is_microseconds(basic: Scanned) -> None:
    first = by_session(basic.events)[(PARENT, 410)]
    assert first.timestamp == datetime.fromtimestamp(1790000004, tz=UTC)


@pytest.mark.parametrize(
    "value", [1790000004, 1790000004000, 1790000004000000, "2026-09-21T14:13:24+00:00"]
)
def test_timestamp_units_all_resolve_to_same_instant(tmp_path: Path, value: object) -> None:
    path = write(tmp_path, [meta(), completed(recorded_at=value)])
    ts = next(parse(path, [])).timestamp
    assert ts == datetime.fromtimestamp(1790000004, tz=UTC)


def test_retained_frame_wrapper_is_unwrapped(tmp_path: Path) -> None:
    inner = json.dumps(completed(seq=9))
    nested = {
        "record": "retained_frame",
        "recorded_at": 1790000000000000,
        "children": [{"record_json": json.dumps(meta())}, {"record_json": inner}],
    }
    outer = {"record": "retained_frame", "children": [{"record_json": json.dumps(nested)}]}
    warnings: list[str] = []
    events = list(parse(write(tmp_path, [outer]), warnings))
    assert len(events) == 1
    assert events[0].provider == "meta"
    assert events[0].project == "demo"
    assert warnings == []


def test_unknown_shapes_are_skipped_with_one_aggregate_warning(tmp_path: Path) -> None:
    lines = [
        meta(),
        completed(seq=9),
        {"hello": "world"},
        {"payload_type": "x", "payload": "not-a-dict"},
        {"record": "retained_frame", "children": [{"record_json": "{broken"}, 5]},
        "[1, 2, 3]",
    ]
    warnings: list[str] = []
    events = list(parse(write(tmp_path, lines), warnings))
    assert len(events) == 1
    assert warnings == ["session.jsonl: 4 records in unrecognised format"]


def test_malformed_lines_and_missing_keys_do_not_crash(tmp_path: Path) -> None:
    lines: list = [
        "{truncated",
        meta(),
        completed(seq=9, usage={"input_tokens": "many", "output_tokens": None}),
        completed(seq=10, usage=None) | {"payload": {"event": {"kind": "model_completed"}}},
        completed(seq=11, model=None),
    ]
    warnings: list[str] = []
    events = list(parse(write(tmp_path, lines), warnings))
    assert [e.model for e in events] == [None]  # only the well-formed, model-less step
    assert any("unparsable" in w for w in warnings)


def test_missing_model_with_tokens_is_kept_unpriced(tmp_path: Path) -> None:
    path = write(tmp_path, [meta(), completed(model=None)])
    (event,) = parse(path, [])
    assert event.model is None


def test_echo_provider_produces_no_events(tmp_path: Path) -> None:
    path = write(tmp_path, [meta(provider="echo"), completed()])
    assert list(parse(path, [])) == []


def test_session_without_stream_ids_or_seq_still_counts(tmp_path: Path) -> None:
    path = write(tmp_path, [completed(seq=None, stream=None), completed(seq=None, stream=None)])
    events = list(parse(path, []))
    assert [e.request_id for e in events] == [f"muse-code:{PARENT}:n1", f"muse-code:{PARENT}:n2"]


def test_file_discovery_skips_view_and_catalog_dirs(tmp_path: Path) -> None:
    write(tmp_path, [meta()])
    for skipped in (".msp-view-v1", "model-catalog"):
        (tmp_path / skipped).mkdir()
        (tmp_path / skipped / "session.jsonl").write_text("{}\n", encoding="utf-8")
    (tmp_path / "2026" / "10" / "01" / PARENT / ".session.lock").write_text("1", encoding="utf-8")
    assert [p.parent.name for p in session_files(tmp_path)] == [PARENT]


# --- roots, registry, store, pipeline ---------------------------------------------------


def test_missing_root_yields_nothing(tmp_path: Path) -> None:
    assert session_files(tmp_path / "nope") == []
    assert scan(tmp_path / "nope").events == []


def test_muse_data_dir_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("MUSE_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg"))
    assert default_roots() == [tmp_path]


def test_xdg_and_home_default_roots(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("MUSE_DATA_DIR", raising=False)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    assert default_roots() == [tmp_path / "muse" / "sessions"]
    monkeypatch.delenv("XDG_DATA_HOME")
    assert default_roots() == [Path.home() / ".local" / "share" / "muse" / "sessions"]


def test_source_is_experimental_and_discovered() -> None:
    assert SOURCE.experimental is True
    assert registry()["muse-code"] is SOURCE
    assert SOURCE.token_data == "full"


def test_reparse_is_idempotent_by_fingerprint(basic: Scanned) -> None:
    again = scan(BASIC)
    first = [fingerprint_of(e) for e in basic.events]
    assert first == [fingerprint_of(e) for e in again.events]
    assert len(set(first)) == len(first)


def test_pipeline_prices_events_and_survives_unknown_model(tmp_path: Path) -> None:
    rates = {
        "as_of": "2026-10-01",
        "providers": {"meta": {"cache_read": 0.12, "cache_write_5m": 1.0, "cache_write_1h": 1.0}},
        "models": [
            {
                "match": "muse-spark-1.3",
                "provider": "meta",
                "display": "Muse Spark 1.3",
                "input": 1.25,
                "output": 4.25,
            }
        ],
    }
    rates_path = tmp_path / "rates.json"
    rates_path.write_text(json.dumps(rates), encoding="utf-8")
    from ai_usage_cost.pipeline import analyze

    db = tmp_path / "t.db"
    roots = {source_id: [tmp_path / "none"] for source_id in registry()}
    roots["muse-code"] = [BASIC]
    analysis = analyze(db_path=db, roots=roots, rates_path=rates_path)
    muse = [p for p in analysis.events if p.event.source == "muse-code"]
    assert len(muse) == 3
    states = {p.event.model: p.state for p in muse}
    assert states["muse-spark-1.3"] == "priced"
    assert states["muse-spark-1.2"] != "priced"  # no row: unpriced, not a crash
    priced = next(p for p in muse if p.event.model == "muse-spark-1.3")
    assert priced.cost is not None and priced.cost.output == pytest.approx(410 * 4.25 / 1e6)
    assert any("muse-spark-1.2" in w for w in analysis.warnings)
    assert analyze_roots(tmp_path, **{"muse-code": BASIC}).events  # default-rates path runs


def test_negative_token_fields_clamp_to_zero(tmp_path: Path) -> None:
    usage = {
        "input_tokens": -5,
        "output_tokens": -2,
        "cache_read_tokens": -7,
        "cache_write_tokens": -1,
        "reasoning_tokens": -3,
    }
    usage_ok = {"input_tokens": 10, "output_tokens": 4, "reasoning_tokens": 9}
    lines = [meta(), completed(seq=1, usage=usage), completed(seq=2, usage=usage_ok)]
    events = list(parse(write(tmp_path, lines), []))
    assert len(events) == 1  # the all-negative step is zero tokens, so skipped
    tokens = events[0].tokens
    assert tokens is not None
    assert tokens.output == 4
    assert tokens.reasoning_output == 4  # clamped to output
    assert min(tokens.uncached_input, tokens.cache_read, tokens.cache_write) >= 0


def test_own_stream_fallback_survives_mirrored_child_first(tmp_path: Path) -> None:
    session = "not-a-stream-id"
    parent_stream = "7c1d0000-0000-4000-8000-0000000000aa"
    lines = [
        completed(seq=1, stream=CHILD),
        meta(parent_stream),
        completed(seq=2, stream=parent_stream),
        completed(seq=3, stream=parent_stream),
    ]
    events = list(parse(write(tmp_path, lines, session), []))
    assert [e.request_id for e in events] == [
        f"muse-code:{parent_stream}:2",
        f"muse-code:{parent_stream}:3",
    ]
    assert events[0].provider == "meta"
