# Layout Gotchas

Ten issues that reliably show up when rendering Excalidraw JSON and catch the eye during validation. Read this before generating JSON — most of these are cheaper to avoid than to fix.

---

## 1. Fan-out label collisions

**Symptom**: one source fans out to 3+ targets, the arrow labels pile on top of each other in the middle of the canvas.

**Cause**: arrow labels are placed at the midpoint of each arrow. When arrows share a common source and fan to close-together targets, midpoints cluster.

**Fix**:
- Put the label **on the target shape** instead of on the arrow.
- Or offset label text as a separate `text` element near the arrow tail, not midpoint.
- Or space the targets further apart (minimum 80px vertical gap for horizontal fan-out).

---

## 2. Zone opacity competing with contents

**Symptom**: a dashed section zone is readable but everything *inside* it looks muddy and low contrast.

**Cause**: zone fill is too saturated, or `opacity` was not lowered.

**Fix**: zones should use `backgroundColor: "#f9fafb"` (or similar near-white) AND `opacity: 40`. Keep stroke at full opacity so the boundary is crisp.

---

## 3. Arrow-label overlap with crossing arrows

**Symptom**: two arrows cross and their labels stack on top of each other at the crossing point.

**Cause**: both labels placed at arrow midpoint, and midpoints happen to coincide at the crossing.

**Fix**:
- Route one arrow around the other (add a midpoint to the arrow's `points`).
- Move one label to 30% along the arrow instead of 50%.
- Collapse both arrows into one and use a compound label.

---

## 4. Column alignment drift

**Symptom**: elements that should line up vertically are off by a few pixels.

**Cause**: manually-assigned `x` values drift as you add/edit elements.

**Fix**:
- Pick grid anchors (e.g. columns at x = 120, 440, 760, 1080) and reuse them as variables when generating JSON.
- Snap every element's `x` to a multiple of 20.
- Widths should match across column members: if the column is 280px wide, every shape in the column is 280px wide.

---

## 5. Text overflowing its container

**Symptom**: label text extends past the edge of its rectangle/ellipse.

**Cause**: text element not bound to container, or container width too small for the font size.

**Fix**:
- Bind the text to the container by setting `containerId` on the text and adding `boundElements: [{ type: "text", id: "<text-id>" }]` on the container. Excalidraw will auto-wrap.
- Increase container width: rule of thumb `width >= label_chars * fontSize * 0.6 + 20` padding on each side.
- Shorten the label. If you can't, the container is too small or the concept needs splitting.

---

## 6. Arrow binding lost after edits

**Symptom**: arrows become free-floating after you move or resize their endpoints' shapes.

**Cause**: `startBinding` / `endBinding` still reference the shape IDs but `points` were not updated, or vice versa.

**Fix**:
- Always keep `startBinding.elementId` + `endBinding.elementId` pointing at shape IDs.
- Keep arrow `x`, `y` at the source shape edge, and `points` as deltas from that origin ending at the target shape edge.
- When you move a shape, regenerate the arrow points from the new shape centres.

---

## 7. Z-order: containers covering their contents

**Symptom**: a section zone is drawn on top of the shapes inside it.

**Cause**: Excalidraw renders in element array order — later = on top. The zone was appended after its contents.

**Fix**: put zones and other "background" shapes **first** in the `elements` array, foreground shapes last. One clean ordering:
1. Zones (section backgrounds)
2. Connecting lines (structural, no arrowhead)
3. Shapes (rectangles, ellipses, diamonds)
4. Arrows (flow)
5. Text labels (always on top)

---

## 8. Evidence block padding

**Symptom**: code/JSON text in an evidence block is flush against the dark background edge, looks cramped.

**Cause**: text positioned at the shape's `x, y` with no inset.

**Fix**: inset the text by 12-16px from each edge of the dark rectangle. The rectangle's content area is roughly `(x + 14, y + 12)` to `(x + width - 14, y + height - 12)`. Use monospace font (`fontFamily: 3`) and tight line height (`lineHeight: 1.25`).

---

## 9. Ellipse label offset

**Symptom**: text inside a small ellipse (e.g. timeline marker) is vertically off-centre.

**Cause**: Excalidraw centres bound text by the text's own bounding box, but short labels with descenders (y, g, p) throw the visual centre off.

**Fix**:
- Use `verticalAlign: "middle"` and `textAlign: "center"` on the text element.
- For decorative markers <30px, don't put text inside — put the label as free-floating text beside the ellipse.

---

## 10. Arrowhead direction swapped

**Symptom**: the arrow points from target to source instead of source to target.

**Cause**: `points` drawn in reverse OR `startArrowhead` / `endArrowhead` set on wrong end.

**Fix**: convention for a flow arrow A -> B:
- `x, y` = centre-right of A (the tail)
- `points` = `[[0,0], [B.centre - A.centre]]`
- `startArrowhead: null`
- `endArrowhead: "arrow"`
- `startBinding.elementId: "A"`
- `endBinding.elementId: "B"`

If the head is on the wrong end, swap `startArrowhead` and `endArrowhead` values first — that's almost always the cause, no need to reverse the points.
