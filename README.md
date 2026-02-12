# Civico.net Scraper

Download audio (MP3) and video (MP4) recordings from [civico.net](https://civico.net) council webcast pages — via a simple GUI or the command line.

The tool works with council pages hosted on the Civico platform, such as:
- **Sandwell Council** — https://civico.net/sandwell
- **Slough Borough Council** — https://civico.net/slough/
- **Westminster City Council** — https://streaming.westminster.gov.uk/westminster/

> **Note:** The base URL `civico.net` alone does not work — you need the full council-specific address (e.g. `civico.net/sandwell`). The company page is at [civico.io](https://civico.io/).

Tested and confirmed working on **Sandwell Council** webcasts.

![GUI screenshot](how%20to%20download%20it.jpg)

## Features

- **GUI** — paste a URL, pick audio/video, click Download
- **CLI** — scriptable with `--audio-only`, `--video-only`, `--output-dir`
- **Resumable downloads** — interrupted transfers pick up where they left off
- **Cross-platform** — Windows, macOS, and Linux with 1-click installers

## Finding council policies

Each council hosted on Civico has its own **privacy policy** and terms, usually accessible from the left-hand menu on their page. For example:

- Sandwell: https://civico.net/sandwell/privacy-policy

Check the relevant council's policy page before downloading content.

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

## How I lawfully use council webcast clips

This channel uses short clips from public council webcasts to help residents understand and scrutinise local decision-making. The clips are combined with my own commentary, explanation and (where needed) translation, so that people can see what was actually said and then hear a clear analysis of what it means for our community.

Under UK copyright law, it is sometimes lawful to use short extracts from someone else's material without permission, if this is done fairly and for specific purposes. These are known as "fair dealing" exceptions. For public council webcasts, the most relevant exceptions are for criticism or review, quotation and reporting current events, as set out in section 30 of the Copyright, Designs and Patents Act 1988 and explained in UK government guidance on "Exceptions to copyright".

In practical terms, this is what I do:

- I only use **short clips** from public webcasts, and only where they are needed to show what was said or decided in a meeting. I do not upload whole meetings or act as an alternative archive.
- I always add **substantial commentary and explanation**, so that the video is clearly about criticism, review and reporting of current local events, not about re-posting someone else's content.
- I **acknowledge the source** wherever possible, by naming the council, the meeting, the date and the webcast platform, and by linking to the full recording so viewers can check the full context for themselves.
- I only use as much of the original material as is reasonably necessary to make the point, in line with the guidance that quotations and extracts should be no more than required for the specific purpose.

This video uses short clips from a public council webcast and adds subtitles in another language so that residents who do not speak the original language fluently can understand what is being discussed. Only those parts of the meeting that are necessary to illustrate the issues are translated and shown, so that viewers can follow the debate and understand how decisions are being made. The purpose of including these clips is to enable criticism, review, explanation and reporting of current local events in a way that is accessible to a wider community. The use of short extracts, together with translation and commentary, is intended to fall within the UK "fair dealing" exceptions for quotation, criticism or review and reporting current events under the Copyright, Designs and Patents Act 1988, section 30, and the related guidance on exceptions to copyright published by the UK government.

Where a clip includes statements by named individuals (such as councillors or officers), I aim to represent their words accurately and in context. My commentary may be strongly critical, but it is presented as opinion based on the facts shown and on publicly available information. Viewers who wish to see the full, unedited meeting are encouraged to use the official webcast link provided in the description.

### Sources

1. [Exceptions to copyright — GOV.UK](https://www.gov.uk/guidance/exceptions-to-copyright)
2. [Quotation — CopyrightUser](https://www.copyrightuser.org/understand/exceptions/quotation/)
3. [Exceptions and Fair Dealing — British Copyright Council](https://www.britishcopyright.org/information/information-exceptions-and-fair-dealing/)
4. [Quotation — CopyrightUser](https://www.copyrightuser.org/understand/quotation/)
5. [Copyright, Designs and Patents Act 1988, Section 30](https://www.legislation.gov.uk/ukpga/1988/48/section/30)
6. [Exceptions to copyright: Guidance for consumers (PDF) — GOV.UK](https://assets.publishing.service.gov.uk/media/5a80f292ed915d74e6231597/Exceptions_to_copyright_-_Guidance_for_consumers.pdf)
7. [Exceptions to copyright: Guidance for creators and copyright owners (PDF) — GOV.UK](https://assets.publishing.service.gov.uk/media/5a7f4cf640f0b62305b864e6/Exceptions_to_copyright_-_Guidance_for_creators_and_copyright_owners.pdf)
8. [Exception for use of quotations or extracts of copyright works (PDF)](https://assets.publishing.service.gov.uk/media/5a7ee018ed915d74e6227041/ia-exception-quotations.pdf)
9. [Fair dealing in United Kingdom law — Wikipedia](https://en.wikipedia.org/wiki/Fair_dealing_in_United_Kingdom_law)
10. [Parody, Caricature And... — DACS](https://www.dacs.org.uk/advice/articles/copyright-infringement/permitted-uses)
11. [Fair dealing and copyright in the UK — Harper James Solicitors](https://harperjames.co.uk/article/fair-dealing-copyright/)
12. [United Kingdom — Competition Law Association (PDF)](https://competitionlawassociation.org.uk/wp-content/uploads/documentation_14_1573582717.pdf)
13. [Copyright Exceptions — Solent University](https://libguides.solent.ac.uk/copyright/exceptions)
14. [Copyright, Designs and Patents Act 1988 (historical)](https://www.legislation.gov.uk/ukpga/1988/48/section/30/1993-01-01?view=plain)
15. ['The Exceptions' in more detail — Huddersfield Library Guides](https://hud.libguides.com/c.php?g=655142&p=4610444)
16. [Section 30 — LexisNexis](https://www.lexisnexis.co.uk/legal/legislation/uk-parliament-acts/copyright-designs-and-patents-act-1988-c48/part-i/section-30)


============================================

Whisper Audio Transcription — Roadmap
Overview
Add timestamped transcription to the civicoscr tool using two engines:

faster-whisper — local, offline, handles large files
OpenAI Whisper API — cloud, simpler but 25 MB file limit
Output formats: SRT, VTT, TXT, JSON.

Implementation steps
Step 1: transcriber.py
Core module with lazy imports. Dataclasses for Segment and TranscriptionResult. Functions: transcribe_local(), transcribe_api(), transcribe() dispatcher, and writers for SRT/VTT/TXT/JSON.

Step 2: CLI (scraper.py)
Add --transcribe, --engine, --model, --api-key flags. Run transcription after download when --transcribe is set.

Step 3: GUI (gui.py)
Transcribe checkbox, engine dropdown, conditional model/API key fields. Worker extended to run transcription after download with progress feedback.

Step 4: Optional requirements
requirements-whisper.txt (faster-whisper) and requirements-api.txt (openai).

Step 5: Install scripts
Optional prompt in install.sh / install.bat to install transcription deps.

Step 6: Documentation
Update README.md and CLAUDE.md.

Key design decisions
Lazy imports — faster-whisper/openai imported inside functions, not at module level
Progress callback — (segments_done, estimated_total, status_text) for Whisper
Cancel granularity — per-segment check (~5–30 s each)
Default model=base — 150 MB RAM, good speed/accuracy trade-off
All four formats always written — no per-format selection needed
25 MB API limit — clear error suggesting local engine for large files
