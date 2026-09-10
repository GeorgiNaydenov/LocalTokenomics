from __future__ import annotations

import importlib
import json
import shutil
import webbrowser
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Annotated

import typer
from rich.console import Console
from rich.markup import escape

from .aggregate import Report
from .collect import collect as collect_samples
from .collect import select_backend
from .demo import DEMO_DB_PATH, DEMO_DIR, demo_roots, generate
from .pipeline import DEFAULT_DB_PATH, analyze, report_of
from .render.terminal import render

app = typer.Typer(
    add_completion=False,
    help="Local token usage and API-equivalent cost across every AI coding tool on your machine.",
)
console = Console()

Day = Annotated[str | None, typer.Option(help="ISO date, e.g. 2026-08-01.")]
Root = Annotated[
    list[str] | None,
    typer.Option("--root", help="Override a source's scan root: SOURCE=PATH. Repeatable."),
]
Db = Annotated[
    Path | None, typer.Option(help="SQLite store path. Default ~/.ai-usage-cost/usage.db.")
]
Rates = Annotated[Path | None, typer.Option(help="Alternate rates.json.")]
Rebuild = Annotated[
    bool, typer.Option(help="Discard the store and reparse every log from scratch.")
]


def _day(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def _require(module: str, extra: str) -> ModuleType:
    try:
        return importlib.import_module(module)
    except ImportError:
        console.print(
            f"[red]{module} is not installed.[/red] "
            f'Run: pip install "ai-usage-cost{escape(f"[{extra}]")}"'
        )
        raise typer.Exit(code=2) from None


def _roots(entries: list[str] | None) -> dict[str, list[Path]] | None:
    if not entries:
        return None
    roots: dict[str, list[Path]] = {}
    for entry in entries:
        source, _, path = entry.partition("=")
        if not path:
            raise typer.BadParameter(f"expected SOURCE=PATH, got {entry!r}")
        roots.setdefault(source, []).append(Path(path))
    return roots


@app.command()
def scan(
    since: Day = None,
    until: Day = None,
    source: Annotated[list[str] | None, typer.Option(help="Limit to a source id.")] = None,
    by: Annotated[
        str, typer.Option(help="Break down by model|client|provider|project|day.")
    ] = "model",
    no_sidechains: Annotated[bool, typer.Option(help="Exclude subagent requests.")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show all warnings.")] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the report as JSON.")] = False,
    root: Root = None,
    db: Db = None,
    rates: Rates = None,
    rebuild: Rebuild = False,
) -> None:
    analysis = analyze(db_path=db, roots=_roots(root), rates_path=rates, rebuild=rebuild)
    report = report_of(
        analysis,
        since=_day(since),
        until=_day(until),
        clients=source or None,
        include_sidechains=not no_sidechains,
    )
    if as_json:
        typer.echo(report.model_dump_json(indent=2))
        return
    if not report.totals.events:
        console.print(
            "[yellow]No usage found.[/yellow] Checked "
            f"{report.files_scanned} log file(s). Pass --root SOURCE=PATH "
            "if your logs live elsewhere."
        )
        raise typer.Exit(code=1)
    render(report, console, group_by=by, verbose=verbose)


@app.command()
def serve(
    host: str = "127.0.0.1",
    port: int = 8420,
    open_browser: Annotated[bool, typer.Option("--open/--no-open")] = True,
    root: Root = None,
    db: Db = None,
    rates: Rates = None,
    rebuild: Rebuild = False,
) -> None:
    import uvicorn

    from .api import create_app

    console.print("[dim]Scanning logs...[/dim]")
    roots = _roots(root)
    db_path = db or DEFAULT_DB_PATH
    analysis = analyze(db_path=db_path, roots=roots, rates_path=rates, rebuild=rebuild)
    console.print(
        f"[green]{len(analysis.events):,}[/green] requests from "
        f"{analysis.files:,} log files -> http://{host}:{port}"
    )
    if open_browser:
        webbrowser.open(f"http://{host}:{port}")
    uvicorn.run(
        create_app(analysis, db_path=db_path, rates_path=rates, roots=roots),
        host=host,
        port=port,
        log_level="warning",
    )


@app.command()
def demo(
    port: int = 8420,
    open_browser: Annotated[bool, typer.Option("--open/--no-open")] = True,
    off: Annotated[
        bool,
        typer.Option("--off", help="Delete the demo logs and store, then serve your real logs."),
    ] = False,
) -> None:
    if off:
        removed = DEMO_DIR.exists()
        shutil.rmtree(DEMO_DIR, ignore_errors=True)
        console.print(
            f"Removed [green]{DEMO_DIR}[/green]"
            if removed
            else f"[dim]Nothing to remove at {DEMO_DIR}.[/dim]"
        )
        serve(port=port, open_browser=open_browser)
        return
    if not DEMO_DIR.exists():
        console.print(f"[dim]Generating synthetic logs in {DEMO_DIR}...[/dim]")
        generate(DEMO_DIR)
    console.print(
        "[yellow]Demo data is synthetic.[/yellow] Every number comes from generated logs in "
        f"{DEMO_DIR}; your real logs and your store at {DEFAULT_DB_PATH} are not read or "
        "written. Switch back to your own data with [bold]ai-usage-cost demo --off[/bold]."
    )
    serve(
        port=port,
        open_browser=open_browser,
        root=[f"{source}={path}" for source, path in demo_roots(DEMO_DIR).items()],
        db=DEMO_DB_PATH,
    )


@app.command()
def export(
    out: Annotated[Path, typer.Argument(help="Output file: .json or .png.")],
    since: Day = None,
    until: Day = None,
    root: Root = None,
    db: Db = None,
    rates: Rates = None,
) -> None:
    analysis = analyze(db_path=db, roots=_roots(root), rates_path=rates)
    report = report_of(analysis, since=_day(since), until=_day(until))
    suffix = out.suffix.lower()
    if suffix == ".json":
        out.write_text(json.dumps(report.model_dump(mode="json"), indent=2), encoding="utf-8")
    elif suffix == ".png":
        from .render.png import write_png

        write_png(report, out)
    else:
        console.print(f"[red]Unsupported extension {suffix!r}.[/red] Use .json or .png.")
        raise typer.Exit(code=2)
    console.print(f"Wrote [green]{out}[/green]")


@app.command()
def collect(
    interval: Annotated[float, typer.Option(help="Seconds between samples.")] = 2.0,
    tdp_watts: Annotated[
        float | None,
        typer.Option(help="GPU TDP in watts. Without it energy stays unavailable."),
    ] = None,
    duration: Annotated[
        float | None, typer.Option(help="Stop after this many seconds. Default: until Ctrl+C.")
    ] = None,
    db: Db = None,
) -> None:
    backend = select_backend()
    if backend is None:
        console.print(
            "[red]No GPU sampler available.[/red] nvidia-smi is not on PATH and "
            "PowerShell performance counters are unavailable."
        )
        raise typer.Exit(code=1)
    db_path = db or DEFAULT_DB_PATH
    console.print(f"Sampling via [green]{backend}[/green] every {interval:g}s -> {db_path}")
    samples, energy = collect_samples(db_path, interval, tdp_watts, duration=duration)
    console.print(f"Wrote [green]{len(samples):,}[/green] sample(s).")
    if energy is None:
        console.print("[dim]Energy unavailable: pass --tdp-watts to estimate it.[/dim]")
    else:
        console.print(f"Energy [green]{energy:.6f}[/green] kWh (estimated from TDP, not measured)")


@app.command()
def sql(
    host: str = "127.0.0.1",
    port: int = 8421,
    open_browser: Annotated[bool, typer.Option("--open/--no-open")] = True,
    db: Db = None,
) -> None:
    _require("datasette", "sql")
    from datasette.cli import cli as datasette_cli

    db_path = db or DEFAULT_DB_PATH
    if not db_path.exists():
        console.print(
            f"[red]No store at {db_path}.[/red] Run `ai-usage-cost scan` first, "
            "or point at another store with --db."
        )
        raise typer.Exit(code=2)
    args = ["serve", str(db_path), "--host", host, "--port", str(port)]
    if open_browser:
        args.append("--open")
    datasette_cli(args)


@dataclass(frozen=True)
class AlertDecision:
    fire: bool
    message: str


def alert_decision(
    current: Report, previous: Report | None, *, threshold: float, days: int
) -> AlertDecision:
    total = current.totals.cost.total
    if previous is None:
        amount = total
        headline = f"${total:,.2f} priced spend over the last {days} day(s)"
        compared = f"compared window total ${amount:,.2f} to --over ${threshold:,.2f}"
    else:
        amount = total - previous.totals.cost.total
        headline = (
            f"${total:,.2f} priced spend over the last {days} day(s), "
            f"${amount:+,.2f} from ${previous.totals.cost.total:,.2f} "
            f"in the {days} day(s) before"
        )
        compared = f"compared rise ${amount:+,.2f} to --rise-over ${threshold:,.2f}"
    totals = current.totals
    lines = [
        headline,
        f"{compared} · {totals.tokens.total:,} tokens · "
        f"{totals.events:,} requests · {totals.sessions:,} sessions",
    ]
    excluded = _excluded_from_cost(current)
    if excluded:
        lines.append(excluded)
    return AlertDecision(fire=amount > threshold, message="\n".join(lines))


def _excluded_from_cost(report: Report) -> str:
    parts = []
    if report.unknown_models:
        tokens = sum(item.tokens for item in report.unknown_models)
        parts.append(f"{len(report.unknown_models)} unpriced model(s), {tokens:,} tokens")
    blind = sum(1 for row in report.sessions if row.cost_state == "unavailable")
    if blind:
        parts.append(f"{blind} session(s) whose logs carry no token counts")
    if not parts:
        return ""
    return "Excluded from that cost: " + "; ".join(parts) + " -- unknown, not zero."


@app.command()
def alert(
    to: Annotated[
        list[str], typer.Option("--to", help="Apprise target URL, e.g. ntfy://host/topic.")
    ],
    over: Annotated[
        float | None,
        typer.Option(help="Fire when the window's own total exceeds this many dollars."),
    ] = None,
    rise_over: Annotated[
        float | None,
        typer.Option(
            help="Fire when the rise over the preceding window of the same length "
            "exceeds this many dollars."
        ),
    ] = None,
    days: Annotated[int, typer.Option(help="Window length in days, ending today.")] = 1,
    root: Root = None,
    db: Db = None,
    rates: Rates = None,
    rebuild: Rebuild = False,
) -> None:
    if days < 1:
        raise typer.BadParameter("--days must be at least 1")
    if over is not None and rise_over is not None:
        raise typer.BadParameter("pass --over or --rise-over, not both")
    threshold = over if over is not None else rise_over
    if threshold is None:
        raise typer.BadParameter("pass --over (window total) or --rise-over (rise vs before)")
    apprise = _require("apprise", "alert")

    until = date.today()
    since = until - timedelta(days=days - 1)
    analysis = analyze(db_path=db, roots=_roots(root), rates_path=rates, rebuild=rebuild)
    current = report_of(analysis, since=since, until=until)
    previous = None
    if rise_over is not None:
        previous = report_of(
            analysis, since=since - timedelta(days=days), until=since - timedelta(days=1)
        )

    decision = alert_decision(current, previous, threshold=threshold, days=days)
    console.print(decision.message)
    if not decision.fire:
        return

    notifier = apprise.Apprise()
    for url in to:
        if not notifier.add(url):
            console.print(f"[red]Apprise rejected target {url!r}.[/red]")
            raise typer.Exit(code=1)
    if not notifier.notify(
        title=f"ai-usage-cost: ${current.totals.cost.total:,.2f} over {days} day(s)",
        body=decision.message,
    ):
        console.print("[red]Apprise could not deliver the notification.[/red]")
        raise typer.Exit(code=1)


@app.command()
def tui(
    since: Day = None,
    until: Day = None,
    root: Root = None,
    db: Db = None,
    rates: Rates = None,
    rebuild: Rebuild = False,
) -> None:
    _require("textual", "tui")
    from .tui import run_tui

    analysis = analyze(db_path=db, roots=_roots(root), rates_path=rates, rebuild=rebuild)
    report = report_of(analysis, since=_day(since), until=_day(until))
    if not report.sessions:
        console.print(
            f"[yellow]No usage found.[/yellow] Checked {report.files_scanned} log file(s)."
        )
        raise typer.Exit(code=1)
    run_tui(report)


if __name__ == "__main__":
    app()
