"""Exception hierarchy for twitter_transcribe."""


class TwitterTranscribeError(Exception):
    """Base class for all errors raised by this package."""


class DownloadError(TwitterTranscribeError):
    """Raised when the Twitter/X video cannot be downloaded."""


class AudioError(TwitterTranscribeError):
    """Raised when audio extraction/conversion fails."""


class DurationExceededError(AudioError):
    """Raised when the media is longer than the configured maximum."""

    def __init__(self, duration: float, limit: float):
        self.duration = duration
        self.limit = limit
        super().__init__(
            f"Media is {duration:.0f}s long, which exceeds the limit of "
            f"{limit:.0f}s. Raise it with --max-duration if this is intended."
        )


class TranscriptionError(TwitterTranscribeError):
    """Raised when transcription fails."""
