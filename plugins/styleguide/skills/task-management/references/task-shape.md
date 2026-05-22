# Task Shape

A task is an operational work item. It should be small enough for someone to
own, explicit enough to resume, and clear enough to close without another
planning meeting.

## Title

Name the outcome, not the activity.

Strong:

<strong-task-titles>
Add retry coverage for failed webhook delivery
Split billing migration rollout into tenant batches
Document rollback steps for the cache invalidation release
</strong-task-titles>

Weak:

<weak-task-titles>
Work on webhook tests
Billing migration stuff
Cache follow-up
</weak-task-titles>

## Body Shape

Use only the fields the task earns. A small task can be one sentence plus an
acceptance check. A coordination task may need status, owner, blockers, and
links.

Useful fields:

- `Outcome`: the state that should exist when the task is done.
- `Status`: current work state when it affects next action.
- `Owner`: who owns the next move, not everyone interested.
- `Blocked by`: the concrete blocker and who or what can unblock it.
- `Depends on`: prerequisite work that must land first.
- `Acceptance checks`: two to five checkable completion outcomes.
- `Links`: issue, PR, design doc, incident, customer note, or source material.
- `Follow-up boundary`: what should become a separate task or issue.

Do not include every field by default. Add structure to prevent ambiguity, not
to satisfy a template.

## Status

Status should change the reader's next action.

Good:

<good-task-status>
Status: Blocked on API credentials from Platform. Implementation is ready to
resume once the staging token is available.
</good-task-status>

Weak:

<weak-task-status>
Status: In progress.
</weak-task-status>

Common states:

- `Pending`: known work, no one actively executing.
- `In progress`: someone owns the next move now.
- `Blocked`: progress needs a named dependency, decision, access, or fix.
- `Needs review`: output exists and needs a specific review.
- `Done`: acceptance checks are met.
- `Cancelled`: no longer needed; include why if future readers might restart it.

## Blockers And Dependencies

Name the blocker as a recoverable condition, not a mood.

Strong:

<strong-blocker>
Blocked by missing staging API credentials. Platform owns the token request;
link this task to the credential ticket and resume once the token works in CI.
</strong-blocker>

Weak:

<weak-blocker>
Blocked by Platform.
</weak-blocker>

Dependencies should explain review or execution order:

<dependency-example>
Depends on #214 because this task consumes the repository protocol introduced
there. Do not start adapter wiring until the protocol names settle.
</dependency-example>

## Acceptance Checks

Acceptance checks are observable outcomes. They are not a rewritten task list.

Strong:

<strong-task-acceptance>
Acceptance checks:
- Failed webhook delivery retries once with the configured backoff.
- Exhausted retries emit the existing alert event.
- Existing successful delivery tests still pass.
</strong-task-acceptance>

Weak:

<weak-task-acceptance>
Acceptance checks:
- Update code.
- Add tests.
- Fix docs.
</weak-task-acceptance>

Use two to five checks. More usually means the task should be split.

## Decomposition

Split tasks when one item has too many owners, too many concerns, or too much
sequencing hidden inside it.

Decompose along:

- **Service or package boundaries**: API, worker, frontend, docs.
- **Concern boundaries**: schema, runtime behavior, public API, tests, docs.
- **Dependency boundaries**: contract first, consumers second.
- **Value boundaries**: each task should leave the project better if it lands
  alone.
- **Review boundaries**: separate risky design work from mechanical follow-up.

When splitting work, preserve the parent context with one sentence and a link.
Do not paste the full parent brief into every child task.

## Handoffs

A handoff task should state what has already happened, what remains, and what
would count as done.

<handoff-example>
The adapter protocol is merged in #214. This task wires the SQL adapter to that
protocol without changing the public setup API.

Current state: memory adapter is already updated; SQL adapter still imports the
old repository bundle.

Acceptance checks:
- SQL adapter implements the new protocol.
- Existing SQL persistence tests pass.
- Public setup docs still show the same caller path.
</handoff-example>

## Final Check

Before handing off a task, check:

- The title names one outcome.
- The next owner can start without a meeting.
- Status and blockers name a next action.
- Dependencies explain order, not just related work.
- Acceptance checks are observable.
- Deeper context is linked, not copied.
- Follow-up work is separated when it should not block this task.
