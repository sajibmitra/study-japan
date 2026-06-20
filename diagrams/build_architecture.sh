#!/usr/bin/env bash
# Build system architecture diagrams (text-box + icon visual)
set -euo pipefail
cd "$(dirname "$0")"

python3 generate_architecture.py --tex
python3 generate_architecture_visual.py --tex

pdflatex -interaction=nonstopmode tee_qai_edge_architecture.tex >/dev/null
pdflatex -interaction=nonstopmode tee_qai_edge_architecture_visual.tex >/dev/null 2>&1 || true

echo "Built: tee_qai_edge_architecture.pdf / .png / .svg / .tex"
echo "Built: tee_qai_edge_architecture_visual.pdf / .png / .svg / .tex"
