# Portage

Open-source Claude Code plugins with cross-tool skill compatibility.

Portage distributes Claude Code plugins through a marketplace and exposes the same skills under `.agents/skills/` so tools that follow the Open Skills Standard — Cursor, Codex, OpenCode, and others — can use them without a separate install.

## What's inside

- **`plugins/`** — each plugin is a self-contained directory with its own `plugin.json`, agents, commands, and skills.
- **`.claude-plugin/marketplace.json`** — the registry Claude Code reads.
- **`.claude/skills/`** — symlinks to every skill across every plugin. Populated by the link script.
- **`.agents/skills/`** — a symlink to `.claude/skills/`. Point any Open Skills Standard tool here.

## Install a plugin in Claude Code

Add the marketplace, then install the plugin:

```
/plugin marketplace add birdseye/portage
/plugin install prose@portage
```

## Use skills in other tools

The skills live as self-contained directories under `.agents/skills/`. Each directory has a `SKILL.md` plus any bundled files (`references/`, `scripts/`, `assets/`). Tools that read the Open Skills Standard format can load them directly.

Point your tool at `.agents/skills/` — no extra setup.

## Add a plugin or skill

1. Drop the plugin into `plugins/<plugin-name>/` following the existing structure.
2. Register it in `.claude-plugin/marketplace.json`.
3. Run the link script:
   ```
   ./scripts/link-marketplace-skills.sh
   ```

The script symlinks each skill directory into `.claude/skills/` and maintains the `.agents/skills` symlink. It detects collisions on skill names, cleans up stale symlinks, and flags duplicate frontmatter names.

Re-run the script only when skills are added or removed. Edits inside an existing skill directory propagate through the symlink automatically.

## Available plugins

- **[prose](plugins/prose/)** — composable content quality toolkit. Seven skills for writing craft, citations, SEO, video scripts, social posts, transcript cleanup, and AI artifact removal, plus two commands that chain them into editorial workflows.

## License

GPL-3.0. See [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Portage is early; open an issue before starting significant work.
