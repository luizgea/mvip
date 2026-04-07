from __future__ import annotations

from typing import Any


_LOTS = {
    "LOTE-001": {
        "zone": "ZA",
        "ca": 2.0,
        "occupancy_rate_max": 0.6,
        "max_height": 27.0,
        "setback_front": 4.0,
        "setback_side": 2.0,
        "setback_back": 3.0,
        "altimetry": {"min": 850.0, "max": 890.0},
        "terrain_geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"lot_id": "LOTE-001"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [42, 0], [42, 28], [0, 28], [0, 0]]],
                    },
                }
            ],
        },
    },
    "LOTE-002": {
        "zone": "ZAP",
        "ca": 1.5,
        "occupancy_rate_max": 0.5,
        "max_height": 21.0,
        "setback_front": 5.0,
        "setback_side": 2.5,
        "setback_back": 4.0,
        "altimetry": {"min": 860.0, "max": 905.0},
        "terrain_geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"lot_id": "LOTE-002"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [35, 0], [35, 25], [0, 25], [0, 0]]],
                    },
                }
            ],
        },
    },
}


def fetch_pbh_geodata(lat: float, lon: float) -> dict[str, Any]:
    zone = "ZA" if lat < -19.8 else "ZAP"
    return {
        "source": "PBH WFS/WMS (stub)",
        "lat": lat,
        "lon": lon,
        "zone": zone,
        "altimetry": {"min": 850.0, "max": 890.0},
    }


def fetch_lot_data(lot_id: str) -> dict[str, Any] | None:
    lot = _LOTS.get(lot_id.strip().upper())
    if not lot:
        return None

    return {
        "source": "PBH cadastro de lote (stub)",
        "lot_id": lot_id.strip().upper(),
        "zone": lot["zone"],
        "urban": {
            "ca": lot["ca"],
            "tdc": 0.0,
            "odc": 0.0,
            "setback_front": lot["setback_front"],
            "setback_side": lot["setback_side"],
            "setback_back": lot["setback_back"],
            "max_height": lot["max_height"],
            "altimetry_min": lot["altimetry"]["min"],
            "altimetry_max": lot["altimetry"]["max"],
            "occupancy_rate_max": lot["occupancy_rate_max"],
        },
        "terrain_geojson": lot["terrain_geojson"],
    }
