---
name: Yolando Design System
description: Use this skill when designing ANY Yolando surface — product screens, marketing, email, slides, Looms, internal docs. Yolando is Birdseye Global's AI visibility / GEO (Generative Engine Optimization) B2B SaaS platform. Default to **dark mode**; product is dashboard-heavy and data-dense. Brand is **dry, technical, confident, quietly witty** — never breathless, never "magical." Lavender-purple (#8658EC) is the ONLY accent color; everything else is neutral greys. Skill provides: (1) full token set via colors_and_type.css, (2) 23 preview cards under /preview for every foundation + component, (3) a working React UI kit of the real product under ui_kits/seo_webapp/ to copy from, (4) brand voice + logo rules. Load this BEFORE starting any Yolando work.
---

# Yolando Design System

Birdseye Global · AI visibility / GEO platform.

## Start here — 3 files to read in order

1. **`README.md`** (this project) — product context, audience, what Yolando actually does. Read in full if you're new to the brand.
2. **`colors_and_type.css`** — every design token. Link it: `<link rel="stylesheet" href="colors_and_type.css">`. Defaults to dark mode. Add `class="light"` on `<html>` for light.
3. **`ui_kits/seo_webapp/index.html`** — a live React prototype of the real product (sidebar, topbar, Overview, Topics & prompts, Citations, Content hub). **This is your primary component source** when mocking product screens. Copy its patterns; don't reinvent them.

## Visual cheat sheet

**Mode.** Dark by default. Switch with `<html class="light">` / `<html class="dark">`.

**Palette.** Brand accent = **purple-500 `#8658EC`** (light mode) → **purple-300 `#C8B3FF`** (dark mode). Use SPARINGLY — for CTAs, focus rings, data highlights, active states. Everything else is the lavender-tinted grey scale (`--color-grey-50` through `--color-grey-1000`).

**Semantic colors.** Red/orange/yellow/green/cyan/blue/pink each have a 100→700 scale for status only (Live, Failing, Warning, Draft). Never use them decoratively.

**Typography.**
- `--fontFamily-headings` → **DM Sans** (weights 400/500/600/700, tight tracking: -0.02em)
- `--fontFamily-body` → **Inter** (400/500/600)
- `--fontFamily-mono` → **Geist Mono** (for scores, metrics, IDs)
- `--fontFamily-serif` → **Instrument Serif** (used rarely — covers, hero moments only)

Product UI is almost entirely DM Sans + Inter. Don't use serif in dashboards.

**Shape.** Corners: `--radius-100` 4px · `200` 8px · `300` 12px · `400` 16px · `500` 24px. Cards are 12, buttons are 8, badges are 8, full pills only for avatars/status dots.

**Shadows.** `--shadow-xs` / `-sm` / `-md` / `-lg` — light, crisp, never dramatic. In dark mode shadows are near-invisible; rely on border + background contrast instead.

**Spacing.** 4px base. Standard rhythm: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64. Dense dashboards: 8/12/16. Marketing/hero: 24/32/48.

## Voice & copy

- **Dry, technical, confident. Quietly witty. Never breathless.**
- **No em dashes.** Use a period, comma, or colon. If you need a long pause, start a new sentence.
- Say what the thing does, in plain words. "Track how LLMs answer queries about your brand." Not: "Unlock the power of AI visibility."
- Numbers first when numbers matter. "Cited in 42% of ChatGPT answers" beats "Great citation coverage."
- No em-dash hype ("— and that's just the beginning! —"), no "revolutionize," no "seamless," no rocket emoji. Zero marketing slop.
- Errors and warnings: direct, not cute. "Source failed to reindex. Retry?" not "Oops!"
- Internal voice matches external — Slack and dashboard UI use the same tone.

## Component preview cards

23 reviewable cards under `/preview/` — open any one to see the canonical treatment. When in doubt, copy the HTML verbatim.

- **Colors** · `colors-neutrals.html` · `colors-purple.html` · `colors-accents.html` · `colors-semantic.html`
- **Type** · `type-families.html` · `type-scale.html`
- **Spacing** · `spacing-scale.html` · `spacing-radii.html` · `spacing-shadows.html`
- **Components** · `components-buttons.html` · `components-inputs.html` · `components-badges.html` · `components-card.html` · `components-alerts.html` · `components-toggles.html` · `components-avatar.html` · `components-nav.html`
- **Brand** · `brand-logo-lockups.html` · `brand-logo-rules.html` · `brand-iconography.html` · `brand-voice.html` · `brand-platforms.html`

## Working patterns

**Building a new product screen.** Start by copying `ui_kits/seo_webapp/` into your working directory, or import its `primitives.jsx` + `shell.jsx` + `kit.css`. Build your new screen as `screen-<name>.jsx` following the pattern of the existing four. Keep the sidebar and topbar; swap only the canvas.

**Building a marketing surface (landing page, email, slide).** Pull from `colors_and_type.css` + the `brand-*` preview cards. Marketing can use slightly more breathing room and the Instrument Serif display face for hero moments. Dark mode is still the default.

**Data viz.** Grid lines: `--color-grey-200`. Axis labels: `--color-grey-500` in Inter 11/16. Primary series: purple-500 (light) / purple-300 (dark). Secondary series: grey-600. Positive delta: green-500. Negative: red-500. Never rainbow.

**Icons.** Lucide, stroke 1.5, 16/18/20/24px. Match text color of parent. Never filled, never custom-drawn for product UI.

**Logos.** `assets/yolando-full-light.svg` on dark backgrounds, `assets/yolando-full-dark.svg` on light. Icon-only variants exist too. **Never place the logo on orange / peach backgrounds** — the orange accent inside the mark becomes unreadable. Safe surfaces: white, grey-50 through grey-200, grey-800 through grey-1000, purple-100. See `brand-logo-rules.html` for clearspace.

## What NOT to do

- No gradients as backgrounds (one exception: the subtle purple wash on auth/onboarding covers)
- No rounded-corner + left-border-accent callouts
- No emoji in product UI
- No stock-photo hero imagery
- No "AI sparkle" ✨ iconography. Yolando IS the AI — it doesn't need to announce it.
- No competing accent colors. Purple carries the whole brand.
- No drop-shadows on type, no glows, no neon
- No `Inter` or `Roboto` substituted for DM Sans in headings — the tight tracking is part of the identity
