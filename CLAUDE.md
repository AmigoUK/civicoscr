# CLAUDE.md — Civico.net Scraper

## Project overview

CLI + GUI tool for downloading audio (MP3) and video (MP4) from civico.net council meeting webcasts. Tested on Sandwell Council. Written in Python, uses tkinter for the GUI.

## Key files

- `scraper.py` — Core logic: URL parsing, API calls, resumable downloads (CLI entry point)
- `gui.py` — Tkinter GUI with bootstrap that auto-relaunches via `.venv/` Python
- `install.bat` / `install.sh` — Platform installers (Windows / macOS+Linux)
- `run_gui.bat` / `run_gui.sh` — 1-click launchers (run install if `.venv/` missing, then launch GUI)
- `requirements.txt` — Dependencies: `requests`, `tqdm`

## Architecture

- **API**: `admin.civico.net/api/streams/{id}` for metadata, `vod.civico.net/.../manifest.json` for VOD paths
- **Downloads**: HTTP Range headers for resume support, `tqdm` progress in CLI, callback-based progress in GUI
- **Bootstrap** (`gui.py` lines 11–33): Detects if running outside `.venv/`, if so `os.execv()` re-launches via venv Python. This avoids macOS Tahoe's broken system-Python tkinter.
- **GUI threading**: Downloads run in a background `threading.Thread`, UI updates via `root.after()`

## Platform notes

- **macOS Tahoe**: System Python (`/usr/bin/python3`) has broken tkinter. `install.sh` deliberately skips it and uses Homebrew `python@3.13` + `python-tk@3.13`.
- **Windows**: `install.bat` tries `py -3` launcher, then `winget`, then python.org direct download.
- **Linux**: `install.sh` tries `apt-get` (Debian/Ubuntu) or `dnf` (Fedora/RHEL).

## Coding conventions

- Pure Python, no frameworks beyond stdlib + requests/tqdm
- No type stubs or mypy config — keep it simple
- GUI follows single-class pattern (`CivicoApp`) with state machine (`idle`/`downloading`/`done`)
- Shell scripts use `#!/usr/bin/env bash` with `set -euo pipefail`
- Batch files use `setlocal EnableDelayedExpansion`

## Git / GitHub

- Repo: `AmigoUK/civicoscr` (private)
- Branch: `main`
- `.gitignore` excludes: `.venv/`, `__pycache__/`, `*.mp3`, `*.mp4`, `Backup/`, `.DS_Store`, `.playwright-mcp/`
- Downloaded media files should never be committed
