import { Hono } from "hono";
import { streamSSE } from "hono/streaming";
import { cors } from "hono/cors";
import * as fs from "node:fs";
import * as path from "node:path";
import { watch as chokidarWatch } from "chokidar";
import { generatePostmortem, writePostmortem } from "./postmortem";

const ROOT = path.resolve(import.meta.dir, "..");
const EVENTS_DIR = path.join(ROOT, "events");

const app = new Hono();
app.use("/api/*", cors({ origin: "*" }));

app.get("/api/runs", (c) => {
  if (!fs.existsSync(EVENTS_DIR)) return c.json({ runs: [] });
  const runs = fs
    .readdirSync(EVENTS_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory() && d.name.startsWith("apex-"))
    .map((d) => d.name)
    .sort()
    .reverse();
  return c.json({ runs });
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

const port = Number(process.env.PORT ?? 5757);
console.log(`apex-dash sample server listening on http://127.0.0.1:${port}`);

export default {
  port,
  hostname: "127.0.0.1",
  fetch: app.fetch,
};
