# Portage Bootstrap — Design

**Date:** 2026-04-08
**Status:** Approved

## Purpose

Create Portage: an open-source repository that distributes Claude Code plugins and exposes their skills for cross-tool use (Cursor, Codex, OpenCode, and anything else that follows the Open Skills Standard). Portage starts by copying one plugin — `content-writing` from the internal Agora marketplace — and renaming it to `prose`. Additional plugins will be vetted and copied over later; this spec covers only the bootstrap.

## Non-Goals

- Porting plugins beyond `prose`
- GitHub Actions or CI workflows
- Pre-commit hook automation for the skill linker (planned follow-up)
- Full open-source governance scaffolding (CoC, issue templates, contributor ladder)
- Resurrecting the removed `content-structure` skill

## Repository Layout

```text
portage/
├── .claude-plugin/
│   └── marketplace.json
├── .claude/
│   └── skills/                          # Populated by the link script
│       └── <skill> -> ../../plugins/<plugin>/skills/<skill>
├── .agents/
│   └── skills -> ../.claude/skills      # Cross-tool compatibility
├── plugins/
│   └── prose/
│       ├── .claude-plugin/plugin.json
│       ├── agents/copy-desk.md
│       ├── commands/{prose-check.md, editorial-review.md}
│       ├── skills/
│       │   ├── prose-craft/
│       │   ├── citation-sourcing/
│       │   ├── humanizer/
│       │   ├── seo-optimization/
│       │   ├── social-media/
│       │   ├── transcript-cleanup/
│       │   └── video-scripting/
│       ├── CLAUDE.md
│       └── README.md
├── scripts/
│   └── link-marketplace-skills.sh
├── docs/
│   └── superpowers/specs/
├── LICENSE                              # GPL-3.0
├── README.md
├── CONTRIBUTING.md                      # Short boilerplate
└── .gitignore
```

## Component Details

### The `prose` plugin

Source: verbatim copy of `agora/plugins/content-writing/`, minus the leftover nested `agora/plugins/content-writing/` directory (14 empty CLAUDE.md stub files from a pre-rename state — dead weight).

Edits after copying:

- `plugin.json`:
  - `name`: `content-writing` → `prose`
  - `version`: reset to `0.1.0`
  - `license`: `Proprietary` → `GPL-3.0`
  - `author`: placeholder `"Portage Contributors"` (to be set by repo owner)
  - `skills[]`: replace the stale `./skills/writing` entry with `./skills/prose-craft`; other entries unchanged
  - `description` and `keywords`: unchanged (already generic)
- Plugin `README.md`: replace any `content-writing` references with `prose`. No content rewrites.

The seven skill directories (`prose-craft`, `citation-sourcing`, `humanizer`, `seo-optimization`, `social-media`, `transcript-cleanup`, `video-scripting`) copy as-is.

### Marketplace registry

`.claude-plugin/marketplace.json`:

```json
{
  "name": "portage",
  "owner": {
    "name": "<org name — placeholder>",
    "url": "<org github url — placeholder>"
  },
  "metadata": {
    "description": "Open-source Claude Code plugins with cross-tool skill compatibility",
    "version": "0.1.0"
  },
  "plugins": [{ "name": "prose", "source": "./plugins/prose" }]
}
```

### Skill linking script

Copy `agora/scripts/link-marketplace-skills.sh` verbatim. It:

- Symlinks each skill directory from `plugins/*/skills/<name>` into `.claude/skills/<name>`. The whole directory is linked, so `SKILL.md`, `references/`, `scripts/`, `assets/`, and any other bundled files propagate automatically — matching the Open Skills Standard expectation that a skill is a self-contained directory.
- Creates the `.agents/skills` → `../.claude/skills` symlink so tools that read `.agents/skills/` (Cursor, Codex, OpenCode) see the same skills.
- Detects collisions on skill names across plugins.
- Cleans stale symlinks when skills are removed.
- Audits for duplicate `name:` fields in skill frontmatter across linked skills.

Contributors run it once after cloning, and again when adding or removing skills. Edits to files _inside_ an existing skill directory need no re-run — they propagate through the symlink.

### README

Pragmatic technical tone. Sections:

1. What Portage is — one paragraph. A Claude Code plugin marketplace that also exposes skills under `.agents/skills/` for any tool implementing the Open Skills Standard.
2. Installing a plugin — marketplace add + `/plugin install prose@portage`.
3. Using skills in other tools — point the tool at `.agents/skills/`.
4. Adding a plugin or skill — copy into `plugins/`, run `./scripts/link-marketplace-skills.sh`.
5. License — GPL-3.0.

Written with the `prose-craft` skill.

### License and contributing

- `LICENSE`: GPL-3.0 full text.
- `CONTRIBUTING.md`: short boilerplate. Open an issue, open a PR, follow the existing plugin structure, run the link script, note that governance is still being settled.
- `.gitignore`: minimal — OS cruft (`.DS_Store`), editor files.

## Side Task: Agora Cleanup

Separate commit on Agora's main branch, outside the Portage repo:

1. `agora/plugins/content-writing/.claude-plugin/plugin.json`: replace `./skills/writing` with `./skills/prose-craft` in the `skills` array.
2. Delete the leftover nested directory `agora/plugins/content-writing/agora/` (contains only 14 empty CLAUDE.md stub files referencing skills that no longer exist: `writing/` and `content-structure/`).

## Acceptance

- `portage/` exists as a git repo with the layout above.
- `plugins/prose/.claude-plugin/plugin.json` validates (name, version, license, correct skill references).
- Running `./scripts/link-marketplace-skills.sh` creates working symlinks under `.claude/skills/` and the `.agents/skills` top-level symlink, with zero collisions or warnings.
- README renders cleanly and passes a prose-craft-informed read.
- Agora's `content-writing` `plugin.json` no longer references `./skills/writing`; the nested `agora/` leftover is gone.
