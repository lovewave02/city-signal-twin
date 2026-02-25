from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .simulator import make_city_signals, make_hourly_trend

app = FastAPI(title="City Signal Twin API", version="0.1.0")

WEB_DIR = Path(__file__).resolve().parent / "web"
app.mount("/web", StaticFiles(directory=str(WEB_DIR)), name="web")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/signals")
def get_signals() -> dict:
    return make_city_signals()


@app.get("/stress/hotspots")
def hotspots(limit: int = 3) -> dict:
    areas = make_city_signals()["areas"]
    ordered = sorted(areas, key=lambda x: x["stress_index"], reverse=True)
    return {"hotspots": ordered[: max(1, min(limit, 10))]}


@app.get("/stress/trend")
def trend(hours: int = 12) -> dict:
    capped = max(3, min(hours, 72))
    return {"points": make_hourly_trend(hours=capped)}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")
