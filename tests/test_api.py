from fastapi.testclient import TestClient

from src.api import app


def test_health():
    client = TestClient(app)
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_signals_and_hotspots_shape():
    client = TestClient(app)

    signals = client.get('/signals')
    assert signals.status_code == 200
    body = signals.json()
    assert len(body['areas']) >= 5
    assert 'stress_index' in body['areas'][0]

    hotspots = client.get('/stress/hotspots?limit=3')
    assert hotspots.status_code == 200
    hs = hotspots.json()['hotspots']
    assert len(hs) == 3
    assert hs[0]['stress_index'] >= hs[1]['stress_index']


def test_trend_points():
    client = TestClient(app)
    r = client.get('/stress/trend?hours=6')
    assert r.status_code == 200
    points = r.json()['points']
    assert len(points) == 6
    assert 'avg_stress_index' in points[0]
