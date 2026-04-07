from __future__ import annotations

from dataclasses import asdict

from shapely.geometry import shape

from mvip.models import ProjectInput


def _buildable_polygon(poly, front: float, side: float, back: float):
    # Simplificação: usa o maior recuo como buffer uniforme para manter cálculo estável.
    inset = max(front, side, back)
    result = poly.buffer(-inset)
    if result.is_empty:
        return None
    return result


def generate_volume(project: ProjectInput) -> dict:
    terrain = shape(project.terrain_geojson["features"][0]["geometry"])
    terrain_area = float(terrain.area)

    buildable = _buildable_polygon(
        terrain,
        project.urban.setback_front,
        project.urban.setback_side,
        project.urban.setback_back,
    )

    if not buildable:
        return {
            "terrain_area": terrain_area,
            "buildable_area": 0.0,
            "max_floor_area": 0.0,
            "gross_area": 0.0,
            "used_height": 0.0,
            "steps": [],
            "urban": asdict(project.urban),
        }

    buildable_area = float(buildable.area)
    ca_limit = terrain_area * project.urban.ca
    floor_area_by_ca = ca_limit / max(project.floors, 1)
    occupancy_limit = terrain_area * project.urban.occupancy_rate_max
    max_floor_area = min(buildable_area, floor_area_by_ca, occupancy_limit)

    floor_height = 3.0
    used_height = min(project.floors * floor_height, project.urban.max_height)
    total_possible_floors = int(project.urban.max_height // floor_height)
    effective_floors = min(project.floors, max(total_possible_floors, 1))
    gross_area = max_floor_area * effective_floors

    steps = []
    current = buildable
    for i in range(effective_floors):
        if i > 0 and i % 6 == 0:
            current = current.buffer(-1.5)
        if current.is_empty:
            break
        steps.append(
            {
                "floor": i + 1,
                "area": float(current.area),
                "height": (i + 1) * floor_height,
            }
        )

    return {
        "terrain_area": terrain_area,
        "buildable_area": buildable_area,
        "max_floor_area": max_floor_area,
        "gross_area": gross_area,
        "used_height": used_height,
        "effective_floors": effective_floors,
        "steps": steps,
        "urban": asdict(project.urban),
    }


def simulate_scenarios(project: ProjectInput) -> list[dict]:
    scenarios = []
    base = generate_volume(project)
    scenarios.append({"name": "Base", **base})

    for idx, scenario in enumerate(project.scenarios, start=1):
        original_ca = project.urban.ca
        original_h = project.urban.max_height
        original_rear = project.urban.setback_back

        project.urban.ca = scenario.get("ca", original_ca)
        project.urban.max_height = scenario.get("max_height", original_h)
        project.urban.setback_back = scenario.get("setback_back", original_rear)

        result = generate_volume(project)
        scenarios.append({"name": f"Cenário {idx}", **result})

        project.urban.ca = original_ca
        project.urban.max_height = original_h
        project.urban.setback_back = original_rear

    return scenarios
