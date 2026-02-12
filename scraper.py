#!/usr/bin/env python3
"""Civico.net Audio/Video Scraper

Downloads MP3 and MP4 files from civico.net council meeting stream pages.
Supports resumable downloads via HTTP Range headers.
"""

import argparse
import os
import re
import sys

import requests
from tqdm import tqdm

API_BASE = "https://admin.civico.net/api"
VOD_BASE = "https://vod.civico.net"
CHUNK_SIZE = 8192


def extract_stream_id(url: str) -> int:
    """Extract numeric stream ID from a civico.net URL.

    Example: 'https://civico.net/sandwell/23298-Safer-...' -> 23298
    """
    match = re.search(r"/(\d+)-", url)
    if not match:
        raise ValueError(f"Could not extract stream ID from URL: {url}")
    return int(match.group(1))


def fetch_stream_metadata(stream_id: int) -> dict:
    """Fetch stream metadata from the civico.net API."""
    url = f"{API_BASE}/streams/{stream_id}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_manifest(client_slug: str, subclient_slug: str, slug: str) -> dict:
    """Fetch the VOD manifest containing available formats and vod_base path."""
    url = f"{VOD_BASE}/{client_slug}/{subclient_slug}/{slug}/manifest.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()


def sanitize_filename(title: str) -> str:
    """Replace characters that are invalid in filenames."""
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", title)
    sanitized = re.sub(r"\s+", "_", sanitized)
    sanitized = sanitized.strip("_.")
    return sanitized[:200]  # cap length for filesystem safety


def download_file(
    url: str,
    output_path: str,
    resume: bool = True,
    progress_callback=None,
    cancel_event=None,
) -> None:
    """Download a file with progress bar and optional resume support.

    Args:
        progress_callback: If provided, called with (downloaded_bytes, total_bytes)
                           instead of using tqdm. total_bytes may be None.
        cancel_event: A threading.Event; when set, raises InterruptedError.
    """
    headers = {}
    existing_size = 0

    if resume and os.path.exists(output_path):
        existing_size = os.path.getsize(output_path)
        headers["Range"] = f"bytes={existing_size}-"

    resp = requests.get(url, headers=headers, stream=True, timeout=30)

    # If server returns 416, the file is already fully downloaded
    if resp.status_code == 416:
        if progress_callback is None:
            print(f"  Already complete: {output_path}")
        return

    resp.raise_for_status()

    # Determine total size
    if resp.status_code == 206:  # Partial content — resuming
        content_range = resp.headers.get("Content-Range", "")
        # Format: "bytes START-END/TOTAL"
        total = int(content_range.split("/")[-1]) if "/" in content_range else None
        mode = "ab"
    else:
        total = int(resp.headers.get("Content-Length", 0)) or None
        existing_size = 0  # full download, ignore any partial file
        mode = "wb"

    if progress_callback is not None:
        # GUI mode — use callback instead of tqdm
        downloaded = existing_size
        with open(output_path, mode) as f:
            for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                if cancel_event is not None and cancel_event.is_set():
                    raise InterruptedError("Download cancelled by user")
                f.write(chunk)
                downloaded += len(chunk)
                progress_callback(downloaded, total)
    else:
        # CLI mode — original tqdm behavior
        desc = os.path.basename(output_path)
        with (
            open(output_path, mode) as f,
            tqdm(
                total=total,
                initial=existing_size,
                unit="B",
                unit_scale=True,
                desc=desc,
            ) as bar,
        ):
            for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
                bar.update(len(chunk))


def main():
    parser = argparse.ArgumentParser(
        description="Download audio/video from civico.net stream pages."
    )
    parser.add_argument("url", help="Civico.net stream page URL")
    parser.add_argument(
        "--audio-only", action="store_true", help="Download audio (MP3) only"
    )
    parser.add_argument(
        "--video-only", action="store_true", help="Download video (MP4) only"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to save files (default: current directory)",
    )
    args = parser.parse_args()

    if args.audio_only and args.video_only:
        parser.error("--audio-only and --video-only are mutually exclusive")

    # 1. Extract stream ID
    stream_id = extract_stream_id(args.url)
    print(f"Stream ID: {stream_id}")

    # 2. Fetch metadata
    print("Fetching stream metadata...")
    metadata = fetch_stream_metadata(stream_id)
    title = metadata.get("title", f"stream_{stream_id}")
    slug = metadata["slug"]
    client_slug = metadata["client"]["slug"]
    subclient_slug = metadata["subclient"]["slug"]
    print(f"Title: {title}")
    print(f"Status: {metadata.get('status', 'unknown')}")

    if metadata.get("status") != "published":
        print(f"\nError: Stream is not yet published (status: {metadata.get('status')}).")
        print("Only published streams have downloadable audio/video.")
        sys.exit(1)

    # 3. Fetch manifest
    print("Fetching manifest...")
    manifest = fetch_manifest(client_slug, subclient_slug, slug)
    vod_base = manifest["vod_base"]

    # 4. Build download URLs and filenames
    safe_title = sanitize_filename(title)
    os.makedirs(args.output_dir, exist_ok=True)

    downloaded = []

    if not args.video_only:
        audio_url = f"{VOD_BASE}/{vod_base}/audio.mp3"
        audio_path = os.path.join(args.output_dir, f"{stream_id}_{safe_title}.mp3")
        print(f"\nDownloading audio: {audio_url}")
        download_file(audio_url, audio_path)
        downloaded.append(audio_path)

    if not args.audio_only:
        video_url = f"{VOD_BASE}/{vod_base}/progressive.mp4"
        video_path = os.path.join(args.output_dir, f"{stream_id}_{safe_title}.mp4")
        print(f"\nDownloading video: {video_url}")
        download_file(video_url, video_path)
        downloaded.append(video_path)

    # 5. Summary
    print("\nDone! Downloaded files:")
    for path in downloaded:
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"  {path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
