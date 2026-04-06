---
name: expert-panel
description: >
  Assemble a virtual panel of the most relevant domain experts for any strategic question —
  system design, software architecture, business strategy, product positioning, growth,
  organizational design, or any topic where established thinkers have published frameworks.
  Use this skill whenever the user asks a question that would benefit from multiple expert
  perspectives, even if they don't explicitly ask for "experts" or "what would X say."
  Trigger on patterns like: "how should I approach X", "what's the right architecture for",
  "should I build vs buy", "how do I position this", "what's the tradeoff between",
  strategic decisions, design tradeoffs, or any question where domain-specific thinkers
  would give sharper advice than generic reasoning. Also trigger when the user explicitly
  asks "what would experts say", "who should I study", "what would a group of people say
  about this", or similar.
---

# Expert Panel

When a strategic or architectural question comes up, don't give generic advice. Instead, identify the specific thinkers whose frameworks are most relevant to the exact problem being discussed, and synthesize what they would say about the user's specific situation.

## Why this works

Generic advice ("consider your tradeoffs," "it depends on your context") is useless. But when you identify that the user's problem maps to Geoffrey Moore's bowling pin strategy, or Martin Fowler's strangler fig pattern, or April Dunford's positioning framework — and then *apply* that framework to their specific situation — the advice becomes dramatically more actionable. The expert selection itself is the insight: it tells the user which body of knowledge to draw from.

## How to select experts

The quality of this skill lives or dies on expert selection. Follow these principles:

1. **Match the niche, not the category.** Don't reach for "famous business person" or "well-known architect." Find the person whose *specific framework* addresses the user's *specific problem*. If someone is asking about event sourcing in a multi-tenant system, Martin Kleppmann (DDIA) is more relevant than Martin Fowler, even though Fowler is more famous.

2. **Prefer practitioners over commentators.** People who built things and wrote about what they learned beat people who only write about what others built. Steli Efti (built Close.com, then wrote about cold email) over a generic "sales consultant."

3. **Select for tension, not agreement.** The most useful panels include people who would *disagree* with each other. If one expert says "go vertical first" and another says "horizontal platforms win if you nail the abstraction," that tension is where the insight lives. Don't assemble a panel that just echoes the same take five times.

4. **4-6 experts per topic is the sweet spot.** Enough for coverage, few enough that each one adds a distinct perspective. If a question spans two distinct sub-topics, you can have a panel per sub-topic.

5. **Include at least one contrarian or non-obvious pick.** Someone whose framework the user probably hasn't encountered but whose thinking maps perfectly to their problem.

## Output structure

For each question or topic raised:

### Panel identification

For each expert:
- **Name** and what they're known for (one line — enough for the user to know why they're on the panel)
- **What they'd say** about the user's *specific* situation. Not their general philosophy — their framework applied to the details at hand. Use specifics from the conversation: product names, metrics, architectural choices the user has mentioned.

### Convergence and divergence

After the individual perspectives, synthesize:
- Where do these experts **agree**? (This is likely a strong signal)
- Where do they **disagree**? (This is where the user needs to make a judgment call)
- What **practical next step** falls out of their combined advice?

## Critical stance

These experts should be *critical*, not encouraging. The user isn't looking for validation — they're looking for the sharpest version of the feedback they'd get if they could actually sit in a room with these people. If an expert's framework suggests the user is making a mistake, say so directly. Quote the kind of blunt language the expert is known for.

## Context awareness

Pull from everything available in the conversation:
- The user's product, its architecture, its positioning
- Problems they've described, metrics they've shared
- Decisions they're weighing
- Feedback they've received from others (like advisors, users, investors)

The more specific the application to their context, the more valuable the panel. "April Dunford would say you need better positioning" is useless. "April Dunford would say that 'human integration layer' describes your architecture, not your market — your buyer can't self-select from that phrase" is valuable.

## When NOT to use this

- Purely mechanical questions ("how do I write a for loop", "what's the syntax for X")
- Questions where the user has explicitly said they just want a direct answer, not a discussion
- Trivial decisions that don't warrant strategic analysis
