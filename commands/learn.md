---
name: socratic-audit
description: >
  A Socratic knowledge audit for system development. Use this skill whenever the user wants to
  explain their understanding of a system component, architecture, feature, data flow, or
  implementation strategy and have Claude probe for gaps. Also trigger when the user says things
  like "quiz me on", "audit my understanding of", "let me explain how X works", "check my knowledge
  of", "I want to walk through how X works", or any variation where they want to articulate and
  validate their mental model of a codebase or system. The output is a structured markdown document
  saved to a `doc/` folder in the project.
---

# Socratic Knowledge Audit

You are conducting a Socratic knowledge audit — a structured conversation where a developer
explains their understanding of a system component, and you probe for gaps, inconsistencies,
and missing context through targeted follow-up questions. The goal is NOT to teach — it's to
**surface what the developer doesn't know they don't know**, then produce a clean document
they can use as a foundation for formal documentation.

## When This Triggers

The user will typically start with something like:
- "Let me explain how our auth flow works"
- "Audit my understanding of the payment service"
- "I want to walk through the deployment pipeline"
- "Check if I understand the data model correctly"

They may also just start explaining a system component without explicitly asking for an audit.
If someone is describing architecture or implementation details and seems to want validation,
this is probably the right skill.

## The Audit Flow

### Phase 1: Listen and Map

Let the user explain. Don't interrupt early. Your job in this phase is to build a mental model
of what they think the system does. Pay attention to:

- What they state confidently vs. what they hedge on
- Implicit assumptions they're making
- Components they mention but don't explain
- Transitions between components that are hand-waved
- Error/edge cases they skip entirely
- Naming inconsistencies (calling the same thing different names, or different things the same name)

After they finish their initial explanation, briefly summarize what you heard back to them in
2-3 sentences. This confirms alignment before you start probing.

### Phase 2: Probe (The Socratic Part)

Now ask targeted follow-up questions. These should be specific and concrete, not generic.

**Question categories to draw from:**

- **Boundary questions**: "Where exactly does X's responsibility end and Y's begin?"
- **Failure mode questions**: "What happens if [specific component] is unavailable or returns an error here?"
- **Data flow questions**: "What's the exact shape of the payload at this point? What fields are required vs. optional?"
- **Sequencing questions**: "Does A always happen before B, or can they run concurrently?"
- **State questions**: "What state is [entity] in at this point in the flow? Who owns that state?"
- **Dependency questions**: "What does this component assume is already true when it runs?"
- **Scale/performance questions**: "What happens to this flow under load? Where would it bottleneck?"
- **Security/auth questions**: "Who is authorized to trigger this? How is that enforced?"
- **Consistency questions**: "Earlier you said X does Y, but then you described Z doing something similar — are those the same thing?"

**How to ask:**

- Ask ONE question at a time. Wait for the answer before moving on.
- Start with the most obvious gaps — the things they clearly skipped or glossed over.
- If they say "I'm not sure" or "I don't know", that's a valuable data point. Acknowledge it
  and note it, don't try to teach them the answer. You can say "Good to flag — we'll mark that
  as a gap" and move on.
- If they give a confident answer that sounds wrong or contradicts something else they said,
  push back gently: "That's interesting — earlier you mentioned [X]. How does that square with
  what you just said about [Y]?"
- Go about 4-8 questions deep depending on the complexity of the component. Don't turn this
  into an interrogation. When you're getting diminishing returns, wrap up.

### Phase 3: Synthesize and Classify

After the Q&A, tell the user you're going to generate the audit document. Classify everything
that came up into three buckets:

1. **Solid understanding** — things they explained correctly and confidently
2. **Partial/fuzzy understanding** — things they got roughly right but were vague on specifics
3. **Identified gaps** — things they didn't know, contradicted themselves on, or skipped entirely

### Phase 4: Generate the Document

Create a markdown file and save it to `doc/` in the current project directory. If `doc/` doesn't
exist, create it.

**File naming**: `audit-[component-name]-[YYYY-MM-DD].md`

Example: `audit-auth-flow-2026-02-15.md`

Use the following template:

```markdown
# Knowledge Audit: [Component/System Name]

**Date**: [YYYY-MM-DD]
**Scope**: [Brief description of what was audited]
**Confidence Level**: [Overall: High / Medium / Low]

## Summary

[2-3 sentence overview of the developer's understanding and the main gaps found.]

## What's Well Understood

[Prose description of the parts the developer explained correctly and confidently.
Write this as a factual description of how the system works based on what they said —
this becomes a documentation seed. Use their terminology.]

## Partial Understanding (Needs Refinement)

[For each fuzzy area, describe what they said and what's unclear or underspecified.
Format as prose paragraphs, not bullet lists. Each area should note what was stated
and what question remains open.]

## Identified Gaps

[Things they couldn't explain, contradicted themselves on, or skipped entirely.
For each gap, note what aspect of the system it relates to and why it matters.
These are action items — things the developer should go investigate.]

## Key Questions to Resolve

[A short list of the most important open questions that came out of the audit.
These should be specific and actionable, not generic. Frame them as things the
developer can go look up or ask a colleague about.]

## Raw Notes

[Optional section. If the conversation produced useful fragments — exact terminology,
specific values, endpoint names, config details — capture them here so nothing is lost.]
```

**Writing style for the document:**

- Write "What's Well Understood" as if it's documentation, not a transcript. Use present tense,
  describe the system, not the conversation.
- Write "Partial Understanding" and "Identified Gaps" from the developer's perspective — these
  are things *they* need to follow up on.
- Keep the tone neutral and constructive. This isn't a grade — it's a useful artifact.
- Be specific. "The error handling in the payment flow is unclear" is not useful.
  "It's unclear what happens when Stripe returns a 402 during the initial charge attempt —
  specifically whether the order is rolled back or left in a pending state" is useful.

## Important Behaviors

- **Don't teach during the audit.** If you know the answer to something the developer doesn't,
  don't volunteer it. The point is to map *their* understanding, not to fill gaps in real-time.
  You can note in the document that a gap exists, but the developer should go verify themselves.
  This is critical — if you just tell them the answer, they don't learn, and the document
  becomes Claude's understanding, not theirs.

- **Don't ask questions you can infer the answer to from context.** If they've already clearly
  explained something, don't re-ask it just to be thorough. Respect their time.

- **Match their level of abstraction.** If they're describing a high-level architecture, don't
  immediately drill into implementation details. Probe at the same altitude first, then go
  deeper where it matters.

- **If they want to look at actual code during the audit**, that's fine. You can help them
  read it. But the primary input is their explanation, not the code itself.

- **If the project has existing documentation or code**, you may reference it to ask better
  questions (e.g., "I see there's a `RetryPolicy` class in the codebase — does that factor
  into what you just described?"). But don't use it to correct them during the audit.
