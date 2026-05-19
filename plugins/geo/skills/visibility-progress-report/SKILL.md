---
name: visibility-progress-report
description: |
  Create an executive GEO visibility progress report from time-series LLM prompt execution data. Use when the user needs a monthly or quarterly AI-search visibility update, progress narrative, performance report, platform gap analysis, topic trend summary, or executive briefing from prompt tracking exports.
---

# GEO Visibility Progress Report

Build a progress narrative from prompt execution data.

This skill is for recurring reporting after a brand has enough tracking history to show movement. If there is no time series, produce a baseline visibility report instead and label it as such.

## Inputs

Required:

- Prompt execution CSV.
- Brand name.

Useful columns:

- `Execution Date`
- `Prompt`
- `Topic`
- `Platform`
- `Workspace Brand Mentioned`
- `Competitor Mentions`
- `Citations (Links)`
- `AI Response`

Optional:

- Published content count.
- Draft pipeline count.
- Owned URL list.
- Article title mapping.
- Business context for the reporting period.

## Workflow

1. Parse and normalize dates, platforms, topics, brand mentions, competitors, and citations.
2. Check whether the data has enough history for trend reporting. Default threshold: at least 4 weeks.
3. Compute:
   - Current visibility rate.
   - First-period versus latest-period delta.
   - 7-day or period moving average when dates support it.
   - Topic-level visibility.
   - Platform-level visibility.
   - Owned URL citation counts.
   - Competitor mention context.
4. Identify what changed and why.
5. Write an executive summary and visual/report outline.
6. Recommend next focus areas.

## Helper Script

Use `scripts/build_report.py` when the user wants a PDF progress report from a prompt execution CSV:

```bash
python3 <skill-path>/scripts/build_report.py \
  --csv path/to/prompt-executions.csv \
  --brand "Brand Name" \
  --output visibility-progress-report.pdf \
  --prepared-by "Yolando"
```

The script uses ReportLab and Matplotlib. It defaults to the Yolando logo from the `styleguide` plugin; use `--logo` only to override that default.

Use `scripts/build_deck.py` when the user wants a slide deck:

```bash
python3 <skill-path>/scripts/build_deck.py \
  path/to/prompt-executions.csv \
  "Brand Name" \
  visibility-progress-report.pptx
```

The deck defaults to the Yolando logo from the `styleguide` plugin and a dark branded background. Pass `--assets-dir` only to override the deck assets with `logo_light.png` plus optional `bg.png` and `bg_cover.png`. The script uses `python-pptx` and Matplotlib. If LibreOffice is available, it also writes a matching PDF.

## Recommended Report Sections

Use the user's requested format. If unspecified, return a concise markdown report:

1. Executive summary.
2. Current visibility.
3. Visibility trend.
4. Topic-level movement.
5. Platform gaps.
6. Owned URLs earning citations.
7. Under-cited topics.
8. Competitor context.
9. Next focus areas.
10. Data limitations.

For slide-ready output, provide one section per slide with title, takeaway, chart/table guidance, and speaker notes.

## Analysis Rules

- Lead with the business meaning, then the metric.
- Distinguish growth from noise. Small samples should be labeled.
- Do not over-credit content production unless the citation or topic data supports it.
- Separate brand mentions from owned URL citations.
- Show platform gaps when one AI surface lags the others.
- Use non-branded prompts as the main visibility signal when branded prompts would inflate results.

## Verification

Before finalizing:

- Date parsing errors are reported.
- The denominator for every percentage is clear.
- Branded prompt handling is explained.
- Topic and platform calculations use consistent filters.
- Recommendations tie to the weakest topic, weakest platform, or highest-leverage cited URL.
