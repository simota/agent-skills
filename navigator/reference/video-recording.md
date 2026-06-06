# Video Recording Reference

Recording patterns for browser task evidence and documentation.

---

## Playwright Video Recording

### Context-level Recording (Recommended for task flows)

```typescript
const context = await browser.newContext({
  recordVideo: {
    dir: '.navigator/videos/',
    size: { width: 1280, height: 720 },
  },
});
const page = await context.newPage();

// Perform operations
await page.goto('https://example.com');
await page.fill('[data-testid="search"]', 'keyword');
await page.click('[data-testid="submit"]');

// Get video path after closing
await page.close();
const videoPath = await page.video()?.path();
console.log(`Video saved: ${videoPath}`);

// IMPORTANT: Close context to finalize video
await context.close();
```

### CDP Screen Recording (Advanced, fine-grained control)

```typescript
const client = await page.context().newCDPSession(page);

// Start screencast
await client.send('Page.startScreencast', {
  format: 'jpeg',
  quality: 80,
  everyNthFrame: 2,
});

// Collect frames
const frames: Buffer[] = [];
client.on('Page.screencastFrame', async (event) => {
  frames.push(Buffer.from(event.data, 'base64'));
  await client.send('Page.screencastFrameAck', { sessionId: event.sessionId });
});

// Perform operations...

// Stop and process
await client.send('Page.stopScreencast');
// Convert frames to video using ffmpeg or similar
```

### Video Configuration Options

```typescript
// playwright.config.ts or context options
const videoOptions = {
  size: { width: 1280, height: 720 },  // 720p (recommended)
  // size: { width: 1920, height: 1080 }, // 1080p (larger files)
  dir: '.navigator/videos/',
};

// Per-task recording control
async function recordTask(task: () => Promise<void>, name: string) {
  const context = await browser.newContext({
    recordVideo: { dir: '.navigator/videos/' },
  });
  const page = await context.newPage();

  try {
    await task();
  } finally {
    await page.close();
    const video = page.video();
    if (video) {
      const originalPath = await video.path();
      const newPath = `.navigator/videos/${name}_${Date.now()}.webm`;
      await fs.rename(originalPath, newPath);
    }
    await context.close();
  }
}
```

---

## Best Practices

| Practice | Description |
|----------|-------------|
| **Start recording before navigation** | Capture complete flow including initial load |
| **Use 720p resolution** | Balance between clarity and file size |
| **Close page/context to finalize** | Video file is incomplete until closed |
| **Rename files meaningfully** | `task_checkout_20250127.webm` not `random-uuid.webm` |
| **Record only when necessary** | Videos consume storage; be selective |
| **Include in task report** | Reference video path in final report |
| **Clean up old videos** | Implement retention policy (e.g., 7 days) |

---

## Video File Management

```
.navigator/videos/
├── task_[name]_[timestamp].webm      # Completed task videos
├── error_[name]_[timestamp].webm     # Error reproduction videos
└── evidence_[name]_[timestamp].webm  # Evidence videos
```

---

## Integration with Task Report

```markdown
## Task Report: Checkout Flow Verification

### Evidence
- **Screenshots**: `.navigator/screenshots/checkout_*.png`
- **Video**: `.navigator/videos/task_checkout_20250127_143022.webm`
- **HAR**: `.navigator/har/checkout_20250127.har`

### Video Timestamps
- 0:00 - Page load
- 0:15 - Form filling
- 0:45 - Submit and confirmation
```

---

## Cross-Reference Links

| Reference | Content |
|-----------|---------|
| `execution-templates.md` | Execution phase templates, wait strategies, error handling |
| `playwright-cdp.md` | MCP server operations, CDP methods, connection patterns |
