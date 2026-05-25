# Portage Agent Guide

Portage packages assistant capabilities in `plugins/*` and publishes compatibility
surfaces for Claude Code, Codex, and Open Skills Standard tools.

## Source of Truth

- Skills live in `plugins/<plugin>/skills/<skill>/SKILL.md`.
- Claude commands live in `plugins/<plugin>/commands/*.md`.
- Claude agents live in `plugins/<plugin>/agents/*.md`.
- Do not hand-edit generated Codex command files in `commands/*.toml`.
- Do not hand-edit root agent links in `agents/*.md`; update the source file
  under `plugins/<plugin>/agents/`.

## After Changing Plugin Surfaces

When adding, removing, or renaming any skill, command, or agent, run:

```sh
bun run sync-codex
```

This refreshes:

- `.claude/skills/*`
- `.agents/skills`
- `commands/*.toml`
- `agents/*.md`

Then run:

```sh
bun run lint:json
bun run lint:skills
```

Run the broader `bun run validate` when touching Markdown outside generated or
runtime state. If validation reports only `.omx/state` formatting issues, leave
those runtime files alone unless the task is specifically about OMX state.

## Marketplace Rule

When adding a new plugin directory under `plugins/`, also update
`.claude-plugin/marketplace.json`. The root `.codex-plugin/plugin.json` should
normally not need per-plugin edits because it points at the generated aggregate
surfaces.
