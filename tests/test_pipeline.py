"""Pipeline orchestration test with the heavy I/O stages stubbed out.

We don't hit the network or load a Whisper model here; we monkeypatch the
download/audio/transcribe stages so the test verifies wiring, output-file
writing, and temp-dir cleanup deterministically.
"""

import os

import twitter_transcribe.pipeline as pipeline
from twitter_transcribe.download import DownloadedMedia
from twitter_transcribe.transcribe import Segment, TranscribeResult


def _fake_download(url, dest_dir, *, cookies=None, quiet=False):
    path = os.path.join(dest_dir, "123.m4a")
    with open(path, "wb") as fh:
        fh.write(b"\x00\x00")
    return DownloadedMedia(
        path=path,
        title="A test clip",
        duration=42.0,
        uploader="tester",
        webpage_url="https://x.com/tester/status/123",
    )


def _fake_extract(src_path, dest_path, *, max_duration=3600.0, duration=None):
    with open(dest_path, "wb") as fh:
        fh.write(b"RIFF")
    return duration or 42.0


def _fake_transcribe(wav_path, **kwargs):
    if kwargs.get("progress"):
        kwargs["progress"](42.0, 42.0)
    return TranscribeResult(
        segments=[
            Segment(0.0, 2.0, "Hello."),
            Segment(2.0, 42.0, "Goodbye."),
        ],
        language="en",
        language_probability=0.99,
        duration=42.0,
    )


def test_pipeline_writes_outputs_and_cleans_up(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "download_audio", _fake_download)
    monkeypatch.setattr(pipeline, "extract_wav", _fake_extract)
    monkeypatch.setattr(pipeline, "transcribe_wav", _fake_transcribe)

    created_tmpdirs = []
    real_mkdtemp = pipeline.tempfile.mkdtemp

    def _tracking_mkdtemp(*a, **k):
        d = real_mkdtemp(*a, **k)
        created_tmpdirs.append(d)
        return d

    monkeypatch.setattr(pipeline.tempfile, "mkdtemp", _tracking_mkdtemp)

    out_dir = tmp_path / "transcripts"
    result = pipeline.transcribe_url(
        "https://x.com/tester/status/123",
        output_dir=str(out_dir),
        output_formats=("txt", "srt", "json"),
    )

    assert result.language == "en"
    assert result.title == "A test clip"
    assert "Hello." in result.text and "Goodbye." in result.text
    assert set(result.output_files) == {"txt", "srt", "json"}

    # Files named after the numeric status id, and actually written.
    for fmt, path in result.output_files.items():
        assert os.path.isfile(path)
        assert os.path.basename(path) == f"123.{fmt}"

    # Temp working dir removed (keep_audio defaults to False).
    for d in created_tmpdirs:
        assert not os.path.exists(d)


def test_pipeline_rejects_bad_format(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "download_audio", _fake_download)
    monkeypatch.setattr(pipeline, "extract_wav", _fake_extract)
    monkeypatch.setattr(pipeline, "transcribe_wav", _fake_transcribe)
    try:
        pipeline.transcribe_url(
            "https://x.com/tester/status/123", output_formats=("mp3",)
        )
    except ValueError as exc:
        assert "Unsupported output format" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")
