# Shot Taxonomy

Canonical labels for classifying reel frames. Every frame in the Shot Catalogue uses **exactly one** label from each dimension. Consistency matters more than granularity — if two ingests use "medium" for different things, the cross-reel library becomes noise. Use these labels verbatim.

## Dimensions

Every catalogued frame gets tagged along four dimensions: **distance × angle × motion × treatment**. Add a fifth — **creative signature** — only if the frame does something beyond the conventional combination of the first four.

### 1. Distance (how much of the subject is in frame)

| Label | Description | Common signal |
|-------|-------------|---------------|
| `EWS` | Extreme Wide — subject tiny in frame, environment dominates | "Scale," isolation, cinematic opener |
| `WS` | Wide — full body + significant environment | Context, setting, documentary feel |
| `MWS` | Medium Wide — subject from knees up, some environment | Transition between context and intimacy |
| `MS` | Medium — subject from waist up | Default conversational, walk-and-talk |
| `MCU` | Medium Close-Up — chest up | Interview feel, authority posture |
| `CU` | Close-Up — head + shoulders | Intimacy, emotion, direct address |
| `ECU` | Extreme Close-Up — face feature, hand, object detail | Emotion spike, product reveal, symbolic detail |
| `INSERT` | Non-subject detail shot (object, screen, hands) | B-roll proof, literalization of spoken noun |

### 2. Angle (camera position relative to subject)

| Label | Description | Common signal |
|-------|-------------|---------------|
| `eye-level` | Camera at subject's eye height | Peer-address, neutrality |
| `low-angle` | Camera below subject looking up | Authority, stature, heroic |
| `high-angle` | Camera above subject looking down | Diminishment, vulnerability, overview |
| `overhead` | Directly above (god's-eye) | Layout reveal, flat-lay product, diagrammatic |
| `dutch` / `canted` | Camera tilted off-axis | Disorientation, tension, stylization |
| `POV` | First-person — camera as subject's eyes | Immersion, "doing" energy |
| `OTS` | Over-the-shoulder | Conversation, proof of witness |

### 3. Motion (how the camera moves)

| Label | Description | Common signal |
|-------|-------------|---------------|
| `static` | Locked-off tripod | Script-carried, script has nowhere to hide |
| `handheld` | Subtle breathing, not walking | "Human is holding this," lo-fi authenticity |
| `selfie-cam` | Arm's-length, creator holds the camera | Default personal-brand mode |
| `walk-and-talk` | Creator walking while talking, camera moves with them | Motion-as-authenticity, casual-expert tone |
| `push-in` | Camera moves toward subject | Escalating stakes, "lean in" emphasis |
| `pull-out` | Camera moves away | Reveal context, "zoom out" reframe |
| `pan` | Horizontal rotation | Reveal, follow subject across scene |
| `tilt` | Vertical rotation | Reveal vertical scale, top-to-bottom list |
| `dolly` | Sideways translation (truck/crab) | Cinematic movement, parallax depth |
| `whip-pan` | Fast camera rotation, blurs | Transition device, energy spike |
| `rack-focus` | Camera still, focus shifts between subjects | Shift attention, reveal secondary subject |
| `match-cut` | Not camera motion but shot relationship — outgoing and incoming frames share composition | Transition fluidity, thematic link |
| `gimbal` | Smooth motorized motion, often walking with creator | Professional mode, cinematic feel |

### 4. Treatment (what's in the frame)

| Label | Description |
|-------|-------------|
| `talking-head` | Creator on camera delivering VO |
| `b-roll-documentary` | Real footage of real thing being discussed (event, workspace, product in use) |
| `b-roll-cinematic` | Staged/styled footage graded for mood |
| `title-card` | Full-screen typography, no subject |
| `typography-overlay` | Typography atop subject frame |
| `screen-recording` | Phone/desktop capture |
| `product-shot` | Product on backdrop, studio-lit |
| `demo-in-medium` | Creator *performing* the thing they're describing (coffee-toss fake, UI gesture) |
| `split-screen` | Two frames side-by-side |
| `pip` | Picture-in-picture overlay |
| `reaction-cutaway` | Non-primary subject responding (face, audience) |
| `meme-insert` | Pulled clip / meme image as punchline |
| `archival` | Real historical footage |
| `motion-graphics` | Animated typographic or vector elements |

### 5. Creative signature (optional — only when the frame does more than its conventional combination)

Use this dimension to tag frames that do something noteworthy the four-dimension combination doesn't capture. These are the frames that belong in the creative-shot library. Examples:

- `through-the-glass` — subject shot through window/glass/screen, often with reflection or obstruction as deliberate layer
- `reflection-framing` — subject visible only via mirror / water / surface
- `prop-led` — a prop or object does more compositional work than the subject
- `gesture-as-proof` — creator's hand/body movement literalizes the claim
- `symbolic-object` — an object in frame stands in for the abstract concept
- `frame-within-frame` — doorway / screen / window / mirror creates an internal frame
- `negative-space` — subject deliberately off-center with large empty region
- `foreground-blur` — out-of-focus foreground element adds depth (branch, rack of clothes)
- `silhouette` — subject backlit, only shape visible
- `off-axis-entrance` — subject enters frame unexpectedly from edge/top/bottom
- `match-cut-metaphor` — cut links two unrelated objects by shape/motion, forcing a metaphor
- `physical-punctuation` — gesture/prop timed to a word (e.g., book-close on last line)
- `visual-metronome` — recurring full-screen typography card marks structure (A.R.C letter cards)
- `embossed-object-outro` — tactile branded object held up (patch, letterpress card) as sign-off
- `demo-as-proof` — frame shows the mechanism being named (coffee-toss while explaining bold-action hooks)
- `era-encoded-pip` — subject or quote embedded inside a period-accurate UI/desktop chrome that encodes the era the speaker is describing (e.g., talking-head placed inside an MS Paint window while discussing 1990s web)
- `diegetic-typography` — typographic beat (word card, question, title) displayed on an in-world surface — the story object's own screen, a chalkboard, a page — rather than as post-production overlay. The prop does the title-card's job.
- `analog-screen-capture` — CRT monitor or laptop screen filmed with the physical camera (visible moire, scanlines, RGB split, glare) rather than clean screen-recorded. The capture texture becomes the era/authenticity signature.

**Rule:** never invent ad-hoc labels. If a frame's creative signature doesn't match an existing label, propose a new one in the log and add it to this taxonomy in the same edit. Labels persist across ingests; the value is in cross-reel lookup.

## Attribution: audio + script + message

Every catalogued frame must also record three context fields:

| Field | Content |
|-------|---------|
| `vo` | Verbatim fragment of VO at that timecode (from timestamped transcript) |
| `audio-bed` | Music cue name (from source `## Music`) OR "ambient" OR "speech-only" |
| `message` | One-sentence synthesis: *what does the shot communicate?* Not what's in it — what it means. "Locked eye-level talking head signals 'I stand behind this claim personally.'" |

The `message` is the interpretive layer. Without it, the catalogue is a frame list. With it, the catalogue becomes a reusable shot vocabulary.

## What counts as "creative"

A frame earns `creative_signature` tagging if any of:

1. It does something the reel's other frames don't (variation-as-signal).
2. It's the frame a future scriptwriter would want to *remember how to replicate*.
3. The message the shot conveys can't be reduced to the distance/angle/motion/treatment combo alone — the composition itself is doing work.

Most frames are *not* creative. A locked walk-and-talk talking head at MS/eye-level repeated for 30 frames is correctly tagged once and then *not* flagged creative for any subsequent identical frame. Repetition in the catalogue reads as noise.
