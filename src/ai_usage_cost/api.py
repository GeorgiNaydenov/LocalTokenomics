from __future__ import annotations

import sqlite3
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import privacy, store
from .aggregate import Report, WarningGroup, WarningSeverity, warning_groups_of
from .models import CostState, PricedEvent, UsageEvent
from .pipeline import Analysis, SourceInfo, analyze, report_of
from .pricing import RateTable
from .sources import registry
from .trace import (
    TOOL_KINDS,
    UNATTRIBUTED_TURN_KEY,
    Capabilities,
    ContextSnapshot,
    Economics,
    Outcome,
    OutcomeLabel,
    OutcomeSignals,
    OutcomeUpdate,
    Span,
    SpanContent,
    Trace,
    context_of,
    economics_of,
    insights_of,
    is_error_span,
    tool_result_parent_ids,
)

WEB_DIST = Path(__file__).parent / "web" / "dist"


def _signals_of(spans: list[Span]) -> OutcomeSignals:
    signals = OutcomeSignals()
    parents = tool_result_parent_ids(spans)
    for span in spans:
        if span.kind == "turn":
            signals.last_turn_status = span.status
            if span.status == "aborted":
                signals.aborted_turns += 1
        if span.kind in TOOL_KINDS and span.status == "interrupted":
            signals.interrupted_tools += 1
        if is_error_span(span, parents):
            signals.errors += 1
    return signals


def _first_user_span_by_turn(spans: Sequence[Span]) -> dict[str, Span]:
    """The earliest `user`-kind span for each turn, in the order spans were emitted.
    Used to build a per-turn label from the turn's opening prompt.
    """
    found: dict[str, Span] = {}
    for span in spans:
        if span.kind == "user" and span.turn_id and span.turn_id not in found:
            found[span.turn_id] = span
    return found


def _turn_label(span: Span | None, config: privacy.Config) -> str | None:
    """A single-line, <=80 character, redacted snippet of a turn's first user message,
    read the same way `privacy.read_content` reads any other span (metadata-only config
    or a missing/unreadable record both mean no label, not an empty string).
    """
    if span is None:
        return None
    try:
        content = privacy.read_content(span, config)
    except privacy.ContentUnavailable:
        return None
    single_line = " ".join(content.content.split())
    snippet, _ = privacy.truncate(single_line, 80)
    return snippet or None


class ClientInfo(BaseModel):
    id: str
    label: str


class WarningSummary(BaseModel):
    """Counts of warning *instances* by severity, plus their total estimated dollar impact.

    Computed from the grouped/classified form (`warning_groups_of`), not the raw string
    list, so it reflects the same severity and magnitude reasoning shown on the Sources
    screen's warning groups.
    """

    critical: int = 0
    caution: int = 0
    info: int = 0
    total_delta_cost: float = 0.0


class Meta(BaseModel):
    clients: list[ClientInfo] = Field(default_factory=list)
    providers: list[str] = Field(default_factory=list)
    models: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    first_day: date | None = None
    last_day: date | None = None
    rates_as_of: str = ""
    currency: str = "USD"
    files_scanned: int = 0
    events: int = 0
    warnings: list[str] = Field(default_factory=list)
    warning_summary: WarningSummary = Field(default_factory=WarningSummary)
    # session_id -> sorted distinct warning kinds affecting that session (e.g.
    # ["codex_drift"]). Resolved via each warning's own embedded filename joined against
    # PricedEvent.source_file -- see the module-level docstring-style note near
    # `_session_lookup` below for exactly how this is built and why it isn't a SessionRow
    # field.
    session_warnings: dict[str, list[str]] = Field(default_factory=dict)
    sources: list[SourceInfo] = Field(default_factory=list)
    client_last_seen: dict[str, str] = Field(default_factory=dict)
    model_last_seen: dict[str, str] = Field(default_factory=dict)
    project_last_seen: dict[str, str] = Field(default_factory=dict)


def _last_seen_by(
    events: list[PricedEvent], key: Callable[[UsageEvent], str | None]
) -> dict[str, str]:
    latest: dict[str, str] = {}
    for item in events:
        value = key(item.event)
        if value is None:
            continue
        stamp = item.event.timestamp.isoformat()
        if value not in latest or stamp > latest[value]:
            latest[value] = stamp
    return latest


# --- Warning aggregation wiring -------------------------------------------------------
#
# `SessionRow` (aggregate.py) is off-limits for this change, so the session <-> warning
# join lives entirely here in api.py instead of as a field on that model. It is built the
# same way `SessionRow.raw_source` is: from each priced event's own `source_file`, joined
# against a warning's embedded filename (see `aggregate._file_of`). `Meta.session_warnings`
# is the result: `dict[session_id, list[warning kind]]`, e.g. `{"sess-1": ["codex_drift"]}`.
# A web/session-detail consumer looks up `meta.session_warnings.get(session.session_id)`
# to badge a session -- no change to `SessionRow` or `Report` needed.


def _session_lookup(events: list[PricedEvent]) -> dict[str, str]:
    """File basename -> session id, for every priced event currently loaded."""
    return {Path(item.event.source_file).name: item.event.session_id for item in events}


def _session_totals(events: list[PricedEvent]) -> dict[str, tuple[int, float]]:
    """Session id -> (total tokens, total cost), used only to price a warning's known
    token delta proportionally against the session it was raised against."""
    tokens: dict[str, int] = {}
    cost: dict[str, float] = {}
    for item in events:
        session_id = item.event.session_id
        if item.event.tokens is not None:
            tokens[session_id] = tokens.get(session_id, 0) + item.event.tokens.total
        if item.cost is not None:
            cost[session_id] = cost.get(session_id, 0.0) + item.cost.total
    return {session_id: (total, cost.get(session_id, 0.0)) for session_id, total in tokens.items()}


def _warning_summary(groups: list[WarningGroup]) -> WarningSummary:
    summary = WarningSummary()
    for group in groups:
        for instance in group.instances:
            if instance.severity == WarningSeverity.critical:
                summary.critical += 1
            elif instance.severity == WarningSeverity.caution:
                summary.caution += 1
            else:
                summary.info += 1
    summary.total_delta_cost = sum(group.total_delta_cost for group in groups)
    return summary


def _session_warnings_of(groups: list[WarningGroup]) -> dict[str, list[str]]:
    kinds: dict[str, set[str]] = {}
    for group in groups:
        for instance in group.instances:
            if instance.session_id:
                kinds.setdefault(instance.session_id, set()).add(instance.kind)
    return {session_id: sorted(values) for session_id, values in kinds.items()}


def create_app(
    analysis: Analysis | None = None,
    db_path: Path | None = None,
    rates_path: Path | None = None,
    roots: dict[str, list[Path]] | None = None,
) -> FastAPI:
    state: dict[str, Analysis] = {
        "analysis": analysis or analyze(db_path=db_path, roots=roots, rates_path=rates_path)
    }
    app = FastAPI(title="ai-usage-cost", version="0.1.0", docs_url="/api/docs")

    def current() -> Analysis:
        return state["analysis"]

    @contextmanager
    def opened() -> Iterator[sqlite3.Connection]:
        path = current().db_path
        if path is None:
            raise HTTPException(503, "this analysis was built without a store")
        conn = store.open_store(path)
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def session_spans(
        source: str, session_id: str
    ) -> Iterator[tuple[sqlite3.Connection, list[Span]]]:
        with opened() as conn:
            if not store.session_exists(conn, source, session_id):
                raise HTTPException(404, f"no session {session_id!r} under source {source!r}")
            yield conn, store.load_spans(conn, source, session_id)

    def capabilities_of(source: str) -> Capabilities:
        found = registry().get(source)
        return found.capabilities if found is not None else Capabilities()

    def outcome_of(
        conn: sqlite3.Connection, source: str, session_id: str, spans: list[Span]
    ) -> Outcome:
        stored = store.get_outcome(conn, source, session_id)
        base = stored or Outcome(source=source, session_id=session_id)
        return base.model_copy(update={"signals": _signals_of(spans)})

    @app.get("/api/meta", response_model=Meta)
    def meta() -> Meta:
        found = current()
        labels = found.client_labels
        days = [item.event.timestamp.date() for item in found.events]
        groups = warning_groups_of(
            found.warnings,
            session_lookup=_session_lookup(found.events),
            session_totals=_session_totals(found.events),
        )
        return Meta(
            clients=[
                ClientInfo(id=client, label=labels.get(client, client))
                for client in sorted({item.event.client for item in found.events})
            ],
            providers=sorted({item.event.provider for item in found.events if item.event.provider}),
            models=sorted({item.event.model for item in found.events if item.event.model}),
            projects=sorted({item.event.project for item in found.events if item.event.project}),
            first_day=min(days) if days else None,
            last_day=max(days) if days else None,
            rates_as_of=found.table.as_of,
            currency=found.table.currency,
            files_scanned=found.files,
            events=len(found.events),
            warnings=found.warnings,
            warning_summary=_warning_summary(groups),
            session_warnings=_session_warnings_of(groups),
            sources=found.sources,
            client_last_seen=_last_seen_by(found.events, lambda e: e.client),
            model_last_seen=_last_seen_by(found.events, lambda e: e.model),
            project_last_seen=_last_seen_by(found.events, lambda e: e.project),
        )

    @app.get("/api/report", response_model=Report)
    def report(
        since: date | None = None,
        until: date | None = None,
        search: str | None = None,
        states: Annotated[list[CostState] | None, Query()] = None,
        clients: Annotated[list[str] | None, Query()] = None,
        providers: Annotated[list[str] | None, Query()] = None,
        models: Annotated[list[str] | None, Query()] = None,
        projects: Annotated[list[str] | None, Query()] = None,
        include_sidechains: bool = True,
        outcomes: Annotated[list[OutcomeLabel] | None, Query()] = None,
        traced: bool | None = None,
        has_errors: bool | None = None,
    ) -> Report:
        return report_of(
            current(),
            since=since,
            until=until,
            search=search,
            states=states,
            clients=clients,
            providers=providers,
            models=models,
            projects=projects,
            include_sidechains=include_sidechains,
            outcomes=outcomes,
            traced=traced,
            has_errors=has_errors,
        )

    @app.get("/api/sessions/{source}/{session_id}/trace", response_model=Trace)
    def trace(source: str, session_id: str) -> Trace:
        with session_spans(source, session_id) as (conn, spans):
            table = current().table
            return Trace(
                source=source,
                session_id=session_id,
                capabilities=capabilities_of(source),
                spans=spans,
                outcome=outcome_of(conn, source, session_id, spans),
                insights=insights_of(spans, economics_of(spans, table), table),
            )

    @app.get("/api/sessions/{source}/{session_id}/economics", response_model=Economics)
    def economics(source: str, session_id: str) -> Economics:
        with session_spans(source, session_id) as (_, spans):
            econ = economics_of(spans, current().table)
            config = privacy.load_config()
            first_user = _first_user_span_by_turn(spans)
            for row in econ.by_turn:
                if row.key == UNATTRIBUTED_TURN_KEY:
                    continue
                row.label = _turn_label(first_user.get(row.key), config)
            return econ

    @app.get("/api/sessions/{source}/{session_id}/context", response_model=list[ContextSnapshot])
    def context(source: str, session_id: str) -> list[ContextSnapshot]:
        with session_spans(source, session_id) as (_, spans):
            return context_of(spans, current().table)

    @app.get("/api/sessions/{source}/{session_id}/outcome", response_model=Outcome)
    def outcome(source: str, session_id: str) -> Outcome:
        with session_spans(source, session_id) as (conn, spans):
            return outcome_of(conn, source, session_id, spans)

    @app.put("/api/sessions/{source}/{session_id}/outcome", response_model=Outcome)
    def rate_session(source: str, session_id: str, update: OutcomeUpdate) -> Outcome:
        with session_spans(source, session_id) as (conn, spans):
            stored = store.put_outcome(conn, source, session_id, update)
            return stored.model_copy(update={"signals": _signals_of(spans)})

    @app.delete("/api/sessions/{source}/{session_id}")
    def forget_session(source: str, session_id: str) -> dict[str, int]:
        with opened() as conn:
            if not store.session_exists(conn, source, session_id):
                raise HTTPException(404, f"no session {session_id!r} under source {source!r}")
            return {"deleted_spans": store.delete_session(conn, source, session_id)}

    @app.get(
        "/api/sessions/{source}/{session_id}/spans/{span_id}/content",
        response_model=SpanContent,
    )
    def span_content(source: str, session_id: str, span_id: str) -> SpanContent:
        with session_spans(source, session_id) as (_, spans):
            span = next((item for item in spans if item.span_id == span_id), None)
            if span is None:
                raise HTTPException(404, f"no span {span_id!r} in session {session_id!r}")
            try:
                return privacy.read_content(span, privacy.load_config())
            except privacy.ContentUnavailable as exc:
                raise HTTPException(404, f"no readable content for span {span_id!r}") from exc

    @app.get("/api/rates", response_model=RateTable)
    def rates() -> RateTable:
        return current().table

    @app.post("/api/refresh", response_model=Meta)
    def refresh() -> Meta:
        state["analysis"] = analyze(db_path=db_path, roots=roots, rates_path=rates_path)
        return meta()

    if WEB_DIST.is_dir():
        app.mount("/", StaticFiles(directory=WEB_DIST, html=True), name="dashboard")
    else:

        @app.get("/")
        def missing_build() -> FileResponse | dict[str, str]:
            return {
                "detail": "Dashboard bundle not built. Run `npm ci && npm run build` in web/.",
            }

    return app
