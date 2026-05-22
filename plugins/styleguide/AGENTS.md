# Styleguide Plugin Charter

This plugin separates universal writing judgment from surface-specific artifact
contracts.

## Core Responsibility

`content-styleguide` applies to any human-facing prose. Its job is not to own
every artifact format. Its job is to improve how the agent thinks before,
during, and after writing:

- identify genre, audience, situation, voice, register, and tone;
- clarify the communicative job before choosing structure;
- make claims precise, useful, traceable, and appropriately compressed;
- remove AI-writing artifacts and institutional clutter;
- revise for sentence action, information flow, emphasis, coherence, and
  scanability;
- preserve the writer's real judgment while cutting performative polish.

Use it for Slack messages, email, client-facing communication, docs, Google
Docs, social posts, comments, proposals, PR prose, issues, task text,
stakeholder updates, and any other text a human will read.

## Surface Responsibility

Surface skills own artifact contracts:

- `pull-request` owns reviewer contract, PR summary shape, risk surfaces, review
  guides, changed-file links, and merge-readiness notes.
- `issue-writing` owns issue framing, title shape, scope, decomposition, and
  acceptance criteria.
- `task-management` owns task status, ownership, blockers, dependencies,
  handoffs, and completion checks.
- `stakeholder-update` owns compressed decision support: status, risk,
  decisions, provenance, and asks.
- `visual-styleguide` owns layout, type, color, rendered presentation, and brand
  systems.

Surface skills may include their own examples and checklists. Do not create a
separate reference file in `content-styleguide` for a surface when that guidance
belongs inside the surface skill.

## Development Rule

When adding or changing guidance, ask:

- Is this true across most human-facing prose? Put it in `content-styleguide`.
- Is this about one artifact's contract, expected fields, or workflow? Put it
  in that surface skill.
- Is this about a rendered or branded surface? Put it in `visual-styleguide`.
- Is this a reusable review/workshop workflow? Add it as a separate skill or
  command that explicitly invokes `content-styleguide`.
