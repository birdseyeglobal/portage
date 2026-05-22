---
name: content-styleguide
description: |
  Use for any human-facing prose: drafting, revising, reviewing, or polishing
  text a person will read. Guides the agent through the universal writing
  reasoning that sits beneath every surface: genre, audience, situation, voice,
  register, tone, claim precision, structure, scanability, sentence clarity,
  information flow, and AI-artifact cleanup. Pair with surface skills when a
  specific artifact also has its own contract.
---

# Content Style Guide

This skill improves how the agent thinks about writing before it writes. The
output may be a one-line Slack reply, a client email, a PR summary, a Google
Doc section, a social post, an executive memo, or a long internal report. The
process stays useful because it clarifies the communicative job before
choosing words.

For a short message, run the charter silently. For substantial prose, hold the
answers in mind before drafting.

## Charter

Answer these before drafting or revising. They apply across surfaces because
they are the questions every careful writer asks. The examples in each
question are illustrative — pick from them when they fit, name your own when
they don't.

- **Genre.** What action does this prose perform — for example, to inform,
  persuade, request, respond, teach, record, present, or build consensus?
  Lead with the primary action; let secondary actions shape the ending.
- **Audience.** Who is reading, what do they already know, and what do they
  need from this prose next?
- **Situation.** What state is the reader in — for example, blocked,
  deciding, scanning, reviewing, learning, maintaining, or celebrating?
- **Voice and register.** What relationship and stakes does this prose
  carry? Common examples: peer, manager, customer, public, regulator.
- **Tone.** What does the situation call for — for example, warmth,
  urgency, calm precision, patience, or directness?
- **Claim strength.** What is the strongest truthful claim the facts
  support, and which details are evidence vs. clutter?
- **Structure.** What shape lets the reader recover the point quickly?
- **AI artifacts.** What would make this sound more human without making it
  less precise?

Develop from known to new: define the frame before the exception, the
contract before the edge case, the decision before its consequences. When the
prose carries risk, boundary, or failure information, state it plainly and
early.

## Genre

Structure follows the prose's job, not the author's inventory of topics.

- **Inform** — lead with the answer, then the minimum context needed to
  trust it.
- **Persuade** — state the recommendation early, then show evidence,
  tradeoffs, and the rejected alternative.
- **Request** — ask for one clear action and explain why it matters.
- **Respond** — resolve the point directly, keep the temperature low, make
  the next state clear.
- **Teach** — use sequence, checkpoints, and recovery paths; avoid theory
  unless it prevents mistakes.
- **Record** — be precise, neutral, and retrievable; future readers should
  know what happened and why.
- **Present** — compress deeper work; lose fidelity deliberately, preserve
  provenance, and lead with decisions, risks, and asks.
- **Build consensus** — name the decision, the constraint, the options, and
  why this path is acceptable.

## Voice and tone

Voice is stable across artifacts. Tone modulates with the reader's
situation.

Good prose stays:

- **Precise** — claims are bounded to what the facts support. Better to omit
  a weak claim than pad with unsupported commentary.
- **Direct** — lead with the point; avoid throat-clearing.
- **Useful** — every paragraph helps the reader decide, act, or understand.
- **Calm** — no hype, urgency theatre, significance inflation, or
  motivational gloss.

Tone modulates without changing voice. Match the reader's situation:

- Terse and corrective for blocked or failing workflows.
- Patient and ordered for guides and education.
- Neutral and evidence-first for decisions, reviews, and risks.
- Warm and personal for relationship-building, gratitude, and condolences.
- Concise and decision-oriented for executives and stakeholders.

If a sentence needs excitement to work, the claim is too weak. Preserve
voice that comes from honest judgment and concrete observation; cut
personality that decorates the prose.

Use the most specific register the reader can follow without friction.
Define technical terms when the reader may not share the context; do not
dumb them down when the reader does.

## Structure and scanability

Readable prose is accessible prose. A reader should recover the main point
by scanning, by screen reader, or by returning later.

- Put the most important information first.
- Group related ideas; separate distinct topics.
- Use descriptive headings that name the topic, not decorative labels.
- Use true lists for steps, peer constraints, or examples. Use numbered
  lists only when order matters.
- Use descriptive link text. Avoid signposting, like "click here" or bare URLs unless the URL itself is the subject.
- Define abbreviations or project-specific terms on first use.
- Prefer text over images when text can carry the same information.

Use a structured shape when the artifact repeats, when readers benefit from
familiar sections, or when comparison across examples matters. Skip
structure when headings would restate themselves or the artifact is short
enough for plain prose.

## Review pass

Apply these references before any human-facing prose is handed off. They are
always in force:

- `references/lessons-in-clarity-and-grace.md` — diagnostic revision. Fix
  unclear sentence action, hidden agents, broken information flow, weak
  emphasis, and section coherence.
- `references/humanizer-patterns.md` — Signs of AI Writing. Remove inflated
  significance, generic praise, false balance, stock transitions, and
  synonym cycling.
- `references/humanizer-word-choice.md` — word- and phrase-level review.
  Covers AI-writing vocabulary, institutional clutter (business, academic,
  government, marketing), filler phrases, and promotional puffery.

## Pairing with surface skills

Some artifacts carry their own operating contracts. When the artifact
matches a surface skill, load that surface first; this skill handles the
writing quality beneath it.

- `pull-request` for PR bodies, review comments, review guides, and merge
  notes.
- `issue-writing` for issue titles, bodies, scope, decomposition, and
  acceptance criteria.
- `task-management` for task tracker items, status, blockers, dependencies,
  and handoffs.
- `stakeholder-update` for compressed status, risk, decisions, and asks.
- `visual-styleguide` for rendered surfaces where layout, type, color, or
  brand affect the result.

## References

| File                              | Use                                                                                               |
| --------------------------------- | ------------------------------------------------------------------------------------------------- |
| `lessons-in-clarity-and-grace.md` | Diagnostic revision: sentence action, hidden agents, flow, emphasis, cohesion, and coherence.     |
| `humanizer-patterns.md`           | Signs of AI Writing: artifact patterns with before/after rewrites.                                |
| `humanizer-word-choice.md`        | Word- and phrase-level review: AI vocabulary, institutional clutter, filler, promotional puffery. |
