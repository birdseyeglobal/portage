# Yolando Design System

Use this reference for Yolando-branded visual communication surfaces. Yolando is
Birdseye Global's AI visibility / GEO (Generative Engine Optimization) B2B SaaS
platform.

## Precedence

The Yolando design system is the source of truth for Yolando-branded surfaces.
Apply it before the generic rules in `visual-styleguide`.

Precedence order:

1. Explicit user request for the current artifact.
2. Yolando design system (this reference + files under
   `yolando-design-system/`).
3. `visual-styleguide` generic rules.
4. Local product or document conventions already present in the file.

If these sources conflict, preserve the Yolando design system unless the user
explicitly overrides it for the current artifact.

## Scope

Use the Yolando design system for:

- Yolando product screens and dashboard chrome.
- Yolando-branded HTML pages, landing pages, and marketing surfaces.
- Yolando-branded PDFs, executive guides, and slides.
- Yolando visual docs and strategy memos.
- Customer-facing visual assets that represent Yolando.

Do not load this reference for plain markdown, issue text, pull request text,
comments, changelog entries, or internal notes unless the user explicitly asks
for Yolando brand treatment.

## Source of truth

Canonical token values, components, and assets live in
[`yolando-design-system/`](./yolando-design-system/), copied from the Birdseye
Global design handoff bundle. When a question can be answered by a file in that
folder, read the file — do not guess from this summary.

Authority within the bundle, in order:

1. `yolando-design-system/colors_and_type.css` — token primitives and semantics.
   This is the only file verified against `seo_webapp/app/globals.css` in the
   production `birdseyeglobal/birdseye` repo. **If anything else conflicts with
   this file, this file wins.**
2. `yolando-design-system/README.md` — narrative system documentation
   (foundations, voice, components, imagery).
3. `yolando-design-system/ui_kits/seo_webapp/` — working React prototype of
   the real product. Primary component source when mocking product screens.
4. `yolando-design-system/preview/*.html` — one reviewable card per foundation
   or component (colors, type, spacing, buttons, inputs, etc.). Open the
   matching card before authoring a new instance.
5. `yolando-design-system/SKILL.md` — original agent entry point from the
   bundle. **Known stale on hex values** (it lists purple-500 as `#8658EC`;
   the CSS and README both say `#6d65e1`). Treat as background context only.

## File index

```
yolando-design-system/
├── README.md                — full system narrative (read top-to-bottom for new work)
├── SKILL.md                 — original bundle entry point (background only; see note above)
├── colors_and_type.css      — all tokens + composed .t-* text classes (link this in prototypes)
├── assets/                  — yolando-full-{light,dark}.{svg,png}, yolando-icon-*
├── preview/                 — 23 foundation + component cards
│   ├── _base.css
│   ├── brand-{iconography,logo-lockups,logo-rules,platforms,voice}.html
│   ├── colors-{accents,neutrals,purple,semantic}.html
│   ├── components-{alerts,avatar,badges,buttons,card,inputs,nav,toggles}.html
│   ├── spacing-{radii,scale,shadows}.html
│   └── type-{families,scale}.html
└── ui_kits/seo_webapp/      — working React prototype (sidebar, topbar, 4 screens)
```

Fonts are not checked in. `colors_and_type.css` references `fonts/Inter-*.ttf`
and `fonts/DMSans-*.ttf` — these will 404 on a fresh checkout. For prototypes,
install via `@fontsource/inter` and `@fontsource/dm-sans`, or load from Google
Fonts. Geist Mono is already pulled from Google Fonts inside the CSS.

## Cheat sheet

The full system is in `yolando-design-system/`. This summary covers the
decisions that matter most often.

**Mode.** Dark by default — `<html class="dark">`. Light is available; switch by
removing the class.

**Brand color.**

- Light mode brand: `--color-purple-500` = `#6d65e1`. Primary buttons, links,
  selected states, dominant chart series.
- Dark mode brand: `--color-purple-300` = `#a7a6fe`. In dark mode the primary
  button is `purple-300` with **black** text, not white.
- Use brand purple sparingly. Everything else is the cool grey scale.

**Neutrals.** Straight cool greys, no warmth. App near-black is `grey-1000`
`#161518`. Light-mode canvas is white; dark-mode canvas is `grey-1000`.

**Accent + semantic families.** Red `#df3131`, orange `#c94f0f`, yellow
`#a76909`, green `#288652`, cyan `#048197`, blue `#3471e4`, pink `#d23880`.
These drive charts, avatars, diffs, and semantic state (destructive / success /
warning / info). No separate semantic palette.

**Always prefer semantic over primitive.** Write `bg-default`, `content-subtle`,
`border-card` — not `#ffffff`, `--color-grey-800`, `--color-grey-200`. Semantics
swap cleanly between themes.

**Typography.**

- `--fontFamily-headings` → **DM Sans** (headings, buttons, section titles).
- `--fontFamily-body` → **Inter** (body, captions, labels, input values).
- `--font-mono` → **Geist Mono** (code, tokens, numerical readouts).
- Use composed `.t-*` classes from `colors_and_type.css` (`.t-heading2-emphasized`,
  `.t-body-regular`, `.t-button-md`, etc.) rather than re-declaring family / size
  / weight per element.

**Spacing.** 4px base. Token `100` = 4px, `200` = 8px, `400` = 16px,
`600` = 24px, `800` = 32px. Half-steps exist (`050` = 2px, `150` = 6px,
`250` = 10px) — use them instead of rounding. Page sections at 48 / 64 / 80.
Max content column ~1280px. Sidebar 256px expanded / ~56px collapsed.

**Radii.** Buttons / inputs / chips / toggles: 8px (`borderRadius-200`).
Cards / panels / dialogs: 16px (`borderRadius-400`). Dropdowns / toasts: 12px
(`borderRadius-300`). Pills / avatars: `borderRadius-round` (999999px).

**Shadows.** Five-stop elevation scale, all single-layer black at low opacity
(`shadow-xs` for resting card, `shadow-xl` for modals). Borders are the primary
separation tool; shadow is secondary. In dark mode, rely on
border + background contrast instead of shadow.

**Borders.** Every card, input, menu, and sidebar carries a 1px border. Light
mode: `border-subtle` = `grey-100`, `border-default` = `grey-200`,
`border-bold` = `grey-300`. Dark mode: same hierarchy at `grey-800` /
`grey-700` / `grey-600`. Avoid double borders — shift background tone instead.

**Focus.** 3px spread-only halo. Default `greyAlpha-300`, success
`greenAlpha-300`, destructive `redAlpha-300`. Never the browser outline. Never
mix elevation shadow with focus ring — focus wins.

**Icons.** Lucide, 1.5px stroke, 16 / 20 / 24px, inherits `currentColor`.
Never fill Lucide icons. Never use emoji in product UI.

**Imagery.** No stock photography. Screenshots, charts, and tables only.
Marketing covers can use soft blurred purple + orange ellipses on `grey-1000`.

**Logos.** `assets/yolando-full-light.svg` on dark backgrounds,
`yolando-full-dark.svg` on light. Icon-only variants exist. Never place the
logo on orange / peach backgrounds — the orange accent inside the mark becomes
unreadable. Never recolor or recomposite.

## Voice

The bundle's `README.md` and `SKILL.md` disagree on voice (README is punchy and
em-dash-heavy; SKILL.md forbids em dashes). Until the brand owner reconciles
this, default to:

- **Confident, technical, marketer-native.** Short sentences, verbs first,
  specific numbers and nouns.
- Address the reader as "you". Use "Yolando" for the product. Avoid "we",
  "the platform", "let's", "we'll".
- No generic SaaS filler ("robust", "best-in-class", "seamless", "leverage",
  "unlock the power of"). No AI sparkle (✨), no rocket emoji.
- Casing: sentence case for buttons, nav, cards, dialogs. Title Case only for
  proper nouns (`Competitor Radar`, `Marketing Studio`). UPPERCASE for
  overlines only.
- Errors and warnings: direct, not cute. "Source failed to reindex. Retry?"
  not "Oops!"

If the artifact is product UI, lean toward the more restrained voice (no em
dashes, no slogans). If the artifact is marketing or brand collateral, the
punchier voice in `yolando-design-system/README.md` is in scope — confirm with
the user.

## Working patterns

**New product screen.** Copy `ui_kits/seo_webapp/` into the working directory,
or import its `primitives.jsx` + `shell.jsx` + `kit.css`. Build the new screen
as `screen-<name>.jsx` following the pattern of the existing four. Keep the
sidebar and topbar; swap only the canvas.

**Marketing or brand surface.** Start from `colors_and_type.css` plus the
`brand-*` preview cards. More breathing room than product UI is acceptable.
Dark mode is still the default.

**Data viz.** Grid lines `grey-200`. Axis labels `grey-500` in Inter 11/16.
Primary series `purple-500` (light) / `purple-300` (dark). Secondary series
`grey-600`. Positive delta `green-500`, negative `red-500`. Never rainbow.

**Cards.** Dark: transparent on `bg-default`, 1px `border-card` (`grey-800`),
16px radius, no shadow at rest. Light: white on `bg-bold` canvas, 1px
`border-card` (`grey-200`), 16px radius, `shadow-xs` at rest. Hover swaps
background to `greyAlpha-50` (light) / `greyAlpha-200` (dark) — no translate,
no scale. Header padding `24px 24px 12px`, footer with 1px top border and
flex-end buttons at `12px 24px`.

## What not to do

- No gradients in general UI chrome (one exception: subtle purple wash on
  auth / onboarding covers).
- No drop shadows on type, no glows, no neon.
- No competing accent colors — purple carries the brand.
- No emoji in product UI. The 🗻 mountain is reserved for internal /
  brand-marketing contexts that map to the logo.
- No Inter or Roboto substituted for DM Sans in headings — the tight tracking
  is part of the identity.
- No double-borders, no glass-morphed product chrome, no `translateY` or
  `scale` on card hover.
