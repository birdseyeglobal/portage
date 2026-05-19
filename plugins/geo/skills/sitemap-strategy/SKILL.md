---
name: sitemap-strategy
description: |
  Build a GEO sitemap and page strategy from prompt execution data, citation exports, competitor pages, and a brand domain. Use for sitemap audits, AI-search page strategy, GEO page playbooks, "what pages should we build", "what existing pages should we improve", citation gap analysis, and page-level content architecture recommendations.
---

# GEO Sitemap Strategy

Turn LLM tracking data and live page review into a page-level plan.

The core question: which existing pages should be improved, and which missing pages should be created, so the brand can earn more citations in AI answers?

## Inputs

Required:

- Prompt execution CSV.
- URL-level citation CSV.
- Brand domain.

Helpful:

- Competitor list.
- Sitemap URL.
- Brand guidelines.
- Product or editorial ownership constraints.
- CMS or URL architecture constraints.

If the user has only one CSV, ask for the missing file. Both prompt-level and citation-level evidence are needed for a strong page strategy.

## Workflow

1. Analyze prompt execution data:
   - Total executions and unique prompts.
   - Brand mention rate.
   - Non-branded brand mention rate.
   - Competitor mention rate.
   - Topic clusters and funnel stage distribution.
2. Analyze citations:
   - Owned URLs cited.
   - Competitor URLs cited.
   - Third-party domains cited.
   - Reddit or social citations.
   - URL path patterns.
3. Crawl or inspect the brand site:
   - Sitemap and key landing pages.
   - Word count and section depth.
   - FAQ, schema, trust signals, author signals, and internal links.
4. Inspect winning competitor pages:
   - H1 and page purpose.
   - Section structure.
   - Entities covered.
   - FAQs and schema.
   - Conversion or trust modules.
5. Split recommendations into:
   - Optimize existing pages.
   - Ship new pages.
6. Write P0 page playbooks for the highest-leverage pages.

## Helper Script

Use `scripts/report_components.py` as a report-component library when producing a PDF strategy. It exports table, card, playbook, and page-chrome helpers plus a `build(...)` function for fully assembled report data.

Typical usage is to create an engagement-specific driver script that imports the helpers and passes prepared data dictionaries:

```python
from report_components import build

build(
    report=REPORT,
    kpis=KPIS,
    findings=FINDINGS,
    topic_data=TOPIC_DATA,
    owned_data=OWNED_DATA,
    comp_data=COMP_DATA,
    patterns=PATTERNS,
    gap_blocks=GAP_BLOCKS,
    proposed=PROPOSED,
    phases=PHASES,
    playbooks=PLAYBOOKS,
    alerts=ALERTS,
    output_path="sitemap-strategy.pdf",
    prepared_by="Yolando",
)
```

The helper defaults to the Yolando logo from the `styleguide` plugin. Pass `logo_path` only to override that default.

## Recommendation Buckets

### Optimize Existing Pages

Use this bucket when the brand already has a relevant page but it is underbuilt, underlinked, stale, thin, missing schema, missing FAQs, or missing entities that competitors cover.

Each recommendation should include:

- Current URL.
- Priority: P0, P1, or P2.
- Citation evidence.
- Benchmark competitor URL.
- What exists now.
- Specific edits.
- Schema and internal-link recommendations.

### Ship New Pages

Use this bucket when competitors win citations with page types the brand does not have.

Each recommendation should include:

- Proposed URL slug.
- Priority.
- Page purpose.
- Target queries or prompts.
- Competitor pattern.
- Required sections.
- Owner suggestion, if product/editorial ownership is clear.

## Page Patterns

Use `references/page-patterns.md` for common citation-winning page types. Adapt them to the brand and market. Do not force every pattern into every industry.

## P0 Page Playbook

For each P0 page, write:

- Target URL or slug.
- Target query set.
- Recommended H1 and opening angle.
- Section-by-section outline.
- Entities and proof points.
- FAQ questions and draft answer guidance.
- Schema types.
- Internal links in and out.
- Measurement plan.

## Verification

Before finalizing:

- The strategy separates existing-page work from net-new pages.
- Every P0 item ties to prompt or citation evidence.
- Competitor examples are named.
- Recommendations respect known product, editorial, regulatory, or technical constraints.
- The report states what data was missing or not crawled.
