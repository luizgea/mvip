from __future__ import annotations


def check_compliance(volume: dict) -> dict:
    terrain = volume["terrain_area"]
    max_floor = volume["max_floor_area"]
    gross = volume["gross_area"]
    urban = volume["urban"]

    ca_calc = gross / terrain if terrain else 0
    to_calc = max_floor / terrain if terrain else 0

    items = {
        "ca": {
            "value": round(ca_calc, 3),
            "limit": urban["ca"],
            "ok": ca_calc <= urban["ca"] + 1e-9,
        },
        "to": {
            "value": round(to_calc, 3),
            "limit": urban["occupancy_rate_max"],
            "ok": to_calc <= urban["occupancy_rate_max"] + 1e-9,
        },
        "altura": {
            "value": volume["used_height"],
            "limit": urban["max_height"],
            "ok": volume["used_height"] <= urban["max_height"] + 1e-9,
        },
        "recuos": {
            "value": min(
                urban["setback_front"],
                urban["setback_side"],
                urban["setback_back"],
            ),
            "limit": 1.5,
            "ok": all(
                x >= 1.5
                for x in (
                    urban["setback_front"],
                    urban["setback_side"],
                    urban["setback_back"],
                )
            ),
        },
    }

    fire = _fire_checklist(volume)
    ok = all(v["ok"] for v in items.values()) and all(i["ok"] for i in fire)
    return {"overall_ok": ok, "urban_checks": items, "fire_checklist": fire}


def _fire_checklist(volume: dict) -> list[dict]:
    floors = volume.get("effective_floors", 1)
    height = volume.get("used_height", 0)

    return [
        {
            "item": "Necessidade de escada enclausurada",
            "ok": height <= 12 or floors <= 4,
            "note": "Obrigatória em edifícios mais altos.",
        },
        {
            "item": "Duas saídas independentes",
            "ok": floors <= 3,
            "note": "Duas saídas para ocupações verticais com maior carga.",
        },
        {
            "item": "Posições de hidrantes e extintores",
            "ok": True,
            "note": "Definir pontos por pavimento no projeto executivo.",
        },
        {
            "item": "Rota acessível e iluminada",
            "ok": True,
            "note": "Garantir acessibilidade e iluminação de emergência.",
        },
        {
            "item": "Pressurização de escada ou ventilação forçada",
            "ok": height < 30,
            "note": "Acima de limiar exige solução dedicada.",
        },
    ]
