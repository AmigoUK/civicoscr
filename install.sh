#!/usr/bin/env bash
set -euo pipefail

# ============================================
#   Civico.net Scraper — macOS / Linux Setup
# ============================================

echo "============================================"
echo "  Civico.net Scraper - Setup"
echo "============================================"
echo ""

# ── Locate project directory (where this script lives) ──
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PY="$VENV_DIR/bin/python3"
VENV_PIP="$VENV_DIR/bin/pip"
REQ_FILE="$SCRIPT_DIR/requirements.txt"
MIN_MAJOR=3
MIN_MINOR=10

# ── Helper: check Python version ≥ 3.10 ──
check_python_version() {
    local py="$1"
    local ver
    ver="$("$py" --version 2>&1 | awk '{print $2}')" || return 1
    local major minor
    major="$(echo "$ver" | cut -d. -f1)"
    minor="$(echo "$ver" | cut -d. -f2)"
    if [ "$major" -ge "$MIN_MAJOR" ] && [ "$minor" -ge "$MIN_MINOR" ]; then
        return 0
    fi
    return 1
}

# ── Step 1: Find or install Python 3.10+ ──
echo "[1/4] Checking for Python..."

PYTHON_CMD=""
OS_TYPE="$(uname -s)"

if [ "$OS_TYPE" = "Darwin" ]; then
    # ── macOS ──
    # NEVER use /usr/bin/python3 — system Python's tkinter is broken on Tahoe
    for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3; do
        if [ -x "$candidate" ] && check_python_version "$candidate"; then
            PYTHON_CMD="$candidate"
            break
        fi
    done

    if [ -z "$PYTHON_CMD" ]; then
        echo "  Homebrew Python 3.10+ not found."
        if command -v brew &>/dev/null; then
            echo "  Installing Python 3.13 + tkinter via Homebrew..."
            brew install python@3.13 python-tk@3.13
            # Re-detect after install
            for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3 \
                             /opt/homebrew/bin/python3.13 /usr/local/bin/python3.13; do
                if [ -x "$candidate" ] && check_python_version "$candidate"; then
                    PYTHON_CMD="$candidate"
                    break
                fi
            done
            if [ -z "$PYTHON_CMD" ]; then
                echo ""
                echo "  ERROR: Python still not detected after brew install."
                echo "  Try: brew link python@3.13"
                exit 1
            fi
        else
            echo ""
            echo "  ERROR: Homebrew is not installed."
            echo "  Install it first with:"
            echo '    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            echo "  Then re-run this script."
            exit 1
        fi
    fi

elif [ "$OS_TYPE" = "Linux" ]; then
    # ── Linux ──
    if command -v python3 &>/dev/null && check_python_version python3; then
        PYTHON_CMD="python3"
    else
        echo "  Python 3.10+ not found. Attempting to install..."
        if command -v apt-get &>/dev/null; then
            echo "  Using apt (Debian/Ubuntu)..."
            sudo apt-get update -qq
            sudo apt-get install -y python3 python3-venv python3-tk
        elif command -v dnf &>/dev/null; then
            echo "  Using dnf (Fedora/RHEL)..."
            sudo dnf install -y python3 python3-tkinter
        else
            echo ""
            echo "  ERROR: Could not detect apt or dnf."
            echo "  Please install Python 3.10+ and python3-tk manually,"
            echo "  then re-run this script."
            exit 1
        fi
        # Re-check after install
        if command -v python3 &>/dev/null && check_python_version python3; then
            PYTHON_CMD="python3"
        else
            echo ""
            echo "  ERROR: Python 3.10+ still not available after install."
            exit 1
        fi
    fi

else
    echo "  Unsupported OS: $OS_TYPE"
    echo "  This installer supports macOS and Linux."
    exit 1
fi

PY_VER="$("$PYTHON_CMD" --version 2>&1 | awk '{print $2}')"
echo "  Found Python $PY_VER ($PYTHON_CMD)"

# ── Step 2: Create virtual environment ──
echo ""
echo "[2/4] Creating virtual environment..."

if [ -x "$VENV_PY" ]; then
    echo "  Virtual environment already exists. Updating..."
else
    "$PYTHON_CMD" -m venv "$VENV_DIR"
    echo "  Created .venv/"
fi

# ── Step 3: Upgrade pip ──
echo ""
echo "[3/4] Upgrading pip..."
"$VENV_PY" -m pip install --upgrade pip --quiet || echo "  WARNING: pip upgrade failed, continuing anyway..."

# ── Step 4: Install dependencies ──
echo ""
echo "[4/4] Installing dependencies..."

if [ -f "$REQ_FILE" ]; then
    "$VENV_PIP" install -r "$REQ_FILE" --quiet
else
    echo "  requirements.txt not found, installing defaults..."
    "$VENV_PIP" install requests tqdm --quiet
fi

# ── Verify tkinter ──
echo ""
echo "Verifying tkinter..."
if "$VENV_PY" -c "import tkinter; print('  tkinter OK')" 2>/dev/null; then
    :
else
    echo "  WARNING: tkinter not available. The GUI may not work."
    if [ "$OS_TYPE" = "Darwin" ]; then
        echo "  Try: brew install python-tk@3.13"
    else
        echo "  Try: sudo apt install python3-tk  (Debian/Ubuntu)"
        echo "    or: sudo dnf install python3-tkinter  (Fedora/RHEL)"
    fi
fi

# ── Done ──
echo ""
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "  To launch the GUI:"
echo "    $VENV_PY gui.py"
echo ""
echo "  Or simply:"
echo "    ./run_gui.sh"
echo ""
echo "  To use the CLI scraper:"
echo "    $VENV_PY scraper.py --help"
echo ""
