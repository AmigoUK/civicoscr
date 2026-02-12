# Civico.net Scraper

Download audio (MP3) and video (MP4) recordings from [civico.net](https://civico.net) council meeting pages — via a simple GUI or the command line.

![GUI screenshot](how%20to%20download%20it.jpg)

## Features

- **GUI** — paste a URL, pick audio/video, click Download
- **CLI** — scriptable with `--audio-only`, `--video-only`, `--output-dir`
- **Resumable downloads** — interrupted transfers pick up where they left off
- **Cross-platform** — Windows, macOS, and Linux with 1-click installers

## Quick start

### Windows

Double-click **`install.bat`**, then double-click **`run_gui.bat`**.

### macOS / Linux

```bash
./install.sh      # installs Python + dependencies into .venv/
./run_gui.sh      # launches the GUI (runs install first if needed)
```

> **macOS Tahoe note:** The installer uses Homebrew Python 3.13 + `python-tk@3.13` to avoid Apple's broken system-Python tkinter.

## Installation details

The installer (`install.bat` / `install.sh`) does four things:

1. **Finds or installs Python 3.10+**
   - Windows: tries `py -3`, falls back to `winget` or python.org download
   - macOS: uses Homebrew (`brew install python@3.13 python-tk@3.13`)
   - Linux: uses `apt` or `dnf`
2. **Creates a virtual environment** in `.venv/`
3. **Upgrades pip**
4. **Installs dependencies** from `requirements.txt`

## Usage

### GUI

```bash
./run_gui.sh          # macOS / Linux
run_gui.bat           # Windows
# or directly:
python gui.py
```

1. Paste a civico.net stream URL (e.g. `https://civico.net/sandwell/23298-Safer-Neighbourhoods-...`)
2. Choose output folder
3. Tick Audio (MP3) and/or Video (MP4)
4. Click **Download**

### CLI

```bash
# Download both audio and video
python scraper.py "https://civico.net/sandwell/23298-Safer-Neighbourhoods-..."

# Audio only, to a specific folder
python scraper.py --audio-only --output-dir ~/Downloads "https://civico.net/sandwell/23298-..."

# Video only
python scraper.py --video-only "https://civico.net/sandwell/23298-..."
```

## Requirements

- Python 3.10+
- `requests`, `tqdm` (installed automatically)
- `tkinter` (for the GUI — bundled with Python on Windows; installed via Homebrew/apt/dnf on macOS/Linux)

## Project structure

```
civicoscr/
├── scraper.py       # Core scraper logic (CLI entry point)
├── gui.py           # Tkinter GUI (auto-relaunches via .venv)
├── requirements.txt # Python dependencies
├── install.bat      # Windows installer
├── run_gui.bat      # Windows GUI launcher
├── install.sh       # macOS / Linux installer
└── run_gui.sh       # macOS / Linux GUI launcher
```

## License

This project is provided as-is for personal use. Please respect civico.net's terms of service when downloading content.
