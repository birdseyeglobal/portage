---
name: prose-check
description: Quick prose quality review using a styleguide
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - Skill
  - Agent
argument-hint: <file-path>
---

# Prose Check

Single-pass review focused on prose quality and AI artifact removal.

## Workflow

1. **Identify the target document.** Use the first source that applies:
   - A file path provided as an argument to this command
   - The document most recently edited or discussed in the current session
   - Ask the user if neither applies

2. **Read the full document** before proceeding.

3. **Load the writing skill** by invoking `Skill("content-writing:prose-craft")`. This triggers voice discovery and styleguide selection per the skill's resolution logic.

4. **Load the humanizer skill** by invoking `Skill("content-writing:humanizer")`.

5. **Review the document in a single comprehensive pass.** Evaluate for:
   - Sentence construction (active voice, positive form, parallel structure)
   - Word choice (vague/inflated words, unnecessary jargon)
   - Rhythm and flow (sentence length variation, loose sentence succession)
   - Emphatic placement (strongest words at sentence and paragraph ends)
   - AI artifacts (significance inflation, promotional language, synonym cycling, em dash overuse, negative parallelisms, rule of three overuse, copula avoidance)
   - Styleguide-specific rules from the loaded reference

6. **Present findings organized by severity:**
   - Issues that change meaning or mislead the reader
   - Issues that weaken the prose (vague language, passive voice, filler)
   - Polish opportunities (rhythm, emphasis, word choice upgrades)

7. **Apply fixes** after presenting findings, or ask the user if they'd like you to apply them.

## Constraints

- Do not alter the document's structure, headings, or organization — that's the editorial-review command's job.
- Do not evaluate citations or sources — that's also editorial-review territory.
- Focus exclusively on prose quality and AI artifact removal.
