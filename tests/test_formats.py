import json

from twitter_transcribe.formats import (
    SUPPORTED_FORMATS,
    _fmt_timestamp,
    render,
    to_json,
    to_srt,
    to_text,
    to_vtt,
)
from twitter_transcribe.transcribe import Segment


SEGMENTS = [
    Segment(start=0.0, end=2.5, text="Hello world."),
    Segment(start=2.5, end=3661.25, text="Still talking an hour later."),
    Segment(start=3661.25, end=3663.0, text="   "),  # blank -> skipped
]


def test_fmt_timestamp_srt_and_vtt():
    assert _fmt_timestamp(0, sep=",") == "00:00:00,000"
    # 3661.25s = 1h 1m 1s 250ms -> proves hour-long timestamps format correctly
    assert _fmt_timestamp(3661.25, sep=",") == "01:01:01,250"
    assert _fmt_timestamp(3661.25, sep=".") == "01:01:01.250"


def test_fmt_timestamp_rounding_and_negative():
    assert _fmt_timestamp(-5, sep=",") == "00:00:00,000"
    assert _fmt_timestamp(1.9995, sep=",") == "00:00:02,000"


def test_to_text_skips_blank():
    text = to_text(SEGMENTS)
    assert "Hello world." in text
    assert "Still talking" in text
    assert text.count("\n") == 2  # two non-blank lines, each newline-terminated


def test_to_srt_numbering_and_arrows():
    srt = to_srt(SEGMENTS)
    assert srt.startswith("1\n")
    assert "00:00:00,000 --> 00:00:02,500" in srt
    assert "01:01:01,250" in srt
    # blank segment is dropped, so max index is 2
    assert "\n2\n" in srt
    assert "\n3\n" not in srt


def test_to_vtt_header():
    vtt = to_vtt(SEGMENTS)
    assert vtt.startswith("WEBVTT")
    assert "00:00:00.000 --> 00:00:02.500" in vtt


def test_to_json_roundtrip():
    meta = {"url": "https://x.com/u/status/1", "language": "en"}
    payload = json.loads(to_json(SEGMENTS, metadata=meta))
    assert payload["url"] == "https://x.com/u/status/1"
    assert payload["language"] == "en"
    # blank segment retained in JSON (structured data), so 3 entries
    assert len(payload["segments"]) == 3
    assert payload["segments"][0]["text"] == "Hello world."


def test_render_dispatch_all_formats():
    meta = {"url": "u"}
    for fmt in SUPPORTED_FORMATS:
        out = render(fmt, SEGMENTS, metadata=meta)
        assert isinstance(out, str) and out


def test_render_rejects_unknown():
    try:
        render("mp3", SEGMENTS, metadata={})
    except ValueError as exc:
        assert "Unsupported format" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")
