# Civico.net Downloader — Chrome Extension

Chrome extension version of the civico.net scraper. Downloads audio (MP3) and
video (MP4) from civico.net council meeting webcast pages straight into your
browser's Downloads folder.

## Install (unpacked)

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top-right corner)
3. Click **Load unpacked**
4. Select this `chrome-extension/` folder

The blue download icon appears in the toolbar (pin it via the puzzle-piece menu).

## Usage

1. Open a civico.net meeting page (e.g. `https://civico.net/sandwell/23298-...`)
   — or copy its URL
2. Click the extension icon. If you're on a civico.net page, the URL field is
   pre-filled automatically; otherwise paste the URL
3. Tick **Audio (MP3)** and/or **Video (MP4)**
4. Click **Download**

Downloads are handled by Chrome itself, so progress, pause and resume are
available in Chrome's normal download bar / `chrome://downloads` page. Files
are named `{streamId}_{title}.mp3` / `.mp4`, matching the CLI tool.

Note: only **published** streams have downloadable audio/video — the extension
tells you if a stream isn't published yet.

## Publishing to the Chrome Web Store

Everything needed for a store submission lives in [`../store/`](../store/):
listing text, permission justifications, privacy policy, and a 1280×800
screenshot. Build the upload ZIP with:

```bash
./package.sh   # produces ../dist/civico-downloader-v<version>.zip
```

Bump `"version"` in `manifest.json` before each new upload. See
[`../store/store-listing.md`](../store/store-listing.md) for the full
step-by-step.

## How it works

Same flow as `scraper.py`:

1. Extracts the numeric stream ID from the page URL
2. Fetches metadata from `admin.civico.net/api/streams/{id}`
3. Fetches the VOD manifest from `vod.civico.net/.../manifest.json`
4. Hands the final `audio.mp3` / `progressive.mp4` URLs to the
   `chrome.downloads` API
