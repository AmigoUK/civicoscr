# Chrome Web Store listing — Civico.net Downloader

Copy-paste material for the Chrome Web Store Developer Dashboard
(https://chrome.google.com/webstore/devconsole). A one-time $5 developer
registration fee applies to new accounts.

## Product details

**Name:** Civico.net Downloader

**Summary (max 132 chars):**

> Download audio (MP3) and video (MP4) from civico.net council meeting webcasts.

**Category:** Tools (alternatively: Productivity)

**Language:** English

**Description:**

> Download audio (MP3) and video (MP4) recordings of council meeting webcasts
> hosted on the Civico platform (civico.net) — for example Sandwell Council,
> Slough Borough Council and Westminster City Council.
>
> How to use:
> 1. Open a civico.net meeting page (e.g. civico.net/sandwell/...)
> 2. Click the extension icon — the page URL is filled in automatically
> 3. Choose Audio (MP3) and/or Video (MP4) and click Download
>
> Downloads are handled by Chrome itself, so you get Chrome's normal progress
> bar, pause and resume. Files are saved to your Downloads folder named
> {streamId}_{meeting title}.mp3 / .mp4.
>
> Notes:
> - Only published streams have downloadable recordings; the extension tells
>   you if a stream is not yet published.
> - Open source: https://github.com/AmigoUK/civicoscr
>
> Legal: This extension is an independent tool and is not affiliated with,
> endorsed by, or connected to Civico or any council. It only automates
> access to recordings that councils have already made publicly available —
> it does not bypass any authentication or access controls. Recordings
> remain the property of the respective council and/or its streaming
> provider. You are responsible for ensuring your use of downloaded material
> complies with the council's terms of use, privacy policy, and applicable
> copyright law. Provided "as is", without warranty of any kind.

## Graphic assets

- **Store icon (128×128):** `chrome-extension/icons/icon128.png`
- **Screenshot (1280×800):** `store/screenshot-1280x800.jpg` (at least one
  screenshot is required)
- Small promo tile (440×280) — optional, not provided

## Privacy tab

**Single purpose description:**

> This extension does one thing: it downloads the publicly available MP3/MP4
> recording of a civico.net council meeting webcast to the user's Downloads
> folder, at the user's explicit request (clicking the Download button).

**Permission justifications:**

- `downloads` — Used to save the meeting's MP3/MP4 file to the user's
  Downloads folder via the chrome.downloads API. This is the extension's core
  function.
- `activeTab` — Used only to pre-fill the popup's URL field with the address
  of the currently open civico.net meeting page when the user clicks the
  extension icon. No page content is read or modified.
- Host permission `https://admin.civico.net/*` — Used to fetch the meeting's
  public metadata (title, publication status, URL slugs) from the Civico API
  so the download links can be constructed.
- Host permission `https://vod.civico.net/*` — Used to fetch the meeting's
  public VOD manifest and to download the MP3/MP4 files themselves.

**Remote code:** No — the extension contains no remotely hosted code; it only
fetches JSON metadata and media files.

**Data usage disclosures:** The extension does not collect, store, or transmit
any user data. All checkboxes in the "data collected" section can be left
unticked. It communicates only with civico.net servers to fetch public
metadata and media.

**Privacy policy URL:** required field — host `store/privacy-policy.md`
somewhere public (GitHub Pages, a public gist, or make the repo public and use
the raw file URL), then paste that URL.

## Legal / disclaimer

The full legal disclaimer lives in [`../DISCLAIMER.md`](../DISCLAIMER.md)
(no affiliation with Civico or any council, content ownership, user
responsibilities, no warranty, takedown contact). A short version is baked
into the extension popup itself (footer + expandable "Legal notice"), and a
condensed paragraph is part of the store description above — keep all three
in sync if the wording changes.

## Upload

Build the ZIP and upload it on the "Package" tab:

```bash
./chrome-extension/package.sh   # produces dist/civico-downloader-v<version>.zip
```

Remember to bump `"version"` in `manifest.json` for every new upload.
