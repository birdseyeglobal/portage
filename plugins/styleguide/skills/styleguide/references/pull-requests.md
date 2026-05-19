# Pull Request Prose

Use this reference for how pull request text should read. Use the
`pull-request` skill for operating logic: review posture, standalone review
guides, external context, Mermaid diagrams, verification evidence, and GitHub
updates.

## Opening

Start with what changed. If the opener has two jobs, split it into two short
paragraphs: one for what changed, one for why it matters.

Strong:

<strong-pr-opening>
Adds adapter-backed session persistence so callers can swap SQL and in-memory
storage without changing agent code.

This removes SQLAlchemy assumptions from the session handler and gives tests a
first-class in-memory path.

</strong-pr-opening>

Weak:

<weak-pr-opening>
This pull request updates persistence files and adds tests.
</weak-pr-opening>

## Reviewer Address

Address the reviewer directly, but do not over-control their role. Use calm
phrasing that suggests where attention matters while leaving room for the
reviewer to define their own responsibility.

Strong:

<strong-reviewer-address>
Suggested review focus: whether the adapter boundary is clear enough for future
storage backends.
</strong-reviewer-address>

Weak:

<weak-reviewer-address>
Please review everything carefully.
</weak-reviewer-address>

Architecture design review:

<strong-architecture-reviewer-address>
Suggested design review: please test the new session boundary against the
[session architecture design](https://github.com/org/repo/blob/main/docs/architecture/session-boundaries.md)
before reviewing naming or local cleanup. The main question is whether future
adapters can extend this shape without inheriting SQL assumptions.
</strong-architecture-reviewer-address>

<weak-architecture-reviewer-address>
Please take a look at the architecture and let me know what you think.
</weak-architecture-reviewer-address>

Mixed-risk review:

<strong-mixed-risk-reviewer-address>
Suggested review split: the command-palette copy changes are experimental and
low risk, so a light read is enough there. Please review the persistence
adapter path more closely because it changes the failure boundary.

Known keyboard navigation gaps are tracked in
[follow-up issue #123](https://github.com/org/repo/issues/123)
so they should not block this pull request unless this diff makes them worse.
</strong-mixed-risk-reviewer-address>

<weak-mixed-risk-reviewer-address>
Some parts are experimental and some parts matter more. There are also follow-up
issues, so please review accordingly.
</weak-mixed-risk-reviewer-address>

## Shape

Use only the structure the pull request earns. A narrow change may need an
opening paragraph and two bullets. A broad or risky change may need headings,
but the headings should reduce review work.

Prefer:

- `Changed` for reviewer-scannable scope.
- `Context` for links or decisions that affect review.
- `Review Focus` for suggested attention.
- `Verified` only when evidence changes reviewer trust.

Avoid ritual sections. Do not add `Tested`, `Validation`, or `Not Tested`
sections when CI already covers the meaningful test surface, the change is
prose-only, or the commands do not map to a specific risk.

## File Links

When a file path is meant to send the reviewer to a changed file, prefer a
clickable PR file link over a path name in code spans. Raw paths are fine when
they identify a symbol or location in prose, but links are better when the
reader is expected to navigate.

Use the `pull-request` skill for the GitHub file-diff anchor format.

Strong:

<strong-file-link-example>
Start with
[the pull request skill](https://github.com/org/repo/pull/123/files#diff-799c72a57fed869235078067a04f4f3d7490d97945b7eccc8ecf99a2f49d607c)
to review the communication contract.
</strong-file-link-example>

Weak:

<weak-file-link-example>
Start with `.claude/skills/pull-request/SKILL.md`.
</weak-file-link-example>

## Clarity Checks

- Does the first sentence name the behavioral or structural result?
- Does each paragraph do one job?
- Is the reviewer ask specific without being coercive?
- Are risks and boundaries stated plainly?
- Are links explained by relationship, not listed as decoration?
- Are review-destination file paths clickable when the reviewer is expected to
  open them?
- Can implementation details obvious from the diff be cut?

The best pull request prose feels shaped, not templated. The reviewer should
know what changed, why it matters, and where their attention is useful.
