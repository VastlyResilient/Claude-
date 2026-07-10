"""Command-line interface for twitter_transcribe."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__
from .errors import TwitterTranscribeError
from .formats import SUPPORTED_FORMATS
from .pipeline import transcribe_url


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="twitter-transcribe",
        description=(
            "Download a Twitter/X video and transcribe it to text. "
            "Handles videos up to one hour long (raise --max-duration for more)."
        ),
    )
    p.add_argument("url", help="Twitter/X status URL, e.g. https://x.com/user/status/123")
    p.add_argument(
        "-o",
        "--output-dir",
        default="transcripts",
        help="Directory to write transcript files into (default: ./transcripts).",
    )
    p.add_argument(
        "-f",
        "--formats",
        default="txt,srt,json",
        help=(
            "Comma-separated output formats. "
            f"Choices: {', '.join(SUPPORTED_FORMATS)} (default: txt,srt,json)."
        ),
    )
    p.add_argument(
        "-m",
        "--model",
        default="base",
        help=(
            "Whisper model size: tiny, base, small, medium, large-v3 "
            "(append .en for English-only). Bigger = more accurate, slower. "
            "Default: base."
        ),
    )
    p.add_argument(
        "-l",
        "--language",
        default=None,
        help="Force a language (ISO code, e.g. en). Default: auto-detect.",
    )
    p.add_argument(
        "--device",
        default="auto",
        choices=["auto", "cpu", "cuda"],
        help="Compute device (default: auto).",
    )
    p.add_argument(
        "--compute-type",
        default="auto",
        help="faster-whisper compute type, e.g. int8, float16, auto (default: auto).",
    )
    p.add_argument(
        "--max-duration",
        type=float,
        default=3600.0,
        help="Reject media longer than this many seconds (default: 3600 = 1h). "
        "Use 0 to disable the limit.",
    )
    p.add_argument(
        "--cookies",
        default=None,
        help="Path to a Netscape cookies.txt for gated/age-restricted videos.",
    )
    p.add_argument(
        "--keep-audio",
        action="store_true",
        help="Also save the extracted 16kHz WAV alongside the transcripts.",
    )
    p.add_argument(
        "--no-vad",
        action="store_true",
        help="Disable voice-activity-detection filtering.",
    )
    p.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress progress output.",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def _make_progress(quiet: bool):
    if quiet:
        return None
    state = {"last": -1}

    def _cb(processed: float, total: Optional[float]) -> None:
        if total and total > 0:
            pct = min(100, int(processed / total * 100))
            if pct != state["last"]:
                state["last"] = pct
                print(f"\r  transcribing... {pct:3d}%", end="", file=sys.stderr, flush=True)
        else:
            print(
                f"\r  transcribing... {processed:6.0f}s",
                end="",
                file=sys.stderr,
                flush=True,
            )

    return _cb


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)

    formats = [f.strip() for f in args.formats.split(",") if f.strip()]
    max_duration = None if args.max_duration == 0 else args.max_duration

    if not args.quiet:
        print(f"Downloading and transcribing {args.url} ...", file=sys.stderr)

    try:
        result = transcribe_url(
            args.url,
            model=args.model,
            language=args.language,
            output_dir=args.output_dir,
            output_formats=formats,
            device=args.device,
            compute_type=args.compute_type,
            max_duration=max_duration,
            cookies=args.cookies,
            keep_audio=args.keep_audio,
            vad_filter=not args.no_vad,
            quiet=args.quiet,
            progress=_make_progress(args.quiet),
        )
    except TwitterTranscribeError as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:  # pragma: no cover
        print("\nInterrupted.", file=sys.stderr)
        return 130

    if not args.quiet:
        print("", file=sys.stderr)  # newline after progress
        lang = result.language or "unknown"
        dur = result.duration or 0
        print(
            f"Done. Language: {lang}, duration: {dur:.0f}s, "
            f"{len(result.segments)} segments.",
            file=sys.stderr,
        )
        for fmt, path in result.output_files.items():
            print(f"  wrote {fmt}: {path}", file=sys.stderr)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
