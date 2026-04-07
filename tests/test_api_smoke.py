from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


def sample_payload():
    return {
        "name": "Teste API",
        "typology": "mista",
        "floors": 6,
        "floor_height": 3.0,
        "terrain_geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [30, 0], [30, 20], [0, 20], [0, 0]]],
                    },
                }
            ],
        },
        "urban": {
            "ca": 2.0,
            "tdc": 0.0,
            "odc": 0.0,
            "setback_front": 3.0,
            "setback_side": 2.0,
            "setback_back": 3.0,
            "max_height": 24.0,
            "altimetry_min": 850.0,
            "altimetry_max": 890.0,
            "occupancy_rate_max": 0.6,
        },
        "scenarios": [{"ca": 1.8}, {"ca": 2.2, "max_height": 30}],
    }


def test_analyze_endpoint_returns_volume_and_compliance():
    with app.test_client() as client:
        response = client.post("/api/analyze", json=sample_payload())

    assert response.status_code == 200
    data = response.get_json()
    assert "volume" in data
    assert "compliance" in data
    assert "scenarios" in data
    assert data["volume"]["terrain_area"] > 0
    assert data["volume"]["floor_height"] == 3.0


def test_export_endpoint_returns_artifacts_list():
    with app.test_client() as client:
        response = client.post("/api/export", json=sample_payload())

    assert response.status_code == 200
    data = response.get_json()
    assert data["report_pdf"].endswith(".pdf")
    assert data["fire_pdf"].endswith(".pdf")
    assert data["dwg"].endswith(".dwg")
    assert data["volume_png"].endswith(".png")
    assert data["chart_png"].endswith(".png")


def test_lot_lookup_autofill_stub():
    with app.test_client() as client:
        response = client.get("/api/lote/LOTE-001")

    assert response.status_code == 200
    data = response.get_json()
    assert data["lot_id"] == "LOTE-001"
    assert "urban" in data
    assert "terrain_geojson" in data
