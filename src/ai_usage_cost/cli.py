from __future__ import annotations

import json
import webbrowser
from datetime import date
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .collect import collect as collect_samples
from .collect import select_backend
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
        console.print("[yellow]No usage found.[/yellow] Checked "
                      f"{report.files_scanned} log file(s). Pass --root SOURCE=PATH "
                      "if your logs live elsewhere.")
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
        console.print("[red]No GPU sampler available.[/red] nvidia-smi is not on PATH and "
                      "PowerShell performance counters are unavailable.")
        raise typer.Exit(code=1)
    db_path = db or DEFAULT_DB_PATH
    console.print(f"Sampling via [green]{backend}[/green] every {interval:g}s -> {db_path}")
    samples, energy = collect_samples(db_path, interval, tdp_watts, duration=duration)
    console.print(f"Wrote [green]{len(samples):,}[/green] sample(s).")
    if energy is None:
        console.print("[dim]Energy unavailable: pass --tdp-watts to estimate it.[/dim]")
    else:
        console.print(f"Energy [green]{energy:.6f}[/green] kWh (estimated from TDP, not measured)")


if __name__ == "__main__":
    app()
