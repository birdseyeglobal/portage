---
name: editorial-review
description: Editorial review — prose quality, citations, and AI artifacts. Add "with independent scoring" for parallel Copy Desk evaluation.
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - Skill
  - Agent
argument-hint: <file-path>
---

# Editorial Review

Three-pass editorial review in the main context window. Each pass loads a skill,
evaluates the document, presents findings, and applies fixes before moving on.

For an independent evaluation using parallel sub-agents, add "with independent
scoring" to the command invocation.

## Default: Main Context Review

### Step 1 — Identify the document

Use the first source that applies:

- A file path provided as an argument to this command
- The document most recently edited or discussed in the current session
- Ask the user if neither applies

Read the full document before proceeding.

### Step 2 — Load skills

Load the writing skill by invoking `Skill("content-writing:prose-craft")`. This
triggers voice discovery and styleguide selection.

Load the humanizer skill by invoking `Skill("content-writing:humanizer")`.

If the document contains claims, statistics, or external references, load
citation-sourcing by invoking `Skill("content-writing:citation-sourcing")`.

If the document is intended for search performance, load seo-optimization by
invoking `Skill("content-writing:seo-optimization")`.

### Step 3 — Pass 1: Prose quality

Apply the writing skill with the established voice and styleguide:

- Principles that always apply (consistency, clarity of intent, progressive
  development)
- Construction techniques (sentence rhythm, paragraph construction, strong
  openings and closes)
- Styleguide-specific rules from the loaded reference

Present prose findings and apply fixes.

### Step 4 — Pass 2: Citations (if loaded)

Apply the citation-sourcing skill:

- Source tier validation
- Named attribution for all statistics
- Hallucination red flags (conflicting data, unsourced precision)
- Temporal recency
- Vendor disclosure

Present citation findings and apply fixes.

### Step 5 — Pass 3: AI artifacts

Apply the humanizer skill with its full reference files:

- All 29 detection patterns
- AI word choice corrections (GPT and Claude vocabulary)
- Filler and throat-clearing phrases

Present humanizer findings and apply fixes.

### Step 6 — Summary

Summarize changes grouped by pass.

## Option: Independent Scoring ("with independent scoring")

When the user adds "with independent scoring" (e.g., `/editorial-review
docs/article.md with independent scoring`), replace the three-pass main-context
review with parallel Copy Desk evaluation.

### How it works

1. Complete Steps 1 and 2 (identify document, load skills, establish voice and
   styleguide).

2. Dispatch parallel evaluator agents — one per dimension. Each agent receives
   the document and the instructions for its assigned scope. Each evaluates
   independently in a fresh context.

   Dispatch all agents in a single message so they run simultaneously:
   - **Universal quality** — consistency, clarity of intent, progressive
     development
   - **Voice compliance** — register, person, evidence norms, jargon stance
     (criteria extracted from the voice statement)
   - **Citation quality** — source tiers, attribution, hallucination flags,
     recency, vendor disclosure
   - **SEO compliance** — answer-first, keyword placement, depth, linking, FAQ
     completeness, duplicate content
   - **Humanizer** — full 29-pattern scan with word-watch lists and
     model-generation vocabulary

3. When all agents complete, merge their reports into a unified scorecard with
   Pass/Partial/Fail per criterion.

4. Present the scorecard. Highlight critical failures. Ask the user whether to
   apply fixes for all failing criteria or selectively.

5. Apply approved fixes. Summarize before and after scores.

### When to recommend independent scoring

- The document was written by the same agent that would be reviewing it (self-
  evaluation bias)
- The user wants a formal quality gate with a scored report
- Multiple stakeholders need to see an objective scorecard
- The document is high-stakes (public-facing, regulatory, executive audience)

For routine editorial passes on drafts in progress, the default three-pass
review is faster and sufficient.
