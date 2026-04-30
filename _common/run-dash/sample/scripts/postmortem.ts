#!/usr/bin/env bun
// CLI: regenerate <run-id>'s postmortem.md from its events.jsonl
// Usage:
//   bun run scripts/postmortem.ts <run-id>
//   bun run scripts/postmortem.ts            # newest run

import * as fs from "node:fs";
import * as path from "node:path";
import { writePostmortem } from "../server/postmortem";

const ROOT = path.resolve(import.meta.dir, "..");
const EVENTS_DIR = path.join(ROOT, "events");

function pickNewest(): string | undefined {
  if (!fs.existsSync(EVENTS_DIR)) return undefined;
  const runs = fs
    .readdirSync(EVENTS_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory() && d.name.startsWith("apex-"))
    .map((d) => d.name)
    .sort()
    .reverse();
  return runs[0];
}

const runId = process.argv[2] ?? pickNewest();
if (!runId) {
  console.error("no run-id specified and no runs found under events/");
  process.exit(1);
}

const out = await writePostmortem(runId, EVENTS_DIR, "sample");
console.log(`postmortem written: ${out}`);
