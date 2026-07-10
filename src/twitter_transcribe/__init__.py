"""Transcribe Twitter/X videos (up to one hour long) to text.

Public API::

    from twitter_transcribe import transcribe_url, TranscriptionResult

    result = transcribe_url("https://x.com/user/status/123", model="base")
    print(result.text)
"""

from .errors import (
    TwitterTranscribeError,
    DownloadError,
    AudioError,
    TranscriptionError,
    DurationExceededError,
)
from .pipeline import transcribe_url, TranscriptionResult
from .transcribe import Segment

__all__ = [
    "transcribe_url",
    "TranscriptionResult",
    "Segment",
    "TwitterTranscribeError",
    "DownloadError",
    "AudioError",
    "TranscriptionError",
    "DurationExceededError",
]

__version__ = "0.1.0"
