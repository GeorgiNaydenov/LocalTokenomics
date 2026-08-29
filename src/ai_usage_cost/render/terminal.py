"""Rich terminal rendering of a :class:`Report`."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..aggregate import Bucket, Report

TOKEN_COLUMNS = (
    ("Input", lambda t: t.uncached_input),
    ("Cache read", lambda t: t.cache_read),
    ("Cache write", lambda t: t.cache_write),
    ("Output", lambda t: t.output),
)


def render(
    report: Report, console: Console, *, group_by: str = "model", verbose: bool = False
) -> None:
    console.print(_headline(report))

    tables = {
        "model": ("By model", report.by_model),
        "tool": ("By tool", report.by_tool),
        "project": ("By project", report.by_project),
        "day": ("By day", report.by_day),
    }
    title, buckets = tables.get(group_by, tables["model"])
    if buckets:
        console.print(_bucket_table(title, buckets, ascending=group_by == "day"))

    if report.unknown_models:
        unknown = Table(title="Unpriced models (excluded from totals)", title_style="bold yellow")
        unknown.add_column("Model")
        unknown.add_column("Tokens", justify="right")
        for item in report.unknown_models:
            unknown.add_row(item.model, f"{item.tokens:,}")
        console.print(unknown)
        console.print("[yellow]Add these to rates.json to include them.[/yellow]")

    if verbose and report.warnings:
        for warning in report.warnings:
            console.print(f"[yellow]![/yellow] {warning}")
    elif report.warnings:
        console.print(f"[dim]{len(report.warnings)} warning(s) -- rerun with --verbose[/dim]")


def _headline(report: Report) -> Panel:
    totals = report.totals
    span = "no data"
    if totals.first_event and totals.last_event:
        span = f"{totals.first_event:%Y-%m-%d} to {totals.last_event:%Y-%m-%d}"
    savings = totals.cost.cache_savings
    body = (
        f"[bold green]${totals.cost.total:,.2f}[/bold green] API-equivalent cost\n"
        f"{totals.tokens.total:,} tokens across {totals.events:,} requests "
        f"in {totals.sessions:,} sessions\n"
        f"[dim]{span} · {report.files_scanned:,} log files · "
        f"rates as of {report.rates_as_of or 'unknown'}[/dim]"
    )
    if savings > 0:
        body += (
            f"\n[cyan]Prompt caching saved ${savings:,.2f}[/cyan] "
            f"[dim](would have been ${totals.cost.no_cache_equivalent:,.2f})[/dim]"
        )
    return Panel(body, title="Total", border_style="green")


def _bucket_table(title: str, buckets: list[Bucket], *, ascending: bool) -> Table:
    table = Table(title=title, title_style="bold", header_style="bold")
    table.add_column("")
    table.add_column("Cost", justify="right", style="green")
    for name, _ in TOKEN_COLUMNS:
        table.add_column(name, justify="right")
    table.add_column("Requests", justify="right", style="dim")

    rows = sorted(buckets, key=lambda b: b.key) if ascending else buckets
    for bucket in rows[:30]:
        table.add_row(
            bucket.label,
            f"${bucket.cost.total:,.2f}",
            *[f"{getter(bucket.tokens):,}" for _, getter in TOKEN_COLUMNS],
            f"{bucket.events:,}",
        )
    return table
