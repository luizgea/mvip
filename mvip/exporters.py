from __future__ import annotations

from pathlib import Path

import ezdxf
import matplotlib.pyplot as plt


def export_dwg(volume: dict, output_file: Path) -> Path:
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    side = volume["max_floor_area"] ** 0.5 if volume["max_floor_area"] > 0 else 1
    points = [(0, 0), (side, 0), (side, side), (0, side), (0, 0)]
    msp.add_lwpolyline(points)
    doc.saveas(output_file)
    return output_file


def export_volume_png(volume: dict, output_file: Path) -> Path:
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection="3d")

    steps = volume.get("steps") or [{"floor": 1, "area": 1, "height": 3}]
    x, y = 0, 0
    for s in steps:
        side = max(s["area"], 1) ** 0.5
        z = s["height"] - 3
        ax.bar3d(x, y, z, side, side, 3, shade=True, alpha=0.7)

    ax.set_title("Massa 3D simplificada")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    fig.tight_layout()
    fig.savefig(output_file)
    plt.close(fig)
    return output_file
