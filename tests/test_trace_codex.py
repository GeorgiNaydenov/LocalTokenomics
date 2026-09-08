from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from ai_usage_cost.privacy import Config, read_content
from ai_usage_cost.sources.base import jsonl_files
from ai_usage_cost.sources.codex import SOURCE, spans
from ai_usage_cost.trace import Span
from conftest import CODEX_TRACE, CODEX_TRACE_LEGACY


def _local(span_id: str | None) -> str:
    if span_id is None:
        return ""
    head, sep, tail = span_id.partition(":")
    return tail if sep and head.startswith("rollout-") else span_id


@dataclass
class Scanned:
    spans: list[Span] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def by_id(self, span_id: str) -> Span:
        return next(span for span in self.spans if _local(span.span_id) == span_id)

    def of_kind(self, kind: str) -> list[Span]:
        return [span for span in self.spans if span.kind == kind]


def scan(root: Path) -> Scanned:
    result = Scanned()
    for path in jsonl_files(root):
        result.spans.extend(spans(path, result.warnings))
    return result


@pytest.fixture
def traced() -> Scanned:
    return scan(CODEX_TRACE)


@pytest.fixture
def legacy() -> Scanned:
    return scan(CODEX_TRACE_LEGACY)


def test_the_source_declares_its_span_capabilities() -> None:
    assert SOURCE.spans is spans
    assert SOURCE.capabilities.model_dump() == {
        "trace": "measured",
        "tokens": "measured",
        "cost": "derived",
        "context": "measured",
        "latency": "measured",
    }


def test_task_complete_closes_the_turn_with_a_measured_duration_and_ttft(
    traced: Scanned,
) -> None:
    turn = traced.by_id("turn-1")
    assert turn.kind == "turn"
    assert turn.status == "ok"
    assert (turn.duration_ms, turn.duration_provenance) == (17_000, "measured")
    assert turn.ttft_ms == 900
    assert turn.detail["project"] == "gamma"
    assert turn.detail["working_directory"] == "/home/user/gamma"
    assert turn.detail["effort"] == "medium"


def test_ttft_is_recorded_on_the_turn_and_never_on_a_model_call(traced: Scanned) -> None:
    assert all(span.ttft_ms is None for span in traced.spans if span.kind != "turn")


def test_turn_aborted_closes_the_turn_with_its_reason(traced: Scanned) -> None:
    turn = traced.by_id("turn-2")
    assert turn.status == "aborted"
    assert turn.name == "interrupted"
    assert turn.detail["reason"] == "interrupted"
    assert (turn.duration_ms, turn.duration_provenance) == (13_000, "measured")


def test_an_item_completed_before_its_record_still_times_the_reasoning_span(
    traced: Scanned,
) -> None:
    reasoning = traced.by_id("rs_1")
    assert reasoning.kind == "reasoning"
    assert (reasoning.duration_ms, reasoning.duration_provenance) == (2_500, "measured")
    assert reasoning.content_path == "payload.summary"


def test_command_execution_times_the_open_call_it_does_not_id_match(traced: Scanned) -> None:
    call = traced.by_id("call1")
    assert (call.duration_ms, call.duration_provenance) == (3_250, "measured")
    assert call.detail["item_id"] == "exec-1"
    assert call.detail["exit_code"] == 0
    assert call.status == "ok"


def test_a_leading_exit_code_in_the_output_sets_the_result_status(traced: Scanned) -> None:
    result = traced.by_id("call1:out")
    assert result.kind == "tool_result"
    assert _local(result.parent_id) == "call1"
    assert result.detail["exit_code"] == 0
    assert result.status == "ok"


def test_a_non_zero_exit_code_marks_the_result_and_the_call_as_an_error(tmp_path: Path) -> None:
    path = tmp_path / "rollout-2026-09-02T10-00-00-cccccccc-dddd-eeee-ffff-000000000000.jsonl"
    records = [
        {"timestamp": "2026-09-02T10:00:00Z", "type": "event_msg",
         "payload": {"type": "task_started", "turn_id": "turn-9"}},
        {"timestamp": "2026-09-02T10:00:01Z", "type": "response_item",
         "payload": {"type": "function_call", "name": "shell", "arguments": "{}",
                     "call_id": "c9"}},
        {"timestamp": "2026-09-02T10:00:03Z", "type": "response_item",
         "payload": {"type": "function_call_output", "call_id": "c9",
                     "output": "Exit code: 2\nboom"}},
    ]
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
    found = scan(tmp_path)
    assert found.by_id("c9:out").status == "error"
    assert found.by_id("c9:out").detail["exit_code"] == 2
    assert found.by_id("c9").status == "error"
    assert (found.by_id("c9").duration_ms, found.by_id("c9").duration_provenance) == (
        2_000,
        "derived",
    )


def test_mcp_tool_call_end_duration_is_converted_to_milliseconds(traced: Scanned) -> None:
    call = traced.by_id("call3")
    assert (call.duration_ms, call.duration_provenance) == (2_500, "measured")
    assert call.status == "ok"


def test_one_model_call_per_token_count_delta_with_its_tokens_and_capacity(
    traced: Scanned,
) -> None:
    calls = traced.of_kind("model_call")
    assert [_local(call.span_id) for call in calls] == [
        "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee:mc:1",
        "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee:mc:2",
        "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee:mc:3",
    ]
    assert [call.tokens.total for call in calls if call.tokens] == [12_400, 14_300, 9_200]
    assert {call.tokens_provenance for call in calls} == {"measured"}
    assert {(call.context_capacity, call.capacity_provenance) for call in calls} == {
        (272_000, "measured")
    }
    assert calls[0].model == "gpt-5-codex"


def test_pending_spans_are_reparented_to_the_model_call_that_closes_them(
    traced: Scanned,
) -> None:
    first = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee:mc:1"
    children = [_local(span.span_id) for span in traced.spans if _local(span.parent_id) == first]
    assert children == ["rs_1", "call1"]
    assert _local(traced.by_id(first).parent_id) == "turn-1"
    assert _local(traced.by_id("msg_u1").parent_id) == "turn-1"


def test_a_model_call_is_measured_only_when_the_item_timings_bound_it(traced: Scanned) -> None:
    assert traced.by_id("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee:mc:1").duration_provenance == (
        "measured"
    )
    third = traced.by_id("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee:mc:3")
    assert (third.duration_ms, third.duration_provenance) == (12_000, "derived")


def test_a_compaction_records_how_many_entries_replaced_the_history(traced: Scanned) -> None:
    compaction = traced.of_kind("compaction")[0]
    assert compaction.detail["replacement_count"] == 2
    assert compaction.content_path == "payload.replacement_history"
    assert _local(compaction.parent_id) == "turn-2"


def test_every_span_belongs_to_a_turn_and_to_a_span_that_exists(traced: Scanned) -> None:
    ids = {span.span_id for span in traced.spans}
    assert len(ids) == len(traced.spans)
    assert all(_local(span.turn_id) in ("turn-1", "turn-2") for span in traced.spans)
    assert all(span.parent_id in ids for span in traced.spans if span.parent_id)
    assert [span.seq for span in traced.spans] == sorted(span.seq for span in traced.spans)


def test_the_recorded_offset_and_length_re_read_the_source_record(traced: Scanned) -> None:
    span = traced.by_id("rs_1")
    with Path(span.source_file).open("rb") as handle:
        handle.seek(span.record_offset)
        record = json.loads(handle.read(span.record_length))
    assert record["payload"]["id"] == "rs_1"


def test_a_legacy_rollout_without_item_timings_never_claims_a_measured_model_call(
    legacy: Scanned,
) -> None:
    inferred_from_items = [
        span for span in legacy.spans if span.kind in ("reasoning", "assistant", "model_call")
    ]
    assert {span.duration_provenance for span in inferred_from_items} == {
        "derived",
        "unavailable",
    }
    assert legacy.by_id("call4").duration_provenance == "derived"


def test_a_legacy_rollout_never_reports_a_zero_duration(legacy: Scanned) -> None:
    assert all(span.duration_ms != 0 for span in legacy.spans)
    assert all(
        (span.duration_ms is None) == (span.duration_provenance == "unavailable")
        for span in legacy.spans
    )


def test_a_legacy_rollout_keeps_the_durations_the_log_itself_measured(legacy: Scanned) -> None:
    measured = {
        _local(span.span_id)
        for span in legacy.spans
        if span.duration_provenance == "measured"
    }
    assert measured == {"turn-3", "turn-4", "call6"}


def test_a_legacy_rollout_still_produces_the_same_span_shape(legacy: Scanned) -> None:
    assert [span.kind for span in legacy.spans] == [
        "turn", "user", "reasoning", "tool_call", "tool_result", "model_call",
        "assistant", "model_call", "turn", "tool_call", "tool_result", "tool_call",
        "compaction", "model_call",
    ]
    assert legacy.warnings == []


def test_every_content_path_resolves_through_the_reader() -> None:
    config = Config(metadata_only=False)
    checked = 0
    for span in scan(CODEX_TRACE).spans + scan(CODEX_TRACE_LEGACY).spans:
        if span.content_path is None:
            continue
        assert read_content(span, config).content != ""
        checked += 1
    assert checked > 0
