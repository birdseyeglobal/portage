#!/usr/bin/env bun
/**
 * Validate SKILL.md YAML frontmatter against the Claude Code skill spec.
 *
 * Allowed fields (strict):
 *   - name        (required)
 *   - description (required)
 *
 * Any other top-level field is an error. The `name` field must match
 * the skill's directory name.
 *
 * Extend ALLOWED_FIELDS below on a case-by-case basis if a non-standard
 * field is deliberately adopted.
 */

import { readFileSync } from "node:fs";
import { basename, dirname, resolve } from "node:path";
import { Glob } from "bun";

const ALLOWED_FIELDS = new Set(["name", "description"]);
const REQUIRED_FIELDS = ["name", "description"] as const;

const FRONTMATTER_RE = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/;
const BLOCK_SCALAR_MARKERS = new Set(["|", ">", "|-", ">-", "|+", ">+"]);

type Pair = { key: string; value: string };

function topLevelPairs(frontmatter: string): Pair[] {
  const lines = frontmatter.split(/\r?\n/);
  const pairs: Pair[] = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line || /^\s/.test(line) || !line.includes(":")) continue;

    const colonIdx = line.indexOf(":");
    const key = line.slice(0, colonIdx).trim();
    let value = line.slice(colonIdx + 1).trim();

    if (BLOCK_SCALAR_MARKERS.has(value)) {
      const collected: string[] = [];
      let j = i + 1;
      while (j < lines.length && (lines[j] === "" || /^\s/.test(lines[j]))) {
        collected.push(lines[j].replace(/^\s+/, ""));
        j++;
      }
      value = collected.filter((s) => s.length > 0).join(" ").trim();
      i = j - 1;
    }

    pairs.push({ key, value });
  }

  return pairs;
}

function stripQuotes(s: string): string {
  const trimmed = s.trim();
  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function validate(path: string): string[] {
  const errors: string[] = [];
  const text = readFileSync(path, "utf8");

  const match = text.match(FRONTMATTER_RE);
  if (!match) {
    return [`${path}: missing or malformed YAML frontmatter`];
  }

  const pairs = topLevelPairs(match[1]);
  const keys = new Set(pairs.map((p) => p.key));
  const values = new Map(pairs.map((p) => [p.key, p.value]));

  for (const field of REQUIRED_FIELDS) {
    if (!keys.has(field)) {
      errors.push(`${path}: missing required field '${field}'`);
    }
  }

  const unknown = [...keys].filter((k) => !ALLOWED_FIELDS.has(k)).sort();
  for (const field of unknown) {
    errors.push(
      `${path}: non-standard field '${field}' (allowed: ${[...ALLOWED_FIELDS].sort().join(", ")})`,
    );
  }

  const nameValue = values.get("name");
  if (nameValue !== undefined) {
    const name = stripQuotes(nameValue);
    const dirName = basename(dirname(path));
    if (name !== dirName) {
      errors.push(
        `${path}: frontmatter name '${name}' does not match directory '${dirName}'`,
      );
    }
  }

  const descriptionValue = values.get("description");
  if (descriptionValue !== undefined) {
    const description = stripQuotes(descriptionValue);
    if (!description) {
      errors.push(`${path}: description is empty`);
    }
  }

  return errors;
}

async function main(): Promise<number> {
  const repoRoot = resolve(import.meta.dir, "..");
  const glob = new Glob("plugins/*/skills/*/SKILL.md");

  const skills: string[] = [];
  for await (const file of glob.scan({ cwd: repoRoot })) {
    skills.push(resolve(repoRoot, file));
  }
  skills.sort();

  if (skills.length === 0) {
    console.error("No SKILL.md files found under plugins/*/skills/*/");
    return 1;
  }

  const allErrors: string[] = [];
  for (const skill of skills) {
    allErrors.push(...validate(skill));
  }

  if (allErrors.length > 0) {
    for (const err of allErrors) {
      console.error(`ERROR: ${err}`);
    }
    console.error(
      `\n${allErrors.length} error(s) across ${skills.length} skill(s)`,
    );
    return 1;
  }

  console.log(`OK: ${skills.length} skill(s) validated`);
  return 0;
}

process.exit(await main());
