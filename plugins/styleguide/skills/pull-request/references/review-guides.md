# Pull Request Review Guides

A review guide is a PR comment that helps reviewers choose an effective path
through a complex or high-risk change. It is not a second PR body.

Use a review guide when the PR body should stay durable, but the reviewer needs
procedural help, role negotiation, or a more detailed reading path.

## When To Write One

Write a review guide when:

- reviewers need different paths for architecture, QA, migration, or copy;
- risk is concentrated in a boundary, data model, security path, or rollout
  sequence;
- the PR should land even though non-blocking feedback belongs in follow-up
  issues;
- external docs or discussions define constraints reviewers should apply;
- live testing or QA needs steps that would clutter the PR body;
- the reviewer may want to define their own responsibility before reviewing.

Do not write a review guide for routine changes where the PR body already gives
the reviewer enough context.

## Shape

Use only the parts the review needs:

- `Suggested Path` for reading order.
- `Review Roles` when different reviewers should inspect different surfaces.
- `Risk Surfaces` for the boundaries where the change could fail.
- `Live Checks` for manual QA, live testing, or verification steps.
- `Follow-ups` for known issues that should not block the PR.
- `Open Question` when the reviewer should help define the review scope.

Keep the tone invitational. The guide should help the reviewer choose their
approach, not assign them a role they did not accept.

## Narrative Flow

A review guide should develop progressively. Start with the review goal, then
give the reading path, then name the risk surfaces or risky boundary, then
separate blocking concerns from follow-up feedback.

Do not dump context, links, and asks in parallel without showing how they
relate. Each section should make the next section easier to understand.

For complex or high-risk work, expect the review guide to improve through a
focused human-in-the-loop pass. Draft the guide, name the assumptions that shape
the review request, and revise as the author clarifies review scope, merge
expectations, or follow-up boundaries.

## Examples

<architecture-review-guide-example>
I think this is ready for a design-focused review before merge.

Suggested path:
1. Start with
   [the streaming event contract](https://github.com/example-org/example-repo/pull/123/files#diff-1e2510c17b8ed7b9cd85e686bb0729bb8fdb54f1cfe10aee890f99df14b8a0c2).
2. Read
   [the harness lifecycle handling](https://github.com/example-org/example-repo/pull/123/files#diff-aafaf6b1f131ec9d2cd8d9c00d7a2490350d90c628b7e8a8863012cff15e834a).
3. Treat the provider adapter changes as translation glue unless they expose a
   mismatch with the contract.

Risk surfaces:
- Event ordering between the adapter and recorder.
- Cancellation cleanup in the harness lifecycle path.
- Provider-specific translation is lower risk unless it breaks the shared event
  contract.

Please widen the review if you think the adapter boundary needs deeper design
review. If so, name the boundary you want to examine.
</architecture-review-guide-example>

<mixed-risk-review-guide-example>
Suggested split:

- Light review: command-palette copy and labels. These are experimental and low
  risk.
- Close review: persistence adapter setup and failure handling. This is the
  part most likely to affect callers.
- Follow-up: keyboard navigation gaps are tracked separately in
  [follow-up issue #123](https://github.com/example-org/example-repo/issues/123).

Risk surfaces:
- Adapter initialization and failed-turn cleanup can affect production callers.
- Command-palette labels are experimental and can change after merge.
- Keyboard navigation remains known follow-up work.

If the adapter failure boundary looks sound, I think the known keyboard gaps can
stay out of this merge decision.
</mixed-risk-review-guide-example>

<live-qa-review-guide-example>
Suggested live QA:

1. Open the app example.
2. Send one message that succeeds and one message that triggers a tool error.
3. Confirm the message list, status strip, and retry affordance stay readable.

Please treat visual polish notes as follow-up issues unless they hide state or
break the main workflow.
</live-qa-review-guide-example>

## What To Avoid

- Restating the PR body.
- Assigning reviewer responsibility as if it were already agreed.
- Turning every comment into an interview.
- Mixing blocking risks with nice-to-have polish.
- Listing links without explaining how each link should affect review.
