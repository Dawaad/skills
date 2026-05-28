# Wiki Routing for Transcript-Derived Pages

Mirrors the master schema in `~/Documents/wiki/CLAUDE.md`. Use this to pick
which wiki each candidate page belongs in. Multi-wiki fanout is expected for
long-form content — videos often span several domains.

## Wikis

| Wiki | Scope | Trigger patterns |
|------|-------|------------------|
| `Riven/` | Riven internal tech: architecture, decisions, flows, system SOPs | speaker is talking about *your* product / system; specific component names you own |
| `Dev/` | General engineering: languages, frameworks, tooling, patterns, algorithms — **product-agnostic** | tool/library mechanics, language idioms, general patterns, debugging craft, perf, build systems |
| `Marketing/` | Product marketing: ICP, positioning, voice, objections, proof points | go-to-market, positioning, ICP discovery, messaging tests, narrative |
| `Content/` | Platform growth, hooks, formats, distribution, content SOPs | short-form scripting, hook mechanics, retention curves, platform algorithm behavior, posting cadence |
| `Personal/` | Self-systems, productivity, focus, decision rules, life SOPs | energy, focus, habits, sleep, learning routines, life decisions |
| `Homelab/` | Server, networking, NAS, Linux ops, infra SOPs | self-hosting, RAID, networking, hardware decisions, home server stack |
| `Meta/` | Cross-domain frameworks, learning patterns, mental models | when the *same* insight applies to ≥2 of the above domains (e.g. OODA, JTBD, first principles, "easy vs simple") |

## Routing rules

1. **Read the page's claim, not the video's topic.** A "developer productivity"
   podcast can produce a `Dev/` page (a tool insight), a `Personal/` page
   (an energy-management SOP), and a `Meta/` page (a learning framework) all
   from the same source.

2. **Product-agnostic vs product-specific.** If the claim is *only* true for
   the speaker's own product, it goes nowhere (skip — you're not running
   their company). If it's true for any project of the same shape → `Dev/`.
   If it's true for your project specifically → `Riven/`.

3. **Promote to Meta only when it's actually cross-domain.** A framework
   that only meaningfully applies to engineering belongs in `Dev/`, even if
   it sounds abstract. The Meta bar is: would I cite this from *two
   different* wikis? If no, demote it.

4. **Marketing vs Content split.** Marketing = "who is the buyer, what
   moves them, what do they object to". Content = "how do I make the post
   land". A hook insight is Content. An ICP-pain insight is Marketing.

5. **Same insight, two wikis.** Don't write the same page twice. Write it
   once in the better-fit wiki and create a *companion stub* in the other
   that just wikilinks across. Or, if both perspectives are genuinely
   distinct, split into two narrowly-scoped pages.

## Working-directory hint

If the user invokes this skill from inside a specific wiki path
(e.g. `cd ~/Documents/wiki/Dev/`), bias the default routing toward that
wiki — but never *only* route there. Long-form sources almost always have
cross-cutting insight. Surface the fanout candidates anyway and let the
user trim.

## When in doubt

Ask. The cost of asking "Dev or Meta for this one?" once is much lower than
the cost of mis-shelving a page that future-you will fail to find later.
