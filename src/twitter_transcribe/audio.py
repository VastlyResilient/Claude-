"""Audio extraction and normalisation via ffmpeg/ffprobe.

Whisper models expect 16 kHz mono PCM. We convert whatever yt-dlp produced
into that canonical form before transcription, and expose a duration check so
callers can reject media that is longer than they are willing to process.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from typing import Optional

from .errors import AudioError, DurationExceededError

TARGET_SAMPLE_RATE = 16_000
TARGET_CHANNELS = 1


def _resolve(tool: str) -> str:
    exe = shutil.which(tool)
    if not exe:
        raise AudioError(
            f"{tool} is not installed or not on PATH. Install ffmpeg "
            "(which provides ffmpeg and ffprobe) via your OS package manager."
        )
    return exe


def probe_duration(path: str) -> float:
    """Return the media duration in seconds using ffprobe."""
    exe = _resolve("ffprobe")
    cmd = [
        exe,
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        path,
    ]
    try:
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise AudioError(
            f"ffprobe failed for {path}: {exc.stderr.strip()}"
        ) from exc

    try:
        data = json.loads(proc.stdout)
        return float(data["format"]["duration"])
    except (json.JSONDecodeError, KeyError, ValueError) as exc:
        raise AudioError(f"Could not read duration from ffprobe output.") from exc


def extract_wav(
    src_path: str,
    dest_path: str,
    *,
    max_duration: Optional[float] = 3600.0,
    duration: Optional[float] = None,
) -> float:
    """Convert ``src_path`` to a 16 kHz mono WAV at ``dest_path``.

    Parameters
    ----------
    max_duration:
        Reject media longer than this many seconds (default one hour). Pass
        ``None`` to disable the check.
    duration:
        Pre-probed duration, if the caller already has it (avoids a second
        ffprobe call).

    Returns
    -------
    float
        The media duration in seconds.
    """
    if not os.path.isfile(src_path):
        raise AudioError(f"Source media not found: {src_path}")

    if duration is None:
        duration = probe_duration(src_path)

    if max_duration is not None and duration > max_duration:
        raise DurationExceededError(duration, max_duration)

    exe = _resolve("ffmpeg")
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    cmd = [
        exe,
        "-y",
        "-i",
        src_path,
        "-vn",  # drop any video stream
        "-ac",
        str(TARGET_CHANNELS),
        "-ar",
        str(TARGET_SAMPLE_RATE),
        "-c:a",
        "pcm_s16le",
        dest_path,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise AudioError(
            f"ffmpeg failed to extract audio: {exc.stderr.strip()}"
        ) from exc

    if not os.path.isfile(dest_path) or os.path.getsize(dest_path) == 0:
        raise AudioError("ffmpeg produced an empty audio file.")

    return duration
