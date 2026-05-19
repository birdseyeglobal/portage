---
name: styleguide
description: |
  Use when drafting, revising, or polishing communication across an
  organization — internal updates, customer-facing notes, GitHub issues, pull
  requests, replies, discussion threads, CHANGELOG entries, READMEs,
  architecture docs, guides, design proposals or RFCs, docstrings, inline
  comments, roadmap entries, stakeholder updates, presentations, and agent
  instructions. Also load when removing AI writing artifacts (humanizing
  AI-generated prose, fixing AI-sounding text, cutting LLM tells like "delve",
  "leverage", "seamless").
---

# Organization Style Guide

## Surface Selection

Most work under this skill is markdown, comments, issues, pull requests, docs,
or messages. For those surfaces, focus on content, structure, headings, links,
and scanability rather than visual styling.

When producing reading-first HTML, PDF, briefing pages, executive guides, or
other designed communication surfaces, load the `visual-styleguide` skill.

## Principles for good writing

> For detailed diagnostic revision guidance, use
> `references/lessons-in-clarity-and-grace.md`.

### Simplicity

Simple prose is a courtesy to the reader and a constraint on the writer.
If an idea can't survive ordinary words, the idea is probably not ready.

Clear thinking produces clear writing. Unclear writing almost always
reflects unclear thinking. When a sentence is hard to parse, the problem
is rarely vocabulary or grammar — it is that the writer has not decided
what they mean.

#### Tips

1. Never use a long word where a short one will do.
2. Use the technical term when it carries irreducible technical meaning. Use
   the everyday word when it would do the same work. "Synergize" almost always
   loses to "work together." "Leverage" almost always loses to "use." "Ideate"
   almost always loses to "think of."

### Clutter

Every profession and institution generates its own clutter: words and
phrases that sound important but add nothing. Cutting clutter is not
about making sentences shorter — it is about making every word earn its
place.

Common clutter by domain:

| Domain     | Clutter                                 | Clean                        |
| ---------- | --------------------------------------- | ---------------------------- |
| Business   | "at this point in time"                 | "now"                        |
| Business   | "in the event that"                     | "if"                         |
| Academic   | "it is important to note that"          | (just state it)              |
| Academic   | "the question of whether"               | "whether"                    |
| Technology | "provides the ability to"               | "can"                        |
| Technology | "in order to"                           | "to"                         |
| Technology | "in order to facilitate"                | "to help"                    |
| Technology | "utilize"                               | "use"                        |
| Technology | "it will render the system inoperative" | "will break the system"      |
| Technology | "leveraging our platform"               | "using our platform"         |
| Government | "at the present time"                   | "now"                        |
| Government | "for the purpose of"                    | "to"                         |
| Government | "with regard to"                        | "about"                      |
| Marketing  | "best-in-class solution"                | (name what it actually does) |
| Marketing  | "empower your team"                     | (name what they can do)      |
| Marketing  | "drive meaningful results"              | (name the results)           |

Omit needless words. If it is possible to cut a word out, always cut it out.
Each cut returns a word's worth of attention to the reader. If a paragraph can
become a sentence, rewrite it.

Avoid the use of adjectives, especially such extravagant ones as
splendid, gorgeous, grand and magnificent. No superlatives
("world-class"), no consultant verbs ("leverage", "delve"), no
marketing adjectives ("seamless", "robust").

Avoid commentary the facts cannot themselves deliver.

## Always-loaded craft references

Load these references whenever this skill is used. They are always in force:

- `references/lessons-in-clarity-and-grace.md` — diagnostic revision. Use it
  to fix unclear sentence action, hidden agents, broken information flow, weak
  emphasis, and section coherence.
- `references/humanizer-patterns.md` — Signs of AI Writing. Use it to remove
  artifact patterns such as inflated significance, generic praise, false
  balance, stock transitions, and synonym cycling.
- `references/humanizer-word-choice.md` — AI-writing word choice. Use it to
  replace LLM vocabulary while preserving meaning and register.

Do not treat these as optional cleanup. Apply them before any human-facing
prose is handed off.

## Runtime flow

Before drafting or revising, route the prose through five passes:

1. **Genre pass** — what action does this prose perform?
2. **Audience / situation pass** — who is reading, what are they trying to do,
   and what state are they in?
3. **Voice / tone pass** — which voice constants must hold, and what tone does
   this situation need?
4. **Scanability pass** — can a reader skim the page and still find the main
   point, next action, and supporting context?
5. **Surface conventions** — what does this artifact type require?

For substantial prose, briefly hold the answers in mind before drafting. For
small replies, apply the passes silently and keep moving.

Develop from known to new: define the frame before the exception, the contract
before the edge case, and the decision before its consequences.

## Genre pass

Before drafting, identify the primary action this prose performs. Many
artifacts perform more than one action; choose the primary action first, then
let secondary actions shape the ending.

Structure follows the prose's job, not the author's inventory of topics.

- **Inform**: explain a fact, concept, status, or change. Lead with the answer,
  then give the minimum context needed to trust it.
- **Persuade**: argue for a direction or priority. State the recommendation
  early, then show evidence, tradeoffs, and the rejected alternative.
- **Build consensus**: align reviewers or stakeholders around a design
  decision. Name the decision, the constraint, the options, and why this path
  is acceptable.
- **Transfer skill**: teach someone how to use or modify the project. Use sequence,
  checkpoints, and recovery paths; avoid theory unless it prevents mistakes.
- **Certify / record**: create durable history. Be precise, neutral, and
  retrievable; future readers should know what happened and why.
- **Respond**: answer a comment, review, issue, or discussion thread. Resolve
  the point directly, keep the temperature low, and make the next state clear.
- **Request**: ask for review, input, approval, reproduction steps, or a
  decision. Ask for one clear action and explain why it matters.
- **Present**: compress deeper work for a meeting, deck, or executive update.
  Lose fidelity deliberately, preserve provenance, and lead with decisions,
  risks, and asks.

When the prose carries risk, boundary, or failure information, state it plainly
and early.

## Audience / situation pass

Org prose has two reader classes: humans and agents. Humans need clarity,
judgment, and usable context. Agents need explicit boundaries, traceable
decisions, and enough structure to resume work without guessing. Write for the
human first, but preserve provenance and constraints for the agent later.

Identify the primary human reader:

- **Reviewer**: needs scope, risk, reading path, and test evidence.
- **Maintainer**: needs durable context, constraints, and why-decisions.
- **User**: needs steps, outcomes, and recovery paths.
- **Contributor**: needs contracts, extension points, and local conventions.
- **Stakeholder**: needs compressed status, decisions, risks, and asks.

Then identify the reader's situation:

- **Reviewing**: needs scope, risk, reading path, and evidence.
- **Blocked**: needs the answer, the next step, and recovery path early.
- **Deciding**: needs options, tradeoffs, recommendation, and consequence.
- **Learning**: needs sequence, concepts before exceptions, and examples.
- **Maintaining**: needs provenance, constraints, and why-decisions.
- **Scanning**: needs hierarchy, descriptive headings, and short units.

Use the most specific register the reader can follow without friction. Do not
dumb down precise terms; define them when the reader may not share the context.

## Voice / tone pass

Voice is stable. Tone changes with the reader's situation.

Org prose is:

- **Precise**: claims are bounded to what the code, roadmap, or decision record
  supports. Better to omit a weak claim than pad with unsupported commentary.
- **Direct**: lead with the point; avoid throat-clearing.
- **Engineerly**: make constraints, tradeoffs, decisions, and evidence visible.
- **Calm**: no hype, urgency theatre, significance inflation, or motivational gloss.
- **Useful**: every paragraph helps someone decide, review, use, or understand.
  Do not spend paragraphs on what any competent reader would already assume;
  surface the constraint, tradeoff, or implication this work reveals.
- **Traceable**: summaries preserve where claims came from, even when
  compressed.

Do not make the organization sound like a product marketer. If a sentence needs excitement
to work, the claim is too weak.

Tone adjusts without changing voice:

- Use a terse, corrective tone for blocked or failing workflows.
- Use a patient, ordered tone for guides and educational docs.
- Use a neutral, evidence-first tone for decisions, reviews, and risks.
- Use a concise, decision-oriented tone for stakeholders.
- Use a direct but non-coercive tone for requests and reviewer asks.

Avoid ornate writing. Avoid added warmth, humor, or persona when the
reader needs precision, recovery, or accountability. The prose should work like
a clear window: the reader sees the point, not the writer performing.

This does not mean stripping out voice. Preserve the voice that comes from
honest judgment, concrete observation, and sentence rhythm. Cut personality when
it decorates the prose; keep voice when it makes the thinking clearer.

## Accessibility and scanability

Readable prose is accessible prose. A reader should be able to scan the page,
use a screen reader, or return later and recover the main point.

- Put the most important information first.
- Group related ideas together; separate different topics with headings.
- Use descriptive headings that name the topic, not decorative labels.
- Use descriptive link text. Avoid signposting with "click here", "read this", or bare URLs
  unless the URL itself is the subject.
- Use true lists for steps, peer constraints, examples, or acceptance checks.
- Use numbered lists only when order matters.
- Avoid directional language that depends on visual layout, such as "in the
  right sidebar", unless the location is the actual product instruction.
- Define abbreviations or project-specific terms on first use when the reader
  may not know them.
- Prefer text over images when text can carry the same information. If an image
  or diagram carries meaning, include surrounding prose that preserves the
  point.

## Structured content

Some artifacts deserve reusable structure because they repeat, need fast
scanning, or must be produced consistently. Others should be shaped around the
specific job of the prose.

Use a structured shape when:

- the artifact type repeats often;
- readers benefit from familiar sections;
- the same fields need to be compared across examples;
- an agent needs a reliable checklist to avoid omission.

Avoid a structured shape when:

- headings would restate themselves;
- the artifact is short enough for plain prose;
- the structure would make the text feel ritualized;
- the writer needs judgment more than a form.

When a surface needs detailed structure, keep the core rule here and move the
examples or full workflow into a reference file or a separate skill.

## Surface conventions

### README

First-contact product explanation. Lead with what the project is, who it is for, and
the smallest useful path to understanding or trying it.

- Keep deep architecture, roadmap detail, and full API reference out of the
  README; link to them.
- Prefer concrete concepts and runnable examples over positioning language.
- Make the next step obvious.

### Docs

Durable project knowledge. Pair this skill with the `documentation` skill
before editing docs.

- Respect the document's job: architecture explains stable design, guides teach
  current workflows, research preserves evidence, roadmap describes future
  direction.
- Use prose for concepts and judgment; use structure for retrieval, parallel
  comparison, and commands.
- Link to the canonical home instead of duplicating detail.

### Roadmap docs

Future direction, not implementation task lists.

- State the outcome, current status, rough shape, open questions, and
  references.
- Keep pull request sequences, task breakdowns, and rollout checklists out
  unless they are deliberately historical context.
- Do not make speculative work sound shipped.

### Pull requests

Reviewer guidance. Help the reviewer understand scope, risk, reading path, and
evidence.

- Open with what the pull request changes and why it matters.
- Name risk, migration impact, and behavioural change early.
- Address the reviewer directly without over-controlling their role. Use the
  summary to suggest the review posture; use a comment when you need dialogue
  about the reviewer's responsibility or approach.
- Include test evidence and known gaps only when they help the reviewer judge a
  code path, behavior change, migration, or release risk. Omit ritual testing
  sections when CI already covers the meaningful test surface or when the
  change is prose-only or process-only.
- Mirror the CHANGELOG entry when relevant.

Use `references/pull-requests.md` for detailed pull request guidance.

### Issues

Actionable problem or proposal framing. Put the punchline in the title and make
the next unit of work clear.

- State the observed problem, desired outcome, constraints, and acceptance
  criteria.
- Keep straightforward issues short; add context only when it changes the work.
- Split work that cannot be completed by one person in hours-to-days.
- Move deep design, durable architecture, and research evidence into the right
  document; link it from the issue.

Use `references/issues.md` for detailed issue-writing guidance.

### Replies / discussion threads

Thread resolution.

- Answer the specific point first.
- Keep the temperature low and the next state clear.
- Quote or name the concern you are resolving when context might be lost.
- Do not litigate more history than the reply needs.

### Changelog entries

Durable release memory for users and maintainers.

- State user-visible change first.
- Group by Added / Changed / Removed / Fixed / Breaking when the release earns
  structure.
- Include migration notes or before/after examples for breaking changes.
- Avoid internal implementation trivia unless it changes behaviour.

### Docstrings / inline comments

Local contract and rationale.

- Docstrings describe public contract: purpose, parameters, returns, errors,
  side effects.
- Inline comments explain non-obvious why, not what the next line does.
- Keep private implementation narration out of public API docs.

### Executive / stakeholder updates and presentations

Compressed decision support.

- Lead with what changed, what matters, what is blocked, and what decision or
  support is needed.
- Use deliberate fidelity loss. Compress the source material around the
  reader's decision, risk, or status need.
- Preserve provenance by naming the strongest source behind important claims:
  docs, metrics, incidents, customer evidence, research, pull requests, or
  roadmap items.
- Prefer decisions, risks, tradeoffs, and next asks over implementation trivia.
- When there is a presentation surface, make the spoken path clear. Slides and
  companion notes should support the conversation, not replace it.

Use `references/stakeholder-updates.md` for detailed stakeholder update and
presentation guidance.

### Agent instructions

Prompt and instruction surfaces: `AGENTS.md`, skills, role prompts, and workflow
prompts.

- Apply this skill to prose clarity, but do not treat prompt design as ordinary
  documentation.
- Keep instructions direct, testable, scoped, and bounded.
- Review trigger conditions, precedence, conflict risk, and failure modes
  separately.

## References

| File                              | Use                                                                                                                                   |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `lessons-in-clarity-and-grace.md` | Diagnostic revision for unclear sentence action, hidden agents, information flow, emphasis, cohesion, and coherence. Always in force. |
| `humanizer-patterns.md`           | Signs of AI Writing: artifact patterns with before/after rewrites. Always in force.                                                   |
| `humanizer-word-choice.md`        | AI-writing word choice: substitutions for LLM vocabulary. Always in force.                                                            |
| `pull-requests.md`                | Pull request anatomy, reading paths, related pull request handling, review guidance, and verification evidence.                       |
| `issues.md`                       | Issue-writing practice: titles, scope, decomposition, acceptance criteria, and when to move material into separate docs.              |
| `stakeholder-updates.md`          | Executive updates and presentations: compression, provenance, risks, decisions, asks, and spoken-support material.                    |
