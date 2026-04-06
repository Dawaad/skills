# Real-Time Sync Architecture Recommendation

## Bottom Line Up Front

Go with **Option 3 (last-write-wins with WebSocket push)**, augmented with per-block granularity and optimistic UI updates. At 5k concurrent users without deep distributed systems expertise, CRDTs and OT are overengineered for your situation and will create more problems than they solve.

---

## Why Not CRDTs (Option 1)

CRDTs are theoretically elegant but practically painful:

- **Steep learning curve.** Implementing or even integrating a CRDT library (Yjs, Automerge) correctly requires understanding the data model deeply. Debugging convergence issues is a specialized skill your team has said it lacks.
- **Storage overhead.** CRDTs carry tombstones and version vectors that bloat document size over time. You need compaction strategies, which add complexity.
- **Overkill for block-based editing.** CRDTs shine when two users are typing in the same paragraph simultaneously. In a Notion-like tool, the editing unit is a block (a paragraph, a checklist item, a table cell). Simultaneous edits to the *same block* by two users are relatively rare compared to, say, Google Docs-style co-authoring of prose.

CRDTs become the right choice if you later need offline-first support or true peer-to-peer sync. You are not there yet.

## Why Not OT (Option 2)

- **Server complexity.** OT requires a centralized transformation server that understands every operation type. Every new block type or operation you add needs corresponding transform functions. Google spent years getting this right.
- **Difficult to implement correctly.** OT's transform functions are notoriously hard to prove correct. Academic papers on OT are full of counterexamples to previously "correct" algorithms.
- **No off-the-shelf solution fits easily.** ShareDB exists but locks you into its data model. You would be coupling your entire architecture to it.

## Why Last-Write-Wins + WebSocket Push (Option 3) Works

At your scale and with your team's expertise, this approach gives you 90% of the user experience for 20% of the complexity.

### Recommended Architecture

```
Client A                    Server                     Client B
   |                          |                           |
   |-- WS: subscribe(doc) --->|                           |
   |                          |<--- WS: subscribe(doc) ---|
   |                          |                           |
   |-- WS: update(block_7) -->|                           |
   |   {version: 4, ...}      |                           |
   |                          |-- validate version -----  |
   |                          |-- write to PostgreSQL --   |
   |                          |-- broadcast ------------->|
   |<-- WS: ack(block_7, v5) -|   WS: update(block_7,v5) |
```

### Key Design Decisions

**1. Per-block granularity, not per-document.**

Each block has its own version counter. When a user edits block 7, only block 7 is locked/versioned. Two users editing different blocks in the same page never conflict. This dramatically reduces conflict frequency.

```sql
CREATE TABLE blocks (
    id UUID PRIMARY KEY,
    page_id UUID NOT NULL REFERENCES pages(id),
    content JSONB NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    updated_by UUID REFERENCES users(id),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    sort_order FLOAT NOT NULL
);

-- Optimistic concurrency control
UPDATE blocks
SET content = $new_content, version = version + 1, updated_by = $user_id
WHERE id = $block_id AND version = $expected_version
RETURNING version;
```

If the UPDATE returns 0 rows, the version has changed -- that is your conflict signal.

**2. Optimistic UI with server reconciliation.**

- Client applies the edit immediately in the UI (optimistic update).
- Client sends the edit over WebSocket with the expected version.
- Server validates and either confirms (broadcast to all) or rejects (conflict).
- On conflict, client fetches the latest block state and either auto-merges (if the fields edited are different) or shows the user a simple conflict indicator.

**3. Presence and cursors are separate from data sync.**

Broadcast cursor positions and "User X is editing block Y" indicators over WebSocket on a fire-and-forget basis. These do not need persistence or conflict resolution. Debounce to every 100-200ms.

**4. WebSocket infrastructure.**

At 5k concurrent connections, a single Node.js or Go process handles this easily (a modern server handles 100k+ WebSocket connections). Use Redis Pub/Sub to fan out if you later need multiple server instances:

- **Single server (start here):** Process manages all connections in-memory. Simple.
- **Scale-out path:** Add Redis Pub/Sub. When server instance A receives an edit, it publishes to a Redis channel. All server instances subscribed to that channel push to their local clients.

You do not need Kafka, RabbitMQ, or any heavy message broker at 5k users.

**5. PostgreSQL LISTEN/NOTIFY as an alternative to Redis (for now).**

Since you already have PostgreSQL, you can use `LISTEN/NOTIFY` to push change events to your application server, avoiding an additional dependency. This works well up to moderate scale. Switch to Redis Pub/Sub when you outgrow it.

```sql
-- Trigger on block update
CREATE OR REPLACE FUNCTION notify_block_change() RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('block_changes', json_build_object(
        'page_id', NEW.page_id,
        'block_id', NEW.id,
        'version', NEW.version
    )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Handling the Remaining Edge Cases

| Scenario | Solution |
|----------|----------|
| Two users edit the same block | Optimistic concurrency via version check. Loser gets a conflict, re-fetches, retries or sees a notification. |
| Block reordering conflicts | Use fractional indexing (e.g., sort_order as float between neighbors). Two reorders to different positions do not conflict. |
| User goes offline briefly | Queue edits locally, replay on reconnect. If versions conflict, re-fetch and retry. |
| Block creation race | Use client-generated UUIDs. Two blocks created at the same position use fractional indexing to resolve order. |

### What You Defer (and When to Revisit)

- **CRDT migration:** If you later need true offline-first (mobile app with extended offline use), consider migrating block content to Yjs or Automerge at that point. Your block-level architecture makes this a per-block migration, not a rewrite.
- **Rich text co-editing within a block:** If you need two cursors in the same text block simultaneously (like Google Docs), that specific block type may warrant Yjs for its internal content. You can adopt CRDTs surgically for rich-text blocks while keeping the rest of the system simple.
- **Horizontal scaling beyond ~50k users:** At that point, introduce Redis Pub/Sub, partition WebSocket connections by page/workspace, and consider a dedicated real-time service.

---

## Summary

| Criterion | LWW + WebSocket | CRDTs | OT |
|-----------|----------------|-------|-----|
| Implementation complexity | Low | High | High |
| Team expertise required | General backend | Specialized | Specialized |
| Conflict handling | Per-block versioning, rare conflicts | Automatic merge | Automatic merge |
| Scales to 5k users | Easily | Easily | Easily |
| Offline support | Basic (queue + retry) | Excellent | Poor |
| Time to production | 2-4 weeks | 2-4 months | 2-4 months |

Start simple. Ship the WebSocket + per-block versioning approach. It handles your current scale, matches your team's expertise, and leaves a clear upgrade path to CRDTs for specific block types if you genuinely need them later.
