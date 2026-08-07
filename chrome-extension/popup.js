// Civico.net Downloader — Chrome extension port of scraper.py
// Fetches stream metadata + VOD manifest, then hands the MP3/MP4 URLs
// to chrome.downloads (which provides its own progress UI and resume).

const API_BASE = "https://admin.civico.net/api";
const VOD_BASE = "https://vod.civico.net";

const urlInput = document.getElementById("url");
const audioCheck = document.getElementById("audio");
const videoCheck = document.getElementById("video");
const downloadBtn = document.getElementById("download");
const statusEl = document.getElementById("status");

function setStatus(text, kind) {
  statusEl.textContent = text;
  statusEl.className = "status" + (kind ? " " + kind : "");
}

function extractStreamId(url) {
  const match = url.match(/\/(\d+)-/);
  if (!match) {
    throw new Error("Could not extract stream ID from URL: " + url);
  }
  return parseInt(match[1], 10);
}

function sanitizeFilename(title) {
  let sanitized = title.replace(/[<>:"/\\|?*]/g, "_");
  sanitized = sanitized.replace(/\s+/g, "_");
  sanitized = sanitized.replace(/^[_.]+|[_.]+$/g, "");
  return sanitized.slice(0, 200);
}

async function fetchJson(url) {
  const resp = await fetch(url);
  if (!resp.ok) {
    throw new Error(`HTTP ${resp.status} for ${url}`);
  }
  return resp.json();
}

function startDownload(url, filename) {
  return new Promise((resolve, reject) => {
    chrome.downloads.download({ url, filename }, (downloadId) => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
      } else {
        resolve(downloadId);
      }
    });
  });
}

async function run() {
  const pageUrl = urlInput.value.trim();
  if (!pageUrl) {
    setStatus("Enter a civico.net stream page URL.", "error");
    return;
  }
  if (!audioCheck.checked && !videoCheck.checked) {
    setStatus("Select at least one format.", "error");
    return;
  }

  downloadBtn.disabled = true;
  try {
    const streamId = extractStreamId(pageUrl);
    setStatus(`Stream ID: ${streamId}\nFetching stream metadata...`);

    const metadata = await fetchJson(`${API_BASE}/streams/${streamId}`);
    const title = metadata.title || `stream_${streamId}`;

    if (metadata.status !== "published") {
      setStatus(
        `Stream is not yet published (status: ${metadata.status}).\n` +
          "Only published streams have downloadable audio/video.",
        "error"
      );
      return;
    }

    setStatus(`Title: ${title}\nFetching manifest...`);
    const clientSlug = metadata.client.slug;
    const subclientSlug = metadata.subclient.slug;
    const manifest = await fetchJson(
      `${VOD_BASE}/${clientSlug}/${subclientSlug}/${metadata.slug}/manifest.json`
    );
    const vodBase = manifest.vod_base;

    const safeTitle = sanitizeFilename(title);
    const started = [];

    if (audioCheck.checked) {
      await startDownload(
        `${VOD_BASE}/${vodBase}/audio.mp3`,
        `${streamId}_${safeTitle}.mp3`
      );
      started.push("MP3");
    }
    if (videoCheck.checked) {
      await startDownload(
        `${VOD_BASE}/${vodBase}/progressive.mp4`,
        `${streamId}_${safeTitle}.mp4`
      );
      started.push("MP4");
    }

    setStatus(
      `Title: ${title}\nStarted ${started.join(" + ")} download` +
        (started.length > 1 ? "s" : "") +
        ".\nCheck Chrome's download bar for progress.",
      "success"
    );
  } catch (err) {
    setStatus("Error: " + err.message, "error");
  } finally {
    downloadBtn.disabled = false;
  }
}

downloadBtn.addEventListener("click", run);
urlInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") run();
});

// Pre-fill the URL field from the active tab if it's a civico.net stream page.
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const tabUrl = tabs[0] && tabs[0].url;
  if (tabUrl && /^https?:\/\/(www\.)?civico\.net\//.test(tabUrl)) {
    urlInput.value = tabUrl;
  }
});
