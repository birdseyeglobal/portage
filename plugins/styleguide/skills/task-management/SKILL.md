---
name: task-management
description: |
  Use when drafting, revising, or reviewing operational task tracker items,
  task lists, project tasks, implementation subtasks, status-bearing work
  items, blocker notes, dependency notes, ownership handoffs, follow-up tasks,
  and task decomposition. Handles actionable outcomes, assignee expectations,
  current status, blockers, dependencies, acceptance checks, and follow-up
  boundaries. Built on the Linear Method. Pair with content-styleguide for
  deeper prose quality.
---

# Task Management Guidelines

This skill owns task tracker and work-management writing. It is built on the
[Linear Method](https://linear.app/method) — the canonical operating
philosophy for shaping issues, prioritizing work, and maintaining momentum.
Pair with `content-styleguide` for deeper revision: clarity, word choice,
voice, tone, and AI-artifact cleanup.

## Task Contract

A task tells someone what outcome to produce, what state the work is in, and
what would make it complete. It is not a design document, roadmap item, PR
summary, or meeting transcript.

A useful task answers:

- What single outcome should exist when the task is done?
- Who owns the next move?
- What is the current status?
- What is blocked, dependent, or intentionally out of scope?
- How will completion be checked?
- Where does deeper context live?

## Linear Method Principles

These principles are always in force. Defer to
`references/linear-method.md` for the full deep dive when style judgment
calls arise.

### Write issues, not user stories

Write short, plain-language tasks. Skip "As a user, I want..." framing — it
obscures the work and pushes engineers into checking off requirements
instead of reasoning about the product. Discuss user experience at the
project or feature level; let task descriptions stay focused on the
concrete outcome.

### Verb-led titles

Start titles with a verb that names the outcome: Add, Fix, Implement,
Remove, Update, Replace, Document, Split. Keep them under ~60 characters
and skip service prefixes (labels carry routing).

### Three description checks

Descriptions are optional, not required. Before writing more, ask:

1. Could a competent engineer start working from this? If yes, it's enough.
2. Is there anything here the reader already knows? Remove it.
3. Would this be shorter as a conversation? Keep it short.

When quoting user feedback, quote it verbatim and link the source.

### Enabler, blocker, or maintenance

Triage value first, severity second. A task is one of:

- **Blocker** — removes friction preventing users from using the product.
- **Enabler** — adds new value or capability.
- **Maintenance** — tech debt, refactoring, tooling.

For enablers, ask whether the work moves the needle this cycle, has
compounding effects, faces external timing pressure, or unblocks other
high-value work. Present reasoning, not just a priority number.

### Scope to hours or days

One person, one to three days. Decompose larger work along service,
concern, or skill boundaries — each piece independently completable and
valuable. Work that needs 1–3 weeks and 1–3 people is a project, not a
task.

### Momentum

> Instead of thinking or talking about doing something, you decide to do
> it or not. Then you do it today instead of tomorrow.

Auto-detect service, type, and assignee when unambiguous. Present one
complete draft. Target zero to one clarifying question per task. When in
doubt, act; clarity arrives through feedback, not planning.

## Workflow

1. Name one actionable outcome in a verb-led title.
2. Classify the work — blocker, enabler, or maintenance — and let that
   drive priority.
3. State the current status only if it changes what the reader should do.
4. Add owner or assignee expectations when responsibility could be
   ambiguous.
5. Name blockers and dependencies as concrete next-state problems.
6. Add acceptance checks when "done" could be interpreted more than one
   way.
7. Link deeper context instead of copying design, roadmap, or PR history.
8. Decompose oversized work along natural boundaries before handoff.

For detailed task shapes and examples, read `references/task-shape.md`.
For the full Linear Method as a task style guide, read
`references/linear-method.md`.

## Boundary With Issues And PRs

Use `issue-writing` for durable GitHub issue framing: problem, outcome,
scope, and acceptance criteria.

Use `pull-request` for what changed, how it was verified, and how
reviewers should read the diff.

Use this skill for operational work state: tasks, subtasks, dependencies,
blockers, owners, and handoffs. A task can point to an issue or PR, but
it should not become either one.

## What To Cut

- Design debate that belongs in a document.
- Full PR histories when a link and one-sentence relationship will do.
- Status labels with no next-state implication.
- Checklists that rewrite the implementation line by line.
- Multi-owner work bundled into one task without decomposition.
- "As a user, I want..." framing — write the task directly.
- Required template sections that restate the title or pad the body.
- Service prefixes in titles when labels already carry routing.

## References

| File               | Use                                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| `task-shape.md`    | Operational shape for tasks: titles, fields, status, blockers, acceptance checks, decomposition. |
| `linear-method.md` | Full Linear Method as a task style guide. Defer here when style judgment calls arise.            |
