---
name: issue-writing
description: |
  Use when drafting, revising, triaging, or reviewing GitHub issue titles and
  bodies, bug reports, feature requests, internal implementation issues,
  acceptance criteria, scope boundaries, decomposition notes, and links to
  supporting documents. Handles issue framing, scope, title shape, checkable
  outcomes, and when context belongs somewhere else. Pair with
  content-styleguide for deeper prose quality.
---

# Issue Writing Guidelines

This skill owns GitHub issue operating logic. Pair with `content-styleguide` for
deeper revision: clarity, word choice, voice, tone, and AI-artifact cleanup.

## Issue Contract

An issue frames one unit of work clearly enough that a competent assignee can
start. It is not a ritual template, a user story, a design document, or a PR
summary.

The standard is practical: could the assignee start without another planning
meeting? If yes, the issue is probably detailed enough. If no, add the missing
constraint, example, acceptance check, or link to the document that owns the
deeper context.

## Workflow

1. Identify whether the issue is public intake, internal implementation work,
   bug reproduction, feature proposal, or follow-up capture.
2. Name the outcome in the title.
3. State the problem or opportunity and the desired end state.
4. Add only the context, constraints, evidence, and links that change the work.
5. Add two to five acceptance checks when completion could otherwise be
   ambiguous.
6. Decompose oversized work before handing it off.

For detailed examples and checks, read `references/issue-shape.md`.

## Boundary With Task Management

Use this skill for GitHub issues: durable work framing, issue titles, issue
bodies, and acceptance criteria.

Use `task-management` for operational task tracker items, status, blockers,
ownership, dependencies, handoffs, and follow-up boundaries. A task can point to
an issue, but it should not duplicate the issue's deeper frame.

## What To Cut

- Forced templates that restate themselves.
- Design rationale that belongs in a supporting document.
- Long transcripts, stack traces, or research dumps without a compact summary.
- Acceptance criteria that are just implementation steps.
- Vague verbs such as "improve", "rework", "modernize", or "clean up" without a
  concrete outcome.
