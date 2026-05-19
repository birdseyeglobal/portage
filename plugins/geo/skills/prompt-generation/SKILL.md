---
name: prompt-generation
description: |
  Generate brand-representative prompts for LLM visibility tracking and AI-search discovery monitoring. Use when the user needs natural-language prompts grouped by topic and funnel stage, including prompt sets for ChatGPT, Claude, Gemini, Perplexity, or AI Overviews tracking. Produces CSV-ready prompts that reflect how buyers, consumers, or researchers ask LLMs about a market.
---

# GEO Prompt Generation

Generate natural-language prompts that represent how people discover and evaluate brands through LLMs and AI-search surfaces.

The output is a CSV-ready table with:

- `Topic`
- `Prompt`
- `Funnel Stage`

## Inputs

Gather or infer:

- Brand name and website.
- Products, services, or use cases.
- Target audience and buying context.
- Geographic markets, if relevant.
- Competitors, if known.
- Any terms the brand uses internally.

If a field is missing but the website or source material provides enough context, proceed and note the assumption.

## Workflow

1. Map the brand's products and services into topic categories.
2. Validate the audience's vocabulary before writing prompts.
3. Generate prompts across funnel stages.
4. Check for natural language, commercial intent, and topic coverage.
5. Return CSV-ready output.

## Vocabulary Validation

Before writing prompts, check how the audience actually describes the category.

Use keyword tools, search results, customer language, reviews, forums, sales pages, or competitor copy. Paid SEO tools are useful but not required.

Look for:

- Search terms with real demand.
- Plain-language pain points.
- Outcome framing versus mechanism framing.
- Competitor alternatives people actually compare.
- Jargon that belongs only in bottom-funnel prompts.

Prompts should sound like someone asking an assistant for help, not like ad keywords or internal positioning copy.

## Funnel Mix

Default distribution:

- TOFU: 5 to 10 percent. Educational prompts about concepts and problem framing.
- MOFU: 50 to 60 percent. Evaluation prompts with needs, constraints, or use cases.
- BOFU: 30 to 40 percent. Vendor selection, alternatives, pricing, migration, and comparison prompts.

Adjust the mix when the user asks for a specific tracking purpose.

## Prompt Patterns

Use `references/prompt-patterns.md` for reusable structures. Adapt the pattern to the market instead of filling blanks mechanically.

Strong prompts:

- Use lowercase unless a product or company name requires capitalization.
- Use first-person phrasing when natural.
- Include concrete constraints or situations.
- Describe outcomes the audience wants.
- Avoid brand names in unbranded tracking prompts.
- Vary structure so the set does not look templated.

## Quality Check

Before finalizing, verify:

- Every topic has enough MOFU and BOFU coverage.
- The prompts use the audience's vocabulary.
- The prompts do not overuse the same opening phrase.
- The prompt set includes commercial intent.
- Branded prompts are clearly separated if included.
- Competitor-named prompts are supported by evidence or explicitly requested.

## Output

Return a CSV-ready table:

```csv
Topic,Prompt,Funnel Stage
Embedded Payments,how do saas companies make money from payment processing,TOFU
Embedded Payments,i want to add payments to my saas app without handling compliance myself,MOFU
Embedded Payments,best stripe connect alternative for vertical saas platforms,BOFU
```
