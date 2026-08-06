# Portfolio entry brief — for a coding agent

This file is a self-contained brief for a coding agent whose task is to create
a portfolio entry for this project on **attv.uk**. Everything you need — copy,
image paths, tags, and constraints — is below. Match the structure, styling,
and conventions of the existing portfolio entries on attv.uk; where this brief
conflicts with the site's conventions, the site's conventions win.

## Project identity

- **Name:** Civico.net Scraper
- **Tagline (EN):** Download council meeting webcasts as MP3/MP4 — CLI, GUI, and Chrome extension.
- **Tagline (PL):** Pobieranie nagrań posiedzeń rad miejskich jako MP3/MP4 — CLI, GUI i wtyczka Chrome.
- **Type:** Open-source desktop + browser tool
- **Repo:** https://github.com/AmigoUK/civicoscr (**private** — do not link it
  publicly unless it has been made public; check first, and if it is still
  private describe the project without a source link)
- **Live demo:** none (desktop/browser tool)

## Suggested entry copy

### English

> **Civico.net Scraper** — a cross-platform toolkit for archiving UK council
> meeting webcasts hosted on the Civico platform (tested on Sandwell,
> works with e.g. Slough and Westminster).
>
> Paste a meeting URL and get the recording as MP3 audio or MP4 video. Three
> front-ends share one core: a scriptable Python CLI with resumable downloads
> (HTTP Range), a Tkinter GUI with one-click installers for Windows, macOS and
> Linux, and a Chrome extension (Manifest V3) that auto-fills the URL from the
> active tab and hands downloads to the browser's native download manager.
>
> Under the hood it reverse-engineers Civico's public API: stream metadata
> from `admin.civico.net`, a VOD manifest lookup, then direct media URLs —
> no scraping of rendered pages, no headless browser needed.

### Polish

> **Civico.net Scraper** — wieloplatformowy zestaw narzędzi do archiwizacji
> nagrań posiedzeń brytyjskich rad miejskich z platformy Civico (testowany na
> Sandwell, działa też m.in. ze Slough i Westminster).
>
> Wklejasz adres posiedzenia i dostajesz nagranie jako audio MP3 lub wideo
> MP4. Trzy interfejsy współdzielą jeden rdzeń: skryptowalne CLI w Pythonie ze
> wznawianiem pobierania (HTTP Range), GUI w Tkinter z instalatorami 1-click
> dla Windows, macOS i Linuksa oraz wtyczka Chrome (Manifest V3), która sama
> podstawia URL z aktywnej karty i przekazuje pobieranie natywnemu menedżerowi
> pobrań przeglądarki.
>
> Pod maską: odtworzona publiczna warstwa API Civico — metadane streamu z
> `admin.civico.net`, odczyt manifestu VOD i bezpośrednie adresy mediów — bez
> scrapowania renderowanych stron i bez headless przeglądarki.

## Feature bullets (pick 4–6)

- Resumable downloads via HTTP Range headers (CLI/GUI)
- Chrome extension: URL auto-fill from the active civico.net tab, downloads
  via the `chrome.downloads` API (native progress/pause/resume)
- 1-click installers: `install.bat` (py launcher → winget → python.org) and
  `install.sh` (Homebrew on macOS, apt/dnf on Linux)
- Works around macOS Tahoe's broken system-Python tkinter by bootstrapping
  into a Homebrew-Python venv
- Chrome Web Store submission package included: listing copy, permission
  justifications, privacy policy, 1280×800 screenshot, ZIP build script
- Zero-dependency-heavy stack: stdlib + `requests` + `tqdm` only

## Tech stack / tags

`Python` `Tkinter` `JavaScript` `Chrome Extension (MV3)` `REST API`
`Bash` `Batch` `Playwright` (used to generate store assets)

## Images (paths relative to repo root)

Screenshots — use these; do not skip imagery in the entry:

- `store/screenshot-1280x800.jpg` — polished 1280×800 promo shot of the
  Chrome extension popup on a branded background (best-looking asset;
  strong hero candidate)
- `screenshots/extension-popup.png` — extension popup, default empty state
  (2× retina PNG)
- `screenshots/extension-popup-success.png` — popup after starting MP3+MP4
  downloads, success status (2× retina PNG)
- `screenshots/extension-popup-error.png` — popup showing the
  unpublished-stream error state (2× retina PNG)
- `how to download it.jpg` — GUI screenshot with usage annotations
- `Downloads_folder.jpg` — resulting files in the Downloads folder
- `chrome-extension/icons/icon128.png` — app icon (blue rounded square,
  white download arrow)

Copy the image files into the portfolio site's own asset pipeline — do not
hotlink to GitHub (the repo is private, raw links will 404 for visitors).

## Facts you may cite

- Started as a Python CLI, grew a GUI, then a Chrome extension port — all
  three share the same API flow (stream ID → metadata → manifest → media URL)
- ~200-line core (`scraper.py`); the extension is dependency-free vanilla JS
- Store-ready: `dist/civico-downloader-v1.0.0.zip` builds via
  `chrome-extension/package.sh`

## Constraints — do not skip

- Include a short disclaimer: the tool is **not affiliated with Civico**, and
  users should check the relevant council's privacy policy/terms before
  downloading content.
- Do not publish the repo URL while the repo is private (verify at build time).
- Do not invent metrics (downloads, users, stars) — none are tracked.
- Downloaded media files are never part of the repo; do not imply the project
  redistributes council recordings.
