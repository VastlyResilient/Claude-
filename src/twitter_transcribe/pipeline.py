"""End-to-end pipeline: Twitter/X URL -> audio -> transcript files."""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from . import formats
from .audio import extract_wav
from .download import download_audio
from .transcribe import Segment, TranscribeResult, transcribe_wav, ProgressCallback


@dataclass
class TranscriptionResult:
    """The result of transcribing one video, plus everything about the source."""

    url: str
    text: str
    segments: List[Segment]
    language: Optional[str]
    duration: Optional[float]
    title: Optional[str] = None
    uploader: Optional[str] = None
    output_files: Dict[str, str] = field(default_factory=dict)

    def metadata(self) -> Dict:
        return {
            "url": self.url,
            "title": self.title,
            "uploader": self.uploader,
            "language": self.language,
            "duration": self.duration,
        }


def transcribe_url(
    url: str,
    *,
    model: str = "base",
    language: Optional[str] = None,
    output_dir: Optional[str] = None,
    output_formats: Sequence[str] = ("txt", "srt", "json"),
    device: str = "auto",
    compute_type: str = "auto",
    max_duration: Optional[float] = 3600.0,
    cookies: Optional[str] = None,
    keep_audio: bool = False,
    vad_filter: bool = True,
    quiet: bool = False,
    progress: Optional[ProgressCallback] = None,
) -> TranscriptionResult:
    """Download, extract audio from, and transcribe a Twitter/X video.

    If ``output_dir`` is given, transcript files are written there in each of
    ``output_formats`` and their paths recorded on the result. All intermediate
    media lives in a temp directory that is cleaned up unless ``keep_audio``.
    """
    for fmt in output_formats:
        if fmt.lower() not in formats.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported output format {fmt!r}; choose from "
                f"{', '.join(formats.SUPPORTED_FORMATS)}."
            )

    workdir = tempfile.mkdtemp(prefix="twitter_transcribe_")
    try:
        media = download_audio(url, workdir, cookies=cookies, quiet=quiet)

        wav_path = os.path.join(workdir, "audio.wav")
        duration = extract_wav(
            media.path,
            wav_path,
            max_duration=max_duration,
            duration=media.duration,
        )

        result: TranscribeResult = transcribe_wav(
            wav_path,
            model_size=model,
            device=device,
            compute_type=compute_type,
            language=language,
            vad_filter=vad_filter,
            progress=progress,
        )

        out = TranscriptionResult(
            url=media.webpage_url or url,
            text=result.text,
            segments=result.segments,
            language=result.language,
            duration=result.duration or duration,
            title=media.title,
            uploader=media.uploader,
        )

        if output_dir:
            out.output_files = _write_outputs(out, output_dir, output_formats, media)

        if keep_audio and output_dir:
            kept = os.path.join(output_dir, _basename(media, "audio") + ".wav")
            os.makedirs(output_dir, exist_ok=True)
            _copy(wav_path, kept)
            out.output_files["wav"] = kept

        return out
    finally:
        if not keep_audio:
            _rmtree(workdir)


def _write_outputs(
    result: TranscriptionResult,
    output_dir: str,
    output_formats: Sequence[str],
    media,
) -> Dict[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    base = _basename(media, "transcript")
    written: Dict[str, str] = {}
    for fmt in output_formats:
        content = formats.render(fmt, result.segments, metadata=result.metadata())
        path = os.path.join(output_dir, f"{base}.{fmt.lower()}")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        written[fmt.lower()] = path
    return written


def _basename(media, fallback: str) -> str:
    """A filesystem-safe base name derived from the media id/title."""
    raw = None
    if getattr(media, "webpage_url", None):
        # Prefer the numeric status id for stability.
        tail = media.webpage_url.rstrip("/").split("/")[-1]
        if tail.isdigit():
            raw = tail
    if not raw:
        raw = getattr(media, "title", None) or fallback
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in raw).strip("_")
    return safe or fallback


def _copy(src: str, dst: str) -> None:
    import shutil

    shutil.copyfile(src, dst)


def _rmtree(path: str) -> None:
    import shutil

    shutil.rmtree(path, ignore_errors=True)
