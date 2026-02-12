#!/usr/bin/env python3
"""Civico.net Scraper — GUI

Cross-platform tkinter interface for downloading audio/video
from civico.net council meeting pages.
"""

import os
import sys

# --- Bootstrap: ensure we run from the project venv (fixes macOS Tahoe tkinter crash) ---
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_VENV_DIR = os.path.join(_SCRIPT_DIR, ".venv")
if sys.platform == "win32":
    _VENV_PY = os.path.join(_VENV_DIR, "Scripts", "python.exe")
else:
    _VENV_PY = os.path.join(_VENV_DIR, "bin", "python3")

if not sys.prefix.startswith(_VENV_DIR) and os.path.isfile(_VENV_PY):
    os.execv(_VENV_PY, [_VENV_PY] + sys.argv)

if not sys.prefix.startswith(_VENV_DIR):
    print("Error: Virtual environment not found at .venv/")
    print("Set it up with:")
    if sys.platform == "win32":
        print(f'  python -m venv "{_VENV_DIR}"')
        print(f'  "{_VENV_DIR}\\Scripts\\pip" install requests tqdm')
        print("  Or just run: install.bat")
    else:
        print(f"  python3.13 -m venv {_VENV_DIR}")
        print(f"  {_VENV_DIR}/bin/pip3 install requests tqdm")
        print("  Or just run: ./install.sh")
    sys.exit(1)
# --- End bootstrap ---

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from scraper import (
    download_file,
    extract_stream_id,
    fetch_manifest,
    fetch_stream_metadata,
    sanitize_filename,
    VOD_BASE,
)


class CivicoApp:
    """Main application window."""

    THROTTLE_BYTES = 50 * 1024  # update UI every ~50 KB

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Civico.net Scraper")
        self.root.resizable(False, False)

        self.cancel_event = threading.Event()
        self._last_reported = 0  # for progress throttling

        self._build_ui()
        self._set_state("idle")

    # ── UI construction ──────────────────────────────────────────

    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(sticky="nsew")

        # URL row
        ttk.Label(frame, text="URL:").grid(row=0, column=0, sticky="w", **pad)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, sticky="ew", **pad)
        self.paste_btn = ttk.Button(frame, text="Paste", command=self._paste_url)
        self.paste_btn.grid(row=0, column=2, **pad)

        # Output directory row
        ttk.Label(frame, text="Output:").grid(row=1, column=0, sticky="w", **pad)
        self.dir_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.dir_entry = ttk.Entry(frame, textvariable=self.dir_var, width=50)
        self.dir_entry.grid(row=1, column=1, sticky="ew", **pad)
        self.browse_btn = ttk.Button(frame, text="Browse", command=self._browse_dir)
        self.browse_btn.grid(row=1, column=2, **pad)

        # Format checkboxes row
        ttk.Label(frame, text="Download:").grid(row=2, column=0, sticky="w", **pad)
        fmt_frame = ttk.Frame(frame)
        fmt_frame.grid(row=2, column=1, sticky="w", **pad)
        self.audio_var = tk.BooleanVar(value=True)
        self.video_var = tk.BooleanVar(value=True)
        self.audio_cb = ttk.Checkbutton(
            fmt_frame, text="Audio (MP3)", variable=self.audio_var
        )
        self.audio_cb.pack(side="left", padx=(0, 12))
        self.video_cb = ttk.Checkbutton(
            fmt_frame, text="Video (MP4)", variable=self.video_var
        )
        self.video_cb.pack(side="left")

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            frame, variable=self.progress_var, maximum=100, length=400
        )
        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky="ew", **pad)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            frame, textvariable=self.status_var, wraplength=400
        )
        self.status_label.grid(row=4, column=0, columnspan=3, **pad)

        # Buttons row
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=(8, 0))
        self.download_btn = ttk.Button(
            btn_frame, text="Download", command=self._on_download
        )
        self.download_btn.pack(side="left", padx=8)
        self.cancel_btn = ttk.Button(
            btn_frame, text="Cancel", command=self._on_cancel
        )
        self.cancel_btn.pack(side="left", padx=8)

        frame.columnconfigure(1, weight=1)

    # ── State management ─────────────────────────────────────────

    def _set_state(self, state: str):
        """Transition the UI to idle / downloading / done."""
        is_idle = state in ("idle", "done")
        entry_state = "normal" if is_idle else "disabled"
        self.url_entry.configure(state=entry_state)
        self.dir_entry.configure(state=entry_state)
        self.paste_btn.configure(state="normal" if is_idle else "disabled")
        self.browse_btn.configure(state="normal" if is_idle else "disabled")
        self.audio_cb.configure(state="normal" if is_idle else "disabled")
        self.video_cb.configure(state="normal" if is_idle else "disabled")
        self.download_btn.configure(state="normal" if is_idle else "disabled")
        self.cancel_btn.configure(state="normal" if state == "downloading" else "disabled")

        if state == "idle":
            self.progress_var.set(0)
            self.status_var.set("Ready")
            self.status_label.configure(foreground="")

    # ── Helpers ───────────────────────────────────────────────────

    def _paste_url(self):
        try:
            text = self.root.clipboard_get()
            self.url_var.set(text.strip())
        except tk.TclError:
            pass

    def _browse_dir(self):
        path = filedialog.askdirectory(initialdir=self.dir_var.get())
        if path:
            self.dir_var.set(path)

    @staticmethod
    def _fmt_bytes(n: int) -> str:
        if n < 1024:
            return f"{n} B"
        elif n < 1024 * 1024:
            return f"{n / 1024:.1f} KB"
        else:
            return f"{n / (1024 * 1024):.1f} MB"

    # ── Download logic ────────────────────────────────────────────

    def _on_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please enter a civico.net URL.")
            return
        if not self.audio_var.get() and not self.video_var.get():
            messagebox.showwarning(
                "No format selected", "Select at least Audio or Video."
            )
            return

        self.cancel_event.clear()
        self._set_state("downloading")
        self.status_var.set("Fetching stream info...")

        thread = threading.Thread(target=self._worker, args=(url,), daemon=True)
        thread.start()

    def _on_cancel(self):
        self.cancel_event.set()

    def _worker(self, url: str):
        """Run in background thread — performs all network I/O."""
        try:
            stream_id = extract_stream_id(url)
        except ValueError as e:
            self.root.after(0, lambda: self._show_error("Invalid URL", str(e)))
            return

        try:
            metadata = fetch_stream_metadata(stream_id)
        except Exception as e:
            self.root.after(
                0, lambda: self._show_error("Metadata Error", str(e))
            )
            return

        status = metadata.get("status", "unknown")
        if status != "published":
            self.root.after(
                0,
                lambda: self._show_error(
                    "Not Published",
                    f"Stream status is '{status}'. Only published streams "
                    "have downloadable audio/video.",
                ),
            )
            return

        title = metadata.get("title", f"stream_{stream_id}")
        slug = metadata["slug"]
        client_slug = metadata["client"]["slug"]
        subclient_slug = metadata["subclient"]["slug"]

        try:
            manifest = fetch_manifest(client_slug, subclient_slug, slug)
        except Exception as e:
            self.root.after(
                0, lambda: self._show_error("Manifest Error", str(e))
            )
            return

        vod_base = manifest["vod_base"]
        safe_title = sanitize_filename(title)
        output_dir = self.dir_var.get()
        os.makedirs(output_dir, exist_ok=True)

        downloaded_files = []

        # Download audio
        if self.audio_var.get():
            audio_url = f"{VOD_BASE}/{vod_base}/audio.mp3"
            audio_path = os.path.join(output_dir, f"{stream_id}_{safe_title}.mp3")
            self.root.after(0, lambda: self.status_var.set("Downloading audio..."))
            try:
                self._download_with_progress(audio_url, audio_path)
            except InterruptedError:
                self.root.after(0, self._handle_cancelled)
                return
            except Exception as e:
                self.root.after(
                    0, lambda: self._show_error("Download Error", str(e))
                )
                return
            downloaded_files.append(audio_path)

        # Download video
        if self.video_var.get():
            video_url = f"{VOD_BASE}/{vod_base}/progressive.mp4"
            video_path = os.path.join(output_dir, f"{stream_id}_{safe_title}.mp4")
            self.root.after(0, lambda: self.status_var.set("Downloading video..."))
            self._last_reported = 0
            try:
                self._download_with_progress(video_url, video_path)
            except InterruptedError:
                self.root.after(0, self._handle_cancelled)
                return
            except Exception as e:
                self.root.after(
                    0, lambda: self._show_error("Download Error", str(e))
                )
                return
            downloaded_files.append(video_path)

        # Done
        summary_parts = []
        for p in downloaded_files:
            size_mb = os.path.getsize(p) / (1024 * 1024)
            summary_parts.append(f"{os.path.basename(p)} ({size_mb:.1f} MB)")
        summary = "Done! " + ", ".join(summary_parts)

        self.root.after(0, lambda: self._handle_done(summary))

    def _download_with_progress(self, url: str, output_path: str):
        self._last_reported = 0

        def progress_cb(downloaded, total):
            if downloaded - self._last_reported < self.THROTTLE_BYTES:
                if total is None or downloaded < total:
                    return
            self._last_reported = downloaded
            dl_str = self._fmt_bytes(downloaded)
            total_str = self._fmt_bytes(total) if total else "?"
            pct = (downloaded / total * 100) if total else 0
            label = os.path.basename(output_path)
            self.root.after(
                0,
                lambda p=pct, s=f"{label}  {dl_str} / {total_str}": self._update_progress(
                    p, s
                ),
            )

        download_file(
            url,
            output_path,
            resume=True,
            progress_callback=progress_cb,
            cancel_event=self.cancel_event,
        )

    # ── UI update callbacks (always called on main thread) ────────

    def _update_progress(self, percent: float, status_text: str):
        self.progress_var.set(percent)
        self.status_var.set(status_text)

    def _handle_done(self, summary: str):
        self.progress_var.set(100)
        self.status_var.set(summary)
        self.status_label.configure(foreground="green")
        self._set_state("done")
        # keep the green summary visible (don't reset via _set_state)
        self.status_var.set(summary)
        self.status_label.configure(foreground="green")

    def _handle_cancelled(self):
        self.status_var.set("Download cancelled")
        self.status_label.configure(foreground="orange")
        self._set_state("idle")
        # override the "Ready" text that _set_state writes
        self.status_var.set("Download cancelled")
        self.status_label.configure(foreground="orange")

    def _show_error(self, title: str, message: str):
        messagebox.showerror(title, message)
        self._set_state("idle")


def main():
    root = tk.Tk()
    CivicoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
