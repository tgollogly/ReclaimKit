#!/usr/bin/env bash
# Regenerate docs/COMPLETE-GUIDE.pdf from the Markdown source.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MD="$ROOT/docs/COMPLETE-GUIDE.md"
PDF="$ROOT/docs/COMPLETE-GUIDE.pdf"
CSS="$ROOT/docs/guide-pdf.css"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc is required. Install: sudo apt-get install pandoc wkhtmltopdf" >&2
  exit 1
fi

pandoc "$MD" \
  -o "$PDF" \
  --standalone \
  --pdf-engine=wkhtmltopdf \
  --css="$CSS" \
  --metadata title="ReclaimKit - Complete User Guide" \
  --metadata author="tgollogly" \
  -V margin-top=18mm \
  -V margin-bottom=18mm \
  -V margin-left=16mm \
  -V margin-right=16mm

echo "Wrote $PDF"
