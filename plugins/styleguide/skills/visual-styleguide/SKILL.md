---
name: visual-styleguide
description: |
  Use when producing or revising designed communication surfaces for the
  organization: reading-first HTML/PDF pages, executive guides, briefing pages,
  presentation support pages, visual docs, landing pages, and other rendered
  prose surfaces where layout, type, color, and link styling affect the result.
  Load `references/yolando-design-system.md` for Yolando-branded surfaces.
  Pair with the `styleguide` skill when the work also needs voice, structure,
  tone, or AI-writing artifact cleanup.
---

# Visual Style Guide

Use this skill for rendered or designed communication surfaces. Most markdown,
issues, pull requests, comments, and plain messages should use `styleguide`
instead.

## Brand Systems

For Yolando-branded surfaces, load `references/yolando-design-system.md` before
applying the generic visual rules below. The Yolando design system is the source
of truth for brand-specific color, type, components, spacing, imagery, and
visual identity. Use this skill's generic defaults only where the brand system
is silent.

## Minimal Reading Surfaces

Use this rule for executive guides, briefing pages, long-form notes, and other
reading-first HTML/PDF surfaces that do not already have a stronger brand or
product design-system rule.

Layout:

- Desktop content width: `640px`.
- Desktop top offset: `160px`.
- Mobile horizontal padding: `16px`.
- Mobile top offset: `80px`.

Type:

- Primary paragraph text: `18px`, `0.02em` letter spacing, `150%`
  line-height.
- Paragraph spacing: `12px`.
- List item spacing: `6px`.
- Header text: `24px`, `125%` line-height.
- Small text: `11px`.

Color and links:

- Use as few colors as possible: black, white, and 50% grey.
- Support dark mode and light mode from the device preference.
- Text links use an underline expressed as a bottom border.

Principles:

- Use as few styles as possible.
- Use as few colors as possible.
- Let the content, hierarchy, and spacing carry the page.

## Relationship To `styleguide`

`styleguide` governs what the communication says and how it is structured.
`visual-styleguide` governs how designed communication surfaces are laid out and
rendered.

Load both when the artifact needs both prose judgment and visual presentation,
such as an executive briefing page, customer-facing PDF, visual strategy memo,
or presentation support page.

## References

| File                                  | Use                                                                                                                         |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `references/yolando-design-system.md` | Yolando brand precedence, cheat sheet, and pointer into the checked-in design bundle. Load before any Yolando-branded work. |
| `references/yolando-design-system/`   | Canonical bundle: token CSS, brand README, preview cards, working React UI kit, and logo assets.                            |
