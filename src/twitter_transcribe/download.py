"""Download a Twitter/X video's audio track using yt-dlp.

We only need the audio for transcription, so we ask yt-dlp for the best
audio-only stream when one is available (falling back to the best combined
stream). This keeps downloads small even for hour-long videos.
"""

from __future__ import annotations

import glob
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from typing import Optional

from .errors import DownloadError

# twitter.com, x.com, mobile.twitter.com, etc. + a /status/<id> path.
_STATUS_RE = re.compile(
    r"^https?://(?:[\w-]+\.)*(?:twitter|x)\.com/[^/]+/status/\d+",
    re.IGNORECASE,
)


@dataclass
class DownloadedMedia:
    """A downloaded media file plus whatever metadata yt-dlp exposed."""

    path: str
    title: Optional[str] = None
    duration: Optional[float] = None
    uploader: Optional[str] = None
    webpage_url: Optional[str] = None


def is_twitter_status_url(url: str) -> bool:
    """Return True for a well-formed twitter.com / x.com status URL."""
    return bool(_STATUS_RE.match(url.strip()))


def _resolve_yt_dlp() -> str:
    exe = shutil.which("yt-dlp")
    if not exe:
        raise DownloadError(
            "yt-dlp is not installed or not on PATH. Install it with "
            "`pip install yt-dlp` (it is listed in requirements.txt)."
        )
    return exe


def download_audio(
    url: str,
    dest_dir: str,
    *,
    cookies: Optional[str] = None,
    quiet: bool = False,
) -> DownloadedMedia:
    """Download the best audio stream for ``url`` into ``dest_dir``.

    Parameters
    ----------
    url:
        A twitter.com / x.com status URL.
    dest_dir:
        Directory the media file is written to (created if missing).
    cookies:
        Optional path to a Netscape-format cookies file, needed for
        age-restricted or otherwise gated videos.
    quiet:
        Suppress yt-dlp's own progress output.

    Returns
    -------
    DownloadedMedia
    """
    url = url.strip()
    if not is_twitter_status_url(url):
        raise DownloadError(
            f"{url!r} does not look like a Twitter/X status URL "
            "(expected e.g. https://x.com/<user>/status/<id>)."
        )

    exe = _resolve_yt_dlp()
    os.makedirs(dest_dir, exist_ok=True)

    outtmpl = os.path.join(dest_dir, "%(id)s.%(ext)s")
    cmd = [
        exe,
        "--no-playlist",
        # bestaudio when Twitter exposes a separate audio stream; otherwise
        # the best combined stream (audio is extracted downstream by ffmpeg).
        "-f",
        "bestaudio/best",
        "--print-json",
        "--no-simulate",
        "-o",
        outtmpl,
    ]
    if cookies:
        if not os.path.isfile(cookies):
            raise DownloadError(f"Cookies file not found: {cookies}")
        cmd += ["--cookies", cookies]
    if quiet:
        cmd.append("--quiet")
    cmd.append(url)

    try:
        proc = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:  # pragma: no cover - resolved above
        raise DownloadError("yt-dlp executable disappeared during run.") from exc
    except subprocess.CalledProcessError as exc:
        raise DownloadError(
            f"yt-dlp failed (exit {exc.returncode}). Stderr:\n{exc.stderr.strip()}"
        ) from exc

    info = _parse_info_json(proc.stdout)
    path = _locate_downloaded_file(dest_dir, info)
    return DownloadedMedia(
        path=path,
        title=(info or {}).get("title"),
        duration=(info or {}).get("duration"),
        uploader=(info or {}).get("uploader") or (info or {}).get("uploader_id"),
        webpage_url=(info or {}).get("webpage_url") or url,
    )


def _parse_info_json(stdout: str) -> Optional[dict]:
    import json

    # --print-json emits one JSON object per line; take the last valid one.
    for line in reversed(stdout.strip().splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


def _locate_downloaded_file(dest_dir: str, info: Optional[dict]) -> str:
    """Find the file yt-dlp actually wrote.

    We resolve by media id where possible; otherwise fall back to the newest
    file in the destination directory.
    """
    if info:
        for key in ("_filename", "filepath"):
            candidate = info.get(key)
            if candidate and os.path.isfile(candidate):
                return candidate
        media_id = info.get("id")
        if media_id:
            matches = glob.glob(os.path.join(dest_dir, f"{media_id}.*"))
            matches = [m for m in matches if os.path.isfile(m)]
            if matches:
                return max(matches, key=os.path.getmtime)

    files = [
        os.path.join(dest_dir, f)
        for f in os.listdir(dest_dir)
        if os.path.isfile(os.path.join(dest_dir, f))
    ]
    if not files:
        raise DownloadError(
            "yt-dlp reported success but no media file was found on disk."
        )
    return max(files, key=os.path.getmtime)
