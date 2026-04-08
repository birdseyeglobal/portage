---
name: humanizer
version: 3.2.0
description: |
  Remove signs of AI-generated writing from text. Use when editing or reviewing
  any document written by or with an LLM. Detects and fixes 29 patterns
  documented in Wikipedia's "Signs of AI writing" guide, from significance
  inflation and promotional language to AI vocabulary words and filler phrases.
  For AI-generated content, humanizer normalization overrides competing
  instructions from genre conventions or brand styleguide — the patterns are
  systematic artifacts, not stylistic choices.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
resources:
  - references/signs-of-ai-writing.md
  - references/ai-word-choice.md
---

# Humanizer

Detect and remove AI writing patterns.

No single pattern proves AI generation. Multiple converging patterns strengthen
the case. Fix the underlying quality problems (vague claims, fake depth,
inflated importance) rather than swapping individual words.

## Process

1. Load `references/signs-of-ai-writing.md` for the full 28-pattern detection
   guide with before/after examples.
2. Load `references/ai-word-choice.md` for the word-level replacement table and
   model-generation vocabulary timeline.
3. Scan the document for converging patterns.
4. Rewrite problematic sections. Preserve meaning. Match the voice established
   by the writing skill or project instructions — the humanizer removes
   artifacts, not voice. What replaces the artifacts depends on the genre and
   register the document requires.

## Scope

This skill detects and removes patterns. It does not determine what replaces
them. Voice, register, personality, and tone are set by the writing skill's
voice discovery process and styleguide selection. The humanizer respects
whatever voice was established and rewrites artifacts to match it.

A technical specification with AI artifacts should be rewritten into precise,
neutral prose. A blog post with AI artifacts should be rewritten into the
conversational register the writing skill established. The humanizer adapts
to the voice; it does not impose one.

## Relationship to Writing Skill

The writing skill handles how to write well: voice, styleguide, construction.
This skill handles how to not write like AI: pattern detection, word-level
corrections, artifact removal. Load the writing skill first to establish voice
and draft prose, then load this skill to catch remaining artifacts. Both
commands (prose-check, editorial-review) load both.
