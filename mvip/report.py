from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_comparison_chart(scenarios: list[dict], output_file: Path) -> Path:
    names = [s["name"] for s in scenarios]
    built = [s["gross_area"] for s in scenarios]
    terrain = [s["terrain_area"] for s in scenarios]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(names, built, label="Área construída")
    ax.plot(names, terrain, color="orange", marker="o", label="Área do terreno")
    ax.set_title("Comparativo de cenários")
    ax.set_ylabel("m²")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_file)
    plt.close(fig)
    return output_file


def build_report_pdf(
    path: Path,
    project_name: str,
    input_params: dict,
    compliance: dict,
    chart_path: Path,
    volume_png: Path,
) -> Path:
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "MViP — Relatório de Viabilidade")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Projeto: {project_name}")
    c.drawString(50, height - 100, "Sumário executivo")
    c.drawString(50, height - 120, "Análise paramétrica automatizada com verificação de conformidade.")

    y = height - 160
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Parâmetros de entrada")
    y -= 20
    c.setFont("Helvetica", 10)
    for k, v in input_params.items():
        c.drawString(55, y, f"- {k}: {v}")
        y -= 14

    y -= 10
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Conformidade")
    y -= 20
    c.setFont("Helvetica", 10)
    for k, v in compliance["urban_checks"].items():
        c.drawString(55, y, f"- {k}: {v['value']} / limite {v['limit']} -> {'OK' if v['ok'] else 'NÃO OK'}")
        y -= 14

    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Gráficos volumétricos")
    c.drawImage(str(chart_path), 50, height - 350, width=500, height=250, preserveAspectRatio=True)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 390, "Imagem 3D")
    c.drawImage(str(volume_png), 50, 100, width=500, height=250, preserveAspectRatio=True)

    c.save()
    return path


def build_fire_pdf(path: Path, project_name: str, checklist: list[dict]) -> Path:
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Checklist de Segurança — IT 08 (CBMMG)")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 75, f"Projeto: {project_name}")

    y = height - 120
    for item in checklist:
        line = f"[{'X' if item['ok'] else ' '}] {item['item']} — {item['note']}"
        c.drawString(50, y, line[:110])
        y -= 22
        if y < 80:
            c.showPage()
            y = height - 70

    c.save()
    return path
