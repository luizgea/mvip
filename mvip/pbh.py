from __future__ import annotations

from typing import Any


def fetch_pbh_geodata(lat: float, lon: float) -> dict[str, Any]:
    """
    Stub para integração futura com WFS/WMS da PBH.

    Retorna dados de zoneamento/altimetria sintéticos para manter o fluxo funcional.
    """
    zone = "ZA" if lat < -19.8 else "ZAP"
    return {
        "source": "PBH WFS/WMS (stub)",
        "lat": lat,
        "lon": lon,
        "zone": zone,
        "altimetry": {"min": 850.0, "max": 890.0},
    }
