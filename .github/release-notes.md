First release of the **Chrome extension** version of the Civico.net downloader, alongside the existing Python CLI and Tkinter GUI.

## Chrome extension (Manifest V3)

- Popup UI: URL auto-filled from the active civico.net tab, Audio (MP3) / Video (MP4) checkboxes, one-click Download
- Same API flow as the CLI: stream ID → metadata (`admin.civico.net`) → VOD manifest → direct media URLs
- Downloads handed to the `chrome.downloads` API — Chrome's native progress bar, pause and resume
- Filenames match the CLI: `{streamId}_{title}.mp3` / `.mp4`
- Built-in legal notice (no affiliation with Civico or any council — see `DISCLAIMER.md`)

## Install

Download **civico-downloader-v1.0.0.zip** below, unzip it, then load the folder via `chrome://extensions/` → **Developer mode** → **Load unpacked**. Full instructions in `chrome-extension/README.md`.

Chrome Web Store submission materials (listing copy, permission justifications, privacy policy, screenshots) live in `store/`.
