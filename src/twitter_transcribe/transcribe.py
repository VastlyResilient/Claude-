"""Speech-to-text using faster-whisper.

faster-whisper streams an hour of audio in bounded memory: it slides a 30 s
window across the file and yields one segment at a time, so we never hold the
whole transcript's audio in RAM. Voice-activity detection (VAD) is enabled by
default to skip silence, which both speeds things up and avoids hallucinated
text during long pauses — common in hour-long talks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterator, List, Optional

from .errors import TranscriptionError


@dataclass
class Segment:
    """A single transcribed span of audio."""

    start: float  # seconds
    end: float  # seconds
    text: str


@dataclass
class TranscribeResult:
    segments: List[Segment]
    language: Optional[str]
    language_probability: Optional[float]
    duration: Optional[float]

    @property
    def text(self) -> str:
        return " ".join(s.text.strip() for s in self.segments if s.text.strip())


# Progress callbacks receive (seconds_processed, total_seconds_or_None).
ProgressCallback = Callable[[float, Optional[float]], None]


def transcribe_wav(
    wav_path: str,
    *,
    model_size: str = "base",
    device: str = "auto",
    compute_type: str = "auto",
    language: Optional[str] = None,
    vad_filter: bool = True,
    beam_size: int = 5,
    progress: Optional[ProgressCallback] = None,
) -> TranscribeResult:
    """Transcribe a 16 kHz mono WAV file.

    Parameters
    ----------
    model_size:
        Whisper model: tiny/base/small/medium/large-v3, optionally with an
        ``.en`` suffix for English-only variants.
    device:
        "cpu", "cuda", or "auto".
    compute_type:
        e.g. "int8" (CPU-friendly), "float16" (GPU), or "auto".
    language:
        ISO code (e.g. "en") to skip auto-detection, or None to detect.
    vad_filter:
        Skip non-speech regions before transcription.
    progress:
        Optional callback invoked as each segment completes, receiving the
        end timestamp reached so far and the total duration.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:  # pragma: no cover - env dependent
        raise TranscriptionError(
            "faster-whisper is not installed. Run `pip install faster-whisper` "
            "(it is listed in requirements.txt)."
        ) from exc

    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
    except Exception as exc:  # noqa: BLE001 - surface any backend error clearly
        raise TranscriptionError(
            f"Failed to load Whisper model {model_size!r}: {exc}"
        ) from exc

    try:
        segment_iter, info = model.transcribe(
            wav_path,
            language=language,
            beam_size=beam_size,
            vad_filter=vad_filter,
        )
        segments = list(_iter_segments(segment_iter, info, progress))
    except Exception as exc:  # noqa: BLE001
        raise TranscriptionError(f"Transcription failed: {exc}") from exc

    return TranscribeResult(
        segments=segments,
        language=getattr(info, "language", None),
        language_probability=getattr(info, "language_probability", None),
        duration=getattr(info, "duration", None),
    )


def _iter_segments(segment_iter, info, progress) -> Iterator[Segment]:
    total = getattr(info, "duration", None)
    for seg in segment_iter:
        if progress is not None:
            progress(float(seg.end), total)
        yield Segment(start=float(seg.start), end=float(seg.end), text=seg.text.strip())
