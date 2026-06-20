#!/usr/bin/env python3
"""Generate tee_qai_edge_architecture (.pdf, .png, .svg, .tex) — text-box layout."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parent
OUT_PNG = ROOT / "tee_qai_edge_architecture.png"
OUT_PDF = ROOT / "tee_qai_edge_architecture.pdf"
OUT_SVG = ROOT / "tee_qai_edge_architecture.svg"
OUT_TEX = ROOT / "tee_qai_edge_architecture.tex"

FIG_W = 18.0
FIG_H = 11.0

# Component: id, cx, cy, w, h, lines, fill (hex)
COMPONENTS = [
    # Development row
    ("ds", 0.10, 0.875, 0.13, 0.055, ["Public Datasets", "NSL-KDD, Edge-IIoTset"], "#FFE0B2"),
    ("pt", 0.24, 0.875, 0.13, 0.055, ["PyTorch", "classical baseline"], "#FFE0B2"),
    ("qk", 0.38, 0.875, 0.13, 0.055, ["Qiskit", "sim / cloud QPU"], "#FFE0B2"),
    ("pl", 0.52, 0.875, 0.13, 0.055, ["PennyLane", "VQC / kernel"], "#FFE0B2"),
    ("cmp", 0.66, 0.875, 0.13, 0.055, ["Compress & Export"], "#FFE0B2"),
    ("sign", 0.80, 0.875, 0.13, 0.055, ["Sign & Encrypt"], "#FFE0B2"),
    # IoT
    ("s1", 0.12, 0.735, 0.15, 0.055, ["Sensors"], "#C8E6C9"),
    ("s2", 0.30, 0.735, 0.15, 0.055, ["Actuators"], "#C8E6C9"),
    ("s3", 0.48, 0.735, 0.15, 0.055, ["ESP32-class", "nodes"], "#C8E6C9"),
    ("gw", 0.70, 0.735, 0.17, 0.055, ["IoT Gateway", "Radio / Field bus"], "#C8E6C9"),
    # Edge data path
    ("ingest", 0.20, 0.615, 0.17, 0.055, ["Data Collection", "ingest, buffer, parse"], "#ECEFF1"),
    ("feat", 0.44, 0.615, 0.17, 0.055, ["Feature Extraction", "REE-side preprocessing"], "#FFCDD2"),
    ("bench", 0.70, 0.615, 0.15, 0.055, ["Benchmark", "Harness"], "#ECEFF1"),
    # REE
    ("kernel", 0.10, 0.465, 0.14, 0.055, ["Linux Kernel"], "#FFCDD2"),
    ("net", 0.24, 0.465, 0.14, 0.055, ["Network", "Stack"], "#FFCDD2"),
    ("mgmt", 0.38, 0.465, 0.14, 0.055, ["Management", "Agent"], "#FFCDD2"),
    ("teeapi", 0.46, 0.465, 0.14, 0.055, ["TEE Client", "API / SMC"], "#FFCDD2"),
    # TEE top row
    ("keys", 0.58, 0.505, 0.13, 0.050, ["Secure Key", "Storage"], "#BBDEFB"),
    ("mstore", 0.70, 0.505, 0.13, 0.050, ["Trusted AI", "Model Storage"], "#BBDEFB"),
    ("infer", 0.82, 0.505, 0.13, 0.050, ["Trusted", "Inference TA"], "#BBDEFB"),
    ("hybrid", 0.94, 0.505, 0.13, 0.050, ["Hybrid Q-C", "Detection Engine"], "#BBDEFB"),
    # TEE bottom row
    ("ra", 0.64, 0.405, 0.13, 0.050, ["Remote", "Attestation"], "#BBDEFB"),
    ("decide", 0.78, 0.405, 0.20, 0.050, ["Security Decision Logic"], "#BBDEFB"),
    ("hw", 0.92, 0.405, 0.13, 0.050, ["ARM Gateway /", "FPGA SoC runtime"], "#BBDEFB"),
    # Cloud
    ("verify", 0.12, 0.215, 0.15, 0.055, ["Attestation", "Verifier"], "#B3E5FC"),
    ("fleet", 0.34, 0.215, 0.15, 0.055, ["Fleet", "Management"], "#B3E5FC"),
    ("policy", 0.56, 0.215, 0.15, 0.055, ["Security", "Policy"], "#B3E5FC"),
    ("monitor", 0.78, 0.215, 0.15, 0.055, ["Monitoring", "& Analytics"], "#B3E5FC"),
]

ZONES = [
    {"xy": (0.03, 0.82), "w": 0.94, "h": 0.11, "fill": "#FFE0B2", "title": "Development & Training (offline)"},
    {"xy": (0.03, 0.69), "w": 0.94, "h": 0.10, "fill": "#C8E6C9", "title": "IoT Layer"},
    {"xy": (0.03, 0.57), "w": 0.94, "h": 0.10, "fill": "#ECEFF1", "title": "Edge Data Path"},
    {"xy": (0.03, 0.41), "w": 0.44, "h": 0.13, "fill": "#FFCDD2", "title": "REE — Linux OS (untrusted)"},
    {"xy": (0.50, 0.36), "w": 0.47, "h": 0.18, "fill": "#BBDEFB", "title": "TEE — OP-TEE / ARM TrustZone (protected)"},
    {"xy": (0.03, 0.16), "w": 0.94, "h": 0.12, "fill": "#B3E5FC", "title": "Cloud Management & Monitoring"},
]

DEV_ARROWS = [
    ("ds", "pt"), ("ds", "qk"), ("qk", "pl"), ("pt", "cmp"), ("pl", "cmp"), ("cmp", "sign"),
]

ARROWS = [
    # x1,y1,x2,y2, style, color, label
    (0.12, 0.69, 0.20, 0.645, "-", "#37474F", None),
    (0.30, 0.69, 0.20, 0.645, "-", "#37474F", None),
    (0.48, 0.69, 0.20, 0.645, "-", "#37474F", None),
    (0.70, 0.69, 0.20, 0.645, "-", "#37474F", None),
    (0.20, 0.615, 0.44, 0.615, "-", "#37474F", "streams"),
    (0.44, 0.615, 0.82, 0.535, "-", "#37474F", "features"),
    (0.46, 0.465, 0.82, 0.505, "-", "#1565C0", "invoke TA"),
    (0.58, 0.505, 0.70, 0.505, "-", "#1565C0", None),
    (0.70, 0.505, 0.82, 0.505, "-", "#1565C0", None),
    (0.82, 0.505, 0.94, 0.505, "-", "#1565C0", None),
    (0.94, 0.505, 0.78, 0.405, "-", "#1565C0", None),
    (0.70, 0.505, 0.64, 0.405, "-", "#1565C0", None),
    (0.92, 0.405, 0.94, 0.505, "-", "#1565C0", None),
    (0.78, 0.405, 0.12, 0.28, "--", "#1565C0", "attestation quote"),
    (0.78, 0.405, 0.78, 0.28, "-", "#37474F", "alerts"),
    (0.80, 0.875, 0.70, 0.535, "--", "#E65100", "secure model deploy"),
    (0.70, 0.615, 0.94, 0.505, "--", "#37474F", None),
]

NOTES = [
    (0.03, 0.03, "#FFEBEE", "Threats mitigated:\nmodel tampering; unauthorized replacement; extraction; unauthorized inference; compromised REE"),
    (0.27, 0.03, "#E3F2FD", "TEE protects:\nmodel storage, inference, keys, decision logic"),
    (0.51, 0.03, "#FFF8E1", "QAI role:\nanomaly engine inside TEE; not a security primitive"),
    (0.73, 0.03, "#E8F5E9", "RQ:\nHybrid Q-C vs. TinyML for zero-day / unseen attacks under deployability & TEE constraints"),
]

COMP_BY_ID = {c[0]: c for c in COMPONENTS}


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
    }
    out = text
    for old, new in repl.items():
        out = out.replace(old, new)
    return out


def comp_center(comp) -> tuple[float, float]:
    _, cx, cy, w, h, *_ = comp
    return cx, cy


def comp_box(comp) -> tuple[float, float, float, float]:
    _, cx, cy, w, h, *_ = comp
    return cx - w / 2, cy - h / 2, w, h


def draw_zone_mpl(ax, xy, w, h, color, title, alpha=0.35, zorder=1):
    rect = mpatches.FancyBboxPatch(
        xy, w, h, boxstyle="round,pad=0.012,rounding_size=0.015",
        linewidth=1.2, edgecolor="#455A64", facecolor=color, alpha=alpha, zorder=zorder,
    )
    ax.add_patch(rect)
    ax.text(xy[0] + 0.012, xy[1] + h - 0.018, title, fontsize=10, fontweight="bold", va="top", zorder=zorder + 1)


def draw_component_mpl(ax, comp):
    _, cx, cy, w, h, lines, fill = comp
    x, y, _, _ = comp_box(comp)
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.01",
        linewidth=0.8, edgecolor="#455A64", facecolor=fill, alpha=0.9, zorder=3,
    )
    ax.add_patch(rect)
    text = lines[0] if len(lines) == 1 else f"{lines[0]}\n{lines[1]}"
    ax.text(cx, cy, text, ha="center", va="center", fontsize=7.5, zorder=4)


def arrow_mpl(ax, x1, y1, x2, y2, color="#37474F", style="-", label=None):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5, linestyle=style, shrinkA=3, shrinkB=3),
        zorder=2,
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.012, label, ha="center", va="bottom", fontsize=7, color=color, zorder=5)


def build_matplotlib() -> None:
    plt.rcParams["svg.fonttype"] = "none"  # keep editable text in SVG
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Edge gateway wrapper (draw first, behind zones)
    draw_zone_mpl(ax, (0.03, 0.36), 0.94, 0.43, "#E0E0E0", "Edge Gateway Platform", alpha=0.15, zorder=0)

    for zone in ZONES:
        draw_zone_mpl(ax, zone["xy"], zone["w"], zone["h"], zone["fill"], zone["title"])

    for comp in COMPONENTS:
        draw_component_mpl(ax, comp)

    for a, b in DEV_ARROWS:
        x1, y1 = comp_center(COMP_BY_ID[a])
        x2, y2 = comp_center(COMP_BY_ID[b])
        arrow_mpl(ax, x1 + 0.05, y1, x2 - 0.05, y2, color="#37474F")

    for x1, y1, x2, y2, style, color, label in ARROWS:
        arrow_mpl(ax, x1, y1, x2, y2, color=color, style=style, label=label)

    for x, y, color, txt in NOTES:
        ax.text(x, y, txt, fontsize=7.5, va="bottom", ha="left",
                bbox=dict(boxstyle="round,pad=0.35", facecolor=color, edgecolor="#90A4AE", alpha=0.95))

    ax.text(0.97, 0.82, "—— data   —— trusted   - - deploy",
            ha="right", va="top", fontsize=7.5, color="#455A64")

    fig.savefig(OUT_PNG, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT_PDF, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT_SVG, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def export_tikz(out_path: Path = OUT_TEX) -> Path:
    lines: list[str] = [
        "% Auto-generated by generate_architecture.py",
        "% Compile: pdflatex tee_qai_edge_architecture.tex",
        r"\documentclass[tikz,border=10pt]{standalone}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{xcolor}",
        r"\usepackage{tikz}",
        r"\usetikzlibrary{arrows.meta,calc,positioning,fit}",
        "",
    ]
    zone_html = ["FFE0B2", "C8E6C9", "ECEFF1", "FFCDD2", "BBDEFB", "B3E5FC", "E0E0E0"]
    for i, html in enumerate(zone_html):
        lines.append(rf"\definecolor{{zonefill{i}}}{{HTML}}{{{html}}}")

    lines.extend([
        "",
        r"\tikzset{",
        r"  cmp/.style={draw=black!65, rounded corners=3pt, line width=0.7pt, fill=white,",
        r"    align=center, inner sep=5pt, minimum height=0.72cm, font=\small},",
        r"  zone/.style={draw=black!55, rounded corners=5pt, line width=0.85pt, inner sep=10pt, opacity=0.35},",
        r"  arr/.style={-{Latex}, line width=0.85pt, draw=black!70},",
        r"  trust/.style={-{Latex}, line width=0.9pt, draw=blue!60!black},",
        r"  deploy/.style={-{Latex}, line width=0.85pt, draw=orange!70!black, dashed},",
        r"  lbl/.style={font=\scriptsize, fill=white, inner sep=1pt, text=black!70},",
        r"  notebox/.style={draw=black!35, rounded corners=3pt, fill=white, font=\scriptsize,",
        r"    align=left, inner sep=5pt, text width=3.15cm},",
        r"}",
        "",
        r"\begin{document}",
        rf"\begin{{tikzpicture}}[x={FIG_W:.1f}cm, y={FIG_H:.1f}cm]",
        "",
    ])

    # Edge wrapper
    lines.append(r"\draw[zone, fill=zonefill6] (0.03,0.36) rectangle (0.97,0.79);")
    lines.append(r"\node[anchor=north west, font=\bfseries] at (0.042,0.786) {Edge Gateway Platform};")

    for i, zone in enumerate(ZONES):
        x, y = zone["xy"]
        lines.append(
            rf"\draw[zone, fill=zonefill{i}] ({x:.3f},{y:.3f}) rectangle ({x + zone['w']:.3f},{y + zone['h']:.3f});"
        )
        lines.append(
            rf"\node[anchor=north west, font=\bfseries\small] at ({x + 0.012:.3f},{y + zone['h'] - 0.018:.3f}) {{{tex_escape(zone['title'])}}};"
        )

    for comp in COMPONENTS:
        cid, cx, cy, w, h, comp_lines, fill = comp
        html = fill.lstrip("#")
        lines.append(rf"\definecolor{{fill{cid}}}{{HTML}}{{{html}}}")
        body = r" \\ ".join(tex_escape(line) for line in comp_lines)
        if len(comp_lines) > 1:
            body = rf"{tex_escape(comp_lines[0])}\\{{\tiny {tex_escape(comp_lines[1])}}}"
        else:
            body = tex_escape(comp_lines[0])
        lines.append(
            rf"\node[cmp, fill=fill{cid}, minimum width={w * FIG_W:.2f}cm] ({cid}) at ({cx:.3f},{cy:.3f}) {{{body}}};"
        )

    for a, b in DEV_ARROWS:
        lines.append(rf"\draw[arr] ({a}.east) -- ({b}.west);")

    for x1, y1, x2, y2, style, color, label in ARROWS:
        st = "arr"
        if color == "#1565C0":
            st = "trust"
        elif color == "#E65100":
            st = "deploy"
        dash = ", dashed" if style == "--" else ""
        lines.append(rf"\draw[{st}{dash}] ({x1:.3f},{y1:.3f}) -- ({x2:.3f},{y2:.3f});")
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            lines.append(rf"\node[lbl] at ({mx:.3f},{my + 0.012:.3f}) {{{tex_escape(label)}}};")

    note_fills = ["red!6", "blue!6", "yellow!12", "green!8"]
    for i, (note, nf) in enumerate(zip(NOTES, note_fills)):
        body = r" \\ ".join(tex_escape(line) for line in note[3].split("\n"))
        if i == 0:
            lines.append(rf"\node[notebox, fill={nf}, anchor=north west] at ([xshift=0.2cm,yshift=-0.15cm]0.03,0.16) {{{body}}};")
        elif i == 1:
            lines.append(rf"\node[notebox, fill={nf}, anchor=north] at ($(0.03,0.16)!0.5!(0.97,0.16)$) {{{body}}};")
        elif i == 2:
            lines.append(rf"\node[notebox, fill={nf}, anchor=north east] at ([xshift=-0.2cm,yshift=-0.15cm]0.97,0.16) {{{body}}};")
        else:
            lines.append(rf"\node[notebox, fill={nf}, anchor=north west] at ([xshift=0.2cm,yshift=-0.15cm]0.03,0.82) {{{body}}};")

    lines.extend([
        r"\node[font=\scriptsize, anchor=north east] at (0.97,0.82) {",
        r"  \tikz{\draw[arr] (0,0)--(0.07,0);} data \quad",
        r"  \tikz{\draw[trust] (0,0)--(0.07,0);} trusted \quad",
        r"  \tikz{\draw[deploy] (0,0)--(0.07,0);} deploy",
        r"};",
        r"\end{tikzpicture}",
        r"\end{document}",
        "",
    ])

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate tee_qai_edge_architecture PDF/PNG/SVG/TEX."
    )
    parser.add_argument(
        "--tex",
        action="store_true",
        help="Also export tee_qai_edge_architecture.tex (tikzpicture).",
    )
    parser.add_argument(
        "--tex-only",
        action="store_true",
        help="Export only the LaTeX file.",
    )
    parser.add_argument(
        "--no-matplotlib",
        action="store_true",
        help="Skip matplotlib PNG/PDF/SVG export.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    export_mpl = not args.no_matplotlib and not args.tex_only
    export_tex = args.tex or args.tex_only

    if export_mpl:
        build_matplotlib()
        print(f"Built: {OUT_PNG}")
        print(f"Built: {OUT_PDF}")
        print(f"Built: {OUT_SVG}")

    if export_tex:
        path = export_tikz()
        print(f"Built: {path}")
        print("Compile: pdflatex tee_qai_edge_architecture.tex")


if __name__ == "__main__":
    main()
