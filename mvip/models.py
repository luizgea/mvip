from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class UrbanParams:
    ca: float
    tdc: float
    odc: float
    setback_front: float
    setback_side: float
    setback_back: float
    max_height: float
    altimetry_min: float
    altimetry_max: float
    occupancy_rate_max: float


@dataclass
class ProjectInput:
    name: str
    typology: str
    floors: int
    floor_height: float
    terrain_geojson: dict[str, Any]
    urban: UrbanParams
    scenarios: list[dict[str, float]] = field(default_factory=list)
