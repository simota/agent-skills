import { Hono } from "hono";
import { streamSSE } from "hono/streaming";
import { cors } from "hono/cors";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { watch as chokidarWatch } from "chokidar";
import { generatePostmortem, writePostmortem } from "./postmortem";

const ROOT = path.resolve(import.meta.dir, "..");

// Resolve events root: prefer RUN_DASH_EVENTS_DIR (global usage),
// fall back to <sample>/events for the bundled fixtures.
function expandHome(p: string): string {
  if (p.startsWith("~")) return path.join(os.homedir(), p.slice(1));
  return p;
}

const EVENTS_DIR = process.env.RUN_DASH_EVENTS_DIR
  ? path.resolve(expandHome(process.env.RUN_DASH_EVENTS_DIR))
  : path.join(ROOT, "events");

const RUN_NAME_RE = /^[a-z][a-z0-9-]*-\d/;

interface RunSummary {
  id: string;
  runKind?: string;
  project?: string;
  goal?: string;
  startedAt?: string;
}

function readRunSummary(dir: string, id: string): RunSummary {
  const file = path.join(dir, id, "events.jsonl");
  const summary: RunSummary = { id };
  if (!fs.existsSync(file)) return summary;
  try {
    const head = fs.readFileSync(file, "utf8").split("\n", 2)[0];
    if (!head) return summary;
    const ev = JSON.parse(head) as {
      kind?: string;
      ts?: string;
      run_kind?: string;
      meta?: { project?: string; goal?: string };
    };
    if (ev.kind === "run_start") {
      summary.runKind = ev.run_kind;
      summary.project = ev.meta?.project;
      summary.goal = ev.meta?.goal;
      summary.startedAt = ev.ts;
    }
  } catch {
    // tolerate corrupt heads
  }
  return summary;
}

const app = new Hono();
app.use("/api/*", cors({ origin: "*" }));

app.get("/api/runs", (c) => {
  if (!fs.existsSync(EVENTS_DIR)) return c.json({ runs: [], events_dir: EVENTS_DIR });
  const runs: RunSummary[] = fs
    .readdirSync(EVENTS_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory() && RUN_NAME_RE.test(d.name))
    .map((d) => readRunSummary(EVENTS_DIR, d.name))
    .sort((a, b) => (a.id < b.id ? 1 : -1));
  return c.json({ runs, events_dir: EVENTS_DIR });
});

app.get("/api/events/:run", (c) => {
  const run = c.req.param("run");
  const file = path.join(EVENTS_DIR, run, "events.jsonl");

  return streamSSE(c, async (stream) => {
    let cursor = 0;

    const drain = async () => {
      if (!fs.existsSync(file)) return;
      const buf = fs.readFileSync(file, "utf8");
      if (buf.length <= cursor) return;
      const slice = buf.slice(cursor);
      cursor = buf.length;
      const lines = slice.split("\n").filter((l) => l.trim().length > 0);
      for (const line of lines) {
        await stream.writeSSE({ data: line });
      }
    };

    await drain();

    const watcher = chokidarWatch(file, {
      persistent: true,
      ignoreInitial: true,
      awaitWriteFinish: { stabilityThreshold: 50, pollInterval: 25 },
    });

    let alive = true;
    watcher.on("change", drain);
    watcher.on("add", drain);

    stream.onAbort(() => {
      alive = false;
      watcher.close();
    });

    while (alive) {
      await stream.sleep(1000);
      try {
        await stream.writeSSE({ event: "ping", data: "keepalive" });
      } catch {
        alive = false;
      }
    }
  });
});

app.get("/api/postmortem/:run", async (c) => {
  const run = c.req.param("run");
  try {
    await writePostmortem(run, EVENTS_DIR);
    const md = await generatePostmortem(run, EVENTS_DIR);
    return c.text(md, 200, {
      "Content-Type": "text/markdown; charset=utf-8",
    });
  } catch (e) {
    return c.json({ error: String(e) }, 500);
  }
});

const port = Number(process.env.RUN_DASH_SERVER_PORT ?? process.env.PORT ?? 5757);
const hostname = "127.0.0.1";

Bun.serve({
  port,
  hostname,
  fetch: app.fetch,
});

console.log(`run-dash sample server listening on http://${hostname}:${port}`);
console.log(`  events_dir: ${EVENTS_DIR}`);
