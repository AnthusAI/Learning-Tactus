#!/usr/bin/env bash
set -euo pipefail

# Render both HTML and PDF to stable locations.
#
# Outputs:
#   _output/html/index.html
#   _output/pdf/Learning-Tactus.pdf

./scripts/render-html.sh "$@"
./scripts/render-pdf.sh "$@"

