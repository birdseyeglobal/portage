# Styleguide Plugin

A standalone organization-wide style guide for human-facing prose and rendered
communication surfaces.

The plugin contains surface-specific skills plus a shared content styleguide:

- `content-styleguide` for any human-facing prose: genre, audience, voice,
  register, tone, structure, claim precision, meta-cognitive revision, and
  AI-writing artifact cleanup.
- `pull-request` for GitHub pull request bodies, comments, review guides,
  reviewer asks, risk surfaces, and merge-readiness notes.
- `issue-writing` for GitHub issue titles, bodies, scope, decomposition, and
  acceptance criteria.
- `task-management` for task tracker items, status, blockers, dependencies,
  owners, handoffs, and follow-up boundaries.
- `stakeholder-update` for compressed status, risk, decisions, asks, and
  presentation support.
- `visual-styleguide` for rendered communication surfaces where layout, type,
  color, brand systems, and link styling affect the result.

It is intentionally separate from the broader prose plugin so an organization
can load the style guides for general communication without adopting SEO, social
media, video scripting, citation, or transcript workflows.

## Skills

### Content Styleguide

Use for internal updates, customer-facing notes, replies, discussion threads,
changelog entries, READMEs, architecture docs, guides, design proposals, RFCs,
docstrings, inline comments, roadmap entries, presentations, and agent
instructions. Also use for Slack messages, emails, Google Docs, client-facing
communication, social posts, issue comments, review replies, and any other text
a human will read.

The guide's differentiable value is meta-cognitive. It helps the agent reason
about genre, audience, situation, voice, register, tone, claim strength,
structure, sentence clarity, information flow, scanability, and revision before
it chooses a surface-specific shape. It also includes explicit cleanup passes
for common AI-writing artifacts such as inflated significance, generic praise,
stock transitions, synonym cycling, and LLM-heavy word choice.

Core rule: `content-styleguide` controls deeper writing quality: voice, clarity,
tone, scanability, meta-cognitive revision, and AI-artifact cleanup. Surface
skills control artifact contracts. For pull requests, issues, task tracker
items, and stakeholder updates, load the surface skill first and pair
`content-styleguide` only for deeper prose quality.

## Charter

The plugin follows a simple separation of concerns:

- **Universal writing guidance** belongs in `content-styleguide` when it applies
  across most human-facing prose.
- **Surface contracts** belong in surface skills when they describe an artifact's
  expected fields, review path, workflow, or completion criteria.
- **Rendered presentation** belongs in `visual-styleguide` when layout, type,
  color, brand, or visual hierarchy changes the result.
- **Explicit review/workshop workflows** should become separate skills or
  commands that invoke `content-styleguide` rather than bloating the core skill.

Good future additions to this plugin could include an editor-in-chief review
skill, a structured writing-review skill, a styleguide-extraction workflow, or a
deep interactive writing workshop. Those should stay separate execution
surfaces while reusing `content-styleguide` as the universal writing judgment.

### Pull Request

Use for GitHub pull request bodies, comments, review guides, reviewer asks,
review focus sections, risk surfaces, external context, changed-file links,
verification evidence, and merge-readiness notes.

The skill keeps the PR body durable and reviewer-centered. It separates summary
prose from review-guide comments so complex PRs can give reviewers a useful
reading path without turning the PR body into a procedural checklist.

### Issue Writing

Use for GitHub issue titles and bodies, internal implementation issues, public
intake issues, acceptance criteria, scope boundaries, decomposition, and links
to supporting documents.

The skill keeps issues actionable: one unit of work, outcome-first title,
enough context to start, checkable acceptance criteria, and links to deeper
context instead of pasted design material.

### Task Management

Use for operational task tracker items, project tasks, implementation subtasks,
status-bearing work items, blockers, dependencies, owners, handoffs, and
follow-up boundaries.

The skill keeps tasks operational rather than documentary. A task names one
outcome, the current work state when it matters, ownership, blockers,
dependencies, and completion checks.

### Stakeholder Update

Use for stakeholder updates, executive updates, status notes, leadership briefs,
decision memos, meeting briefs, presentation notes, update emails, Slack
updates, and compressed summaries.

The skill compresses source material around status, risk, decisions, tradeoffs,
provenance, and asks. Pair with `visual-styleguide` when the update becomes a
rendered page, deck, PDF, or other designed surface.

### Visual Styleguide

Use for reading-first HTML/PDF pages, executive guides, briefing pages,
presentation support pages, visual docs, landing pages, and other designed
communication surfaces.

The guide keeps visual surfaces restrained: narrow reading width, stable type,
simple color, clear links, and spacing that lets the content carry the page.
Load `content-styleguide` with it when the artifact also needs voice, tone,
structure, or AI-writing artifact cleanup.

For Yolando-branded surfaces, `visual-styleguide` loads
`references/yolando-design-system.md` first. The Yolando design system wins over
generic visual defaults wherever it has a rule.

## References

- `content-styleguide/references/lessons-in-clarity-and-grace.md` — diagnostic
  revision for unclear sentence action, hidden agents, information flow,
  emphasis, cohesion, and coherence.
- `content-styleguide/references/humanizer-patterns.md` — AI-writing artifact
  patterns with before/after rewrites.
- `content-styleguide/references/humanizer-word-choice.md` — word- and
  phrase-level review covering AI vocabulary, institutional clutter, filler
  phrases, and promotional puffery.
- `pull-request/references/review-guides.md` — standalone review guide comment
  triggers, shape, examples, and anti-patterns.
- `issue-writing/references/issue-shape.md` — issue titles, scope,
  decomposition, acceptance checks, and template boundaries.
- `task-management/references/task-shape.md` — task titles, status, blockers,
  dependencies, acceptance checks, decomposition, and handoffs.
- `stakeholder-update/references/update-shape.md` — compression, provenance,
  risks, decisions, asks, freshness, and presentation surfaces.
- `visual-styleguide/references/yolando-design-system.md` — Yolando-specific
  visual language, type, color, links, and component conventions.

## Plugin Files

- [content-styleguide](skills/content-styleguide/SKILL.md)
- [pull-request](skills/pull-request/SKILL.md)
- [issue-writing](skills/issue-writing/SKILL.md)
- [task-management](skills/task-management/SKILL.md)
- [stakeholder-update](skills/stakeholder-update/SKILL.md)
- [visual-styleguide](skills/visual-styleguide/SKILL.md)
