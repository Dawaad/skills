#!/usr/bin/env python3
"""Render a .excalidraw file to PNG for visual validation.

Usage:
    uv run python render_excalidraw.py path/to/file.excalidraw

Writes `file.png` next to the input. Uses a headless Chromium + the
Excalidraw library's `exportToCanvas` utility loaded from a CDN.

First-time setup:
    uv sync
    uv run playwright install chromium
"""
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright>=1.40"]
# ///

import asyncio
import base64
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright


EXCALIDRAW_VERSION = "0.17.6"

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>html, body { margin: 0; padding: 0; background: #ffffff; }</style>
</head>
<body>
  <div id="root"></div>
  <script type="module">
    import Excalidraw from 'https://esm.sh/@excalidraw/excalidraw@__VERSION__?bundle-deps';
    const { exportToCanvas } = Excalidraw;
    window.__renderExcalidraw = async (scene, scale) => {
      const canvas = await exportToCanvas({
        elements: scene.elements || [],
        appState: {
          ...(scene.appState || {}),
          exportBackground: true,
          exportWithDarkMode: false,
          viewBackgroundColor:
            (scene.appState && scene.appState.viewBackgroundColor) || '#ffffff',
        },
        files: scene.files || {},
        getDimensions: (width, height) => ({
          width: width * scale,
          height: height * scale,
          scale,
        }),
      });
      return canvas.toDataURL('image/png');
    };
    window.__excalidrawReady = true;
  </script>
</body>
</html>"""


async def render(input_path: Path, scale: int = 2) -> Path:
    scene = json.loads(input_path.read_text())
    if scene.get("type") != "excalidraw":
        raise ValueError(
            f"{input_path} does not look like an Excalidraw scene "
            f"(expected top-level type=\"excalidraw\", got {scene.get('type')!r})"
        )

    output_path = input_path.with_suffix(".png")
    html = HTML_TEMPLATE.replace("__VERSION__", EXCALIDRAW_VERSION)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        console_errors: list[str] = []
        page.on(
            "pageerror",
            lambda exc: console_errors.append(f"pageerror: {exc}"),
        )
        page.on(
            "console",
            lambda msg: console_errors.append(f"console.{msg.type}: {msg.text}")
            if msg.type == "error"
            else None,
        )

        await page.set_content(html, wait_until="load")
        try:
            await page.wait_for_function(
                "window.__excalidrawReady === true", timeout=30_000
            )
        except Exception:
            await browser.close()
            detail = "\n".join(console_errors) or "(no browser console output)"
            raise RuntimeError(
                "Excalidraw library did not load from CDN. Check network "
                f"access or pin a different EXCALIDRAW_VERSION.\n{detail}"
            )

        data_url = await page.evaluate(
            "([scene, scale]) => window.__renderExcalidraw(scene, scale)",
            [scene, scale],
        )
        await browser.close()

    header, _, encoded = data_url.partition(",")
    if not encoded or not header.startswith("data:image/png"):
        raise RuntimeError(f"Unexpected export payload: {header[:40]}...")

    output_path.write_bytes(base64.b64decode(encoded))
    return output_path


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help"}:
        print(__doc__)
        return 0 if len(sys.argv) >= 2 else 2

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.exists():
        print(f"error: file not found: {input_path}", file=sys.stderr)
        return 1

    scale = 2
    if len(sys.argv) >= 3:
        try:
            scale = int(sys.argv[2])
        except ValueError:
            print(f"error: scale must be an integer, got {sys.argv[2]!r}", file=sys.stderr)
            return 2

    try:
        out = asyncio.run(render(input_path, scale=scale))
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
