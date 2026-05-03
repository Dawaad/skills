# Excalidraw JSON Schema

Element-level reference for generating `.excalidraw` files by hand. This is not the full Excalidraw spec — it covers what the SKILL actually needs.

---

## File Wrapper

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "mezcorp-claude-code",
  "elements": [ /* array of elements */ ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

`version: 2` is the current element-schema version. `source` is an arbitrary tag. `files` is used for embedded images — leave empty.

---

## Common Fields (every element)

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Must be unique across the file. Use descriptive names (`"input-queue"`) not random strings. |
| `type` | string | `"rectangle"`, `"ellipse"`, `"diamond"`, `"text"`, `"arrow"`, `"line"`, `"freedraw"`, `"image"`, `"frame"`. |
| `x`, `y` | number | Top-left corner in canvas coordinates. |
| `width`, `height` | number | Size in pixels. |
| `angle` | number | Rotation in radians. `0` for axis-aligned. |
| `strokeColor` | string | Hex colour, e.g. `"#111827"`. |
| `backgroundColor` | string | Hex colour or `"transparent"`. |
| `fillStyle` | string | `"solid"`, `"hachure"`, `"cross-hatch"`, `"zigzag"`. Use `"solid"`. |
| `strokeWidth` | number | `1`, `1.5`, `2`, or `4`. Default `1.5`. |
| `strokeStyle` | string | `"solid"`, `"dashed"`, `"dotted"`. |
| `roughness` | number | `0` = clean, `1` = default sketchy, `2` = very sketchy. Use `0`. |
| `opacity` | number | `0`-`100`. |
| `groupIds` | string[] | Optional grouping. |
| `frameId` | string \| null | For elements inside a frame. |
| `roundness` | object \| null | `{ "type": 3 }` for rounded rectangles, `null` otherwise. |
| `seed` | number | Random seed; any integer is fine. Namespace by section (100xxx, 200xxx). |
| `version` | number | Per-element version counter. Start at `1`. |
| `versionNonce` | number | Any integer. |
| `isDeleted` | boolean | `false`. |
| `boundElements` | array \| null | Refs to bound text/arrows. See below. |
| `updated` | number | Epoch ms. `1700000000000` is fine. |
| `link` | string \| null | Clickable URL. |
| `locked` | boolean | `false`. |

---

## Shape-specific Fields

### `rectangle`, `ellipse`, `diamond`

No extra fields beyond the common set. Use `roundness: { "type": 3 }` for rounded rectangles; `null` for sharp corners, ellipses, and diamonds.

### `text`

| Field | Type | Notes |
|-------|------|-------|
| `text` | string | Literal text. Use `\n` for line breaks. |
| `fontSize` | number | 14, 16, 20, 24 are the usual sizes. |
| `fontFamily` | number | `1` = Virgil (hand-drawn), `2` = Helvetica, `3` = Cascadia (monospace). Use `3`. |
| `textAlign` | string | `"left"`, `"center"`, `"right"`. |
| `verticalAlign` | string | `"top"`, `"middle"`, `"bottom"`. |
| `baseline` | number | Text baseline offset. Roughly `fontSize * 0.8`. |
| `containerId` | string \| null | ID of the shape this text is bound inside. `null` for free-floating. |
| `originalText` | string | Same as `text`, pre-wrap. |
| `lineHeight` | number | `1.25` is the SKILL default. |

When a text is bound to a container:
- Set `text.containerId = <shape.id>`.
- Set `shape.boundElements = [{ "type": "text", "id": <text.id> }]`.
- Excalidraw auto-wraps to the shape width.

### `arrow`, `line`

| Field | Type | Notes |
|-------|------|-------|
| `points` | number[][] | Array of `[dx, dy]` offsets from `(x, y)`. First point is always `[0, 0]`. |
| `lastCommittedPoint` | null | `null`. |
| `startBinding` | object \| null | `{ "elementId": "<id>", "focus": 0, "gap": 4 }`. |
| `endBinding` | object \| null | Same shape as `startBinding`. |
| `startArrowhead` | string \| null | `null` (or `"arrow"`, `"bar"`, `"triangle"`, `"dot"`). |
| `endArrowhead` | string \| null | `"arrow"` for a normal flow arrow. |
| `elbowed` | boolean | `false`. `true` for right-angle routing. |

For lines, use the same fields but `startArrowhead` and `endArrowhead` = `null`.

### `frame`

A frame is a labelled container that groups and can clip its children.

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Label shown at the top of the frame. |
| `children` | — | Implicit: any element with `frameId = <frame.id>`. |

---

## Bindings

### Text inside a shape

```json
// shape
{
  "id": "shape-a",
  "type": "rectangle",
  "boundElements": [{ "type": "text", "id": "text-a" }],
  ...
}
// text
{
  "id": "text-a",
  "type": "text",
  "containerId": "shape-a",
  "text": "Hello",
  ...
}
```

### Arrow between two shapes

```json
// arrow
{
  "id": "arrow-a-b",
  "type": "arrow",
  "x": <A right edge x>,
  "y": <A centre y>,
  "points": [[0, 0], [<B.x - A.x - A.width>, <B.cy - A.cy>]],
  "startBinding": { "elementId": "shape-a", "focus": 0, "gap": 4 },
  "endBinding":   { "elementId": "shape-b", "focus": 0, "gap": 4 },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  ...
}
// optionally add to both shapes' boundElements:
// { "type": "arrow", "id": "arrow-a-b" }
```

### Label on an arrow

```json
// text
{
  "id": "label-a-b",
  "type": "text",
  "containerId": "arrow-a-b",
  "text": "sends event",
  ...
}
// arrow
{
  "id": "arrow-a-b",
  "boundElements": [{ "type": "text", "id": "label-a-b" }],
  ...
}
```

---

## Coordinate System

- Origin `(0, 0)` is top-left of the canvas.
- `+x` is right, `+y` is down.
- There is no canvas boundary — elements can live at any coordinate.
- For a comprehensive diagram, pick a working area like `(0, 0)` to `(2000, 1400)` and align everything to a 20px grid.

---

## Minimum Valid Element

A rectangle with only the required fields Excalidraw will accept:

```json
{
  "id": "r1",
  "type": "rectangle",
  "x": 100, "y": 100,
  "width": 200, "height": 80,
  "angle": 0,
  "strokeColor": "#111827",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1.5,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": 100001,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

Copy from `element-templates.md` rather than typing this out each time.
