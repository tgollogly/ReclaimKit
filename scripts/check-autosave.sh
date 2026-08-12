#!/usr/bin/env bash
# Verify ReclaimKit autosave (bind mounts + saved files on disk).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "============================================"
echo " ReclaimKit autosave check"
echo "============================================"
echo ""
echo "Repo: $ROOT"
echo ""

ok=0
warn=0

check() {
  if [[ -e "$1" ]]; then
    echo "[OK]   $2"
    echo "       $1"
    ok=$((ok + 1))
  else
    echo "[MISS] $2"
    echo "       $1"
    warn=$((warn + 1))
  fi
}

check "$ROOT/config.yaml" "Config (your details)"
check "$ROOT/output" "Output folder (letters, logs, campaign state)"
check "$ROOT/output/campaign/state.json" "Campaign state tracker"
check "$ROOT/evidence/screenshots" "Screenshots folder"

if [[ -f "$ROOT/deploy/docker-compose.yml" ]]; then
  if grep -q '../output:/app/output' "$ROOT/deploy/docker-compose.yml"; then
    echo "[OK]   Docker bind-mount: output/ → saved on disk"
    ok=$((ok + 1))
  else
    echo "[MISS] Docker output bind-mount not found in deploy/docker-compose.yml"
    warn=$((warn + 1))
  fi
  if grep -q '../evidence:/app/evidence' "$ROOT/deploy/docker-compose.yml"; then
    echo "[OK]   Docker bind-mount: evidence/ → saved on disk"
    ok=$((ok + 1))
  else
    echo "[MISS] Docker evidence bind-mount not found"
    warn=$((warn + 1))
  fi
fi

echo ""
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  if [[ -d "$ROOT/deploy" ]]; then
    cd "$ROOT/deploy"
    if docker compose ps --status running 2>/dev/null | grep -q reclaimkit; then
      echo "[OK]   Docker container running (daily cron active)"
    else
      echo "[WARN] Docker container not running — start with:"
      echo "       cd $ROOT/deploy && docker compose up -d"
    fi
  fi
else
  echo "[INFO] Docker not running — files still saved on disk above."
fi

echo ""
echo "Summary: autosave is ON when output/ and evidence/ exist on disk"
echo "         and deploy/docker-compose.yml bind-mounts them (default)."
echo ""
if [[ $warn -eq 0 ]]; then
  echo "All checks passed. Closing the terminal does NOT delete your data."
else
  echo "Some items missing — run setup or campaign init if you have not yet."
fi
echo ""
