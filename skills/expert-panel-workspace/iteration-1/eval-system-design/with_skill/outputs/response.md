# Real-Time Sync Architecture for a Notion-Like Project Management Tool

## The Panel

### 1. Martin Kleppmann — Author of *Designing Data-Intensive Applications*, researcher on CRDTs and local-first software

**What he'd say about your situation:**

"You're asking the right question, but you're framing it wrong. The question isn't 'CRDTs vs OT vs last-write-wins' — it's 'what are your consistency requirements per data type?' A project management tool with blocks is not a text editor. Most of your operations — moving a block, changing a status field, assigning a task — are not character-by-character text edits. They're discrete state mutations on structured data.

CRDTs are powerful, but they impose serious engineering costs. You need to model every data type as a CRDT, handle tombstones and garbage collection, deal with metadata bloat over time, and debug convergence issues that are subtle and hard to reproduce. At 5k concurrent users you are nowhere near the scale where you *need* CRDTs for availability reasons. You don't have a multi-datacenter partition tolerance problem — you have a 'two people edited the same block' problem.

If you don't have deep distributed systems expertise on the team, building a custom CRDT system is how you burn six months and ship nothing. I'd say this bluntly: CRDTs are the wrong default for teams that can't afford to become CRDT experts."

### 2. Evan Wallace — Co-founder of Figma, built their real-time multiplayer system

**What he'd say about your situation:**

"We built Figma's multiplayer on a server-authoritative model, not CRDTs, and not OT. The server is the source of truth. Clients send operations, the server applies them, resolves conflicts with simple deterministic rules, and broadcasts the result. It scaled to millions of concurrent users.

For your use case at 5k concurrent users, this is the obvious path. You already have PostgreSQL as your source of truth. Add a WebSocket layer that pushes change events to connected clients. When a user edits a block, the client sends the operation to the server, the server writes to Postgres, and fans the update out via WebSocket. For conflict resolution on most fields — title, description, status — last-write-wins is completely fine. Users editing the *same field* of the *same block* at the *same instant* is rare in a project management tool. It's not Google Docs where fifty people type in the same paragraph.

The one place you might want something smarter is rich-text content within a block. For that, consider using an existing library like Yjs rather than building your own. But don't let the rich-text sub-problem drive the architecture of your entire system."

### 3. James Long — Creator of CRDT-based sync engine Automerge (contributor) and author of "CRDTs are the future" and later, pragmatic critiques of CRDT adoption

**What he'd say about your situation:**

"I've spent years working on CRDTs and I'll tell you directly: most teams should not build their own CRDT layer. The gap between 'I understand the concept' and 'I've handled all the edge cases in production' is enormous. Schema migrations with CRDTs are painful. Undo/redo is painful. Access control is painful. Garbage collection is painful.

What I'd actually recommend for your situation: use a proven library. Yjs is battle-tested, fast, and handles the hard parts. Use it specifically for the blocks where you need character-level collaboration (rich text editing). For everything else — block ordering, metadata, assignments, statuses — server-authoritative last-write-wins over WebSockets is simpler, easier to reason about, and easier to debug. You don't need one sync mechanism for your entire data model."

### 4. Nikita Prokopov (tonsky) — Author of "A Look at Conflict-Free Replicated Data Types" and pragmatic systems thinker, creator of DataScript

**What he'd say about your situation:**

"The industry has a pattern of over-engineering real-time collaboration. Notion itself started with a relatively simple model — not CRDTs, not OT. They used a server-authoritative approach with operational data pushed over WebSockets.

At 5k concurrent users, your bottleneck is not conflict resolution algorithms. Your bottleneck is operational — WebSocket connection management, reconnection handling, state reconciliation after disconnects, and making sure your Postgres write path doesn't become a chokepoint. Focus your engineering effort there.

Here's the thing people miss: the hardest part of real-time sync isn't the algorithm. It's the UX. What does the user see when they're offline? What happens when they reconnect? How do you show presence indicators? How do you handle cursor positions? These problems are the same regardless of whether you use CRDTs, OT, or last-write-wins. Solve the UX problems first with the simplest backend approach, then upgrade the sync algorithm later if you actually hit its limits."

### 5. Chris Olah / Ben Thompson (Stratechery lens) — I'm substituting Ben Thompson here for the strategic product perspective

**Ben Thompson — Stratechery, strategic technology analyst:**

"From a product strategy perspective, ask yourself: is real-time collaboration your differentiator, or is it table stakes? If you're building a project management tool, your users expect to see changes appear without refreshing. They do *not* expect Google-Docs-level character-by-character co-editing on every field.

The risk of choosing CRDTs or OT is not just engineering cost — it's opportunity cost. Every month your team spends building and debugging a sophisticated sync engine is a month you're not spending on the features that actually differentiate your product. At your scale, a simpler architecture that ships in weeks beats a sophisticated one that ships in months.

Ship the 90% solution now. If you later find that users are actually co-editing rich text in blocks frequently enough that last-write-wins causes visible data loss, *then* integrate Yjs for that specific sub-problem."

### 6. Werner Vogels — CTO of Amazon, architect of eventually consistent systems at massive scale

**What he'd say about your situation:**

"At 5,000 concurrent users, you do not have a distributed systems problem. You have a web application problem. I've seen teams adopt the complexity of eventual consistency, CRDTs, and sophisticated conflict resolution when they have one database in one datacenter serving a few thousand users. This is over-engineering.

Your PostgreSQL instance can handle 5k concurrent users. A single WebSocket server (or a small cluster behind a load balancer with Redis pub/sub for fan-out) can handle 5k connections trivially. The architecture is simple: writes go through your REST API to Postgres, a change-data-capture mechanism (even just LISTEN/NOTIFY in Postgres) pushes events to WebSocket servers, and those fan out to clients.

Build for the scale you have. Architect so you *can* evolve, but don't build for a million users today."

---

## Convergence

The panel agrees strongly on several points:

1. **CRDTs are wrong for your situation.** Every expert, including the ones who build and advocate for CRDTs, says that a team without deep distributed systems expertise should not build a custom CRDT layer for a 5k-user project management tool. The engineering cost is disproportionate to the benefit.

2. **Server-authoritative with WebSocket push is the right architecture.** Your PostgreSQL database remains the source of truth. Clients send mutations via your existing REST API (or upgrade to WebSocket-based RPC). The server writes to Postgres and broadcasts changes to connected clients. This is the Figma model, the early Notion model, and the model that virtually every successful real-time collaborative app started with.

3. **Last-write-wins is fine for structured data.** For fields like task status, assignee, due date, block position — last-write-wins with server timestamps is sufficient. Conflicts on these fields are rare and low-stakes in a project management context.

4. **Use an off-the-shelf library if you need rich-text co-editing.** If blocks contain rich text that multiple users edit simultaneously, integrate Yjs or a similar library specifically for that sub-problem. Don't let it dictate your overall architecture.

## Divergence

The main area of disagreement is **how much to invest in the rich-text sub-problem now vs. later:**

- Kleppmann and Long would say: if you know you'll need rich-text co-editing, integrate Yjs from the start rather than retrofitting it.
- Thompson and Vogels would say: ship last-write-wins everywhere first, and only add Yjs when you have evidence that users are actually losing work due to conflicts in text fields.

This is a judgment call that depends on how central rich-text block editing is to your product. If it's a core workflow (users spend most of their time writing in blocks), lean toward integrating Yjs early. If blocks are mostly structured fields with occasional text, defer it.

## Practical Next Steps

1. **Add a WebSocket layer to your existing REST API.** Use something like Socket.IO, or raw WebSockets with a library. When a client connects, subscribe them to the resources they're viewing.

2. **Implement change fan-out from Postgres.** Use Postgres LISTEN/NOTIFY or a lightweight change-data-capture approach. When a row changes, notify connected WebSocket clients who are subscribed to that resource.

3. **Apply last-write-wins with server timestamps for all fields.** Add an `updated_at` column if you don't have one. When a write comes in, compare timestamps. Broadcast the winning write to all clients.

4. **Add optimistic updates on the client.** When a user makes a change, apply it locally immediately, send it to the server, and reconcile when the server responds. This makes the app feel instant.

5. **For WebSocket scaling**, put Redis pub/sub between your API servers and WebSocket servers. This lets you run multiple WebSocket server instances behind a load balancer. At 5k users, you may not even need this yet — a single Node.js process can handle tens of thousands of WebSocket connections.

6. **Defer rich-text CRDT integration.** Revisit in 2-3 months based on actual user behavior. If you do need it, Yjs with y-websocket is the most mature option and can be scoped to just the text-editing component without changing your overall architecture.

This approach gets you to a working real-time collaborative product in weeks, not months, with technology your team can understand, debug, and maintain.
