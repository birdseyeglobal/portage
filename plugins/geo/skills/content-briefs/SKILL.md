---
name: content-briefs
description: |
  Generate citation-grounded GEO content briefs from LLM prompt execution data, citation exports, AI responses, competitor pages, and keyword evidence. Use when the user needs differentiated article briefs that explain what to write, why it should win citations, which competitor patterns to address, and which sources or entities the writer should cover.
---

# GEO Content Briefs

Create writer-ready content briefs from AI-search evidence.

This skill is for depth over volume. It is most useful when a team has prompt tracking data and wants a small set of briefs that are specific enough for a writer or AI drafting system to execute without doing the research again.

## Inputs

Required:

- Prompt execution data. See `references/input-format.md`.
- Brand context: website, offer, audience, geography, and positioning.

Recommended:

- URL-level citation export.
- Example AI responses for the target prompts.
- Competitor domains or pages.
- Keyword research with volume and difficulty.
- Brand voice or editorial guidelines.

If paid SEO or brand-radar tools are unavailable, work from the uploaded data, search results, cited URLs, and source pages. State the limitation.

## Workflow

1. Load the prompt execution data.
2. Compute priority signals: prompt count, brand mention rate, competitor mention rate, citation gaps, funnel stage, and topic importance.
3. Select a focused target set. Default to 5 to 15 briefs.
4. For each target prompt or cluster:
   - Parse citation URLs and classify source types.
   - Read the most-cited pages.
   - Mine AI responses for answer structure, entities, and repeated omissions.
   - Check keyword opportunity when keyword data is available.
   - Identify the market-specific content angle.
   - Collect external sources the writer should cite.
   - Write a full section-by-section article outline.
5. Verify that briefs do not collapse into the same template.
6. Output a CSV or Markdown brief set.

## What Each Brief Must Contain

Use `references/output-columns.md` for the full CSV schema. At minimum, each brief needs:

- Target prompt or cluster.
- Funnel stage.
- Primary keyword or query theme.
- Target audience.
- Citation gap evidence.
- Competitor pages to study.
- What current content gets wrong.
- Brand angle.
- Article outline with section-level guidance.
- Entities and source types to include.
- Suggested external data sources.
- Internal links or owned pages to connect.
- Quality checklist for the writer.

## Brief Quality Rules

Do not write generic content tasks.

Weak:

- "Write a comprehensive guide about payment processing."

Strong:

- "Write a decision guide for vertical SaaS founders comparing payment facilitation, referral, and managed PayFac models. Explain risk ownership, underwriting, revenue share, implementation time, and what changes once a platform crosses meaningful payment volume."

Every brief should include data-grounded specificity:

- Named competitor URL patterns.
- Citation counts or source frequency when available.
- Keyword volume or difficulty when available.
- Concrete entities, questions, and sections to include.
- A reason this article should be cited by LLMs.

## Verification

Before finalizing:

- Each brief has a distinct angle.
- No outline is a reused skeleton with swapped nouns.
- All numerical claims are sourced or marked for verification.
- The brief can be handed to a writer without additional research.
- The recommendation ties back to AI-search evidence, not just SEO intuition.
