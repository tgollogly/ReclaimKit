#!/usr/bin/env bash
# ReclaimKit — remove a WSL install (including Docker-owned output files)
set -euo pipefail

INSTALL_DIR="${INSTALL_DIR:-$HOME/reclaimkit}"

echo "============================================"
echo " ReclaimKit — remove WSL install"
echo "============================================"
echo ""
echo "This stops Docker containers and deletes:"
echo "  $INSTALL_DIR"
echo ""

if [[ ! -d "$INSTALL_DIR" ]]; then
  echo "[OK] Nothing to remove — $INSTALL_DIR does not exist."
  exit 0
fi

if [[ -d "$INSTALL_DIR/deploy" ]]; then
  echo "[..] Stopping Docker containers..."
  (
    cd "$INSTALL_DIR/deploy"
    docker compose down --remove-orphans 2>/dev/null || true
  )
fi

echo "[..] Removing repo (sudo needed for Docker-owned files in output/)..."
sudo rm -rf "$INSTALL_DIR"

echo ""
echo "[OK] Removed $INSTALL_DIR"
echo "Run ./scripts/wsl-setup-and-test.sh for a fresh install."
