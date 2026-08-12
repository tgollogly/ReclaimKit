#!/usr/bin/env bash
# Build all ReclaimKit documentation PDFs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CSS="$ROOT/docs/guide-pdf.css"
BUILD="$ROOT/scripts/build-guide-pdf.sh"

build_one() {
  local md="$1"
  local pdf="$2"
  local title="$3"
  pandoc "$md" -o "$pdf" --standalone --pdf-engine=wkhtmltopdf --css="$CSS" \
    --metadata title="$title" --metadata author="ReclaimKit contributors" \
    -V margin-top=18mm -V margin-bottom=18mm \
    -V margin-left=16mm -V margin-right=16mm
  echo "Wrote $pdf"
}

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc required: sudo apt-get install pandoc wkhtmltopdf" >&2
  exit 1
fi

build_one "$ROOT/docs/COMPLETE-GUIDE.md" "$ROOT/docs/COMPLETE-GUIDE.pdf" "ReclaimKit - Complete User Guide"
build_one "$ROOT/docs/QUICK-START.md" "$ROOT/docs/QUICK-START.pdf" "ReclaimKit - Quick Start"
build_one "$ROOT/docs/AUTO-EMAIL-SETUP.md" "$ROOT/docs/AUTO-EMAIL-SETUP.pdf" "ReclaimKit - Auto Email Setup"
build_one "$ROOT/docs/WINDOWS-WSL-DOCKER.md" "$ROOT/docs/WINDOWS-WSL-DOCKER.pdf" "ReclaimKit - Windows WSL Docker"
build_one "$ROOT/deploy/VPS-GUIDE.md" "$ROOT/docs/VPS-GUIDE.pdf" "ReclaimKit - VPS Guide"

echo "All PDFs built in docs/"
