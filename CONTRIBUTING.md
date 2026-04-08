# Contributing to Portage

Portage is early. Governance is still being settled. In the meantime:

- **Open an issue** before starting significant work so we can discuss scope.
- **Follow the existing plugin structure** under `plugins/`. Each plugin has its own `.claude-plugin/plugin.json`, plus `agents/`, `commands/`, and `skills/` directories as needed.
- **Keep skills self-contained.** A skill is a directory with a `SKILL.md` and any supporting files (`references/`, `scripts/`, `assets/`). The directory is what gets symlinked into `.claude/skills/` and surfaced to other tools.
- **Run the link script** after adding or removing a skill:
  ```
  ./scripts/link-marketplace-skills.sh
  ```
  Edits to files inside an existing skill directory don't need a re-run — they propagate through the symlink.
- **Keep content generic.** Skills and plugins should apply to any project using the relevant tech. Avoid company or product names.
- **License.** By contributing, you agree that your work will be distributed under GPL-3.0.

Open a pull request when ready. Questions, concerns, or design discussions go in issues.
