#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PY="$SCRIPT_DIR/.venv/bin/python3"

if [ ! -x "$VENV_PY" ]; then
    echo "Virtual environment not found. Running installer first..."
    echo ""
    bash "$SCRIPT_DIR/install.sh"
    if [ ! -x "$VENV_PY" ]; then
        exit 1
    fi
fi

exec "$VENV_PY" "$SCRIPT_DIR/gui.py"
