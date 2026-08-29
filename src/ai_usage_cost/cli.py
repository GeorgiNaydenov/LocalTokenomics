"""Command line entry point: ``scan``, ``serve``, ``export``."""

from __future__ import annotations

import json
import webbrowser
from datetime import date
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .pipeline import analyze, report_of
from .render.terminal import render

app = typer.Typer(
    add_completion=False,
    help="Token usage and API-equivalent cost for your local Claude Code and Codex logs.",
)
console = Console()

Day = Annotated[str | None, typer.Option(help="ISO date, e.g. 2026-08-01.")]
ClaudeDir = Annotated[Path | None, typer.Option(help="Override ~/.claude/projects.")]
CodexDir = Annotated[Path | None, typer.Option(help="Override ~/.codex/sessions.")]
Rates = Annotated[Path | None, typer.Option(help="Alternate rates.json.")]


def _day(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def _roots(claude_dir: Path | None, codex_dir: Path | None) -> dict[str, list[Path]] | None:
    roots: dict[str, list[Path]] = {}
    if claude_dir:
        roots["claude-code"] = [claude_dir]
    if codex_dir:
        roots["codex"] = [codex_dir]
    return roots or None


@app.command()
def scan(
    since: Day = None,
    until: Day = None,
    tool: Annotated[list[str] | None, typer.Option(help="Limit to a source id.")] = None,
    by: Annotated[str, typer.Option(help="Break down by model|tool|project|day.")] = "model",
    no_sidechains: Annotated[bool, typer.Option(help="Exclude subagent requests.")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show all warnings.")] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the report as JSON.")] = False,
    claude_dir: ClaudeDir = None,
    codex_dir: CodexDir = None,
    rates: Rates = None,
) -> None:
    """Summarise local usage in the terminal."""
    analysis = analyze(tools=tool or None, roots=_roots(claude_dir, codex_dir), rates_path=rates)
    report = report_of(
        analysis,
        since=_day(since),
        until=_day(until),
        include_sidechains=not no_sidechains,
    )
    if as_json:
        typer.echo(report.model_dump_json(indent=2))
        return
    if not report.totals.events:
        console.print("[yellow]No usage found.[/yellow] Checked "
                      f"{report.files_scanned} log file(s). Pass --claude-dir/--codex-dir "
                      "if your logs live elsewhere.")
        raise typer.Exit(code=1)
    render(report, console, group_by=by, verbose=verbose)


@app.command()
def serve(
    host: str = "127.0.0.1",
    port: int = 8420,
    open_browser: Annotated[bool, typer.Option("--open/--no-open")] = True,
    claude_dir: ClaudeDir = None,
    codex_dir: CodexDir = None,
    rates: Rates = None,
) -> None:
    """Run the local dashboard."""
    import uvicorn

    from .api import create_app

    console.print("[dim]Scanning logs...[/dim]")
    roots = _roots(claude_dir, codex_dir)
    analysis = analyze(roots=roots, rates_path=rates)
    console.print(
        f"[green]{len(analysis.priced):,}[/green] priced requests from "
        f"{analysis.files:,} log files -> http://{host}:{port}"
    )
    if open_browser:
        webbrowser.open(f"http://{host}:{port}")
    uvicorn.run(
        create_app(analysis, rates_path=rates, roots=roots),
        host=host,
        port=port,
        log_level="warning",
    )


@app.command()
def export(
    out: Annotated[Path, typer.Argument(help="Output file: .json or .png.")],
    since: Day = None,
    until: Day = None,
    claude_dir: ClaudeDir = None,
    codex_dir: CodexDir = None,
    rates: Rates = None,
) -> None:
    """Write the report to a file (format chosen by extension)."""
    analysis = analyze(roots=_roots(claude_dir, codex_dir), rates_path=rates)
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


if __name__ == "__main__":
    app()
