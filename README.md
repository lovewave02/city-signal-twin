# City Signal Twin

A mini digital twin that fuses transit delay, PM2.5, and weather discomfort to estimate commuter stress hotspots.

## MVP implemented
- FastAPI backend with synthetic city-signal generator
- Stress model and discomfort index functions
- APIs:
  - `GET /signals`
  - `GET /stress/hotspots?limit=5`
  - `GET /stress/trend?hours=12`
  - `GET /health`
- Browser dashboard with MapLibre markers + hotspot list + 12h trend bars

## Quick start
```bash
pip install -r requirements.txt
uvicorn src.api:app --reload
```
Open `http://127.0.0.1:8000`.

## Tests
```bash
pytest -q
```

## Structure
- `src/model.py`: stress/discomfort formulas
- `src/simulator.py`: city signal and trend generators
- `src/api.py`: API and static web serving
- `src/web/`: map dashboard files
- `tests/`: model/API tests

## Next roadmap
1. Replace synthetic data with real APIs (weather, AQ, transit)
2. Calibrate score weights by historical commute data
3. Add district-level time slider and anomaly alerts
