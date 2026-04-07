from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

from config import OUTPUT_DIR
from mvip.compliance import check_compliance
from mvip.exporters import export_dwg, export_volume_png
from mvip.geometry import generate_volume, simulate_scenarios
from mvip.models import ProjectInput, UrbanParams
from mvip.pbh import fetch_pbh_geodata
from mvip.report import build_fire_pdf, build_report_pdf, create_comparison_chart
from mvip.storage import (
    create_project,
    delete_project,
    get_project,
    init_db,
    list_projects,
    update_project,
)

app = Flask(__name__)
init_db()


def _project_from_payload(payload: dict) -> ProjectInput:
    urban = UrbanParams(**payload["urban"])
    return ProjectInput(
        name=payload["name"],
        typology=payload["typology"],
        floors=int(payload["floors"]),
        terrain_geojson=payload["terrain_geojson"],
        urban=urban,
        scenarios=payload.get("scenarios", []),
    )


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(force=True)
    project = _project_from_payload(payload)

    base_volume = generate_volume(project)
    scenarios = simulate_scenarios(project)
    compliance = check_compliance(base_volume)

    return jsonify({"volume": base_volume, "scenarios": scenarios, "compliance": compliance})


@app.post("/api/pbh")
def pbh_data():
    payload = request.get_json(force=True)
    lat = float(payload.get("lat", -19.92))
    lon = float(payload.get("lon", -43.94))
    return jsonify(fetch_pbh_geodata(lat, lon))


@app.post("/api/projects")
def save_project():
    payload = request.get_json(force=True)
    project_id = create_project(payload["name"], payload)
    return jsonify({"id": project_id})


@app.get("/api/projects")
def projects():
    return jsonify(list_projects())


@app.get("/api/projects/<int:project_id>")
def project(project_id: int):
    data = get_project(project_id)
    if not data:
        return jsonify({"error": "not found"}), 404
    return jsonify(data)


@app.put("/api/projects/<int:project_id>")
def project_update(project_id: int):
    payload = request.get_json(force=True)
    updated = update_project(project_id, payload["name"], payload)
    return jsonify({"updated": updated})


@app.delete("/api/projects/<int:project_id>")
def project_delete(project_id: int):
    deleted = delete_project(project_id)
    return jsonify({"deleted": deleted})


@app.post("/api/export")
def export_all():
    payload = request.get_json(force=True)
    project = _project_from_payload(payload)

    volume = generate_volume(project)
    scenarios = simulate_scenarios(project)
    compliance = check_compliance(volume)

    stem = payload["name"].replace(" ", "_").lower()
    chart = create_comparison_chart(scenarios, OUTPUT_DIR / f"{stem}_chart.png")
    vol_png = export_volume_png(volume, OUTPUT_DIR / f"{stem}_volume.png")
    dwg = export_dwg(volume, OUTPUT_DIR / f"{stem}_implantacao.dwg")

    report_pdf = build_report_pdf(
        OUTPUT_DIR / f"{stem}_relatorio.pdf",
        project_name=payload["name"],
        input_params={
            "Tipologia": payload["typology"],
            "Pavimentos": payload["floors"],
            "CA": payload["urban"]["ca"],
            "Altura máx": payload["urban"]["max_height"],
        },
        compliance=compliance,
        chart_path=chart,
        volume_png=vol_png,
    )
    fire_pdf = build_fire_pdf(OUTPUT_DIR / f"{stem}_incendio.pdf", payload["name"], compliance["fire_checklist"])

    return jsonify(
        {
            "report_pdf": str(report_pdf.name),
            "fire_pdf": str(fire_pdf.name),
            "chart_png": str(chart.name),
            "volume_png": str(vol_png.name),
            "dwg": str(dwg.name),
        }
    )


@app.get("/api/download/<path:filename>")
def download(filename: str):
    target = Path(OUTPUT_DIR) / filename
    if not target.exists():
        return jsonify({"error": "file not found"}), 404
    return send_file(target, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
