"""Local JSON API + static host for the dashboard.

Everything is parsed and priced once at startup and held in memory; the endpoints only
filter and re-aggregate, so the UI stays responsive. ``POST /api/refresh`` re-reads the
logs. Nothing leaves the machine -- the server binds to localhost by default.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .aggregate import Report
from .pipeline import Analysis, analyze, report_of
from .pricing import RateTable

WEB_DIST = Path(__file__).parent / "web" / "dist"


class ToolInfo(BaseModel):
    id: str
    label: str


class Meta(BaseModel):
    tools: list[ToolInfo] = Field(default_factory=list)
    models: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    first_day: date | None = None
    last_day: date | None = None
    rates_as_of: str = ""
    files_scanned: int = 0
    events: int = 0
    warnings: list[str] = Field(default_factory=list)


def create_app(
    analysis: Analysis | None = None,
    rates_path: Path | None = None,
    roots: dict[str, list[Path]] | None = None,
) -> FastAPI:
    """``roots`` must match what ``analysis`` was built from, so that a refresh
    re-reads the same logs rather than falling back to the default locations."""
    state: dict[str, Analysis] = {
        "analysis": analysis or analyze(roots=roots, rates_path=rates_path)
    }
    app = FastAPI(title="ai-usage-cost", version="0.1.0", docs_url="/api/docs")

    def current() -> Analysis:
        return state["analysis"]

    @app.get("/api/meta", response_model=Meta)
    def meta() -> Meta:
        found = current()
        labels = found.tool_labels
        days = [item.event.timestamp.date() for item in found.priced]
        return Meta(
            tools=[
                ToolInfo(id=tool, label=labels.get(tool, tool))
                for tool in sorted({item.event.tool for item in found.priced})
            ],
            models=sorted({item.event.model for item in found.priced}),
            projects=sorted({item.event.project for item in found.priced if item.event.project}),
            first_day=min(days) if days else None,
            last_day=max(days) if days else None,
            rates_as_of=found.pricer.table.as_of,
            files_scanned=found.files,
            events=len(found.priced),
            warnings=found.warnings,
        )

    @app.get("/api/report", response_model=Report)
    def report(
        since: date | None = None,
        until: date | None = None,
        tools: Annotated[list[str] | None, Query()] = None,
        models: Annotated[list[str] | None, Query()] = None,
        projects: Annotated[list[str] | None, Query()] = None,
        include_sidechains: bool = True,
    ) -> Report:
        return report_of(
            current(),
            since=since,
            until=until,
            tools=tools,
            models=models,
            projects=projects,
            include_sidechains=include_sidechains,
        )

    @app.get("/api/rates", response_model=RateTable)
    def rates() -> RateTable:
        return current().pricer.table

    @app.post("/api/refresh", response_model=Meta)
    def refresh() -> Meta:
        state["analysis"] = analyze(roots=roots, rates_path=rates_path)
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
