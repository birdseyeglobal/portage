# Contributing to Portage

Portage is early. Governance is still being settled. In the meantime:

## Local setup

After cloning:

```sh
npm install
pre-commit install
```

`npm install` pulls in Biome, Prettier, and markdownlint-cli2.
`pre-commit install` wires the hooks so every commit is checked automatically.
Install `pre-commit` itself via `pipx install pre-commit` or `brew install pre-commit` if you don't have it yet.

## What gets checked

Every commit (and every CI run) validates:

- **JSON formatting and lint** — Biome, scoped to `**/*.json`
- **Markdown formatting** — Prettier, scoped to `**/*.md`
- **Markdown linting** — markdownlint-cli2, basic heading and code-block rules
- **SKILL.md frontmatter** — strict schema: only `name` and `description` are allowed; `name` must match the skill's directory
- **Marketplace symlinks** — `./scripts/link-marketplace-skills.sh` is auto-run when anything under `plugins/*/skills/` changes, and CI verifies the result is committed

Run everything manually with `npm run validate` (format check + lint + skill frontmatter).

## Contribution guidelines

- **Open an issue** before starting significant work so we can discuss scope.
- **Follow the existing plugin structure** under `plugins/`. Each plugin has its own `.claude-plugin/plugin.json`, plus `agents/`, `commands/`, and `skills/` directories as needed.
- **Keep skills self-contained.** A skill is a directory with a `SKILL.md` and any supporting files (`references/`, `scripts/`, `assets/`). The directory is what gets symlinked into `.claude/skills/` and surfaced to other tools.
- **Keep content generic.** Skills and plugins should apply to any project using the relevant tech. Avoid company or product names.
- **License.** By contributing, you agree that your work will be distributed under GPL-3.0.

Open a pull request when ready. Questions, concerns, or design discussions go in issues.
