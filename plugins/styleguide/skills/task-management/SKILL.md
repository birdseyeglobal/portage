---
name: task-management
description: |
  Use when drafting, revising, or reviewing operational task tracker items,
  task lists, project tasks, implementation subtasks, status-bearing work
  items, blocker notes, dependency notes, ownership handoffs, follow-up tasks,
  and task decomposition. Handles actionable outcomes, assignee expectations,
  current status, blockers, dependencies, acceptance checks, and follow-up
  boundaries. Pair with content-styleguide for deeper prose quality.
---

# Task Management Guidelines

This skill owns task tracker and work-management writing. Pair with
`content-styleguide` for deeper revision: clarity, word choice, voice, tone, and
AI-artifact cleanup.

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

## Workflow

1. Name one actionable outcome in the title.
2. State the current status only if it changes what the reader should do.
3. Add owner or assignee expectations when responsibility could be ambiguous.
4. Name blockers and dependencies as concrete next-state problems.
5. Add acceptance checks when "done" could be interpreted more than one way.
6. Link deeper context instead of copying design, roadmap, or PR history.
7. Decompose oversized tasks along a natural boundary before handoff.

For detailed task shapes and examples, read `references/task-shape.md`.

## Boundary With Issues And PRs

Use `issue-writing` for durable GitHub issue framing: problem, outcome, scope,
and acceptance criteria.

Use `pull-request` for what changed, how it was verified, and how reviewers
should read the diff.

Use this skill for operational work state: tasks, subtasks, dependencies,
blockers, owners, and handoffs. A task can point to an issue or PR, but it
should not become either one.

## What To Cut

- Design debate that belongs in a document.
- Full PR histories when a link and one-sentence relationship will do.
- Status labels with no next-state implication.
- Checklists that rewrite the implementation line by line.
- Multi-owner work bundled into one task without decomposition.
