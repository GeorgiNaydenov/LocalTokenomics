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


class ClientInfo(BaseModel):
    id: str
    label: str


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

    @app.get("/api/meta", response_model=Meta)
    def meta() -> Meta:
        found = current()
        labels = found.client_labels
        days = [item.event.timestamp.date() for item in found.events]
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
        )

    @app.get("/api/report", response_model=Report)
    def report(
        since: date | None = None,
        until: date | None = None,
        clients: Annotated[list[str] | None, Query()] = None,
        providers: Annotated[list[str] | None, Query()] = None,
        models: Annotated[list[str] | None, Query()] = None,
        projects: Annotated[list[str] | None, Query()] = None,
        include_sidechains: bool = True,
    ) -> Report:
        return report_of(
            current(),
            since=since,
            until=until,
            clients=clients,
            providers=providers,
            models=models,
            projects=projects,
            include_sidechains=include_sidechains,
        )

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
