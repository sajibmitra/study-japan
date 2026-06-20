#!/usr/bin/env python3
"""Generate TEE + hybrid QAI edge system architecture with icon images."""

from __future__ import annotations

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
    for ang, xy in zip([210, 330, 90], [(24, 88), (104, 88), (64, 104)]):
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


def build(icons: dict[str, Path]) -> None:
    fig, ax = plt.subplots(figsize=(18, 11))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.5, 0.975, "Trustworthy Hybrid Quantum–Classical AI for Secure IoT Edge Systems",
            ha="center", va="top", fontsize=15, fontweight="bold")
    ax.text(0.5, 0.948, "System Architecture — TEE-protected deployment, trusted inference, and hybrid anomaly detection",
            ha="center", va="top", fontsize=10, color="#455A64")

    # --- Development zone ---
    draw_zone(ax, (0.03, 0.82), 0.94, 0.11, "#FFE0B2", "Development & Training (offline)")
    dev_y = 0.865
    dev_items = [
        (0.08, "database", "Datasets"),
        (0.22, "pytorch", "PyTorch"),
        (0.36, "qiskit", "Qiskit"),
        (0.50, "pennylane", "PennyLane"),
        (0.64, "compress", "Compress"),
        (0.78, "lock", "Sign & Encrypt"),
    ]
    for x, key, lbl in dev_items:
        place_icon(ax, (x, dev_y), icons[key], lbl, zoom=0.24, label_y=-0.045)
    for i in range(len(dev_items) - 1):
        arrow(ax, (dev_items[i][0] + 0.05, dev_y), (dev_items[i + 1][0] - 0.05, dev_y), color="#E65100")

    # --- IoT zone ---
    draw_zone(ax, (0.03, 0.69), 0.94, 0.10, "#C8E6C9", "IoT Layer")
    iot_y = 0.735
    for x, key, lbl in [(0.14, "sensor", "Sensors"), (0.32, "iot", "Actuators"), (0.50, "sensor", "ESP32 nodes"), (0.72, "iot", "Field Gateway")]:
        place_icon(ax, (x, iot_y), icons[key], lbl, zoom=0.24, label_y=-0.045)
    arrow(ax, (0.50, 0.69), (0.50, 0.635), text="telemetry")

    # --- Edge data path ---
    draw_zone(ax, (0.03, 0.57), 0.94, 0.10, "#ECEFF1", "Edge Data Path")
    dp_y = 0.615
    for x, key, lbl in [(0.22, "collect", "Data Collection"), (0.46, "feature", "Feature Extraction (REE)"), (0.70, "bench", "Benchmark Harness")]:
        place_icon(ax, (x, dp_y), icons[key], lbl, zoom=0.24, label_y=-0.045)
    arrow(ax, (0.27, dp_y), (0.41, dp_y), text="streams")
    arrow(ax, (0.51, dp_y), (0.65, dp_y), text="features")

    # --- REE zone ---
    draw_zone(ax, (0.03, 0.41), 0.44, 0.13, "#FFCDD2", "REE — Linux OS (untrusted)")
    ree_y = 0.465
    for x, key, lbl in [(0.10, "linux", "Linux"), (0.22, "network", "Network"), (0.34, "management", "Mgmt Agent"), (0.46, "tee_api", "TEE Client API")]:
        place_icon(ax, (x, ree_y), icons[key], lbl, zoom=0.22, label_y=-0.048)

    # --- TEE zone ---
    draw_zone(ax, (0.50, 0.36), 0.47, 0.18, "#BBDEFB", "TEE — OP-TEE / ARM TrustZone (protected)")
    tee_items = [
        (0.56, 0.505, "key", "Secure Keys"),
        (0.68, 0.505, "model", "Model Store"),
        (0.80, 0.505, "inference", "Inference TA"),
        (0.92, 0.505, "hybrid", "Hybrid Q-C Engine"),
        (0.62, 0.405, "attest", "Remote Attestation"),
        (0.78, 0.405, "decision", "Security Decision"),
        (0.90, 0.405, "fpga", "ARM / FPGA Runtime"),
    ]
    for x, y, key, lbl in tee_items:
        place_icon(ax, (x, y), icons[key], lbl, zoom=0.21, label_y=-0.048)

    arrow(ax, (0.46, ree_y), (0.56, 0.505), color="#1565C0", text="invoke TA")
    arrow(ax, (0.65, 0.57), (0.80, 0.535), color="#37474F", text="features")
    arrow(ax, (0.78, 0.82), (0.68, 0.535), color="#E65100", style="--", text="deploy model")

    # internal TEE chain
    arrow(ax, (0.61, 0.505), (0.63, 0.505), color="#1565C0")
    arrow(ax, (0.73, 0.505), (0.75, 0.505), color="#1565C0")
    arrow(ax, (0.85, 0.505), (0.87, 0.505), color="#1565C0")
    arrow(ax, (0.92, 0.485), (0.78, 0.425), color="#1565C0")
    arrow(ax, (0.68, 0.485), (0.62, 0.425), color="#1565C0")

    # --- Cloud zone ---
    draw_zone(ax, (0.03, 0.16), 0.94, 0.12, "#B3E5FC", "Cloud Management & Monitoring")
    cloud_y = 0.215
    for x, key, lbl in [(0.14, "verify", "Attestation Verify"), (0.36, "fleet", "Fleet Mgmt"), (0.58, "policy", "Security Policy"), (0.80, "monitor", "Monitoring")]:
        place_icon(ax, (x, cloud_y), icons[key], lbl, zoom=0.24, label_y=-0.045)
    arrow(ax, (0.78, 0.36), (0.14, 0.28), color="#1565C0", style="--", text="attestation quote")
    arrow(ax, (0.78, 0.36), (0.80, 0.28), color="#37474F", text="alerts")

    # Footer notes
    notes = [
        (0.03, 0.03, "#FFEBEE", "Threats mitigated:\nmodel tampering · replacement · extraction · unauthorized inference · compromised REE"),
        (0.27, 0.03, "#E3F2FD", "TEE protects:\nmodel storage · inference · keys · decision logic"),
        (0.51, 0.03, "#FFF8E1", "QAI role:\nanomaly engine inside TEE (not a security primitive)"),
        (0.73, 0.03, "#E8F5E9", "RQ:\nHybrid Q-C vs TinyML for unseen attacks under deployability & TEE constraints"),
    ]
    for x, y, color, txt in notes:
        ax.text(x, y, txt, fontsize=8.2, va="bottom", ha="left",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=color, edgecolor="#90A4AE", alpha=0.95))

    # Legend
    ax.text(0.97, 0.82, "—— data flow    —— trusted path    - - deploy", ha="right", va="top", fontsize=8, color="#455A64")

    fig.savefig(OUT_PNG, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT_PDF, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT_SVG, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    icons = ensure_icons()
    build(icons)
    print(f"Icons: {ICON_DIR} ({len(icons)} files)")
    print(f"Built: {OUT_PNG}")
    print(f"Built: {OUT_PDF}")
    print(f"Built: {OUT_SVG}")


if __name__ == "__main__":
    main()
