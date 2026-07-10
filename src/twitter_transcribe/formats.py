"""Serialise transcription segments to text, JSON, SRT and WebVTT."""

from __future__ import annotations

import json
from typing import Dict, List, Sequence

from .transcribe import Segment

SUPPORTED_FORMATS = ("txt", "json", "srt", "vtt")


def _fmt_timestamp(seconds: float, *, sep: str) -> str:
    """Format seconds as HH:MM:SS<sep>mmm (sep is ',' for SRT, '.' for VTT)."""
    if seconds < 0:
        seconds = 0.0
    millis = int(round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{millis:03d}"


def to_text(segments: Sequence[Segment]) -> str:
    """Plain running transcript, one segment per line."""
    return "\n".join(s.text.strip() for s in segments if s.text.strip()) + "\n"


def to_srt(segments: Sequence[Segment]) -> str:
    lines: List[str] = []
    index = 1
    for seg in segments:
        if not seg.text.strip():
            continue
        start = _fmt_timestamp(seg.start, sep=",")
        end = _fmt_timestamp(seg.end, sep=",")
        lines.append(str(index))
        lines.append(f"{start} --> {end}")
        lines.append(seg.text.strip())
        lines.append("")
        index += 1
    return "\n".join(lines)


def to_vtt(segments: Sequence[Segment]) -> str:
    lines: List[str] = ["WEBVTT", ""]
    for seg in segments:
        if not seg.text.strip():
            continue
        start = _fmt_timestamp(seg.start, sep=".")
        end = _fmt_timestamp(seg.end, sep=".")
        lines.append(f"{start} --> {end}")
        lines.append(seg.text.strip())
        lines.append("")
    return "\n".join(lines)


def to_json(segments: Sequence[Segment], *, metadata: Dict) -> str:
    payload = {
        **metadata,
        "segments": [
            {"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip()}
            for s in segments
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render(fmt: str, segments: Sequence[Segment], *, metadata: Dict) -> str:
    fmt = fmt.lower()
    if fmt == "txt":
        return to_text(segments)
    if fmt == "srt":
        return to_srt(segments)
    if fmt == "vtt":
        return to_vtt(segments)
    if fmt == "json":
        return to_json(segments, metadata=metadata)
    raise ValueError(
        f"Unsupported format {fmt!r}; choose from {', '.join(SUPPORTED_FORMATS)}."
    )
