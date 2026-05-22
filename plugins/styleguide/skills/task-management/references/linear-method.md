# Linear Method as a Task Style Guide

Adapted from [linear.app/method](https://linear.app/method). This is the
canonical operating philosophy for shaping, writing, prioritizing, and
resolving work items. When task style decisions are ambiguous, defer to the
principles below.

## Contents

- [Core philosophy](#core-philosophy)
- [Write issues, not user stories](#write-issues-not-user-stories)
- [Title style](#title-style)
- [Description style](#description-style)
- [Authorship](#authorship)
- [Enablers, blockers, and maintenance](#enablers-blockers-and-maintenance)
- [Scope](#scope)
- [Momentum](#momentum)
- [Direction hierarchy](#direction-hierarchy)
- [Cycles](#cycles)
- [Building with users](#building-with-users)
- [Design tasks](#design-tasks)
- [Launching](#launching)
- [Building in public](#building-in-public)

## Core philosophy

Three quotes set the posture:

> Software project management tools should build with the end users — the
> creators — in mind.

> User stories have become a cargo cult ritual that feels good but wastes a
> lot of resources and time.

> Startups rarely die because they made too much progress or because of a
> single bad decision, but they do die when they move too slow or give up.

Tasks exist to keep creators productive. Tooling, hierarchy, status, and
labels are scaffolding for execution — not artifacts to maintain for their
own sake. If a field, section, template, or status doesn't change the next
action, cut it.

Don't invent terms. Projects should be called projects. Issues should be
called issues. Tasks should be called tasks. Inventing new words for the
same concept confuses teams and obscures the actual operating model.

There isn't always a best answer. Sometimes the most important thing is to
make a decision and move on. Reserve space on product timelines for
unplanned work, and allow plans to change when needed.

## Write issues, not user stories

User stories evolved twenty years ago to translate customer requests into
engineering work. Today they slow execution: they hide the task behind
ceremony, silo engineers into checking off requirements instead of
reasoning about user experience, and bring product-level details to the
task level where they don't belong.

Write short, plain-language issues that describe a concrete task. Discuss
user experience at the **product level** when scoping a project; once the
work is delegated, let the assignee execute against an outcome.

A task should describe:

- A piece of code, design, document, or action with a clear outcome.
- Just enough context that the assignee can start working.
- Links to deeper discussion when more context is genuinely needed.

If it's not a task, don't file it as one. Project ideas, design
explorations, and large features belong in specs, conversations, or
parent-with-subtasks structures.

Exceptions are fine. Placeholder issues like "Explore design" or "Write
project spec" frame deliverables that precede concrete work; break them
down once the shape is known.

## Title style

Titles are scanned in lists. Optimize for fast recognition.

- **Start with a verb.** Add, Fix, Implement, Remove, Update, Replace,
  Document, Split, Move, Rename.
- **Name the outcome, not the process.** "Add rate limiting to prompts
  API" beats "Work on rate limiting."
- **Keep titles under ~60 characters.** A scannable title is a usable one.
- **Skip service prefixes.** Labels carry routing information; the title
  shouldn't repeat it.

<strong-titles>
Add rate limiting to prompts API
Fix mobile layout on dashboard charts
Replace polling with WebSocket for live updates
</strong-titles>

<weak-titles>
[Backend] Add rate limiting to the prompts API endpoint
User should be able to see charts on mobile
As a user, I want real-time updates so that I can see changes
</weak-titles>

## Description style

Descriptions are optional, not required. Write only what the assignee can't
infer from the title or their own context.

**Three checks before writing more:**

1. **Could a competent engineer start working from this?** If yes, it's
   enough.
2. **Is there anything here the reader already knows?** Remove it.
3. **Would this be shorter as a conversation?** Keep it short and let the
   assignee ask.

**Straightforward task:**

> Add per-API-key rate limiting (100 req/min) to the prompts endpoint
> using FastAPI middleware backed by Redis.

**More context genuinely needed:**

> Consolidate the three recommendation scoring functions into a single
> pipeline. Currently brand_score(), relevance_score(), and recency_score()
> are called independently with redundant DB queries. A single pass would
> cut query count from 9 to 3 per recommendation request.
>
> The tricky part: recency_score() has a side effect that updates
> last_scored_at. That needs to be preserved.

**Never write:**

```
## Summary
[restating the title]

## Requirements
- [ ] Checkbox 1
- [ ] Checkbox 2

## Acceptance Criteria
- [ ] The same checkboxes, reworded
```

When quoting user feedback, quote it verbatim and link to the source
conversation. The customer's words are usually more authentic than a
summary, and the link makes it easy to get more if needed.

## Authorship

Everyone writes their own issues. The person closest to the work
understands it best, and writing forces them to think it through before
starting. AI-assisted drafts are fine; the human reviews and refines
before submission.

Every task should have a single named owner. Other people can be
involved, but responsibility lives with one person.

Exceptions:

- **Bug reports:** filed by whoever finds the bug, framed as the problem.
  The assignee proposes the solution and rewrites the issue as a task.
- **Placeholder issues:** when work needs exploration before it can be
  scoped (e.g., "Explore design for X", "Write project spec for Y").
  Break them down once the shape is known.

## Enablers, blockers, and maintenance

Linear replaces "how severe is this?" with "what kind of value does this
create?" Three categories drive priority:

| Type            | Definition                                                |
| --------------- | --------------------------------------------------------- |
| **Blocker**     | Removes friction preventing users from using the product. |
| **Enabler**     | Adds new value or capability.                             |
| **Maintenance** | Tech debt, refactoring, tooling.                          |

### Mapping to priority

```
BLOCKER
  Critical (product unusable)                     → Urgent (P1)
  Significant (major workflow broken)             → High (P2)
  Minor (friction exists, workaround available)   → Medium (P3)

ENABLER
  Moves the needle THIS cycle?                    → High (P2)
  Strategic but not time-sensitive?               → Medium (P3)
  Nice-to-have, no urgency?                       → Low (P4)

MAINTENANCE
  Delaying makes future work harder?              → Medium (P3)
  Stable cost, can wait?                          → Low (P4)
```

### Timeliness questions for enablers

1. Does this align with an active project or initiative?
2. Are there compounding effects — does doing this now make future work
   easier?
3. Is there external timing pressure (customer commitment, market window)?
4. Does completing this unblock other high-value work?

### How to present priority

Show reasoning, not just a number:

> Type: Blocker — users can't export reports without this
> Urgency: High (no workaround exists)

> Type: Enabler — unlocks self-serve onboarding
> Timing: High (aligns with current project goals)

> Type: Maintenance — test suite takes 12 minutes
> Urgency: Medium (slowing every PR, compounding daily)

## Scope

> Scope issues to be as small as possible.

- Issues complete in **hours to days** by one person.
- Projects complete in **1–3 weeks** with 1–3 people.

Shorter scopes force prioritization of the most important feature, build
the habit of shipping continuously, and create quick feedback loops with
customers. Smaller teams reduce management and communication overhead.

### Oversized signals

| Signal             | Example                                      |
| ------------------ | -------------------------------------------- |
| Multiple services  | "API endpoint and dashboard UI"              |
| Multiple concerns  | "Fix query and add caching and update tests" |
| Vague scope        | "Improve the recommendations system"         |
| Large surface area | 10+ files across 3+ directories              |
| Multiple actors    | Backend + frontend engineers needed          |

### Response to oversized issues

Propose decomposition along natural boundaries:

- **Service boundaries** — backend issue + frontend issue.
- **Concern boundaries** — data layer + business logic + presentation.
- **Skill boundaries** — what different people would naturally own.

Each sub-issue must be independently completable and valuable.

### Scope heuristic

```
Can one person complete this in 1–3 days?
├─ YES → Single issue
└─ NO → Can it be broken into 1–3 day pieces?
    ├─ YES → Propose decomposition
    └─ NO → This is a project, not an issue
```

If a project can't be scoped down to 1–3 weeks, break it into stages and
ship the first stage.

## Momentum

> Instead of thinking or talking about doing something, you decide to do
> it or not. Then you do it today instead of tomorrow.

Generate momentum daily. When you don't know the most important thing,
trust your intuition and act; clarity arrives through feedback, not
planning. Talk to users. Correct or revert if you got it wrong — that's
cheaper than paralysis.

It's hard to see visible progress on large tasks, which is demotivating.
Break work into smaller pieces so you can complete several concrete tasks
each week. Marking issues done feels good and sustains momentum.

### Status by priority

- **Urgent / High (P1/P2)** → Todo (immediate attention)
- **Medium / Low (P3/P4)** → Backlog (scheduled later)

### Implications for task creation

- Auto-detect service, type, and assignee when unambiguous — don't ask.
- Present one complete draft with decisions made.
- Reviewer sees the whole proposal, not sequential questions.
- Target zero to one clarifying question per issue.

### Backlog discipline

Not every feature request deserves a permanent home. Important ones
resurface; low-priority ones never get done. A focused backlog makes
planning faster and ensures work actually ships. Prune freely.

## Direction hierarchy

Linear organizes work in three tiers:

```
Initiative  →  Strategic goal (quarterly/annual, workspace-wide)
  └─ Project  →  Time-bound deliverable (1–6 weeks, cross-team)
       └─ Issue  →  Single task (hours to days, one team)
```

### Initiatives

- Express goals the organization aims to achieve.
- Curated collections of projects.
- Workspace-wide visibility, owners, target dates, health status.

### Projects

- Specific, time-bound deliverables (e.g., launching a feature).
- Brief specs communicating "why", "what", "how".
- Can span multiple teams.
- Should correlate to a strategic initiative.

### Connecting issues to direction

When creating an issue:

1. Check active projects — suggest linking if relevant.
2. If no project fits, note it; don't block creation.
3. Never create projects inline during issue creation.

### Strategic posture

Set ambitious, strategic goals — not feature-level ones. Walk back from
the goal to find the path: ten users starts with one user, which starts
with a product someone can find. Successful startups often start with
something small, figure it out, and then scale.

## Cycles

- Time-boxed periods for focused work, **typically two weeks**.
- Maintain a healthy momentum; don't rush toward the end.
- Don't overload cycles — let unfinished work roll to the next cycle
  automatically.
- Cycles are time-based scheduling; projects are goal-based grouping.
- Issues can belong to both a project AND a cycle.
- Include bugs and other fixes as part of cycles.
- Invest in tooling: it's a force multiplier when done right.

## Building with users

When users request features, solve the underlying problem — not the
feature.

- What are they trying to accomplish?
- Is this truly preventing usage (blocker) or nice-to-have (enabler)?
- Are there simpler solutions inside the existing product?

Quote user feedback verbatim when attaching it to a task. Summaries lose
nuance. Link to the source conversation so the assignee can get more
detail.

Users project their needs from the product they currently see, not the
product you're building. Asking "what problem are you trying to solve?"
moves the conversation from feature request to pain point — where you
can evaluate whether and how to address it.

Don't let feedback alone dictate what you build. Listening to users
outside your target demographic can pull you off course. Strategic
initiatives keep the balance between user demand and product vision.

## Design tasks

Design tasks resist neat planning because outcomes are unknown at the
start. Work with that:

1. **First task is always to verify the problem.** Sales/customers ask
   for feature X to fix problem Y; design's job is to confirm Y is real
   and is the right problem.
2. **Use placeholder issues** like "Explore design for X" during early
   exploration. Break them down once the shape is known.
3. **Get feedback while still exploring.** Alternate between overall
   direction and specific details. Tell reviewers which kind of feedback
   you want; ask why people react the way they do.
4. **Create specific tasks once the direction is clear.** "Design X view"
   beats a single weeks-long "design the feature" task. Marking discrete
   pieces done sustains momentum.
5. **Use sub-issues for design + engineering collaboration.** Designers
   file their own issues. Engineers file their own issues. Sub-issues
   keep the work split while preserving project context.

The final solution should be informed by the engineers who will build
it. They surface technical limitations and alternatives early, which
makes collaboration easier and gives engineering deeper problem context.

## Launching

There is no single launch moment. Launch multiple times — each builds on
the last. Massive launches are risky, slow, and easy to waste; smaller
launches compound interest, refine the story, and reach more people over
time.

For task style: ship daily. Small, frequent task completions create
visible progress and a story you can point to over time.

## Building in public

Write changelogs. Even with few users, changelogs:

- Remind the team what shipped and reinforce momentum.
- Show users the product is improving.
- Demonstrate progress to investors.
- Help during slow periods by surfacing prior wins.

For task style: tasks should be small enough that they map cleanly to a
changelog entry. If a task is too vague to describe in a changelog line,
it's probably too vague to start.

The clearest way to see whether something is complete is the diff in the
code or design file. When tasks are scoped small, changes stay small and
review stays manageable. Avoid massive pull requests or large design
changes.
