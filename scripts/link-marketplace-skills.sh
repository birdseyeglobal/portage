#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root relative to this script's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PLUGINS_DIR="$REPO_ROOT/plugins"

# Primary skills directory (Claude Code / Claude Desktop)
CLAUDE_SKILLS_DIR="$REPO_ROOT/.claude/skills"

# Compatibility symlink targets
AGENTS_SKILLS_DIR="$REPO_ROOT/.agents/skills"  # OpenCode + Codex

linked=0
skipped=0
stale_removed=0
warnings=()

mkdir -p "$CLAUDE_SKILLS_DIR"

# Link skills into .claude/skills/
for skill_md in "$PLUGINS_DIR"/*/skills/*/SKILL.md; do
  [ -f "$skill_md" ] || continue

  skill_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$skill_dir")"
  link_path="$CLAUDE_SKILLS_DIR/$skill_name"

  # Collision check
  if [ -e "$link_path" ] || [ -L "$link_path" ]; then
    if [ -L "$link_path" ]; then
      existing_target="$(readlink "$link_path")"
      plugin_name="$(basename "$(dirname "$(dirname "$skill_dir")")")"
      expected_target="../../plugins/$plugin_name/skills/$skill_name"
      if [ "$existing_target" = "$expected_target" ]; then
        linked=$((linked + 1))
        continue
      fi
    fi
    plugin_name="$(basename "$(dirname "$(dirname "$skill_dir")")")"
    warnings+=("COLLISION: '$skill_name' from '$plugin_name' skipped -- already exists in .claude/skills/")
    skipped=$((skipped + 1))
    continue
  fi

  # Create relative symlink
  plugin_name="$(basename "$(dirname "$(dirname "$skill_dir")")")"
  relative_target="../../plugins/$plugin_name/skills/$skill_name"
  ln -s "$relative_target" "$link_path"
  linked=$((linked + 1))
done

# Clean stale symlinks
for link in "$CLAUDE_SKILLS_DIR"/*/; do
  [ -L "${link%/}" ] || continue
  if [ ! -e "${link%/}" ]; then
    stale_name="$(basename "${link%/}")"
    rm "$CLAUDE_SKILLS_DIR/$stale_name"
    warnings+=("STALE: removed '$stale_name' (target no longer exists)")
    stale_removed=$((stale_removed + 1))
  fi
done

# Create compatibility symlink: .agents/skills -> .claude/skills (OpenCode + Codex)
mkdir -p "$REPO_ROOT/.agents"
if [ -L "$AGENTS_SKILLS_DIR" ]; then
  # Already a symlink -- update if needed
  existing="$(readlink "$AGENTS_SKILLS_DIR")"
  if [ "$existing" != "../.claude/skills" ]; then
    rm "$AGENTS_SKILLS_DIR"
    ln -s "../.claude/skills" "$AGENTS_SKILLS_DIR"
  fi
elif [ ! -e "$AGENTS_SKILLS_DIR" ]; then
  ln -s "../.claude/skills" "$AGENTS_SKILLS_DIR"
else
  warnings+=("COMPAT: .agents/skills/ exists as a real directory, skipping symlink")
fi

# Post-link audit: check for duplicate frontmatter name: fields
name_list=""
for skill_md in "$CLAUDE_SKILLS_DIR"/*/SKILL.md; do
  [ -f "$skill_md" ] || continue
  name="$(awk '/^---$/{c++;next} c==1 && /^name:/{sub(/^name:[[:space:]]*/,""); print; exit}' "$skill_md")"
  [ -z "$name" ] && continue
  skill_folder="$(basename "$(dirname "$skill_md")")"
  entry="$name|$skill_folder"
  existing="$(echo "$name_list" | grep "^$name|" || true)"
  if [ -n "$existing" ]; then
    other_folder="$(echo "$existing" | head -1 | cut -d'|' -f2)"
    warnings+=("DUPLICATE NAME: frontmatter name '$name' in '$skill_folder' conflicts with '$other_folder'")
  fi
  name_list="$name_list
$entry"
done

# Summary
echo "Marketplace skills linked: $linked"
echo "Skipped (collisions): $skipped"
echo "Stale removed: $stale_removed"
echo "Compat symlinks: .agents/skills -> .claude/skills (OpenCode + Codex)"

if [ ${#warnings[@]} -gt 0 ]; then
  echo ""
  echo "Warnings:"
  for w in "${warnings[@]}"; do
    echo "  ⚠ $w"
  done
fi
