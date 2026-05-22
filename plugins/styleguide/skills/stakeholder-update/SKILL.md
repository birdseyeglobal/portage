---
name: stakeholder-update
description: |
  Use when drafting, revising, or reviewing stakeholder updates, executive
  updates, status notes, leadership briefs, decision memos, meeting briefs,
  presentation notes, update emails, Slack updates, and compressed summaries
  for readers who need status, risk, decisions, tradeoffs, provenance, or asks.
  Pair with content-styleguide for deeper prose quality and visual-styleguide
  for rendered surfaces.
---

# Stakeholder Update Guidelines

This skill owns compressed decision-support communication. Pair with
`content-styleguide` for deeper revision: clarity, word choice, voice, tone, and
AI-artifact cleanup. Pair with `visual-styleguide` when the update is a rendered
page, deck, PDF, or other designed surface.

## Update Contract

Stakeholder updates compress deeper work for decision-makers. They are not full
documentation, source archives, or project journals. Their job is to make
status, risk, decisions, and asks clear enough for the next conversation or
decision.

The format can be a Slack note, email, memo, issue comment, meeting brief, PDF,
or deck. The invariant is compression.

## Workflow

1. Identify the decision, risk, status change, or support need the reader cares
   about.
2. Lead with what changed, what matters now, what is blocked or risky, and what
   decision, support, or attention is needed.
3. Compress source material around the reader's next action.
4. Preserve provenance by linking the strongest source for important claims.
5. Cut implementation trivia unless it changes the decision, risk, status, or
   ask.
6. Run a freshness pass before sending.

For detailed update patterns, read `references/update-shape.md`.

## Boundary With Visual Surfaces

Use this skill for the content path: status, risk, decisions, asks, and source
trail.

Use `visual-styleguide` when layout, type, color, link styling, slide structure,
or rendered presentation affects the result.

## What To Cut

- PR lists, research dumps, metric tables, or roadmap inventories that have not
  been converted into a status, decision, risk, or ask.
- Implementation trivia that does not change the stakeholder's next action.
- Weak link piles where one source would be stronger.
- Current-status claims that have not been checked against the latest source of
  truth.
