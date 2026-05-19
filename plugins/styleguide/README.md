# Styleguide Plugin

A standalone organization-wide style guide for communication that humans read,
review, decide from, or act on.

The plugin contains two skills:

- `styleguide` for organization-wide communication, voice, structure, tone, and
  AI-writing artifact cleanup.
- `visual-styleguide` for rendered communication surfaces where layout, type,
  color, brand systems, and link styling affect the result.

It is intentionally separate from the broader prose plugin so an organization
can load the style guides for general communication without adopting SEO, social
media, video scripting, citation, or transcript workflows.

## Skill

### Styleguide

Use for internal updates, customer-facing notes, GitHub issues, pull requests,
replies, discussion threads, changelog entries, READMEs, architecture docs,
guides, design proposals, RFCs, docstrings, inline comments, roadmap entries,
stakeholder updates, presentations, and agent instructions.

The guide keeps communication precise, direct, calm, useful, and traceable.
It also includes explicit cleanup passes for common AI-writing artifacts such as
inflated significance, generic praise, stock transitions, synonym cycling, and
LLM-heavy word choice.

Load `visual-styleguide` instead when the task is primarily about a rendered
surface such as an HTML/PDF briefing page, executive guide, visual doc, landing
page, or presentation support page. Load both when the surface needs prose
judgment and visual presentation.

### Visual Styleguide

Use for reading-first HTML/PDF pages, executive guides, briefing pages,
presentation support pages, visual docs, landing pages, and other designed
communication surfaces.

The guide keeps visual surfaces restrained: narrow reading width, stable type,
simple color, clear links, and spacing that lets the content carry the page.
Load `styleguide` with it when the artifact also needs voice, tone, structure,
or AI-writing artifact cleanup.

For Yolando-branded surfaces, `visual-styleguide` loads
`references/yolando-design-system.md` first. The Yolando design system wins over
generic visual defaults wherever it has a rule.

## References

- `references/lessons-in-clarity-and-grace.md` — diagnostic revision for
  unclear sentence action, hidden agents, information flow, emphasis, cohesion,
  and coherence.
- `references/humanizer-patterns.md` — AI-writing artifact patterns with
  before/after rewrites.
- `references/humanizer-word-choice.md` — word-level replacements for LLM-heavy
  vocabulary.
- `references/pull-requests.md` — pull request openings, reviewer guidance,
  related PR handling, and verification evidence.
- `references/issues.md` — issue titles, scope, decomposition, acceptance
  checks, and template boundaries.
- `references/stakeholder-updates.md` — compression, provenance, risks,
  decisions, asks, and presentation surfaces.

## Plugin Files

- [styleguide](skills/styleguide/SKILL.md)
- [visual-styleguide](skills/visual-styleguide/SKILL.md)
