---
name: reddit-citation-analysis
description: |
  Analyze Reddit citations in LLM tracking exports and produce a GEO strategy for Reddit-sourced AI answers. Use when the user asks where a brand appears on Reddit, how AI answers cite Reddit, which subreddits matter, branded versus unbranded Reddit patterns, competitor Reddit tactics, Reddit citation strategy, or a Reddit-specific report from citation data.
---

# Reddit Citation Analysis

Analyze how Reddit contributes to AI-search answers about a brand, category, or competitor set.

This skill works from citation exports and, when available, thread/comment review. It should not invent comment evidence. If raw Reddit text is unavailable, base conclusions on URL patterns, subreddit names, titles, citation frequency, and AI response snippets, and label that limitation.

## Inputs

Required:

- Citation export with Reddit URLs or a broader citation export that can be filtered to Reddit.
- Brand name.

Helpful:

- Competitor list from the active engagement context.
- Prompt execution data.
- AI response text.
- Raw Reddit thread or comment payloads.
- Brand stance on community engagement.

Useful columns:

- `url`
- `root_domain`
- `title`
- `frequency`
- `unique_executions`
- `type`
- `prompt`
- `topic`
- `ai_response`

## Workflow

1. Resolve competitor candidates from the current engagement.
2. Filter citation rows to Reddit URLs.
3. Normalize subreddit, thread, and user-profile URLs.
4. Split branded prompts from unbranded category prompts when prompt data is available.
5. Rank subreddits by citation frequency and unique executions.
6. Identify thread types:
   - Direct brand reputation threads.
   - Alternatives and comparison threads.
   - "Best for" recommendation threads.
   - Problem-solving threads.
   - Review or complaint threads.
   - User-profile FAQ pages.
7. Compare competitor presence.
8. Extract sentiment only when the source text or AI response supports it.
9. Recommend owned content and community engagement actions.

## Competitor Resolution

Do not rely on generic industry defaults. Before running the helper script, fetch competitors from the best available source for the specific brand and conversation.

Preferred order:

1. Yolando MCP or product/database MCP, when available. Query the active customer, workspace, brand, or tracking project for configured competitors, tracked alternatives, and citation-tracker competitor entities.
2. Postgres MCP, when available. Query the relevant customer/workspace/project tables for competitor names or domains associated with the brand.
3. User-provided competitor list in the conversation.
4. Prompt execution or citation exports, if they contain competitor columns.
5. Public research only as a fallback, and label it as inferred.

Pass the resolved list to the script with `--competitors` or `--competitors-file`. Keep a short note in the final report or handoff stating where the competitor list came from.

## Helper Script

Use `scripts/build_report.py` when the user wants a PDF deliverable from a citation CSV:

```bash
python3 <skill-path>/scripts/build_report.py \
  --csv path/to/citations.csv \
  --brand "Brand Name" \
  --output reddit-citation-analysis.pdf \
  --competitors "Competitor A,Competitor B" \
  --prepared-by "Yolando"
```

For longer lists, write the MCP/database result to a newline, CSV, or JSON file and pass `--competitors-file`.

The script uses ReportLab. It defaults to the Yolando logo from the `styleguide` plugin; use `--logo` only to override that default.

## Responsible Strategy Rules

- Do not recommend spam, astroturfing, fake accounts, vote manipulation, or undisclosed promotion.
- Prefer transparent participation, owned answer pages, customer support improvements, and useful expert responses.
- Separate what the brand can do on Reddit from what it should publish on its own site.
- Flag legal, medical, financial, or regulated advice risks when relevant.

## Report Structure

Return:

1. Executive summary.
2. Data source and coverage.
3. Reddit share of citations.
4. Top cited subreddits and threads.
5. Branded versus unbranded patterns.
6. Competitor tactics.
7. Sentiment and risk notes, if supported.
8. Recommendations by priority.
9. Follow-on data needed.

## High-Leverage Signals

Watch for:

- A small number of threads driving a large share of citations.
- Competitor-owned or competitor-adjacent user-profile FAQ pages.
- Unbranded category threads where the target brand is absent.
- Brand reputation threads that AI answers repeatedly cite.
- Fact-based Reddit threads that should have an owned answer page.

## Verification

Before finalizing:

- Reddit URLs are deduplicated.
- Branded and unbranded findings are not mixed.
- Sentiment claims cite source text or are labeled as unavailable.
- Recommendations are ethical and platform-aware.
- The report states whether raw comments were reviewed.
