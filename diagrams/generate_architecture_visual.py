#!/usr/bin/env python3
"""Generate TEE + hybrid QAI edge system architecture with icon images."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ICON_DIR = ROOT / "icons"
OUT_PNG = ROOT / "tee_qai_edge_architecture_visual.png"
OUT_PDF = ROOT / "tee_qai_edge_architecture_visual.pdf"
OUT_SVG = ROOT / "tee_qai_edge_architecture_visual.svg"
OUT_TEX = ROOT / "tee_qai_edge_architecture_visual.tex"

FIG_W = 18.0  # cm — matches matplotlib figsize width
FIG_H = 11.0  # cm — matches matplotlib figsize height

TITLE = "Trustworthy Hybrid Quantum–Classical AI for Secure IoT Edge Systems"
SUBTITLE = (
    "System Architecture — TEE-protected deployment, trusted inference, "
    "and hybrid anomaly detection"
)

ZONES = [
    {"xy": (0.03, 0.82), "w": 0.94, "h": 0.11, "fill": "#FFE0B2", "title": "Development & Training (offline)"},
    {"xy": (0.03, 0.69), "w": 0.94, "h": 0.10, "fill": "#C8E6C9", "title": "IoT Layer"},
    {"xy": (0.03, 0.57), "w": 0.94, "h": 0.10, "fill": "#ECEFF1", "title": "Edge Data Path"},
    {"xy": (0.03, 0.41), "w": 0.44, "h": 0.13, "fill": "#FFCDD2", "title": "REE — Linux OS (untrusted)"},
    {"xy": (0.50, 0.36), "w": 0.47, "h": 0.18, "fill": "#BBDEFB", "title": "TEE — OP-TEE / ARM TrustZone (protected)"},
    {"xy": (0.03, 0.16), "w": 0.94, "h": 0.12, "fill": "#B3E5FC", "title": "Cloud Management & Monitoring"},
]

DEV_ITEMS = [
    (0.08, "database", "Datasets"),
    (0.22, "pytorch", "PyTorch"),
    (0.36, "qiskit", "Qiskit"),
    (0.50, "pennylane", "PennyLane"),
    (0.64, "compress", "Compress"),
    (0.78, "lock", "Sign & Encrypt"),
]
DEV_Y = 0.865

IOT_ITEMS = [
    (0.14, "sensor", "Sensors"),
    (0.32, "iot", "Actuators"),
    (0.50, "sensor", "ESP32 nodes"),
    (0.72, "iot", "Field Gateway"),
]
IOT_Y = 0.735

DATA_ITEMS = [
    (0.22, "collect", "Data Collection"),
    (0.46, "feature", "Feature Extraction (REE)"),
    (0.70, "bench", "Benchmark Harness"),
]
DATA_Y = 0.615

REE_ITEMS = [
    (0.10, "linux", "Linux"),
    (0.22, "network", "Network"),
    (0.34, "management", "Mgmt Agent"),
    (0.46, "tee_api", "TEE Client API"),
]
REE_Y = 0.465

TEE_ITEMS = [
    (0.56, 0.505, "key", "Secure Keys"),
    (0.68, 0.505, "model", "Model Store"),
    (0.80, 0.505, "inference", "Inference TA"),
    (0.92, 0.505, "hybrid", "Hybrid Q-C Engine"),
    (0.62, 0.405, "attest", "Remote Attestation"),
    (0.78, 0.405, "decision", "Security Decision"),
    (0.90, 0.405, "fpga", "ARM / FPGA Runtime"),
]

ARROWS = [
    # (x1, y1, x2, y2, color, style, label)
    (0.50, 0.69, 0.50, 0.635, "#37474F", "-", "telemetry"),
    (0.27, DATA_Y, 0.41, DATA_Y, "#37474F", "-", "streams"),
    (0.51, DATA_Y, 0.65, DATA_Y, "#37474F", "-", "features"),
    (0.46, REE_Y, 0.56, 0.505, "#1565C0", "-", "invoke TA"),
    (0.65, 0.57, 0.80, 0.535, "#37474F", "-", "features"),
    (0.78, 0.82, 0.68, 0.535, "#E65100", "--", "deploy model"),
    (0.61, 0.505, 0.63, 0.505, "#1565C0", "-", None),
    (0.73, 0.505, 0.75, 0.505, "#1565C0", "-", None),
    (0.85, 0.505, 0.87, 0.505, "#1565C0", "-", None),
    (0.92, 0.485, 0.78, 0.425, "#1565C0", "-", None),
    (0.68, 0.485, 0.62, 0.425, "#1565C0", "-", None),
    (0.78, 0.36, 0.14, 0.28, "#1565C0", "--", "attestation quote"),
    (0.78, 0.36, 0.80, 0.28, "#37474F", "-", "alerts"),
]

NOTES = [
    (0.03, 0.03, "#FFEBEE", "Threats mitigated:\nmodel tampering · replacement · extraction · unauthorized inference · compromised REE"),
    (0.27, 0.03, "#E3F2FD", "TEE protects:\nmodel storage · inference · keys · decision logic"),
    (0.51, 0.03, "#FFF8E1", "QAI role:\nanomaly engine inside TEE (not a security primitive)"),
    (0.73, 0.03, "#E8F5E9", "RQ:\nHybrid Q-C vs TinyML for unseen attacks under deployability & TEE constraints"),
]

SIZE = 128


def _font(size: int = 28):
    for name in ("DejaVuSans-Bold.ttf", "Arial Bold.ttf", "Helvetica.ttc"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def save_icon(name: str, draw_fn) -> Path:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    path = ICON_DIR / f"{name}.png"
    if path.exists():
        return path
    img = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw_fn(draw, SIZE)
    img.save(path)
    return path


def icon_iot(d, s):
    d.ellipse([8, 28, 44, 64], fill="#43A047")
    d.ellipse([52, 28, 88, 64], fill="#66BB6A")
    d.rectangle([38, 52, 58, 92], fill="#2E7D32")
    d.text((s // 2 - 8, s - 28), "IoT", fill="white", font=_font(18))


def icon_sensor(d, s):
    d.ellipse([20, 20, 108, 108], fill="#81C784", outline="#2E7D32", width=3)
    pts = []
    for x in range(30, 98, 4):
        y = 64 + 22 * math.sin((x - 30) / 10)
        pts.append((x, y))
    d.line(pts, fill="#1B5E20", width=4)


def icon_database(d, s):
    d.ellipse([24, 18, 104, 46], fill="#546E7A", outline="#37474F", width=2)
    d.rectangle([24, 32, 104, 88], fill="#78909C")
    d.ellipse([24, 72, 104, 100], fill="#546E7A", outline="#37474F", width=2)


def icon_pytorch(d, s):
    d.ellipse([16, 16, 112, 112], fill="#EE4C2C")
    d.polygon([(64, 28), (92, 78), (36, 78)], fill="#FFE0B2")
    d.text((44, 82), "PT", fill="white", font=_font(22))


def icon_qiskit(d, s):
    d.rounded_rectangle([12, 12, 116, 116], radius=18, fill="#6929C4")
    d.text((38, 38), "Q", fill="white", font=_font(46))


def icon_pennylane(d, s):
    d.rounded_rectangle([12, 12, 116, 116], radius=18, fill="#019848")
    d.text((24, 40), "PL", fill="white", font=_font(34))


def icon_compress(d, s):
    d.rounded_rectangle([18, 30, 110, 98], fill="#FFB74D", outline="#F57C00", width=3)
    d.text((34, 46), "ZIP", fill="#E65100", font=_font(24))


def icon_lock(d, s):
    d.rounded_rectangle([34, 52, 94, 108], fill="#FFC107", outline="#FF8F00", width=3)
    d.arc([38, 18, 90, 70], 180, 0, fill="#FF8F00", width=8)


def icon_linux(d, s):
    d.ellipse([20, 20, 108, 108], fill="#FBC02D")
    d.ellipse([42, 48, 58, 64], fill="#212121")
    d.ellipse([70, 48, 86, 64], fill="#212121")
    d.arc([48, 70, 80, 92], 10, 170, fill="#212121", width=3)


def icon_network(d, s):
    d.ellipse([56, 18, 72, 34], fill="#1976D2")
    for xy in [(24, 88), (104, 88), (64, 104)]:
        d.ellipse([xy[0] - 8, xy[1] - 8, xy[0] + 8, xy[1] + 8], fill="#42A5F5")
        d.line([(64, 26), xy], fill="#1565C0", width=3)


def icon_management(d, s):
    d.rounded_rectangle([20, 24, 108, 104], fill="#EF5350")
    d.line([(34, 44), (94, 44), (94, 88), (34, 88), (34, 44)], fill="white", width=3)
    d.line([(44, 58), (84, 58), (84, 74), (44, 74), (44, 58)], fill="#FFCDD2", width=0)


def icon_tee_api(d, s):
    d.rounded_rectangle([16, 36, 112, 92], fill="#FF7043")
    d.text((28, 48), "API", fill="white", font=_font(26))


def icon_key(d, s):
    d.ellipse([28, 24, 68, 64], fill="#FFD54F", outline="#F9A825", width=3)
    d.rectangle([60, 52, 104, 64], fill="#F9A825")
    d.rectangle([88, 64, 98, 92], fill="#F9A825")


def icon_model(d, s):
    d.rounded_rectangle([18, 22, 110, 106], fill="#5C6BC0")
    d.text((28, 40), "AI", fill="white", font=_font(34))


def icon_inference(d, s):
    d.polygon([(64, 18), (108, 96), (20, 96)], fill="#3949AB")
    d.text((46, 58), "TA", fill="white", font=_font(24))


def icon_hybrid(d, s):
    d.ellipse([16, 40, 56, 96], fill="#7E57C2")
    d.ellipse([72, 40, 112, 96], fill="#26A69A")
    d.text((48, 46), "+", fill="white", font=_font(30))


def icon_attest(d, s):
    d.polygon([(64, 16), (108, 40), (108, 88), (64, 112), (20, 88), (20, 40)], fill="#00838F")
    d.text((42, 48), "RA", fill="white", font=_font(24))


def icon_decision(d, s):
    d.rounded_rectangle([16, 28, 112, 100], fill="#00897B")
    d.text((22, 44), "SEC", fill="white", font=_font(28))


def icon_fpga(d, s):
    d.rounded_rectangle([22, 22, 106, 106], fill="#455A64")
    for i in range(5):
        d.rectangle([22, 30 + i * 16, 34, 38 + i * 16], fill="#90A4AE")
        d.rectangle([94, 30 + i * 16, 106, 38 + i * 16], fill="#90A4AE")
    d.text((42, 48), "SoC", fill="white", font=_font(22))


def icon_cloud(d, s):
    d.ellipse([16, 48, 56, 88], fill="#29B6F6")
    d.ellipse([40, 36, 88, 84], fill="#4FC3F7")
    d.ellipse([72, 48, 112, 88], fill="#29B6F6")


def icon_verify(d, s):
    d.polygon([(64, 18), (108, 40), (108, 88), (64, 112), (20, 88), (20, 40)], fill="#0288D1")
    d.line([(38, 64), (56, 82), (92, 46)], fill="white", width=6)


def icon_fleet(d, s):
    d.rounded_rectangle([18, 34, 52, 94], fill="#039BE5")
    d.rounded_rectangle([48, 34, 82, 94], fill="#039BE5")
    d.rounded_rectangle([78, 34, 112, 94], fill="#039BE5")


def icon_policy(d, s):
    d.rounded_rectangle([28, 18, 100, 110], fill="#0277BD")
    d.line([(40, 38), (88, 38), (88, 92), (40, 92), (40, 38)], fill="white", width=2)
    d.line([(48, 52), (80, 52), (80, 80), (48, 80), (48, 52)], fill="#B3E5FC", width=0)


def icon_monitor(d, s):
    d.rounded_rectangle([18, 24, 110, 88], fill="#01579B")
    d.line([(30, 72), (48, 52), (64, 62), (88, 38)], fill="#81D4FA", width=4)
    d.rectangle([44, 92, 84, 104], fill="#0277BD")


def icon_collect(d, s):
    d.rounded_rectangle([20, 30, 108, 98], fill="#A5D6A7", outline="#388E3C", width=3)
    d.polygon([(64, 42), (88, 78), (40, 78)], fill="#2E7D32")


def icon_feature(d, s):
    d.rounded_rectangle([20, 24, 108, 104], fill="#FFCDD2", outline="#C62828", width=3)
    d.text((30, 42), "fx", fill="#B71C1C", font=_font(30))


def icon_bench(d, s):
    d.rounded_rectangle([20, 28, 108, 100], fill="#E1BEE7", outline="#6A1B9A", width=3)
    d.text((24, 44), "bench", fill="#4A148C", font=_font(20))


ICON_BUILDERS = {
    "iot": icon_iot,
    "sensor": icon_sensor,
    "database": icon_database,
    "pytorch": icon_pytorch,
    "qiskit": icon_qiskit,
    "pennylane": icon_pennylane,
    "compress": icon_compress,
    "lock": icon_lock,
    "linux": icon_linux,
    "network": icon_network,
    "management": icon_management,
    "tee_api": icon_tee_api,
    "key": icon_key,
    "model": icon_model,
    "inference": icon_inference,
    "hybrid": icon_hybrid,
    "attest": icon_attest,
    "decision": icon_decision,
    "fpga": icon_fpga,
    "cloud": icon_cloud,
    "verify": icon_verify,
    "fleet": icon_fleet,
    "policy": icon_policy,
    "monitor": icon_monitor,
    "collect": icon_collect,
    "feature": icon_feature,
    "bench": icon_bench,
}


def ensure_icons() -> dict[str, Path]:
    return {name: save_icon(name, fn) for name, fn in ICON_BUILDERS.items()}


def load_image(path: Path, zoom: float = 0.28) -> OffsetImage:
    arr = np.asarray(Image.open(path).convert("RGBA"))
    return OffsetImage(arr, zoom=zoom)


def place_icon(ax, xy, icon_path: Path, label: str, zoom=0.28, label_y=-0.02):
    img = load_image(icon_path, zoom)
    ab = AnnotationBbox(img, xy, frameon=False, box_alignment=(0.5, 0.5), zorder=5)
    ax.add_artist(ab)
    ax.text(xy[0], xy[1] + label_y, label, ha="center", va="top", fontsize=8.5, fontweight="bold", zorder=6)


def draw_zone(ax, xy, w, h, color, title, alpha=0.35):
    rect = mpatches.FancyBboxPatch(
        xy, w, h, boxstyle="round,pad=0.012,rounding_size=0.015",
        linewidth=1.2, edgecolor="#455A64", facecolor=color, alpha=alpha, zorder=1,
    )
    ax.add_patch(rect)
    ax.text(xy[0] + 0.012, xy[1] + h - 0.018, title, fontsize=11, fontweight="bold", va="top", zorder=2)


def arrow(ax, p1, p2, color="#37474F", style="-", lw=1.8, text=None, text_pos=0.5):
    ax.annotate(
        "", xy=p2, xytext=p1,
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=style, shrinkA=4, shrinkB=4),
        zorder=3,
    )
    if text:
        mx = p1[0] + (p2[0] - p1[0]) * text_pos
        my = p1[1] + (p2[1] - p1[1]) * text_pos
        ax.text(mx, my + 0.012, text, ha="center", va="bottom", fontsize=7.5, color=color, zorder=4)


def tex_escape(text: str) -> str:
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = text
    for old, new in repl.items():
        out = out.replace(old, new)
    return out


def export_tikz(icons: dict[str, Path], out_path: Path = OUT_TEX) -> Path:
    """Write a standalone LaTeX file with a tikzpicture using icon images."""
    _ = icons  # icons must exist on disk under icons/

    lines: list[str] = [
        "% Auto-generated by generate_architecture_visual.py --tex",
        "% Compile: pdflatex tee_qai_edge_architecture_visual.tex",
        r"\documentclass[tikz,border=10pt]{standalone}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{xcolor}",
        r"\usepackage{graphicx}",
        r"\usepackage{tikz}",
        r"\usetikzlibrary{arrows.meta,calc,positioning}",
        "",
    ]
    for i, zone in enumerate(ZONES):
        html = zone["fill"].lstrip("#")
        lines.append(rf"\definecolor{{zonefill{i}}}{{HTML}}{{{html}}}")

    lines.extend([
        "",
        r"\tikzset{",
        r"  arr/.style={-{Latex}, line width=0.7pt, draw=black!70},",
        r"  trust/.style={-{Latex}, line width=0.75pt, draw=blue!60!black},",
        r"  deploy/.style={-{Latex}, line width=0.7pt, draw=orange!70!black, dashed},",
        r"  icon/.style={align=center, font=\scriptsize\bfseries},",
        r"  zone/.style={draw=black!55, line width=0.8pt, rounded corners=3pt, opacity=0.35},",
        r"  note/.style={draw=black!40, rounded corners=2pt, fill=white, align=left, font=\scriptsize, inner sep=4pt},",
        r"}",
        "",
        r"\begin{document}",
        rf"\begin{{tikzpicture}}[x={FIG_W:.1f}cm, y={FIG_H:.1f}cm]",
        "",
        rf"\node[font=\bfseries\large, align=center, text width=0.85\linewidth] at (0.5, 0.975) {{{tex_escape(TITLE)}}};",
        rf"\node[font=\small, align=center, text=black!60, text width=0.9\linewidth] at (0.5, 0.948) {{{tex_escape(SUBTITLE)}}};",
        "",
    ])

    for i, zone in enumerate(ZONES):
        x, y = zone["xy"]
        w, h = zone["w"], zone["h"]
        x2, y2 = x + w, y + h
        lines.append(
            rf"\draw[zone, fill=zonefill{i}] ({x:.3f},{y:.3f}) rectangle ({x2:.3f},{y2:.3f});"
        )
        lines.append(
            rf"\node[anchor=north west, font=\bfseries\small] at ({x + 0.012:.3f},{y2 - 0.018:.3f}) {{{tex_escape(zone['title'])}}};"
        )

    def icon_node(node_id: str, x: float, y: float, icon_key: str, label: str, width: str = "0.55cm") -> None:
        icon_path = f"icons/{icon_key}.png"
        lines.append(
            rf"\node[icon] ({node_id}) at ({x:.3f},{y:.3f}) {{"
            rf"\includegraphics[width={width}]{{{icon_path}}}\\[-2pt]{tex_escape(label)}}};"
        )

    for i, (x, key, lbl) in enumerate(DEV_ITEMS):
        icon_node(f"dev{i}", x, DEV_Y, key, lbl)
    for i in range(len(DEV_ITEMS) - 1):
        x1 = DEV_ITEMS[i][0] + 0.05
        x2 = DEV_ITEMS[i + 1][0] - 0.05
        lines.append(rf"\draw[arr, draw=orange!70!black] ({x1:.3f},{DEV_Y:.3f}) -- ({x2:.3f},{DEV_Y:.3f});")

    for i, (x, key, lbl) in enumerate(IOT_ITEMS):
        icon_node(f"iot{i}", x, IOT_Y, key, lbl, "0.52cm")

    for i, (x, key, lbl) in enumerate(DATA_ITEMS):
        icon_node(f"data{i}", x, DATA_Y, key, lbl, "0.52cm")

    for i, (x, key, lbl) in enumerate(REE_ITEMS):
        icon_node(f"ree{i}", x, REE_Y, key, lbl, "0.48cm")

    for i, (x, y, key, lbl) in enumerate(TEE_ITEMS):
        icon_node(f"tee{i}", x, y, key, lbl, "0.46cm")

    cloud_items = [
        (0.14, "verify", "Attestation Verify"),
        (0.36, "fleet", "Fleet Mgmt"),
        (0.58, "policy", "Security Policy"),
        (0.80, "monitor", "Monitoring"),
    ]
    cloud_y = 0.215
    for i, (x, key, lbl) in enumerate(cloud_items):
        icon_node(f"cloud{i}", x, cloud_y, key, lbl, "0.52cm")

    for x1, y1, x2, y2, color, style, label in ARROWS:
        style_name = "arr"
        if color == "#1565C0":
            style_name = "trust"
        elif color == "#E65100":
            style_name = "deploy"
        dash = ", dashed" if style == "--" else ""
        lines.append(
            rf"\draw[{style_name}{dash}] ({x1:.3f},{y1:.3f}) -- ({x2:.3f},{y2:.3f});"
        )
        if label:
            mx = x1 + (x2 - x1) * 0.5
            my = y1 + (y2 - y1) * 0.5
            lines.append(
                rf"\node[font=\tiny, fill=white, inner sep=1pt] at ({mx:.3f},{my + 0.012:.3f}) {{{tex_escape(label)}}};"
            )

    for x, y, _fill, txt in NOTES:
        note_lines = [tex_escape(line) for line in txt.split("\n")]
        body = r" \\ ".join(note_lines)
        lines.append(rf"\node[note, anchor=south west] at ({x:.3f},{y:.3f}) {{{body}}};")

    lines.extend([
        r"\node[anchor=north east, font=\tiny, text=black!60] at (0.97,0.82) {—— data flow \quad —— trusted path \quad - - deploy};",
        r"\end{tikzpicture}",
        r"\end{document}",
        "",
    ])

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def build_matplotlib(icons: dict[str, Path]) -> None:
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.5, 0.975, TITLE, ha="center", va="top", fontsize=15, fontweight="bold")
    ax.text(0.5, 0.948, SUBTITLE, ha="center", va="top", fontsize=10, color="#455A64")

    for zone in ZONES:
        draw_zone(ax, zone["xy"], zone["w"], zone["h"], zone["fill"], zone["title"])

    for x, key, lbl in DEV_ITEMS:
        place_icon(ax, (x, DEV_Y), icons[key], lbl, zoom=0.24, label_y=-0.045)
    for i in range(len(DEV_ITEMS) - 1):
        arrow(ax, (DEV_ITEMS[i][0] + 0.05, DEV_Y), (DEV_ITEMS[i + 1][0] - 0.05, DEV_Y), color="#E65100")

    for x, key, lbl in IOT_ITEMS:
        place_icon(ax, (x, IOT_Y), icons[key], lbl, zoom=0.24, label_y=-0.045)

    for x, key, lbl in DATA_ITEMS:
        place_icon(ax, (x, DATA_Y), icons[key], lbl, zoom=0.24, label_y=-0.045)

    for x, key, lbl in REE_ITEMS:
        place_icon(ax, (x, REE_Y), icons[key], lbl, zoom=0.22, label_y=-0.048)

    for x, y, key, lbl in TEE_ITEMS:
        place_icon(ax, (x, y), icons[key], lbl, zoom=0.21, label_y=-0.048)

    cloud_items = [
        (0.14, "verify", "Attestation Verify"),
        (0.36, "fleet", "Fleet Mgmt"),
        (0.58, "policy", "Security Policy"),
        (0.80, "monitor", "Monitoring"),
    ]
    cloud_y = 0.215
    for x, key, lbl in cloud_items:
        place_icon(ax, (x, cloud_y), icons[key], lbl, zoom=0.24, label_y=-0.045)

    for x1, y1, x2, y2, color, style, label in ARROWS:
        arrow(ax, (x1, y1), (x2, y2), color=color, style=style, text=label)

    for x, y, color, txt in NOTES:
        ax.text(x, y, txt, fontsize=8.2, va="bottom", ha="left",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=color, edgecolor="#90A4AE", alpha=0.95))

    ax.text(0.97, 0.82, "—— data flow    —— trusted path    - - deploy",
            ha="right", va="top", fontsize=8, color="#455A64")

    fig.savefig(OUT_PNG, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT_PDF, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT_SVG, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate TEE + QAI architecture diagrams.")
    parser.add_argument(
        "--tex",
        action="store_true",
        help="Also export standalone LaTeX tikzpicture (tee_qai_edge_architecture_visual.tex).",
    )
    parser.add_argument(
        "--tex-only",
        action="store_true",
        help="Export only the LaTeX tikzpicture (skip matplotlib PNG/PDF/SVG).",
    )
    parser.add_argument(
        "--no-matplotlib",
        action="store_true",
        help="Skip matplotlib PNG/PDF/SVG export.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    icons = ensure_icons()

    export_matplotlib = not args.no_matplotlib and not args.tex_only
    export_tex = args.tex or args.tex_only

    if export_matplotlib:
        build_matplotlib(icons)
        print(f"Built: {OUT_PNG}")
        print(f"Built: {OUT_PDF}")
        print(f"Built: {OUT_SVG}")

    if export_tex:
        path = export_tikz(icons)
        print(f"Built: {path}")
        print("Compile: pdflatex tee_qai_edge_architecture_visual.tex")

    print(f"Icons: {ICON_DIR} ({len(icons)} files)")


if __name__ == "__main__":
    main()
