#!/usr/bin/env python3
"""Multi-window Shazam scan.

Slide a short fingerprinting window across the full reel audio and dedupe adjacent
matches. The reel-extractor's default single-shot Shazam pass only catches one bed —
long-form / cinematic reels often swap music 2-5 times and each cue maps to a
narrative beat. Missing them flattens downstream synthesis.

Usage:
    python3 multi_window_shazam.py <audio.wav> [--stride 15] [--window 12] [--json]

Prints a human-readable summary by default, or JSON with --json.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict


@dataclass
class Cue:
    start_s: int
    end_s: int
    title: str | None
    artist: str | None
    shazam_url: str | None = None
    genre: str | None = None


async def _identify_window(path: str) -> tuple[str | None, str | None, str | None, str | None]:
    from ShazamAPI import Shazam  # type: ignore

    with open(path, "rb") as f:
        data = f.read()

    try:
        gen = Shazam(data).recognizeSong()
        for _, match in gen:
            track = match.get("track") or {}
            if not track:
                continue
            title = track.get("title")
            artist = track.get("subtitle")
            url = track.get("url")
            genre = None
            genres = track.get("genres") or {}
            if isinstance(genres, dict):
                genre = genres.get("primary")
            return title, artist, url, genre
    except Exception:
        pass
    return None, None, None, None


def _duration_s(audio_path: str) -> float:
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            audio_path,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(out.stdout.strip())


def _slice(audio_path: str, start: int, length: int, out_path: str) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(start),
            "-t",
            str(length),
            "-i",
            audio_path,
            "-ac",
            "1",
            "-ar",
            "44100",
            out_path,
        ],
        check=True,
        capture_output=True,
    )


async def scan(audio_path: str, stride: int = 15, window: int = 12) -> list[Cue]:
    duration = int(_duration_s(audio_path))
    cues: list[Cue] = []

    with tempfile.TemporaryDirectory() as tmp:
        start = 0
        while start < duration:
            length = min(window, duration - start)
            if length < 4:
                break
            chunk = os.path.join(tmp, f"chunk_{start}.wav")
            _slice(audio_path, start, length, chunk)
            title, artist, url, genre = await _identify_window(chunk)
            cues.append(
                Cue(
                    start_s=start,
                    end_s=start + length,
                    title=title,
                    artist=artist,
                    shazam_url=url,
                    genre=genre,
                )
            )
            start += stride

    return _dedupe_adjacent(cues)


def _dedupe_adjacent(cues: list[Cue]) -> list[Cue]:
    """Merge adjacent windows that match the same (title, artist).

    Collapses the sliding-window overlap into single cue spans. Unidentified
    windows (title is None) are kept as gaps — a viewer reads those as
    speech-dominant / no-distinct-bed regions, which is itself signal.
    """
    if not cues:
        return cues

    merged: list[Cue] = [cues[0]]
    for cue in cues[1:]:
        prev = merged[-1]
        same_match = (
            cue.title is not None
            and cue.title == prev.title
            and cue.artist == prev.artist
        )
        if same_match:
            prev.end_s = cue.end_s
        else:
            merged.append(cue)
    return merged


def _format_timecode(seconds: int) -> str:
    return f"{seconds // 60}:{seconds % 60:02d}"


def _render_markdown(cues: list[Cue]) -> str:
    identified = [c for c in cues if c.title]
    if not identified:
        return "No distinct music tracks identified across the runtime."

    lines = [f"Multi-window scan identified {len(identified)} distinct cue(s):", ""]
    for cue in cues:
        span = f"{_format_timecode(cue.start_s)}–{_format_timecode(cue.end_s)}"
        if cue.title:
            suffix = f" ({cue.genre})" if cue.genre else ""
            url = f" — {cue.shazam_url}" if cue.shazam_url else ""
            lines.append(f"- {span} — {cue.title} — {cue.artist}{suffix}{url}")
        else:
            lines.append(f"- {span} — *(no match — speech-dominant or no distinct bed)*")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", help="Path to audio file (wav/m4a/mp3)")
    parser.add_argument("--stride", type=int, default=15, help="Seconds between window starts (default 15)")
    parser.add_argument("--window", type=int, default=12, help="Seconds per window (default 12)")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    args = parser.parse_args()

    cues = asyncio.run(scan(args.audio, stride=args.stride, window=args.window))

    if args.json:
        print(json.dumps([asdict(c) for c in cues], indent=2))
    else:
        print(_render_markdown(cues))


if __name__ == "__main__":
    main()
