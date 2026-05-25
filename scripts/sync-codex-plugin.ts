#!/usr/bin/env bun
// Keep Codex-facing plugin surfaces in sync with the Claude marketplace source.
//
// Source of truth:
//   - plugin skill directories under plugins/
//   - plugin command Markdown under plugins/
//   - plugin agent Markdown under plugins/
//
// Generated/linked compatibility surfaces:
//   - .claude/skills/*
//   - .agents/skills -> .claude/skills
//   - commands/*.toml
//   - agents/*.md

import {
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { basename, dirname, relative, resolve } from "node:path";
import { Glob } from "bun";

const repoRoot = resolve(import.meta.dir, "..");
const pluginsDir = resolve(repoRoot, "plugins");
const commandsDir = resolve(repoRoot, "commands");
const agentsDir = resolve(repoRoot, "agents");

type SourceFile = {
  plugin: string;
  name: string;
  path: string;
};

async function run(command: string, args: string[]): Promise<void> {
  const proc = Bun.spawn([command, ...args], {
    cwd: repoRoot,
    stdout: "inherit",
    stderr: "inherit",
  });
  const code = await proc.exited;
  if (code !== 0) {
    throw new Error(`${command} ${args.join(" ")} exited with ${code}`);
  }
}

function listPluginFiles(kind: "commands" | "agents"): SourceFile[] {
  const files: SourceFile[] = [];

  for (const plugin of readdirSync(pluginsDir).sort()) {
    const dir = resolve(pluginsDir, plugin, kind);
    if (!existsSync(dir)) continue;

    for (const file of readdirSync(dir).sort()) {
      const expectedExt = kind === "commands" ? ".md" : ".md";
      if (!file.endsWith(expectedExt)) continue;

      files.push({
        plugin,
        name: basename(file, expectedExt),
        path: resolve(dir, file),
      });
    }
  }

  return files;
}

function assertUnique(files: SourceFile[], kind: string): void {
  const seen = new Map<string, SourceFile>();

  for (const file of files) {
    const previous = seen.get(file.name);
    if (previous) {
      throw new Error(
        `Duplicate ${kind} name '${file.name}' in plugins '${previous.plugin}' and '${file.plugin}'`,
      );
    }
    seen.set(file.name, file);
  }
}

function removeGenerated(dir: string, ext: string): void {
  mkdirSync(dir, { recursive: true });

  for (const file of readdirSync(dir)) {
    if (!file.endsWith(ext)) continue;

    const path = resolve(dir, file);
    const stat = lstatSync(path);
    if (stat.isFile() || stat.isSymbolicLink()) {
      rmSync(path);
    }
  }
}

function stripFrontmatter(markdown: string): string {
  return markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "").trim();
}

function adaptClaudeCommandBody(body: string): string {
  return body
    .replace(
      /`Skill\("content-writing:([^"]+)"\)`/g,
      "the active Portage skill named `$1`",
    )
    .replace(
      /`Skill\("([^"]+)"\)`/g,
      "the active Portage skill named `$1`",
    )
    .replace(/\bClaude Code\b/g, "Codex");
}

function tomlString(value: string): string {
  return JSON.stringify(value);
}

function syncCommands(): number {
  const commands = listPluginFiles("commands");
  assertUnique(commands, "command");
  removeGenerated(commandsDir, ".toml");

  for (const command of commands) {
    const source = readFileSync(command.path, "utf8");
    const body = adaptClaudeCommandBody(stripFrontmatter(source));
    const prompt = `${body}\n\nUser request: {{args}}\n`;
    const target = resolve(commandsDir, `${command.name}.toml`);
    writeFileSync(
      target,
      `# Generated from plugins/${command.plugin}/commands/${command.name}.md by scripts/sync-codex-plugin.ts.\n# Do not edit manually.\n\nprompt = ${tomlString(prompt)}\n`,
    );
  }

  return commands.length;
}

function syncAgents(): number {
  const agents = listPluginFiles("agents");
  assertUnique(agents, "agent");
  removeGenerated(agentsDir, ".md");

  for (const agent of agents) {
    const target = resolve(agentsDir, `${agent.name}.md`);
    const linkTarget = relative(dirname(target), agent.path);
    symlinkSync(linkTarget, target);
  }

  return agents.length;
}

async function countSkills(): Promise<{ source: number; linked: number }> {
  let source = 0;

  for await (const _ of new Glob("plugins/*/skills/*/SKILL.md").scan({
    cwd: repoRoot,
  })) {
    source++;
  }

  const linked = readdirSync(resolve(repoRoot, ".claude/skills")).filter((entry) =>
    existsSync(resolve(repoRoot, ".claude/skills", entry, "SKILL.md")),
  ).length;

  return { source, linked };
}

async function main(): Promise<number> {
  await run("bash", ["scripts/link-marketplace-skills.sh"]);

  const commandCount = syncCommands();
  const agentCount = syncAgents();
  const skills = await countSkills();

  if (skills.source !== skills.linked) {
    throw new Error(
      `Codex skill count mismatch: source=${skills.source}, linked=${skills.linked}`,
    );
  }

  console.log("");
  console.log("Codex plugin surfaces synced:");
  console.log(`  Skills: ${skills.linked}/${skills.source}`);
  console.log(`  Commands: ${commandCount}`);
  console.log(`  Agents: ${agentCount}`);
  return 0;
}

try {
  process.exit(await main());
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
}
