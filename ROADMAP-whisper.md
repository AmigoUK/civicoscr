# Whisper Audio Transcription — Roadmap

## Overview

Add timestamped transcription to the civicoscr tool using two engines:
- **faster-whisper** — local, offline, handles large files
- **OpenAI Whisper API** — cloud, simpler but 25 MB file limit

Output formats: SRT, VTT, TXT, JSON.

## Implementation steps

### Step 1: `transcriber.py`
Core module with lazy imports. Dataclasses for `Segment` and `TranscriptionResult`.
Functions: `transcribe_local()`, `transcribe_api()`, `transcribe()` dispatcher,
and writers for SRT/VTT/TXT/JSON.

### Step 2: CLI (`scraper.py`)
Add `--transcribe`, `--engine`, `--model`, `--api-key` flags.
Run transcription after download when `--transcribe` is set.

### Step 3: GUI (`gui.py`)
Transcribe checkbox, engine dropdown, conditional model/API key fields.
Worker extended to run transcription after download with progress feedback.

### Step 4: Optional requirements
`requirements-whisper.txt` (faster-whisper) and `requirements-api.txt` (openai).

### Step 5: Install scripts
Optional prompt in `install.sh` / `install.bat` to install transcription deps.

### Step 6: Documentation
Update README.md and CLAUDE.md.

## Key design decisions

1. **Lazy imports** — faster-whisper/openai imported inside functions, not at module level
2. **Progress callback** — `(segments_done, estimated_total, status_text)` for Whisper
3. **Cancel granularity** — per-segment check (~5–30 s each)
4. **Default model=base** — 150 MB RAM, good speed/accuracy trade-off
5. **All four formats always written** — no per-format selection needed
6. **25 MB API limit** — clear error suggesting local engine for large files
