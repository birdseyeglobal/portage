# Portage

[![CI](https://github.com/grootenberg/Portage/actions/workflows/ci.yml/badge.svg)](https://github.com/grootenberg/Portage/actions/workflows/ci.yml)

A marketplace for portable AI-assistant extensions.

Portage packages skills, commands, and agents as Claude Code plugins _and_ exposes the skills under `.agents/skills/` so tools that follow the Open Skills Standard — Cursor, Codex, OpenCode, and others — can use them without a separate install. Skills are the portable unit: they work anywhere the standard is supported. The plugin format is the richer unit: Claude Code users get skills bundled with commands and agents.

## What's inside

- **`plugins/`** — each plugin is a self-contained directory with its own `plugin.json`, agents, commands, and skills.
- **`.claude-plugin/marketplace.json`** — the registry Claude Code reads.
- **`.codex-plugin/plugin.json`** — the Codex plugin manifest for installing Portage as one bundle of skills, commands, and agents.
- **`.claude/skills/`** — symlinks to every skill across every plugin. Populated by the link script.
- **`.agents/skills/`** — a symlink to `.claude/skills/`. Point any Open Skills Standard tool here.

## Install a plugin in Claude Code

Add the marketplace, then install the plugin:

```text
/plugin marketplace add grootenberg/portage
/plugin install prose@portage
/plugin install styleguide@portage
```

## Use skills in other tools

The skills live as self-contained directories under `.agents/skills/`. Each directory has a `SKILL.md` plus any bundled files (`references/`, `scripts/`, `assets/`). Tools that read the Open Skills Standard format can load them directly.

Point your tool at `.agents/skills/` — no extra setup.

## Install in Codex

Portage also includes a root `.codex-plugin/plugin.json` manifest. The Codex plugin exposes every linked skill through `.agents/skills/`, plus Codex-facing `commands/` and `agents/` entries for the richer Prose workflows.

Before installing or testing locally, refresh the generated compatibility
surfaces:

```sh
bun run sync-codex
```

Then install or load the repository as a local Codex plugin. The plugin root is the repository root, not an individual `plugins/<name>/` directory.

If you add or remove skills, commands, or agents, re-run `bun run sync-codex`
so `.agents/skills/`, `commands/`, and `agents/` continue to reflect the source
plugins.

## Add a plugin or skill

1. Drop the plugin into `plugins/<plugin-name>/` following the existing structure.
2. Register it in `.claude-plugin/marketplace.json`.
3. Run the link script:

   ```sh
   bun run sync-codex
   ```

The sync command symlinks each skill directory into `.claude/skills/`, maintains
the `.agents/skills` symlink, generates Codex command TOMLs, and links Codex
agents from the plugin source directories. It detects collisions on skill,
command, and agent names, cleans up stale generated files, and flags duplicate
frontmatter names.

Re-run the sync command when skills, commands, or agents are added, removed, or
renamed. Edits inside an existing skill or agent directory propagate through the
symlink automatically, but command Markdown changes need the TOML files to be
regenerated.

## Available plugins

- **[prose](plugins/prose/)** — composable content quality toolkit. Seven skills for writing craft, citations, SEO, video scripts, social posts, transcript cleanup, and AI artifact removal, plus two commands that chain them into editorial workflows.
- **[styleguide](plugins/styleguide/)** — standalone organization-wide style guide for internal updates, customer-facing notes, docs, GitHub work, stakeholder communication, and AI artifact cleanup.
- **[geo](plugins/geo/)** — generative engine optimization workflows for AI-search prompt design, citation analysis, content briefs, sitemap strategy, SEO competitor research, and visibility reporting.

## License

MIT. See [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Portage is early; open an issue before starting significant work.
