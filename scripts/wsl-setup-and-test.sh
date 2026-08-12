#!/usr/bin/env bash
# ReclaimKit — WSL + Docker setup and test (run inside Ubuntu/WSL)
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/tgollogly/ReclaimKit.git}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/reclaimkit}"

echo "============================================"
echo " ReclaimKit WSL + Docker setup and test"
echo "============================================"
echo ""

# --- Preflight ---
for cmd in git docker; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERROR: '$cmd' not found."
    echo "  - Install WSL2: wsl --install (PowerShell as Admin)"
    echo "  - Install Docker Desktop + enable WSL integration"
    exit 1
  fi
done

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker daemon not running."
  echo "  Start Docker Desktop on Windows, then retry."
  exit 1
fi

echo "[OK] Docker running"

# --- Clone or use existing ---
if [[ -d "$INSTALL_DIR/.git" ]]; then
  echo "[..] Using existing repo: $INSTALL_DIR"
  cd "$INSTALL_DIR"
  git pull origin main 2>/dev/null || git pull 2>/dev/null || true
else
  echo "[..] Cloning to $INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
  cd "$INSTALL_DIR"
fi

# --- Config ---
if [[ ! -f config.yaml ]]; then
  echo "[..] Creating config.yaml from template"
  cp config.example.yaml config.yaml
  echo "     EDIT config.yaml with your real email and address before emailing Meta!"
fi

mkdir -p evidence/screenshots output

fix_output_permissions() {
  if [[ -d "$INSTALL_DIR/output" ]]; then
    sudo chown -R "$(id -u):$(id -g)" "$INSTALL_DIR/output" 2>/dev/null || true
  fi
}

# --- Build image ---
echo "[..] Building Docker image (first time may take 2-3 min)..."
cd deploy
docker compose build

# --- Run checks inside container ---
run_app() {
  docker compose run --rm --no-TTY --remove-orphans reclaimkit python3 main.py "$@"
  fix_output_permissions
}

echo ""
echo "[..] Running doctor (health check)..."
run_app doctor || true

echo ""
echo "[..] Initializing campaign (Round 1 letters)..."
run_app campaign init

echo ""
echo "[..] Dry-run automation test (no emails, safe)..."
run_app daemon once --dry-run

echo ""
echo "[..] Starting background container (daily cron at 08:00 UTC)..."
docker compose up -d --remove-orphans
fix_output_permissions

echo ""
echo "============================================"
echo " SETUP COMPLETE"
echo "============================================"
echo ""
echo "Repo:     $INSTALL_DIR"
echo "Letters:  $INSTALL_DIR/output/campaign-package-*/round-01-meta/"
echo "Logs:     $INSTALL_DIR/output/cron.log"
echo "State:    $INSTALL_DIR/output/campaign/state.json"
echo ""
echo "NEXT STEPS:"
echo "  1. Edit config (pick one):"
echo "       nano $INSTALL_DIR/config.yaml          # inside Ubuntu/WSL"
echo "       wsl -d Ubuntu nano ~/reclaimkit/config.yaml   # from PowerShell"
echo "  2. Screenshots:  $INSTALL_DIR/evidence/screenshots/"
echo "  3. Email Meta:   use letter in output/campaign-package-.../round-01-meta/"
echo "  4. Record send:  cd $INSTALL_DIR/deploy && docker compose run --rm reclaimkit python3 main.py campaign sent --track meta --round 1"
echo ""
echo "Re-run setup without deleting?  ./scripts/wsl-setup-and-test.sh"
echo "Fresh reinstall?                ./scripts/wsl-reset-repo.sh && ./scripts/wsl-setup-and-test.sh"
echo ""
echo "USEFUL COMMANDS (from $INSTALL_DIR/deploy):"
echo "  docker compose logs -f"
echo "  docker compose run --rm reclaimkit python3 main.py campaign status"
echo "  docker compose run --rm reclaimkit python3 main.py daemon once --dry-run"
echo "  docker compose down"
echo ""
