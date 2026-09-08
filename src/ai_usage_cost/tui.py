from __future__ import annotations

from collections.abc import Callable
from typing import Any

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header, Input

from .aggregate import UNATTRIBUTED, Report, SessionRow

Column = tuple[str, Callable[[SessionRow], str], Callable[[SessionRow], Any]]


def _count(value: int | None) -> str:
    return f"{value:,}" if value is not None else "--"


def _input(row: SessionRow) -> int | None:
    return row.tokens.uncached_input if row.tokens else None


def _cached(row: SessionRow) -> int | None:
    return row.tokens.cache_read if row.tokens else None


def _output(row: SessionRow) -> int | None:
    return row.tokens.output if row.tokens else None


def _cost(row: SessionRow) -> float | None:
    return row.cost.total if row.cost else None


COLUMNS: tuple[Column, ...] = (
    ("Start", lambda r: f"{r.start_time:%Y-%m-%d %H:%M}", lambda r: r.start_time),
    ("Client", lambda r: r.client, lambda r: r.client),
    ("Project", lambda r: r.project or UNATTRIBUTED, lambda r: r.project or UNATTRIBUTED),
    ("Models", lambda r: ", ".join(r.models), lambda r: ", ".join(r.models)),
    ("Requests", lambda r: f"{r.request_count:,}", lambda r: r.request_count),
    ("Input", lambda r: _count(_input(r)), lambda r: _input(r) or 0),
    ("Cached", lambda r: _count(_cached(r)), lambda r: _cached(r) or 0),
    ("Output", lambda r: _count(_output(r)), lambda r: _output(r) or 0),
    (
        "Cost",
        lambda r: f"${_cost(r):,.2f}" if _cost(r) is not None else "--",
        lambda r: _cost(r) or 0.0,
    ),
    ("State", lambda r: r.cost_state, lambda r: r.cost_state),
)

COST_COLUMN = [label for label, _, _ in COLUMNS].index("Cost")


def _matches(row: SessionRow, needle: str) -> bool:
    if not needle:
        return True
    haystack = " ".join(
        [row.session_id, row.client, row.provider, row.project or "", row.cost_state, *row.models]
    )
    return needle in haystack.lower()


class SessionsApp(App[None]):
    TITLE = "ai-usage-cost"
    BINDINGS = [("q", "quit", "Quit"), ("slash", "focus_filter", "Filter")]

    def __init__(self, report: Report) -> None:
        super().__init__()
        self.report = report
        self.sort_column = COST_COLUMN
        self.descending = True

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Filter by session, client, project, model or cost state")
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        for label, _, _ in COLUMNS:
            table.add_column(label)
        self._fill()

    def on_input_changed(self, _: Input.Changed) -> None:
        self._fill()

    def on_data_table_header_selected(self, event: DataTable.HeaderSelected) -> None:
        if event.column_index == self.sort_column:
            self.descending = not self.descending
        else:
            self.sort_column = event.column_index
            self.descending = True
        self._fill()

    def action_focus_filter(self) -> None:
        self.query_one(Input).focus()

    def _fill(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        rows = [
            row
            for row in self.report.sessions
            if _matches(row, self.query_one(Input).value.strip().lower())
        ]
        rows.sort(key=COLUMNS[self.sort_column][2], reverse=self.descending)
        for row in rows:
            table.add_row(*(cell(row) for _, cell, _ in COLUMNS))
        arrow = "v" if self.descending else "^"
        self.sub_title = (
            f"{len(rows)} of {len(self.report.sessions)} sessions · "
            f"sorted by {COLUMNS[self.sort_column][0]} {arrow}"
        )


def run_tui(report: Report) -> None:
    SessionsApp(report).run()
