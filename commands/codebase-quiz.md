---
name: codebase-quiz
description: >
  Generate codebase knowledge questions by scanning source code and docs, then evaluate
  the user's answers for correctness and depth. Use this skill when the user wants to test
  their understanding of the codebase, says things like "quiz me", "test my knowledge",
  "generate questions about", "I want to learn about the X domain", "FAQ questions for",
  or wants to build out FAQ sections in their documentation. Also trigger when the user
  mentions studying a domain, preparing documentation, or wanting to verify they understand
  how something works before writing about it. This is different from /learn (Socratic audit)
  where the user explains first — here, Claude generates the questions and the user goes
  and investigates before answering.
---

# Codebase Knowledge Quiz

You are running a codebase knowledge quiz — a structured learning exercise where you scan
a domain's source code and documentation, generate targeted questions, and then evaluate
the user's answers after they've had time to investigate the codebase themselves.

The goal is to build the user's deep understanding by making them do the detective work,
not by handing them answers. Their verified answers become FAQ entries that serve as a
lasting knowledge base for the project.

## Codebase Layout

- **Documentation**: `docs/system-design/domains/` — each domain has overview docs, sub-domain folders, flow docs, and an `FAQ.md`
- **Source code**: `core/src/main/kotlin/riven/core/` — organized by layer (`service/`, `entity/`, `repository/`, `controller/`) then by domain
- **Domains**: Catalog, Entities, Identity Resolution, Integrations, Storage, Workflows, Workspaces & Users, Knowledge, Notifications

## The Quiz Flow

### Phase 1: Scope and Scan

Ask the user which domain (or cross-domain topic) they want to quiz on. They might say
a specific domain like "Entities" or something cross-cutting like "how integrations
create entity types."

Once you have the scope:

1. **Read the domain docs** — the overview doc, sub-domain docs, and existing FAQ.md
2. **Read the source code** — services, entities, repositories, and controllers for that domain
3. **Read adjacent domains** if the topic is cross-domain
4. **Check for inconsistencies** between docs and code — flag these before generating questions

If you find inconsistencies (docs describe behavior the code doesn't implement, code has
features the docs don't mention, naming mismatches, stale references), present them to the
user as a separate section before the questions:

```
## Inconsistencies Found

While scanning, I found these mismatches between docs and code:

1. **[Brief title]**: The docs say X, but the code does Y. See `path/to/file.kt:123`.
2. ...
```

This is valuable on its own — the user can fix these even if they don't do the quiz.

### Phase 2: Generate Questions (Rounds of 5)

Generate 5 questions per round. Questions should require actually reading the code to answer
well — not things you can guess from general knowledge or skim from a README.

**Question types to mix across rounds:**

- **Flow questions**: "Walk through what happens when X is triggered — which services are
  called, in what order, and what does each one do?"
- **Why questions**: "Why does [component] exist as a separate service instead of being
  part of [other component]?"
- **Mechanism questions**: "How does [specific feature] work? What tables/entities are
  involved and what's the data flow?"
- **Edge case questions**: "What happens when [unusual condition]? How does the system
  handle it?"
- **Cross-domain questions**: "How does [Domain A] interact with [Domain B] during
  [specific operation]?"
- **Design decision questions**: "What problem does [pattern/approach] solve? What would
  go wrong without it?"
- **State questions**: "What are the possible states of [entity] and what triggers
  transitions between them?"

**Question quality guidelines:**

- Each question should be answerable by reading specific files — mentally note which files
  contain the answer (you'll need these for grading later), but don't reveal them to the user
- Avoid questions that are already answered in the existing FAQ.md — check first
- Start with foundational questions in round 1, then go deeper in subsequent rounds
- Mix difficulty: some should be straightforward (find the right file and read it), others
  should require connecting dots across multiple files
- For cross-domain topics, include at least 1-2 questions per round that span domain boundaries

**Present questions like this:**

```
## Round 1 — [Domain Name] Fundamentals

Here are your first 5 questions. Take your time investigating the codebase, then come
back with your answers whenever you're ready.

1. [Question]
2. [Question]
3. [Question]
4. [Question]
5. [Question]
```

After presenting questions, stop and wait. The user needs time to investigate. Don't
offer hints unless they ask.

### Phase 3: Evaluate Answers

When the user comes back with answers (they may answer all 5 at once, or a subset),
evaluate each one by comparing against what the code actually says.

For each answer, provide:

**Score** (out of 5):
- **5/5** — Complete and accurate. Covers the key details, correct terminology, and shows
  understanding of why things work this way.
- **4/5** — Mostly correct. Gets the main idea right but misses a secondary detail or
  nuance.
- **3/5** — Partially correct. Understands the general area but has gaps in specifics or
  gets some details wrong.
- **2/5** — On the right track but significant gaps or misunderstandings.
- **1/5** — Attempted but largely incorrect or too vague to demonstrate understanding.

**What was missed** (only for scores < 5): Be specific about what's missing or incorrect.
Don't just say "you missed some details" — say exactly which details and why they matter.

**Code pointers**: Point to the exact files and line ranges where the answer lives. Use
the format `path/to/file.kt:123-145` so the user can go verify.

**Present evaluation like this:**

```
## Evaluation — Round 1

### Q1: [Abbreviated question]
**Score: 4/5**
Your answer correctly identifies that [X]. However, you missed that [Y], which matters
because [Z]. See `core/src/main/kotlin/riven/core/service/entity/EntityTypeService.kt:87-102`.

### Q2: [Abbreviated question]
**Score: 5/5**
Spot on. You nailed [the key insight].

...

**Round Score: 22/25**
```

### Phase 4: Ask About Next Round

After evaluation, offer the user a choice:

1. **Next round** — generate 5 more questions, going deeper based on what they got wrong
   (focus follow-up questions on weak areas)
2. **Re-attempt** — let them try again on questions they scored < 4 on, after reviewing
   the code pointers
3. **Save and stop** — persist what they've done so far to FAQ.md
4. **Switch domain** — start fresh on a different domain

### Phase 5: Persist to FAQ

When the user is done (either they say so, or after completing rounds), write the verified
Q&A pairs into the domain's FAQ.md file.

**What gets persisted:**

- Only questions where the user scored 4/5 or 5/5 — these represent verified understanding
- For 4/5 answers, incorporate the missing detail into the persisted answer so the FAQ
  entry is complete
- For questions scored 3/5 or below, note them as "gaps to revisit" at the bottom of the
  FAQ but don't write full entries (the user hasn't demonstrated solid enough understanding)

**FAQ entry format** (match the existing style — H3 headers, prose answers with code
references):

```markdown
### [Question as written]

[Complete answer incorporating both what the user said and any details that were missing.
Written in present tense, describing how the system works. Include specific service names,
table names, and file references where helpful.]
```

**Persistence rules:**

- Append new entries to the existing FAQ.md, don't overwrite existing content
- If a question overlaps with an existing FAQ entry, update the existing entry instead
  of duplicating
- Add a brief comment at the top noting when entries were last added:
  `<!-- Last updated: YYYY-MM-DD via codebase quiz -->`
- Cross-domain questions go into the FAQ of the primary domain involved, with a note
  referencing the other domain (e.g., "See also: [[Identity Resolution]] FAQ")

## Handling Hints

If the user asks for a hint on a specific question, give them a nudge toward the right
file or concept area without giving away the answer:

- "Look at the services in `service/catalog/` — one of them handles this specific step"
- "The answer involves understanding the difference between two tables — check the entity
  layer for this domain"
- "This is a cross-domain interaction — start from the [Domain A] side and trace the call"

## Important Behaviors

- **Don't give answers during the quiz.** The entire point is that the user investigates
  and learns by reading the code. If you hand them answers, the FAQ entries are Claude's
  understanding, not theirs. The code pointers in evaluation are fine because they come
  AFTER the user has attempted an answer.

- **Grade honestly.** A generous 5/5 on a vague answer doesn't help anyone. The user is
  here to learn — accurate feedback serves them better than flattery.

- **Adapt difficulty across rounds.** If the user is scoring 5/5 on everything, make the
  next round harder (deeper edge cases, more cross-domain). If they're struggling, focus
  on fundamentals they missed.

- **Flag stale docs proactively.** If you notice during scanning that documentation
  references classes, methods, or behaviors that no longer exist in the code, flag it
  immediately. This is as valuable as the quiz itself.
