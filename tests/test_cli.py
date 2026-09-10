from __future__ import annotations

import importlib
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType

import pytest
from typer.testing import CliRunner, Result

from ai_usage_cost import cli
from ai_usage_cost.aggregate import Report, SessionRow, Totals, UnknownModel
from ai_usage_cost.models import CostBreakdown, TokenUsage
from ai_usage_cost.pipeline import Analysis

runner = CliRunner()
NOW = datetime(2026, 9, 8, 12, 0, tzinfo=UTC)


def report(
    cost: float,
    *,
    unknown_models: list[UnknownModel] | None = None,
    sessions: list[SessionRow] | None = None,
) -> Report:
    return Report(
        generated_at=NOW,
        totals=Totals(
            cost=CostBreakdown(output=cost),
            tokens=TokenUsage(output=5_000),
            events=12,
            sessions=3,
        ),
        unknown_models=unknown_models or [],
        sessions=sessions or [],
    )


def session(cost_state: str) -> SessionRow:
    return SessionRow(
        session_id="s1",
        source="jan",
        client="jan",
        provider="unknown",
        start_time=NOW,
        end_time=NOW,
        cost_state=cost_state,  # type: ignore[arg-type]
    )


def invoke(*args: str) -> Result:
    return runner.invoke(cli.app, list(args), env={"COLUMNS": "300"})


def test_spend_under_the_threshold_does_not_fire() -> None:
    decision = cli.alert_decision(report(9.5), None, threshold=10.0, days=7)
    assert decision.fire is False
    assert "$9.50 priced spend over the last 7 day(s)" in decision.message
    assert "compared window total $9.50 to --over $10.00" in decision.message


def test_spend_over_the_threshold_fires() -> None:
    assert cli.alert_decision(report(10.01), None, threshold=10.0, days=1).fire is True


def test_spend_exactly_at_the_threshold_does_not_fire() -> None:
    assert cli.alert_decision(report(10.0), None, threshold=10.0, days=1).fire is False


def test_rise_over_compares_the_rise_not_the_total() -> None:
    current, previous = report(30.0), report(25.0)
    assert cli.alert_decision(current, previous, threshold=10.0, days=7).fire is False
    assert cli.alert_decision(current, report(15.0), threshold=10.0, days=7).fire is True
    message = cli.alert_decision(current, previous, threshold=10.0, days=7).message
    assert "$+5.00 from $25.00 in the 7 day(s) before" in message
    assert "compared rise $+5.00 to --rise-over $10.00" in message


def test_a_drop_never_fires_in_rise_over_mode() -> None:
    assert cli.alert_decision(report(5.0), report(40.0), threshold=1.0, days=1).fire is False


def test_message_reports_unpriced_and_unavailable_usage_as_excluded() -> None:
    decision = cli.alert_decision(
        report(
            12.0,
            unknown_models=[UnknownModel(model="mystery-1", tokens=120_000, events=4)],
            sessions=[session("unavailable"), session("priced")],
        ),
        None,
        threshold=1.0,
        days=1,
    )
    assert "1 unpriced model(s), 120,000 tokens" in decision.message
    assert "1 session(s) whose logs carry no token counts" in decision.message
    assert "unknown, not zero" in decision.message


def test_message_omits_the_exclusion_line_when_everything_is_priced() -> None:
    decision = cli.alert_decision(
        report(12.0, sessions=[session("priced")]), None, threshold=1, days=1
    )
    assert "Excluded" not in decision.message


def fake_apprise(
    monkeypatch: pytest.MonkeyPatch, *, added: bool = True, delivered: bool = True
) -> list[str]:
    calls: list[str] = []

    class FakeApprise:
        def add(self, url: str) -> bool:
            calls.append(f"add {url}")
            return added

        def notify(self, title: str, body: str) -> bool:
            calls.append(f"notify {title}")
            return delivered

    module = ModuleType("apprise")
    module.Apprise = FakeApprise  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "apprise", module)
    return calls


@pytest.fixture
def priced_window(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "analyze", lambda **kwargs: Analysis())
    monkeypatch.setattr(cli, "report_of", lambda analysis, **kwargs: report(50.0))


def test_alert_rejects_a_non_positive_window() -> None:
    for window in ("0", "-5"):
        result = invoke("alert", "--to", "json://example.invalid", "--over", "5", "--days", window)
        assert result.exit_code == 2
        assert "--days must be at least 1" in result.output


def test_alert_needs_exactly_one_threshold() -> None:
    neither = invoke("alert", "--to", "json://example.invalid")
    assert neither.exit_code == 2
    assert "--over" in neither.output and "--rise-over" in neither.output

    both = invoke("alert", "--to", "json://example.invalid", "--over", "5", "--rise-over", "5")
    assert both.exit_code == 2
    assert "not both" in both.output


def test_alert_delivers_and_exits_zero(
    priced_window: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = fake_apprise(monkeypatch)
    result = invoke("alert", "--to", "json://example.invalid", "--over", "5")
    assert result.exit_code == 0
    assert calls == ["add json://example.invalid", "notify ai-usage-cost: $50.00 over 1 day(s)"]


def test_alert_stays_quiet_and_exits_zero_below_the_threshold(
    priced_window: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = fake_apprise(monkeypatch)
    result = invoke("alert", "--to", "json://example.invalid", "--over", "500")
    assert result.exit_code == 0
    assert calls == []


def test_alert_fails_on_a_rejected_target(
    priced_window: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = fake_apprise(monkeypatch, added=False)
    result = invoke("alert", "--to", "nonsense://", "--over", "5")
    assert result.exit_code == 1
    assert "Apprise rejected target" in result.output
    assert calls == ["add nonsense://"]


def test_alert_fails_when_delivery_fails(
    priced_window: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_apprise(monkeypatch, delivered=False)
    result = invoke("alert", "--to", "json://example.invalid", "--over", "5")
    assert result.exit_code == 1
    assert "could not deliver" in result.output


def test_tui_filter_matches_any_visible_session_field() -> None:
    tui = pytest.importorskip("ai_usage_cost.tui")
    row = session("unavailable")
    assert tui._matches(row, "") is True
    assert tui._matches(row, "s1") is True
    assert tui._matches(row, "jan") is True
    assert tui._matches(row, "unavailable") is True
    assert tui._matches(row, "claude") is False


@pytest.fixture
def datasette_args(monkeypatch: pytest.MonkeyPatch) -> list[list[str]]:
    captured: list[list[str]] = []
    package = ModuleType("datasette")
    module = ModuleType("datasette.cli")
    module.cli = captured.append  # type: ignore[attr-defined]
    package.cli = module  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "datasette", package)
    monkeypatch.setitem(sys.modules, "datasette.cli", module)
    return captured


def test_sql_hands_the_explicit_db_to_datasette(
    datasette_args: list[list[str]], tmp_path: Path
) -> None:
    store = tmp_path / "usage.db"
    store.touch()
    result = invoke("sql", "--db", str(store), "--port", "9999")
    assert result.exit_code == 0
    assert datasette_args == [
        ["serve", str(store), "--host", "127.0.0.1", "--port", "9999", "--open"]
    ]


def test_sql_falls_back_to_the_default_store(
    datasette_args: list[list[str]], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = tmp_path / "default.db"
    store.touch()
    monkeypatch.setattr(cli, "DEFAULT_DB_PATH", store)
    assert invoke("sql", "--no-open").exit_code == 0
    assert datasette_args[0][1] == str(store)


def test_sql_names_the_missing_store_instead_of_launching(
    datasette_args: list[list[str]], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cli, "DEFAULT_DB_PATH", tmp_path / "absent.db")
    result = invoke("sql")
    assert result.exit_code == 2
    assert "absent.db" in result.output
    assert datasette_args == []


@pytest.mark.parametrize(
    ("command", "module", "extra"),
    [
        (["sql"], "datasette", "sql"),
        (["alert", "--to", "json://example.invalid", "--over", "5"], "apprise", "alert"),
        (["tui"], "textual", "tui"),
    ],
)
def test_a_missing_extra_explains_how_to_install_it(
    command: list[str], module: str, extra: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = importlib.import_module

    def refuse(name: str, package: str | None = None) -> ModuleType:
        if name == module:
            raise ImportError(name)
        return real(name, package)

    monkeypatch.setattr(importlib, "import_module", refuse)
    result = invoke(*command)
    assert result.exit_code == 2
    assert f'pip install "ai-usage-cost[{extra}]"' in result.output
