# Issues

An issue frames one unit of work clearly enough that a competent engineer can
start. It is not a ritual template, a user story, or a design document.

The standard is practical: could the assignee start without another planning
meeting? If yes, the issue is probably detailed enough. If no, add the missing
constraint, example, acceptance check, or link to the document that owns the
deeper context.

## Title

Use the title to name the outcome, not the process.

- Start with a verb: Add, Fix, Implement, Remove, Update, Replace.
- Keep it short enough to scan in a list.
- Name the object being changed.
- Do not add area prefixes when labels, projects, or file paths already carry
  that metadata.

Good:

<good-issue-titles>
Add API timeout override to streaming runs
Fix orphaned tool result reconciliation
Replace raw Engine persistence configuration
</good-issue-titles>

Weak:

<weak-issue-titles>
[Harness] Work on timeout stuff
User should be able to configure timeouts
As a developer, I want persistence to be better
</weak-issue-titles>

## Body Shape

Keep straightforward issues short. Add context only when it changes the work or
prevents a likely wrong turn.

For a simple implementation issue, one paragraph can be enough:

<simple-issue-example>
Add a per-call `timeout` kwarg to `Agent.run_stream()` that overrides the
class-level `api_timeout`, matching `run()`.
</simple-issue-example>

For work with real context, use short prose and only the sections the work
earns:

<contextual-issue-example>
Replace raw SQLAlchemy `Engine` persistence configuration with explicit
`PersistenceAdapter` setup.

`configure_persistence(engine)` currently hides repository construction behind a
type check, which makes in-memory and future adapters feel secondary. The public
API should require an adapter and fail clearly when passed a raw engine.

Acceptance checks:
- `configure_persistence(SqlAlchemyPersistenceAdapter.from_engine(engine))`
  remains the SQL path.
- Passing a raw `Engine` raises `TypeError` with migration guidance.
- Existing in-memory persistence tests still pass.
</contextual-issue-example>

Avoid forced templates that restate themselves:

<weak-issue-template>
## Summary
Fix persistence.

## Requirements
- [ ] Fix persistence.

## Acceptance Criteria
- [ ] Persistence is fixed.
</weak-issue-template>

## Markdown and Visual Hierarchy

Use Markdown to make the issue scannable, not decorative.

- Keep paragraphs short: one to three sentences.
- Use headings only when they reduce scanning cost.
- Use bullets for peer constraints, acceptance checks, examples, or links.
- Use numbered lists only for ordered reproduction steps or execution sequence.
- Use code spans for symbols, commands, file paths, API names, and literal
  values.
- Put the most important context before supporting detail.

Avoid dense walls of text, nested bullets, and headings that exist only because a
template had them.

## What Belongs in the Issue

Use the issue body for the actionable frame:

- The observed problem or opportunity.
- The outcome the work should produce.
- Constraints, acceptance criteria, or non-goals.
- Evidence that changes the work.
- Links to discussion, code, pull requests, or documents that own deeper context.

Keep evidence compact. A one-sentence summary plus a link is usually better than
pasting a long transcript, traceback, or design thread.

## What Belongs Somewhere Else

Move deep design, durable architecture, research evidence, temporary planning
context, and long rationale into the right document. Link that document from the
issue instead of copying it.

Use this split:

- **Issue**: what work should happen next, why it matters, and how completion is
  checked.
- **Supporting work document**: deeper context needed to understand or execute
  the issue, but too temporary or issue-specific for repo docs.
- **Architecture doc**: stable design concepts, invariants, boundaries,
  ownership, accepted tradeoffs.
- **Roadmap doc**: future direction, unresolved feature shape, open questions.
- **Research doc**: evidence, source quality, methodology, confidence.
- **Pull request**: what actually changed and how it was verified.

Supporting work documents include design briefs, investigation notes, data
appendices, implementation plans, meeting notes, decision notes, and
product/work-tracking documents. They may live outside the repo when the context
belongs to a planning surface rather than the codebase.

If the issue needs more than a few paragraphs of background, the background
probably belongs in a document. Summarize the relevant point in one or two
sentences and link the document as provenance.

## Scope

Scope issues to the smallest independently useful unit of work. A normal issue
should be completable by one person in hours-to-days.

Oversized signals:

- Multiple services or packages need coordinated changes.
- Multiple concerns are bundled together, such as schema, business logic, UI,
  and docs.
- The title uses vague verbs like "improve", "rework", "modernize", or "clean
  up" without a concrete outcome.
- The work requires several owners or specialties.
- The body reads like a project brief.

When an issue is too large, decompose along natural boundaries:

- **Service or package boundaries**: harness core, SQL adapter, Pydantic AI
  adapter, TUI, docs.
- **Concern boundaries**: data model, runtime behaviour, public API, tests,
  docs.
- **Dependency boundaries**: prerequisite contract first, consumers second.
- **Value boundaries**: each issue should leave the project better if it lands
  alone.

If one person cannot complete it in hours-to-days, ask whether it is really a
project, roadmap entry, or design proposal.

## Acceptance Criteria

Acceptance criteria are checkable outcomes, not a rewritten task list.

Good criteria:

- The public API rejects raw `Engine` persistence configuration with migration
  guidance.
- Existing SQL and in-memory persistence tests pass through the same adapter
  protocol.
- The docs show the adapter-based setup path.

Weak criteria:

- Update the persistence code.
- Add tests.
- Update docs.

Prefer two to five acceptance checks. More than that usually means the issue is
too broad or the criteria are implementation steps.

## Public Intake Versus Internal Issues

Public GitHub issue templates collect structured information from people
who may not know the codebase. Respect those templates for bug reports, feature
requests, and documentation reports.

Internal issues can be shorter because the reader shares more context. Do not
copy the public template shape into internal planning unless the structure earns
its place.

## Final Check

Before handing off an issue, check:

- The title names the outcome.
- A competent assignee can start.
- Context that belongs in docs is linked, not pasted.
- Temporary context that belongs in a supporting work document is summarized and
  linked.
- Scope fits one person and hours-to-days, or the issue explicitly names the
  decomposition.
- Acceptance criteria are checkable outcomes.
- The issue does not restate what the assignee already knows.
