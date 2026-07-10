# twitter-transcribe

Transcribe Twitter/X videos — up to one hour long — into plain text, SRT/VTT
subtitles, and structured JSON.

The pipeline is: **download the video** (yt-dlp) → **extract 16 kHz mono audio**
(ffmpeg) → **transcribe** (faster-whisper) → **write transcript files**. Because
transcription runs locally with `faster-whisper`, there is no per-file API size
limit: it streams an hour of audio in bounded memory, sliding a 30-second window
across the file and emitting one segment at a time.

## Why faster-whisper (and not a hosted API)

Hosted speech-to-text endpoints (e.g. OpenAI's Whisper API) cap uploads at
25 MB, which an hour-long video blows past — you'd have to split and stitch.
`faster-whisper` runs the Whisper models locally with CTranslate2, handles
arbitrarily long audio natively, needs no API key, and runs on CPU (int8) or
GPU (float16).

## Install

Requires **Python 3.9+** and **ffmpeg** (which provides `ffmpeg` and `ffprobe`)
on your `PATH`.

```bash
# system dependency
sudo apt-get install ffmpeg        # Debian/Ubuntu
# brew install ffmpeg              # macOS

# the package + its Python dependencies (yt-dlp, faster-whisper)
pip install -e .
```

## Usage

```bash
# Basic: writes txt, srt, json into ./transcripts/
twitter-transcribe https://x.com/SpaceX/status/1732824684683784516

# Pick a bigger, more accurate model and only emit an SRT
twitter-transcribe <url> --model small --formats srt

# Force English, use CPU int8, and keep the extracted audio
twitter-transcribe <url> -l en --device cpu --compute-type int8 --keep-audio

# Gated / age-restricted video: pass exported cookies
twitter-transcribe <url> --cookies cookies.txt

# Allow videos longer than one hour (limit is in seconds; 0 disables it)
twitter-transcribe <url> --max-duration 7200
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-o, --output-dir` | `transcripts` | Where transcript files are written. |
| `-f, --formats` | `txt,srt,json` | Any of `txt`, `srt`, `vtt`, `json`. |
| `-m, --model` | `base` | `tiny`/`base`/`small`/`medium`/`large-v3` (`.en` for English-only). |
| `-l, --language` | auto | Force an ISO language code (e.g. `en`) to skip detection. |
| `--device` | `auto` | `auto`, `cpu`, or `cuda`. |
| `--compute-type` | `auto` | e.g. `int8` (CPU), `float16` (GPU). |
| `--max-duration` | `3600` | Reject longer media (seconds); `0` disables. |
| `--cookies` | — | Netscape `cookies.txt` for gated videos. |
| `--keep-audio` | off | Also save the extracted WAV. |
| `--no-vad` | off | Disable voice-activity-detection filtering. |

The larger the model, the more accurate and the slower. `tiny`/`base` are good
for quick drafts; `small`/`medium` trade speed for quality; `large-v3` is most
accurate. Voice-activity detection is on by default — it skips silence, which
speeds up long talks and avoids Whisper "hallucinating" text during pauses.

## Library API

```python
from twitter_transcribe import transcribe_url

result = transcribe_url(
    "https://x.com/SpaceX/status/1732824684683784516",
    model="base",
    output_dir="transcripts",
    output_formats=("txt", "srt", "json"),
)

print(result.language, result.duration)
print(result.text)
for seg in result.segments:
    print(f"[{seg.start:.1f}-{seg.end:.1f}] {seg.text}")
```

`transcribe_url` returns a `TranscriptionResult` with `.text`, `.segments`
(each a `Segment(start, end, text)`), `.language`, `.duration`, source
metadata (`.title`, `.uploader`, `.url`), and `.output_files` mapping each
format to its written path.

## Package layout

```
src/twitter_transcribe/
  download.py    # yt-dlp: fetch the best audio stream from a status URL
  audio.py       # ffmpeg/ffprobe: probe duration, convert to 16 kHz mono WAV
  transcribe.py  # faster-whisper: streaming transcription -> Segments
  formats.py     # render Segments as txt / srt / vtt / json
  pipeline.py    # orchestrate the stages; write outputs; clean up temp files
  cli.py         # argparse command-line entry point
```

## Development

```bash
pip install -e '.[dev]'
pytest
```

The test suite covers timestamp formatting, all output renderers, URL
validation, and full pipeline orchestration (with the network/model stages
stubbed, so it runs offline in well under a second).

## Notes & limits

- **Guest access.** yt-dlp fetches most public videos without login. Some
  videos are gated; export your browser cookies and pass `--cookies`.
- **First run downloads a model.** faster-whisper fetches the chosen Whisper
  model from the Hugging Face hub the first time and caches it locally.
- **Accuracy** depends on model size, audio quality, accents and background
  noise — pick a larger `--model` when transcripts look rough.
