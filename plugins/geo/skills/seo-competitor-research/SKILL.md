---
name: seo-competitor-research
description: |
  Conduct SEO keyword research and competitor analysis for GEO strategy. Use when the user asks for SEO research, keyword gaps, competitor keyword analysis, content opportunities, organic search strategy, or search evidence to support AI-search visibility work. Produces a markdown report with domain metrics, keyword clusters, competitor benchmarks, page patterns, SERP notes, and prioritized recommendations.
---

# GEO SEO Competitor Research

Produce a search and competitor strategy report that supports GEO content decisions.

This skill can use Ahrefs, Semrush, Search Console, exported CSVs, live search results, or other user-provided data. Always name the data source and date. Do not imply paid-tool precision when the analysis came from public search.

## Inputs

Gather:

- Target domain.
- Competitor domains, ideally 4 to 8.
- Industry or vertical.
- Country or market.
- Keyword seed list, if the user has one.
- Available data source: Ahrefs, Semrush, Search Console, CSV export, or public search.

## Report Structure

Return a markdown report with:

1. Executive summary.
2. Data sources and date.
3. Target domain overview.
4. Competitor comparison.
5. Keyword clusters and content gaps.
6. SERP observations for high-value terms.
7. Competitor page patterns.
8. Existing content opportunities.
9. Prioritized roadmap.
10. Known limits.

## Data Collection

When tool data is available, collect:

- Domain authority or rating metrics.
- Organic traffic estimates.
- Ranking keyword counts.
- Top organic keywords.
- Top pages by traffic.
- Referring domain counts.
- Competitor top pages and top keywords.

When paid data is unavailable:

- Use live SERPs.
- Use competitor site navigation and sitemaps.
- Use page titles, headings, snippets, schema, FAQs, and visible content patterns.
- Treat traffic and difficulty as unknown rather than guessing.

## Analysis Rules

- Group keywords by buyer problem, not only by lexical similarity.
- Separate direct competitors from aspirational publishers or marketplaces.
- Identify page types that repeatedly win: comparison pages, location pages, vertical hubs, alternatives pages, reviews, calculators, FAQs, glossaries, and trust pages.
- Tie every recommendation to observed evidence.
- Distinguish quick wins from authority-building work.
- Do not recommend content solely because a keyword has volume. The page must fit the brand, audience, and funnel stage.

## Verification

Before finalizing:

- The report names all data sources.
- Keyword and traffic numbers are dated.
- Competitor domains are consistently compared.
- Roadmap items name target topics or pages.
- Claims based on public search are labeled as qualitative.
- No raw API output remains in the final report.
