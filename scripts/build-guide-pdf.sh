#!/usr/bin/env bash
# Regenerate docs/COMPLETE-GUIDE.pdf from the Markdown source.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MD="$ROOT/docs/COMPLETE-GUIDE.md"
PDF="$ROOT/docs/COMPLETE-GUIDE.pdf"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc is required. Install: sudo apt-get install pandoc wkhtmltopdf" >&2
  exit 1
fi

pandoc "$MD" \
  -o "$PDF" \
  --pdf-engine=wkhtmltopdf \
  --metadata title="ReclaimKit — Complete User Guide" \
  --metadata author="Thomas Gollogly" \
  -V margin-top=20mm \
  -V margin-bottom=20mm \
  -V margin-left=18mm \
  -V margin-right=18mm

echo "Wrote $PDF"
