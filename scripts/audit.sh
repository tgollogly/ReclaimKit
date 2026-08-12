#!/usr/bin/env bash
# Full repo audit — run before release or after changes.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> pytest"
python3 -m pytest tests/ -v

echo ""
echo "==> config.example.yaml validates"
python3 -c "
from pathlib import Path
from src.config import validate_config
import yaml
cfg = yaml.safe_load(Path('config.example.yaml').read_text(encoding='utf-8'))
validate_config(cfg)
print('OK')
"

echo ""
echo "==> all letter rounds generate"
python3 -c "
from pathlib import Path
import yaml
from src.escalation_letters import TRACKS
cfg = yaml.safe_load(Path('config.example.yaml').read_text(encoding='utf-8'))
for track, rounds in TRACKS.items():
    for n, (_, fn, _, _) in rounds.items():
        fn(cfg, {})
print('OK')
"

echo ""
echo "==> doctor (config.example.yaml)"
python3 main.py --config config.example.yaml doctor

echo ""
echo "==> daemon dry-run"
python3 main.py --config config.example.yaml daemon once --dry-run

echo ""
if command -v pandoc >/dev/null 2>&1; then
  echo "==> PDF build (all docs)"
  "$ROOT/scripts/build-all-pdfs.sh"
fi

echo ""
echo "AUDIT COMPLETE"
