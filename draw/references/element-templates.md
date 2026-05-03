# Element Templates

Copy-paste JSON for the most common elements. Replace `__ID__`, `__SEED__`, coordinates, and colours with real values. Leave the other fields as-is.

All templates assume:
- `roughness: 0` (clean aesthetic)
- `fontFamily: 3` (monospace)
- `strokeWidth: 1.5`
- `updated: 1700000000000` (any fixed epoch is fine)

---

## Rectangle (rounded, neutral)

```json
{
  "id": "__ID__",
  "type": "rectangle",
  "x": 0, "y": 0,
  "width": 240, "height": 80,
  "angle": 0,
  "strokeColor": "#111827",
  "backgroundColor": "#f3f4f6",
  "fillStyle": "solid",
  "strokeWidth": 1.5,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

## Rectangle (evidence / code block)

```json
{
  "id": "__ID__",
  "type": "rectangle",
  "x": 0, "y": 0,
  "width": 360, "height": 140,
  "angle": 0,
  "strokeColor": "#334155",
  "backgroundColor": "#0f172a",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

## Ellipse (start / end node)

```json
{
  "id": "__ID__",
  "type": "ellipse",
  "x": 0, "y": 0,
  "width": 120, "height": 60,
  "angle": 0,
  "strokeColor": "#2563eb",
  "backgroundColor": "#dbeafe",
  "fillStyle": "solid",
  "strokeWidth": 1.5,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

## Ellipse (timeline marker, tiny)

```json
{
  "id": "__ID__",
  "type": "ellipse",
  "x": 0, "y": 0,
  "width": 14, "height": 14,
  "angle": 0,
  "strokeColor": "#111827",
  "backgroundColor": "#111827",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

## Diamond (decision)

```json
{
  "id": "__ID__",
  "type": "diamond",
  "x": 0, "y": 0,
  "width": 180, "height": 100,
  "angle": 0,
  "strokeColor": "#d97706",
  "backgroundColor": "#fef3c7",
  "fillStyle": "solid",
  "strokeWidth": 1.5,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

## Zone (dashed section background)

Place first in the `elements` array so it renders behind its contents.

```json
{
  "id": "__ID__",
  "type": "rectangle",
  "x": 0, "y": 0,
  "width": 800, "height": 400,
  "angle": 0,
  "strokeColor": "#9ca3af",
  "backgroundColor": "#f9fafb",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "dashed",
  "roughness": 0,
  "opacity": 40,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

## Text (free-floating title)

```json
{
  "id": "__ID__",
  "type": "text",
  "x": 0, "y": 0,
  "width": 400, "height": 32,
  "angle": 0,
  "strokeColor": "#111827",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "text": "Section Title",
  "fontSize": 22,
  "fontFamily": 3,
  "textAlign": "left",
  "verticalAlign": "top",
  "baseline": 18,
  "containerId": null,
  "originalText": "Section Title",
  "lineHeight": 1.25
}
```

## Text (bound inside a shape)

Also add `{ "type": "text", "id": "__ID__" }` to the container's `boundElements` array.

```json
{
  "id": "__ID__",
  "type": "text",
  "x": 0, "y": 0,
  "width": 200, "height": 20,
  "angle": 0,
  "strokeColor": "#111827",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "text": "Label",
  "fontSize": 16,
  "fontFamily": 3,
  "textAlign": "center",
  "verticalAlign": "middle",
  "baseline": 13,
  "containerId": "__CONTAINER_ID__",
  "originalText": "Label",
  "lineHeight": 1.25
}
```

## Arrow (flow, A -> B)

```json
{
  "id": "__ID__",
  "type": "arrow",
  "x": 0, "y": 0,
  "width": 200, "height": 0,
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
  "roundness": { "type": 2 },
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "points": [[0, 0], [200, 0]],
  "lastCommittedPoint": null,
  "startBinding": { "elementId": "__SOURCE_ID__", "focus": 0, "gap": 4 },
  "endBinding":   { "elementId": "__TARGET_ID__", "focus": 0, "gap": 4 },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": false
}
```

## Line (structural, no arrowhead)

```json
{
  "id": "__ID__",
  "type": "line",
  "x": 0, "y": 0,
  "width": 400, "height": 0,
  "angle": 0,
  "strokeColor": "#d1d5db",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": __SEED__,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "points": [[0, 0], [400, 0]],
  "lastCommittedPoint": null,
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": null,
  "elbowed": false
}
```

---

## Patterns — Copy Whole Blocks

### Fan-out (1 source, 3 targets)

Replace `__SRC__`, `__T1__`, `__T2__`, `__T3__` with IDs. Seed namespace `1xxxxx`.

```json
[
  { "id": "__SRC__", "type": "rectangle", "x": 100, "y": 300, "width": 200, "height": 80, "...": "rectangle-neutral", "seed": 100001 },
  { "id": "__T1__",  "type": "rectangle", "x": 500, "y": 180, "width": 200, "height": 80, "...": "rectangle-neutral", "seed": 100002 },
  { "id": "__T2__",  "type": "rectangle", "x": 500, "y": 300, "width": 200, "height": 80, "...": "rectangle-neutral", "seed": 100003 },
  { "id": "__T3__",  "type": "rectangle", "x": 500, "y": 420, "width": 200, "height": 80, "...": "rectangle-neutral", "seed": 100004 },
  { "id": "a1", "type": "arrow", "x": 300, "y": 340, "points": [[0,0],[200,-120]], "startBinding": {"elementId":"__SRC__","focus":0,"gap":4}, "endBinding": {"elementId":"__T1__","focus":0,"gap":4}, "endArrowhead":"arrow", "seed": 100005 },
  { "id": "a2", "type": "arrow", "x": 300, "y": 340, "points": [[0,0],[200,0]],    "startBinding": {"elementId":"__SRC__","focus":0,"gap":4}, "endBinding": {"elementId":"__T2__","focus":0,"gap":4}, "endArrowhead":"arrow", "seed": 100006 },
  { "id": "a3", "type": "arrow", "x": 300, "y": 340, "points": [[0,0],[200,120]],  "startBinding": {"elementId":"__SRC__","focus":0,"gap":4}, "endBinding": {"elementId":"__T3__","focus":0,"gap":4}, "endArrowhead":"arrow", "seed": 100007 }
]
```

### Timeline (line + markers + labels)

```json
[
  { "id": "tl-line", "type": "line", "x": 120, "y": 400, "points": [[0,0],[1000,0]], "...": "line-structural", "seed": 200001 },
  { "id": "tl-m1", "type": "ellipse", "x": 113, "y": 393, "width": 14, "height": 14, "...": "marker", "seed": 200002 },
  { "id": "tl-m2", "type": "ellipse", "x": 613, "y": 393, "width": 14, "height": 14, "...": "marker", "seed": 200003 },
  { "id": "tl-m3", "type": "ellipse", "x": 1113,"y": 393, "width": 14, "height": 14, "...": "marker", "seed": 200004 },
  { "id": "tl-l1", "type": "text", "x": 80,  "y": 420, "text": "RUN_STARTED",  "...": "text-body", "seed": 200005 },
  { "id": "tl-l2", "type": "text", "x": 570, "y": 420, "text": "STATE_DELTA",  "...": "text-body", "seed": 200006 },
  { "id": "tl-l3", "type": "text", "x": 1070,"y": 420, "text": "A2UI_UPDATE",  "...": "text-body", "seed": 200007 }
]
```

The `"...": "rectangle-neutral"` notation is shorthand for "fill in all the common fields from the rectangle template above" — expand before pasting into a real file.

---

## ID and Seed Conventions

- **IDs**: descriptive strings scoped to their section. Examples: `"ingest-box"`, `"ingest-label"`, `"arrow-ingest-to-transform"`.
- **Seeds**: namespace by section with a 6-digit scheme:
  - `100xxx` — section 1
  - `200xxx` — section 2
  - `300xxx` — section 3
  - ...and so on

This keeps IDs and seeds predictable as the file grows, and makes cross-section bindings easy to audit by reading the IDs.
