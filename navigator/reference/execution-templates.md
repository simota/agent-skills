# Navigator Execution Templates

Detailed templates for each phase of Navigator's execution process.

---

## RECON Template

```markdown
## RECON Report

**Target**: [URL]
**Access Time**: [YYYY-MM-DD HH:MM:SS]

### Site Structure
- Page type: [SPA / MPA / Hybrid]
- Framework detected: [React / Vue / Angular / Other / Unknown]
- Authentication: [Required / Optional / None]

### Key Elements
| Element | Selector | Purpose |
|---------|----------|---------|
| [Name] | [CSS/XPath] | [What it does] |

### Authentication State
- Current: [Logged in / Logged out / Session expired]
- Required for task: [Yes / No]
- Method: [Cookie / Token / Session / OAuth]

### Obstacles Detected
- [ ] CAPTCHA present
- [ ] Rate limiting detected
- [ ] Geo-restriction
- [ ] JavaScript required
- [ ] Dynamic content loading

### Screenshots
- Initial state: `.navigator/screenshots/recon_initial.png`
```

---

## PLAN Template

```markdown
## Operation Plan

**Task**: [Task description]
**Estimated Steps**: [N]

### Step Breakdown
| # | Action | Target | Expected Result | Fallback |
|---|--------|--------|-----------------|----------|
| 1 | [Action] | [Selector/URL] | [Expected] | [If fails...] |
| 2 | [Action] | [Selector/URL] | [Expected] | [If fails...] |

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | [H/M/L] | [H/M/L] | [Strategy] |

### Destructive Operations
- [ ] Form submission (data change)
- [ ] Delete operation
- [ ] Payment/purchase
- [ ] Account modification

### User Confirmation Required
- [ ] [Operation requiring confirmation]
- [ ] [Operation requiring confirmation]

### Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

---

## EXECUTE Template

### Wait Strategies

```typescript
// Good: Wait for specific conditions
await page.waitForSelector('[data-testid="result"]', { state: 'visible' });
await page.waitForURL('**/success');
await page.waitForLoadState('networkidle');
await page.waitForResponse(resp => resp.url().includes('/api/data'));

// Bad: Arbitrary timeouts
// await page.waitForTimeout(3000); // Avoid this
```

### Error Handling with Retry

```typescript
// Retry logic for transient failures
async function executeWithRetry(action: () => Promise<void>, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await action();
      return;
    } catch (error) {
      if (attempt === maxRetries) throw error;
      await page.waitForTimeout(1000 * attempt); // Exponential backoff
    }
  }
}
```

### Execution Log Template

```markdown
## Execution Log

**Started**: [YYYY-MM-DD HH:MM:SS]

### Step Execution
| # | Action | Status | Duration | Notes |
|---|--------|--------|----------|-------|
| 1 | [Action] | ✅/❌ | [X ms] | [Notes] |
| 2 | [Action] | ✅/❌ | [X ms] | [Notes] |

### Errors Encountered
| Time | Type | Message | Resolution |
|------|------|---------|------------|
| [HH:MM:SS] | [Console/Network] | [Message] | [How resolved] |

**Completed**: [YYYY-MM-DD HH:MM:SS]
**Duration**: [Total time]
```

---

## COLLECT Template

### Data Extraction Examples

```typescript
// Text extraction
const title = await page.locator('h1').textContent();
const items = await page.locator('.item').allTextContents();

// Structured data
const data = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.product')).map(el => ({
    name: el.querySelector('.name')?.textContent,
    price: el.querySelector('.price')?.textContent,
    url: el.querySelector('a')?.href,
  }));
});

// Table data
const tableData = await page.locator('table tbody tr').evaluateAll(rows =>
  rows.map(row => ({
    col1: row.querySelector('td:nth-child(1)')?.textContent,
    col2: row.querySelector('td:nth-child(2)')?.textContent,
  }))
);
```

### Evidence Collection

```typescript
// Screenshot
await page.screenshot({ path: '.navigator/screenshots/result.png', fullPage: true });

// HAR (Network log)
const context = await browser.newContext({ recordHar: { path: '.navigator/har/session.har' } });

// Console logs
page.on('console', msg => {
  fs.appendFileSync('.navigator/logs/console.log', `[${msg.type()}] ${msg.text()}\n`);
});
```

### Collect Output Template

```markdown
## Collected Data Summary

**Collection Time**: [YYYY-MM-DD HH:MM:SS]

### Data Files
| Type | Path | Records | Size |
|------|------|---------|------|
| JSON | `.navigator/data/[name].json` | [N] | [X KB] |
| CSV | `.navigator/data/[name].csv` | [N] | [X KB] |

### Screenshots
| Name | Path | Description |
|------|------|-------------|
| [name] | `.navigator/screenshots/[name].png` | [What it shows] |

### Network Logs
- HAR file: `.navigator/har/[session].har`
- Request count: [N]
- Errors: [N]

### Console Logs
- Log file: `.navigator/logs/console.log`
- Errors: [N]
- Warnings: [N]

### Data Validation
- [ ] All required fields present
- [ ] Data format correct
- [ ] No missing values
- [ ] Duplicates handled
```

---

## REPORT Template

```markdown
## Navigator Task Report

### Task Summary
| Field | Value |
|-------|-------|
| Task ID | [ID or description] |
| Target | [URL] |
| Status | ✅ Complete / ⚠️ Partial / ❌ Failed |
| Duration | [Total time] |
| Steps Completed | [X/Y] |

### Execution Summary
**Goal**: [What was requested]
**Outcome**: [What was achieved]

### Steps Completed
| # | Step | Status | Notes |
|---|------|--------|-------|
| 1 | [Step] | ✅/❌ | [Notes] |

### Data Collected
- **Records**: [N] items
- **Format**: [JSON/CSV/Both]
- **Location**: `.navigator/data/`

### Evidence
| Type | Path |
|------|------|
| Screenshots | `.navigator/screenshots/` |
| HAR logs | `.navigator/har/` |
| Console logs | `.navigator/logs/` |

### Issues Encountered
| Issue | Impact | Resolution |
|-------|--------|------------|
| [Issue] | [Impact] | [How resolved] |

### Verification Steps
1. [How to verify the results]
2. [How to verify the results]

### Recommendations
- [Follow-up actions if any]
```

---

## Cross-Reference Links

| Reference | Content |
|-----------|---------|
| `playwright-cdp.md` | MCP server operations, CDP methods, connection patterns |
| `data-extraction.md` | Data extraction patterns, form operations, authentication |
| `video-recording.md` | Recording configuration, best practices, file management |
| `interaction-triggers.md` | YAML question templates for all 9 triggers |
