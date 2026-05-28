#!/usr/bin/env python3
"""
Extract transcript + metadata from any yt-dlp-supported video URL.

Strategy:
  1. yt-dlp metadata pass (title, channel, duration, chapters, upload date)
  2. Try auto/manual captions via yt-dlp (fast, free, no GPU)
  3. If no captions, download audio and whisper-transcribe (slow, accurate)

Output layout (--save-dir <dir>):
  <save-dir>/<slug>-<YYYY-MM-DD>/
    transcript.md      # timestamped lines
    transcript.vtt     # raw subtitle file (if captions path)
    metadata.json      # full yt-dlp .info.json
    audio.m4a          # only if whisper was used
    chapters.json      # extracted chapter list (may be empty)

Prints final bundle path to stdout.
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys, shutil, tempfile
from pathlib import Path
from datetime import datetime


def slugify(text: str, max_len: int = 60) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:max_len] or "video"


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def fetch_metadata(url: str) -> dict:
    r = run(["yt-dlp", "-J", "--no-warnings", "--skip-download", url])
    if r.returncode != 0:
        sys.exit(f"yt-dlp metadata failed:\n{r.stderr}")
    return json.loads(r.stdout)


def try_captions(url: str, workdir: Path) -> Path | None:
    """Pull manual subs first, then auto-generated. Returns VTT path or None."""
    for kind in ("--write-subs", "--write-auto-subs"):
        r = run([
            "yt-dlp", kind, "--sub-langs", "en.*,en",
            "--skip-download", "--sub-format", "vtt/srt/best",
            "-o", str(workdir / "%(id)s.%(ext)s"), url,
        ])
        if r.returncode != 0:
            continue
        vtts = list(workdir.glob("*.en*.vtt")) + list(workdir.glob("*.en.vtt"))
        if vtts:
            return vtts[0]
    return None


def vtt_to_lines(vtt_path: Path) -> list[tuple[str, str]]:
    """Parse VTT into [(timestamp, text)] pairs, deduped."""
    lines: list[tuple[str, str]] = []
    seen_text: set[str] = set()
    cur_ts = None
    buf: list[str] = []

    def flush():
        nonlocal cur_ts, buf
        if cur_ts and buf:
            text = " ".join(buf).strip()
            # strip inline <c> tags and timestamps
            text = re.sub(r"<[^>]+>", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            if text and text not in seen_text:
                seen_text.add(text)
                lines.append((cur_ts, text))
        cur_ts, buf = None, []

    for raw in vtt_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "-->" in raw:
            flush()
            cur_ts = raw.split("-->")[0].strip().split(".")[0]  # HH:MM:SS
            # YouTube often uses HH:MM:SS.mmm — normalise to HH:MM:SS
            if cur_ts.count(":") == 2 and cur_ts.startswith("00:"):
                cur_ts = cur_ts[3:]  # MM:SS
        elif raw.strip() and not raw.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            buf.append(raw.strip())
        else:
            flush()
    flush()
    return lines


def whisper_transcribe(url: str, workdir: Path) -> tuple[Path, Path]:
    """Download audio and run whisper. Returns (audio_path, transcript_txt)."""
    audio_tmpl = workdir / "audio.%(ext)s"
    r = run([
        "yt-dlp", "-x", "--audio-format", "m4a", "--audio-quality", "0",
        "-o", str(audio_tmpl), url,
    ])
    if r.returncode != 0:
        sys.exit(f"audio download failed:\n{r.stderr}")
    audio = next(workdir.glob("audio.*"))
    print(f"  whisper transcribing {audio.name}…", file=sys.stderr)
    r = run([
        "whisper", str(audio), "--model", "base", "--output_format", "vtt",
        "--output_dir", str(workdir), "--language", "en",
    ])
    if r.returncode != 0:
        sys.exit(f"whisper failed:\n{r.stderr}")
    vtt = next(workdir.glob("audio.vtt"))
    return audio, vtt


def write_transcript_md(out: Path, lines: list[tuple[str, str]], meta: dict) -> None:
    title = meta.get("title", "untitled")
    channel = meta.get("channel") or meta.get("uploader") or "unknown"
    upload = meta.get("upload_date", "")
    if len(upload) == 8:
        upload = f"{upload[:4]}-{upload[4:6]}-{upload[6:]}"
    dur = meta.get("duration", 0)
    dur_str = f"{dur // 60}:{dur % 60:02d}"
    body = [
        f"# {title}",
        "",
        f"- channel: {channel}",
        f"- duration: {dur_str}",
        f"- uploaded: {upload}",
        f"- url: {meta.get('webpage_url', '')}",
        "",
        "## Transcript",
        "",
    ]
    for ts, text in lines:
        body.append(f"`[{ts}]` {text}")
    out.write_text("\n".join(body) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--save-dir", default=str(Path.home() / "Documents/wiki/_Attachments/transcripts"))
    ap.add_argument("--force-whisper", action="store_true",
                    help="Skip caption attempt; always whisper-transcribe")
    args = ap.parse_args()

    save_root = Path(args.save_dir).expanduser()
    save_root.mkdir(parents=True, exist_ok=True)

    print(f"fetching metadata for {args.url}", file=sys.stderr)
    meta = fetch_metadata(args.url)

    slug = slugify(f"{meta.get('channel') or meta.get('uploader') or 'video'}-{meta.get('title','')}")
    upload = meta.get("upload_date", "")
    upload_iso = f"{upload[:4]}-{upload[4:6]}-{upload[6:]}" if len(upload) == 8 else datetime.now().strftime("%Y-%m-%d")
    bundle = save_root / f"{slug}-{upload_iso}"
    bundle.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        vtt_path: Path | None = None
        used_whisper = False

        if not args.force_whisper:
            print("trying captions…", file=sys.stderr)
            vtt_path = try_captions(args.url, workdir)

        if vtt_path is None:
            print("no captions, falling back to whisper…", file=sys.stderr)
            audio, vtt_path = whisper_transcribe(args.url, workdir)
            shutil.copy(audio, bundle / audio.name)
            used_whisper = True

        shutil.copy(vtt_path, bundle / "transcript.vtt")
        lines = vtt_to_lines(vtt_path)

    (bundle / "metadata.json").write_text(json.dumps(meta, indent=2, default=str))
    (bundle / "chapters.json").write_text(json.dumps(meta.get("chapters") or [], indent=2))
    write_transcript_md(bundle / "transcript.md", lines, meta)

    print(f"\nBundle: {bundle}")
    print(f"  transcript: {bundle / 'transcript.md'}")
    print(f"  lines: {len(lines)}")
    print(f"  chapters: {len(meta.get('chapters') or [])}")
    print(f"  source: {'whisper' if used_whisper else 'captions'}")


if __name__ == "__main__":
    main()
