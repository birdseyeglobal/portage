# Yolando Design System

> AI visibility & GEO (Generative Engine Optimization) platform.
> **Made by Birdseye Global.**

---

## What is Yolando?

Yolando helps marketing leaders **see how LLMs represent their brand and shape those answers.** It's a dashboard-heavy B2B SaaS for marketing teams — not a marketing site. Think command center: visibility score, reputation score, citation rate, competitor feeds, recommendation cards, AI-powered content studio.

### Product surfaces / core modules

| Module | Purpose |
|---|---|
| **AI Visibility** | Track how LLMs answer queries about your brand + share of voice |
| **Recommendations** | Actionable GEO tasks to improve visibility |
| **Marketing Studio** | AI-assisted content generation + editing (rich-text, chat) |
| **Competitor Radar** | Feed of rival moves, mentions, citations |
| **Knowledge Base** | Source of truth the platform uses to answer questions about you |

### Audience

Marketing leaders, content teams, SEO/GEO teams, demand gen, agencies — across fintech, legal, healthcare, and data-infra/SaaS.

---

## Sources used to build this system

| Source | Notes |
|---|---|
| `birdseyeglobal/birdseye` @ `main` · `seo_webapp/app/globals.css` | **Canonical source** — every color/spacing/type/shadow token below is verified against this file. |
| `birdseyeglobal/birdseye` @ `main` · `seo_webapp/tailwind.config.ts` | Tailwind → token mapping (`bg-button-primary-default`, `text-content-subtle`, etc.) |
| `birdseyeglobal/birdseye` @ `main` · `seo_webapp/design-system/theme.ts` | Accent color set (`accentColors`) |
| `🗻 Yolando Design System.fig` (Figma) | Component shapes, composition rules, iconography usage |
| Uploaded logos (`uploads/yolando-*`) | Copied into `assets/` |

---

## The system at a glance

- **Numeric scale:** `100 = 4px`. `spacing-200 = 8px`, `spacing-400 = 16px`, `borderRadius-400 = 16px`. Exceptions: `borderWidth`, `fontWeight`, `opacity` use literal values.
- **Two variable collections:**
  - **Primitives** (`--color-grey-*`, `--color-purple-*`, `--color-*Alpha-*`, `--spacing-*`, `--fontSize-*`, …)
  - **Semantics** organised into three namespaces — `--bg-*` · `--content-*` · `--border-*`
- **ALWAYS prefer semantic over primitive.** Write `bg-default` / `content-subtle` / `border-card`, not `#ffffff` / `--color-grey-800` / `--color-grey-200`. Semantics swap cleanly between light and dark.
- **Fonts:** **DM Sans** (headings, buttons), **Inter** (body, captions, labels), **Geist Mono** (code, tokens, numerical read-outs).
- **Theme:** ships light + dark. The app itself **defaults to dark** (`<html class="dark">` in layout) — build prototypes in dark unless the user specifies light.

---

## Content fundamentals

### Voice

**Confident, punchy, marketer-native.** Contrast-driven one-liners. The brand is self-aware about the AI hype cycle and speaks like a peer, not a vendor.

**Signature patterns:**

- *"AI changed the game. Yolando changes the odds."*
- *"Stop guessing. Start winning."*
- *"See what AI sees. Shape what it says."*

### Tone rules

| Do | Don't |
|---|---|
| Short sentences. Verbs first. | "Empower your organization to leverage…" |
| Specific numbers and nouns ("citation rate", "17 strategic edits") | Generic SaaS filler ("robust platform", "best-in-class") |
| Speak to the user as "you" | First-person plural ("we help you…") |
| Marketer vocabulary (share of voice, ranking, demand gen) | Engineering jargon |
| One clear action per screen | "Learn more →" in five places |

### Casing

- **Sentence case** for buttons, nav, cards, dialogs (`"Clear history"`, not `"Clear History"`)
- **Title Case** only for proper nouns (`Competitor Radar`, `Marketing Studio`)
- **UPPERCASE** for eyebrows / overlines only (`OVERVIEW`, `RECOMMENDATIONS`)
- Headings end with a period ⇄ only when they're full sentences. Card titles: no period.

### Pronouns

- "You" for the reader. "Yolando" when naming the product, never "the platform" or "we".
- Avoid "Let's…" / "We'll…" — it sounds like a conference talk.

### Emoji

**Not in UI.** The brand uses a literal mountain emoji 🗻 as the Figma file marker (the logo's triangle stack reads as mountains). The product interface itself uses **no emoji anywhere**. Use Lucide icons when you'd reach for an emoji.

### Examples

- **AI chat empty state:** "Ask anything" — placeholder only.
- **Empty chat history:** "No chats yet. Start one and it'll show up here."
- **Destructive confirm title:** "Clear chat history?"
- **Destructive confirm body:** "This will permanently delete the chat history for everyone in your organization. This action cannot be undone."
- **Recommendation card:** "Pitch Yolando to Reddit's r/marketing. +12 mentions projected."

---

## Visual foundations

### Color

- **Primary is `purple-500 #6d65e1`** — a deep indigo-violet, the brand's workhorse. It appears on primary buttons, selected states, links, brand accents, logos, and as the dominant chart color in light mode.
- **Purple-300 `#a7a6fe`** is the dark-mode primary. In dark mode the purple softens to lavender so it sits correctly on near-black — `bg-button-primary-default` becomes `purple-300` with **black text**.
- **Neutrals** are straight cool greys stepping from `#f8f8f8` → `#161518`. No warmth, no lavender cast. `grey-1000 #161518` is the app's near-black.
- **Accent family (500-variants):** red `#df3131`, orange `#c94f0f`, yellow `#a76909`, green `#288652`, cyan `#048197`, blue `#3471e4`, pink `#d23880`, and purple `#6d65e1`. These drive charts, avatars, diffs, and semantic states.
- **Semantic state colors:** destructive red `#df3131`, success green `#288652`, warning orange `#c94f0f`, info blue `#3471e4`. All derived from the accent family — there is no separate semantic palette.
- **Alpha greys** (`greyAlpha-*`) power hover/nav/skeleton states so the same utility reads correctly on any surface. Prefer them over hard-coded tints.

### Type

Three families, each with a specific job:

| Family | Role | Examples |
|---|---|---|
| **DM Sans** | Headings, buttons, section titles, anything structural | `--fontFamily-headings`, `.t-heading*`, `.t-button-*` |
| **Inter** | Body text, paragraphs, captions, labels, input values | `--fontFamily-body`, `.t-body-*`, `.t-caption-*` |
| **Geist Mono** | Code, tokens, metric readouts, data | `--font-mono` |

**Composition:**
- Headings tighten letter-spacing (`-0.12px` on button-sm up to `-0.64px` on heading2).
- Button text is DM Sans SemiBold with negative tracking — sharp, dense.
- Body paragraph (14/20 Inter Regular) is the default text style.
- Caption (12/16 Inter) for overlines, timestamps, footnotes.

Full composed styles live in `preview/type-*.html` and as `.t-*` utility classes in `colors_and_type.css`.

### Spacing & layout

- 4px base. `spacing-200 = 8px`, `spacing-400 = 16px`, `spacing-600 = 24px`, `spacing-800 = 32px`.
- Half-steps exist: `spacing-050 = 2px`, `spacing-150 = 6px`, `spacing-250 = 10px` — use them instead of rounding up.
- Most padding: 8 / 12 / 16 / 24. Section headers sit at 24 horizontal, 12–16 vertical. Page-level sections at 48 / 64 / 80.
- Max content column ~1280px (`--max-width-7xl`).
- Sidebar: 256px expanded, icon-only collapsed at ~56px.

### Backgrounds

- **App (dark, default):** `bg-default` = `grey-1000 #161518`. Cards sit on top as transparent / `greyAlpha-50` hover.
- **App (light):** `bg-default` = white. Canvas is `bg-bold` = `grey-50 #f8f8f8` for gentle separation under white cards.
- **Tab/skeleton surfaces:** `greyAlpha-200` — a single translucent fill that works on both themes.
- **No gradient fills for general UI chrome.** A single `brand-sheen` gradient exists (`linear-gradient(270deg, greyAlpha-05 → greyAlpha-20)`) and is used sparingly for marketing flourishes.

### Corner radii

- Buttons · inputs · chips · toggles: **8px** (`borderRadius-200`)
- Cards · panels · dialogs: **16px** (`borderRadius-400`)
- Dropdown menus · toasts: **12px** (`borderRadius-300`)
- Fine elements (dots, tiny tags): **2–4px** (`borderRadius-50` / `borderRadius-100`)
- Pills · avatars · chips-full-round: **`borderRadius-round`** (`999999px`)

### Shadows

Two systems:

1. **Elevation** — subtle, single-layer black at low opacity.
   - `shadow-xs`: `0 1px 2px rgba(0,0,0,.08)` — resting card
   - `shadow-sm`: `0 2px 4px rgba(0,0,0,.12)` — hovered card
   - `shadow-md`: `0 4px 8px -2px rgba(0,0,0,.16)` — menus
   - `shadow-lg`: `0 8px 16px -4px rgba(0,0,0,.16)` — popovers
   - `shadow-xl`: `0 12px 32px -8px rgba(0,0,0,.24)` — modals/drawers
2. **Focus ring** — a `3px` spread-only halo.
   - Default: `greyAlpha-300` (neutral UI)
   - Success: `greenAlpha-300` (confirm, save)
   - Destructive: `redAlpha-300` (delete, remove)

Never use the browser's default outline. Never mix elevation shadow with focus ring — focus takes precedence.

### Borders

- **Borders are the primary separation tool; shadow is secondary.** Every card, input, menu, and sidebar carries a 1px `border-card` / `border-input` line.
- Light mode: `border-subtle = grey-100 #e4e4e4`, `border-default = grey-200 #cbcbcf`, `border-bold = grey-300`.
- Dark mode: `border-subtle = grey-800`, `border-default = grey-700`, `border-bold = grey-600`. (Same hierarchy, darker stops.)
- Avoid double-borders (bordered card with bordered inner section). Use a background tone shift (`bg-bold` → `bg-bolder`) instead.

### Animation

- **Fades and soft slide-ins, never bounces.**
- Easing: `cubic-bezier(0.32, 0.72, 0, 1)` for most motion; `ease-out` acceptable for quick hover/press.
- Durations: **120ms** hover/press → **200ms** enter/exit → **320ms** drawer/sheet.
- Accordions: 200ms `ease-out` (tailwind config ships it).
- Chart bars/lines animate on mount (200–400ms), not on every re-render.

### States

| State | Treatment |
|---|---|
| **Hover** (button primary) | `purple-600` in light / `purple-200` in dark |
| **Hover** (ghost / outline) | Swap bg to `greyAlpha-100`; no border change |
| **Press** | One step darker (`purple-700` / `grey-200`); no shrink transform |
| **Focus** | 3px `greyAlpha-300` halo; never the browser ring |
| **Disabled** | Opacity 0.5, keep colors, `pointer-events: none` |
| **Selected** (nav) | `bg-nav-active` = `greyAlpha-200`, label stays same weight |
| **Selected** (card) | `bg-card-selected` = `purpleAlpha-100` + `border-selector-selected` purple |

### Transparency & blur

- Modal/drawer overlays use `blackAlpha-500` backdrop. `backdrop-filter: blur(4px)` is acceptable on dialogs in dark mode; avoid on light.
- Sidebar is opaque. Headers are opaque. Don't glass-morph product chrome.

### Imagery

- No stock photography in product chrome. Screenshots, charts, and tables only.
- When a cover surface needs warmth (marketing home, empty states), overlay soft blurred purple + orange ellipses at low opacity on `grey-1000`. This is the one place warmth appears.
- Avatars use the accent-color set (`theme.ts` → `accentColorValues`) for initials backgrounds — indexed by user id hash, so every user keeps the same color.

### Cards

- **Dark:** transparent on `bg-default`, `1px border-card` (`grey-600`), `borderRadius-400`, no shadow at rest.
- **Light:** white on `bg-bold` canvas, `1px border-card` (`grey-200`), `borderRadius-400`, `shadow-xs` at rest.
- Hover: `bg-card-hover` (`greyAlpha-50` light / `greyAlpha-200` dark). No translateY, no scale.
- Selected: `bg-card-selected` = `purpleAlpha-100` + `border-selector-selected` = `purple-500` (light) / `purple-300` (dark).
- Header: `24px 24px 12px` — DM Sans SemiBold 20/24 title, Inter 14 subtler description.
- Footer: `1px top border-card`, flex-end buttons, `12px 24px`.

---

## Iconography

### System

**Lucide** (stroke icons, 1.5px default weight) — this is what the Figma file uses by convention (`Icon / ChevronDown`, `Icon / Sun`, `Icon / ExternalLink`, `Icon / TrendingUp`). Load from CDN — no sprite bundled.

```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<i data-lucide="trending-up"></i>
<script>lucide.createIcons();</script>
```

- **Stroke width:** 1.5 (Lucide default). Don't change per icon.
- **Size:** 16 / 20 / 24 — match surrounding text.
- **Color:** `currentColor` — inherits `--content-*` from parent.
- **Never fill Lucide icons.** If a filled glyph is needed, author a separate SVG.

### Emoji

**Not used.** Do not use emoji in the UI (labels, buttons, empty states, toasts). Single exception: the 🗻 mountain maps to the logo mark and can appear in internal / marketing-brand copy.

### Unicode as icon

**Avoid.** Use Lucide. The only unicode character used systemically is `—` (em dash) in copy.

### Key logos / assets

In `assets/`:

| File | Use |
|---|---|
| `yolando-full-light.svg` | Full lockup, light background |
| `yolando-full-dark.svg` | Full lockup, dark background |
| `yolando-icon-light.svg` | Mark-only, light background |
| `yolando-icon-dark.svg` | Mark-only, dark background |

The logo is **three stacked triangles + a rotated pin** — the pin is the orange accent (`orange-300 #ea9e59`, same hex as the peach in the brand). Never recolor or recomposite.

---

## Font substitution notice

All three required families ship in this project:

- **Inter** — brand-hosted variable font (`fonts/Inter-VariableFont_opsz_wght.ttf` + italic).
- **DM Sans** — brand-hosted variable font (`fonts/DMSans-VariableFont_opsz_wght.ttf` + italic).
- **Geist Mono** — loaded from Google Fonts in `colors_and_type.css`.

The production app also installs `@fontsource/inter` and `@fontsource/dm-sans` (400/500/600/700) and local Geist Sans + Geist Mono `.woff` via `next/font/local`. For prototypes inside this project, the three families above are sufficient.

---

## File index

```
/
├── README.md                     — this file
├── SKILL.md                      — Agent-Skills / Claude Code entry point
├── colors_and_type.css           — all tokens + composed .t-* text classes
├── assets/
│   ├── yolando-full-{light,dark}.{svg,png}
│   └── yolando-icon-{light,dark}.{svg,png}
├── fonts/                        — Inter + DM Sans variable TTFs
├── preview/                      — Design System tab cards
│   ├── _base.css
│   ├── colors-*.html
│   ├── type-*.html
│   ├── spacing-*.html
│   ├── components-*.html
│   └── brand-*.html
└── ui_kits/
    └── seo_webapp/               — interactive click-through of the real app
```

---

## How to use this system

1. **New prototype:** drop `<link rel="stylesheet" href="colors_and_type.css">` at the top, add `class="dark"` to `<html>` if building the product UI, pull components from `ui_kits/seo_webapp/`.
2. **Production handoff:** the values here match `seo_webapp/app/globals.css` 1:1. Tailwind aliases (`bg-brand`, `text-content-subtle`, `border-card`, etc.) match `tailwind.config.ts`.
3. **Brand / marketing work:** near-black canvas, purple-500 and orange-300 accents, punchy one-liner voice.

**AI changed the game. Yolando changes the odds.**
