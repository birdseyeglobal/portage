# Prose Plugin

A composable toolkit for content quality in Claude Code. Seven skills handle distinct concerns -- writing craft, citations, SEO, video scripts, social posts, transcript cleanup, and AI artifact removal -- and two commands chain them into editorial workflows.

The skills are independent. Load one, load three, load all seven. They don't conflict because they operate on different axes: sentence construction, source integrity, format constraints, and pattern detection. Pick what the task demands.

---

## Skills

### Prose Craft

The core skill. It governs sentence construction, word choice, parallel structure, rhythm, and styleguide calibration. Before drafting or revising, it asks you to choose one of three styleguides -- Elements of Style, Dreyer's English, or Lessons in Clarity and Grace -- then filters every rule through that choice. Strong styleguides earn latitude; weak ones don't.

Two supplementary references layer on top of any styleguide without conflict: On Writing Well for genre-specific voice (technology writing, business strategy, tutorials) and Microstyle for headlines, taglines, and button text.

This isn't a linter. It teaches construction -- how to open a paragraph, where to place the emphatic word, when passive voice is legitimate, why three loose sentences in a row bore the reader. Load it for anything a human will read, review, or act on.

### Citation Sourcing

Source tier definitions, citation formatting, verification patterns, and hallucination prevention. It ranks sources into three tiers -- academic journals and government data at the top, anonymous blogs and content farms at the bottom -- and requires that key claims draw from Tier 1 or 2.

The skill also catches hallucination red flags: suspicious precision without attribution, unnamed experts, unverifiable case studies, statistics that can't be traced to an original source. If a blog post cites a McKinsey report, find and cite the McKinsey report.

### SEO Optimization

Content-level SEO based on the Periodic Table of SEO Elements (Search Engine Land, 7th Edition, 2024). Covers keyword placement, E-E-A-T signals, semantic SEO, topic clustering, and Generative Engine Optimization. Items are tagged by priority: **Must** for every piece of content, **Should** for performance gains, **Context** for background knowledge.

It doesn't cover server configuration or crawl budgets. It covers what a content writer controls.

### Video Scripting

Pure narration for text-to-speech delivery. The output feeds directly into a TTS engine, so the skill enforces a strict constraint: no markdown, no visual directions, no bracketed cues, no stage instructions. If it can't be spoken aloud, it doesn't belong.

Scripts target roughly 150 words per minute. Verbal transitions ("First," "Next," "Here's why this matters") replace headings. The skill covers hook structure, pacing, and how to guide a listener through an argument without visual aids.

### Social Media

Platform-specific formatting, character limits, and tone for LinkedIn, Twitter/X, Instagram, Facebook, Threads, and Reddit. The skill enforces hard rules that apply everywhere: no external links (most platforms penalize them), no placeholders (posts go live as written), no em dashes (they signal AI-generated content to readers), and no image placeholders.

Each platform gets its own conventions, character budgets, and target lengths.

### Humanizer

Detects and removes signs of AI-generated writing. Based on Wikipedia's "Signs of AI writing" guide (maintained by WikiProject AI Cleanup), it catches inflated symbolism, promotional language, synonym cycling, em dash overuse, the rule of three deployed as a tic, vague attributions, and excessive conjunctive phrases.

But removing AI patterns is only half the job. Sterile, voiceless writing is as obvious as slop. The skill pushes for personality -- opinion, specific detail, an actual human perspective behind the words.

### Transcript Cleanup

Cleans speech-to-text artifacts from transcripts and direct quotes without editorializing. The rule: if you can't point to a specific speech artifact or transcription error, don't change the sentence. "Sounds better" isn't a reason to edit.

It handles filler "like," spoken grammar errors (subject-verb agreement, broken comparisons), false starts, run-on transcription, and hedging artifacts. The speaker's vocabulary, sentence structure, and personality stay intact.

---

## Commands

### `/prose-check`

A single-pass review focused on prose quality and AI artifact removal. It loads the writing skill (which triggers styleguide selection) and the humanizer, then reviews the document for sentence construction, word choice, rhythm, emphatic placement, and AI artifacts. Findings are organized by severity: meaning-altering issues first, then weaknesses, then polish opportunities.

It doesn't touch structure, headings, or citations. Those belong to the editorial review.

**Usage:** `/prose-check <file-path>`

### `/editorial-review`

A full sequential editorial workflow with four passes. The order matters -- structure gets fixed first so prose revisions aren't wasted on sections that get reorganized.

1. **Structure** -- heading hierarchy, answer-first formatting, section depth, archetype alignment, thesis threading
2. **Prose** -- active voice, positive form, parallel construction, word choice, sentence rhythm, styleguide-specific rules
3. **Citations** -- source tier validation, hallucination red flags, temporal requirements, citation density and formatting
4. **AI artifacts** -- significance inflation, synonym cycling, em dash overuse, promotional language, vague attributions

Each pass presents findings, applies fixes, then moves to the next. A summary at the end groups changes by pass.

**Usage:** `/editorial-review <file-path>`

---

## Composability

The skills compose because they don't overlap. Prose craft decides how sentences are constructed. Citation sourcing ensures claims are grounded. The humanizer catches patterns that slip through. SEO adds search performance. Video scripting and social media impose format constraints. Transcript cleanup operates on raw speech, not drafted prose.

Load what you need. Skip what you don't.

## Plugin Files

### Agents
- [copy-desk](agents/copy-desk.md)

### Commands
- [editorial-review](commands/editorial-review.md)
- [prose-check](commands/prose-check.md)

### Skills
- [citation-sourcing](skills/citation-sourcing/SKILL.md)
- [humanizer](skills/humanizer/SKILL.md)
- [prose-craft](skills/prose-craft/SKILL.md)
- [seo-optimization](skills/seo-optimization/SKILL.md)
- [social-media](skills/social-media/SKILL.md)
- [transcript-cleanup](skills/transcript-cleanup/SKILL.md)
- [video-scripting](skills/video-scripting/SKILL.md)
