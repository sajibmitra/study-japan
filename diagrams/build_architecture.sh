#!/usr/bin/env bash
# Build system architecture diagrams (TikZ text + visual with icons)
set -euo pipefail
cd "$(dirname "$0")"

pdflatex -interaction=nonstopmode tee_qai_edge_architecture.tex >/dev/null
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r450 \
  -sOutputFile=tee_qai_edge_architecture.png tee_qai_edge_architecture.pdf >/dev/null

python3 generate_architecture_visual.py

echo "Built: tee_qai_edge_architecture.pdf / .png (TikZ)"
echo "Built: tee_qai_edge_architecture_visual.pdf / .png / .svg (with icons)"
echo "Icons: icons/*.png"
