"""Static PNG export via matplotlib -- for pasting a summary somewhere.

Optional dependency: install with ``pip install "ai-usage-cost[png]"``.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

from ..aggregate import Report  # noqa: E402

PALETTE = ["#6366f1", "#22c55e", "#f59e0b", "#ec4899", "#06b6d4", "#a78bfa", "#ef4444"]


def write_png(report: Report, out: Path, dpi: int = 140) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(
        f"API-equivalent cost  ${report.totals.cost.total:,.2f}   ·   "
        f"{report.totals.tokens.total:,} tokens   ·   {report.totals.events:,} requests",
        fontsize=14,
        fontweight="bold",
    )
    _cost_over_time(axes[0][0], report)
    _cost_by_model(axes[0][1], report)
    _token_mix(axes[1][0], report)
    _cost_by_project(axes[1][1], report)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


def _cost_over_time(ax: plt.Axes, report: Report) -> None:
    per_tool: dict[str, dict[date, float]] = defaultdict(lambda: defaultdict(float))
    for point in report.series:
        per_tool[point.tool][point.day] += point.cost
    days = sorted({point.day for point in report.series})
    bottom = [0.0] * len(days)
    for index, (tool, values) in enumerate(sorted(per_tool.items())):
        heights = [values.get(day, 0.0) for day in days]
        ax.bar(
            days,  # type: ignore[arg-type]  # stubs omit the date x-value overload
            heights,
            bottom=bottom,
            label=tool,
            color=PALETTE[index % len(PALETTE)],
        )
        bottom = [b + h for b, h in zip(bottom, heights, strict=True)]
    ax.set_title("Cost per day")
    ax.set_ylabel("USD")
    ax.legend(fontsize=8)
    ax.tick_params(axis="x", rotation=45, labelsize=7)


def _cost_by_model(ax: plt.Axes, report: Report) -> None:
    buckets = report.by_model[:10][::-1]
    ax.barh(
        [b.label for b in buckets],
        [b.cost.total for b in buckets],
        color=[PALETTE[i % len(PALETTE)] for i in range(len(buckets))],
    )
    ax.set_title("Cost by model")
    ax.set_xlabel("USD")
    ax.tick_params(labelsize=8)


def _token_mix(ax: plt.Axes, report: Report) -> None:
    buckets = report.by_model[:8][::-1]
    labels = [b.label for b in buckets]
    parts = [
        ("uncached input", [b.tokens.uncached_input for b in buckets]),
        ("cache read", [b.tokens.cache_read for b in buckets]),
        ("cache write", [b.tokens.cache_write for b in buckets]),
        ("output", [b.tokens.output for b in buckets]),
    ]
    left = [0.0] * len(buckets)
    for index, (name, values) in enumerate(parts):
        ax.barh(labels, values, left=left, label=name, color=PALETTE[index % len(PALETTE)])
        left = [a + b for a, b in zip(left, values, strict=True)]
    ax.set_title("Token mix")
    ax.set_xlabel("tokens")
    ax.legend(fontsize=8)
    ax.tick_params(labelsize=8)


def _cost_by_project(ax: plt.Axes, report: Report) -> None:
    buckets = report.by_project[:10][::-1]
    if not buckets:
        ax.set_axis_off()
        return
    ax.barh(
        [b.label for b in buckets],
        [b.cost.total for b in buckets],
        color=[PALETTE[i % len(PALETTE)] for i in range(len(buckets))],
    )
    ax.set_title("Cost by project")
    ax.set_xlabel("USD")
    ax.tick_params(labelsize=8)
