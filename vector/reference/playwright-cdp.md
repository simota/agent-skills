# Vector Playwright & CDP Integration

Playwright MCP server and CDP integration patterns.

---

## PLAYWRIGHT MCP SERVER INTEGRATION

Vector prefers using Playwright MCP server when available for browser operations.

### MCP Server Detection

```typescript
// Check if Playwright MCP server is available
async function checkPlaywrightMCP(): Promise<boolean> {
  // MCP server availability check logic
  // Returns true if playwright-mcp tools are available
}
```

### MCP Server Operations

| Operation | MCP Tool | Description |
|-----------|----------|-------------|
| Navigate | `playwright_navigate` | Navigate to URL |
| Click | `playwright_click` | Click element by accessibility ref |
| Fill | `playwright_fill` | Fill input field |
| Screenshot | `playwright_screenshot` | Capture screenshot for evidence |
| Snapshot | `playwright_snapshot` | Get accessibility tree snapshot for structured DOM analysis |
| Evaluate | `playwright_evaluate` | Execute JavaScript (also for piercing shadow DOM) |
| Wait | `playwright_wait` | Wait for element/condition |
| Run Code | `browser_run_code` | Execute Playwright scripts directly for complex multi-step interactions beyond individual tool calls |

### Fallback: Direct Playwright

```typescript
import { chromium, Browser, Page } from 'playwright';

class NavigatorBrowser {
  private browser: Browser | null = null;
  private page: Page | null = null;

  async initialize(): Promise<void> {
    this.browser = await chromium.launch({
      headless: process.env.NAVIGATOR_HEADLESS !== 'false',
    });
    const context = await this.browser.newContext({
      viewport: { width: 1280, height: 720 },
      userAgent: 'Vector Agent/1.0',
    });
    this.page = await context.newPage();
  }

  async navigate(url: string): Promise<void> {
    await this.page?.goto(url, { waitUntil: 'networkidle' });
  }

  async click(selector: string): Promise<void> {
    await this.page?.click(selector);
  }

  async fill(selector: string, value: string): Promise<void> {
    await this.page?.fill(selector, value);
  }

  async screenshot(path: string): Promise<void> {
    await this.page?.screenshot({ path, fullPage: true });
  }

  async close(): Promise<void> {
    await this.browser?.close();
  }
}
```

---

## CDP (Chrome DevTools Protocol) INTEGRATION

CDP provides advanced browser control capabilities beyond standard Playwright.

### CDP Use Cases

| Feature | CDP Method | Use Case |
|---------|------------|----------|
| Console Monitoring | `Runtime.consoleAPICalled` | Capture all console messages |
| Network Interception | `Network.requestWillBeSent` | Monitor/modify requests |
| Performance Metrics | `Performance.getMetrics` | Collect performance data |
| DOM Inspection | `DOM.getDocument` | Advanced DOM queries |
| Coverage | `Profiler.startPreciseCoverage` | Code coverage analysis |
| Emulation | `Emulation.*` | Device/network emulation |

### CDP Connection

```typescript
import { chromium } from 'playwright';

async function connectCDP() {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // Get CDP session
  const client = await context.newCDPSession(page);

  // Enable domains
  await client.send('Console.enable');
  await client.send('Network.enable');
  await client.send('Performance.enable');

  return { browser, page, client };
}
```

### Console Monitoring

```typescript
// Capture console messages
client.on('Runtime.consoleAPICalled', (event) => {
  const { type, args, timestamp } = event;
  const message = args.map(arg => arg.value || arg.description).join(' ');

  fs.appendFileSync('.vector/logs/console.log',
    `[${new Date(timestamp).toISOString()}] [${type}] ${message}\n`
  );
});
```

### Network Monitoring

```typescript
// Capture network requests
const requests: NetworkRequest[] = [];

client.on('Network.requestWillBeSent', (event) => {
  requests.push({
    id: event.requestId,
    url: event.request.url,
    method: event.request.method,
    timestamp: event.timestamp,
  });
});

client.on('Network.responseReceived', (event) => {
  const request = requests.find(r => r.id === event.requestId);
  if (request) {
    request.status = event.response.status;
    request.contentType = event.response.headers['content-type'];
  }
});

// Export as HAR
async function exportHAR(path: string) {
  // Convert requests to HAR format
}
```

### Performance Metrics

```typescript
// Collect performance metrics
async function getPerformanceMetrics(client: CDPSession) {
  const { metrics } = await client.send('Performance.getMetrics');

  const metricsMap = new Map(metrics.map(m => [m.name, m.value]));

  return {
    FCP: metricsMap.get('FirstContentfulPaint'),
    LCP: metricsMap.get('LargestContentfulPaint'),
    TTI: metricsMap.get('InteractiveTime'),
    TotalJSHeapSize: metricsMap.get('JSHeapUsedSize'),
    Documents: metricsMap.get('Documents'),
    Frames: metricsMap.get('Frames'),
  };
}
```

---

## Cross-Reference Links

| Reference | Content |
|-----------|---------|
| `execution-templates.md` | Execution phase templates, wait strategies, error handling |
| `data-extraction.md` | Data extraction patterns, form operations, authentication |
| `video-recording.md` | Recording configuration, best practices, file management |


---

## Playwright MCP Server — Long Form (SKILL.md excerpt)

Playwright MCP operates on **structured accessibility snapshots** (not pixel-based screenshots), enabling deterministic element identification via refs. The accessibility tree reflects how screen readers see the page: button names, roles, labels — making selectors resilient to layout shifts and CSS class changes.

**Snapshot mode** (default) handles ~95% of web automation. **Vision mode** (fallback) uses coordinate-based interaction via screenshots for elements not in the accessibility tree: shadow DOM components, canvas, custom-drawn UI.

**Shadow DOM limitation:** Modern design systems (Shoelace, Lit, corporate component libraries) nest elements inside shadow roots invisible to accessibility snapshots. When clicks hit "nothing", switch to vision mode or use `playwright_evaluate` to pierce shadow roots.

**MCP vs CLI decision:** Playwright MCP consumes ~4–10x more tokens per session than Playwright CLI (~114K vs ~27K tokens for equivalent tasks, scaling with interaction count). Microsoft recommends CLI for coding agents with filesystem access (Claude Code, Copilot, Cursor) — CLI saves accessibility snapshots and screenshots to disk as files instead of streaming into the LLM context. For multi-step tasks (>10 sequential interactions), strongly prefer CLI — token accumulation compounds with each step, causing progressive slowdown via quadratic attention cost. MCP is preferred when the agent lacks filesystem access, or needs iterative reasoning with persistent browser state and rich introspection.

**Session lifecycle:** Sessions are either running or gone (no intermediate "stopped" state). Browser profiles are **persistent by default** — login state and cookies are preserved between sessions, with profiles stored in the platform's cache directory. Use `--no-persistent` for ephemeral sessions when you need a clean slate (e.g., testing login flows, avoiding session leakage between unrelated tasks). Always use ephemeral mode when automating tasks involving sensitive data to prevent credential persistence.

