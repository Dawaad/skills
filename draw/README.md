# draw — Excalidraw Diagram Skill

Create `.excalidraw` JSON files that argue visually, then render them to PNG for validation.

See `SKILL.md` for the design methodology. This README only covers **setup**.

---

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) (Python package manager)
- Network access to `esm.sh` (Excalidraw library is loaded from CDN at render time)

---

## First-Time Setup

From the repo root:

```bash
cd .claude/skills/draw/references
uv sync
uv run playwright install chromium
```

`uv sync` installs Playwright into a local `.venv`. `playwright install chromium` downloads the browser binary (~170 MB, one-time).

---

## Customising the Brand Palette

Edit `references/color-palette.md`. That file is the single source of truth for every colour the skill uses. The rest of `SKILL.md` is universal methodology.

---

## Rendering

From any working directory:

```bash
uv run --project .claude/skills/draw/references \
  python .claude/skills/draw/references/render_excalidraw.py \
  path/to/diagram.excalidraw
```

Or, if you are already `cd`'d into `references/`:

```bash
uv run python render_excalidraw.py ../../../../path/to/diagram.excalidraw
```

Writes `diagram.png` next to the input. Pass a second arg to change the export scale (default `2`).

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Design philosophy, patterns, and generation workflow |
| `README.md` | Setup and tooling (this file) |
| `references/color-palette.md` | Brand palette — **edit this to re-skin** |
| `references/layout-gotchas.md` | 10 common render pitfalls and fixes |
| `references/json-schema.md` | Excalidraw element schema reference |
| `references/element-templates.md` | Copy-paste JSON for shapes and patterns |
| `references/render_excalidraw.py` | Headless PNG renderer |
| `references/pyproject.toml` | Python dependencies for the renderer |

---

## Troubleshooting

**"Excalidraw library did not load from CDN"**
The script pins `@excalidraw/excalidraw@0.17.6`. If `esm.sh` is blocked on your network or the pinned version is unreachable, edit `EXCALIDRAW_VERSION` at the top of `render_excalidraw.py`.

**Playwright errors about missing browser**
Re-run `uv run playwright install chromium`.

**PNG is blank / wrong size**
Make sure your `.excalidraw` file has a top-level `"type": "excalidraw"` and a non-empty `elements` array. Invalid scenes export a blank canvas.
