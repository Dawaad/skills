# Colour Palette

This file is the **single source of truth** for all colour choices in generated diagrams. Edit it to change the brand style. The SKILL reads it before every diagram.

Colours are organised by **semantic role**, not by hue. Pick the role first, then look up the hex.

---

## Canvas

| Role | Hex | Notes |
|------|-----|-------|
| Background | `#ffffff` | `viewBackgroundColor` in `appState` |
| Background (dark variant) | `#0f1115` | Use when the diagram is a dark-themed explainer |

---

## Text

| Role | Hex | Size hint |
|------|-----|-----------|
| Title | `#111827` | 20-24px |
| Subtitle | `#374151` | 16-18px |
| Body / label | `#4b5563` | 14-16px |
| Muted / annotation | `#9ca3af` | 12-14px |
| On light fills | `#111827` | inside any light shape |
| On dark fills | `#f3f4f6` | inside any dark shape |
| Accent (callouts) | `#b91c1c` | sparingly, for emphasis |

---

## Strokes

All strokes default to `strokeWidth: 1.5`, `strokeStyle: "solid"`, `roughness: 0`.

| Role | Hex |
|------|-----|
| Primary border | `#111827` |
| Secondary border | `#6b7280` |
| Subtle / guide | `#d1d5db` |
| Dashed zone | `#9ca3af` (with `strokeStyle: "dashed"`) |
| Arrow (flow) | `#111827` |
| Arrow (secondary flow) | `#6b7280` |

---

## Fills — Categorical (6 roles)

Use these to distinguish **kinds of things** in the diagram. Each has a light fill + a matching stroke. Keep usage consistent across the whole file: if "input" is blue in one section, it must be blue everywhere.

| Role | Fill | Stroke | Typical use |
|------|------|--------|-------------|
| Neutral | `#f3f4f6` | `#9ca3af` | generic shapes, containers |
| Primary (blue) | `#dbeafe` | `#2563eb` | inputs, sources, users |
| Success (green) | `#dcfce7` | `#16a34a` | outputs, results, success paths |
| Warning (amber) | `#fef3c7` | `#d97706` | caveats, intermediate state |
| Danger (red) | `#fee2e2` | `#dc2626` | errors, failure paths, anti-patterns |
| Info (violet) | `#ede9fe` | `#7c3aed` | metadata, annotations, side channels |

---

## Fills — Zones / Sections

Labelled regions that group related components. Use **very low opacity** so they read as background, not foreground.

| Role | Fill | Stroke | Stroke style |
|------|------|--------|--------------|
| Section zone | `#f9fafb` | `#d1d5db` | `dashed` |
| Emphasised zone | `#eef2ff` | `#6366f1` | `dashed` |

Apply `opacity: 40` on zones if text/shapes inside compete for attention.

---

## Evidence Artifacts (Code, JSON, Data blocks)

Dark rectangle + syntax-coloured text. These are **always** rendered in the dark scheme regardless of canvas background so they read as "terminal output" / "source material".

| Role | Hex |
|------|-----|
| Block background | `#0f172a` |
| Block border | `#334155` |
| Default text | `#e2e8f0` |
| Keyword / type | `#f472b6` |
| String | `#a7f3d0` |
| Number / constant | `#fbbf24` |
| Comment | `#64748b` |
| Punctuation | `#94a3b8` |

Use `fontFamily: 3` (monospace) and `fontSize: 13-14`.

---

## UI Mockup Colours

When drawing a mock of a real UI inside the diagram:

| Role | Hex |
|------|-----|
| App chrome | `#ffffff` |
| App border | `#e5e7eb` |
| Sidebar / header | `#f9fafb` |
| Primary button | `#2563eb` (text `#ffffff`) |
| Secondary button | `#f3f4f6` (text `#111827`) |
| Placeholder text | `#9ca3af` |

---

## Do / Don't

- **Do** pick the role first, then look up the hex. If no role fits, add a role — don't invent a one-off colour.
- **Do** use the same category colour for the same concept across the whole diagram.
- **Don't** use saturated fills as large backgrounds. Light fills + dark strokes is the rule.
- **Don't** rely on colour alone to carry meaning — always pair with shape, position, or label (accessibility).
