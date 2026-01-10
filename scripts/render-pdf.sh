#!/usr/bin/env bash
set -euo pipefail

# Render PDF to a stable location (doesn't wipe HTML output).
#
# Output:
#   _output/pdf/Learning-Tactus.pdf

quarto render --to pdf --output-dir _output/pdf "$@"

