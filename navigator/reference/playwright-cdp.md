# Navigator Playwright & CDP Integration

Playwright MCP server and CDP integration patterns.

---

## PLAYWRIGHT MCP SERVER INTEGRATION

Navigator prefers using Playwright MCP server when available for browser operations.

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
| Click | `playwright_click` | Click element |
| Fill | `playwright_fill` | Fill input field |
| Screenshot | `playwright_screenshot` | Capture screenshot |
| Evaluate | `playwright_evaluate` | Execute JavaScript |
| Wait | `playwright_wait` | Wait for element/condition |

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
      userAgent: 'Navigator Agent/1.0',
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

  fs.appendFileSync('.navigator/logs/console.log',
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
