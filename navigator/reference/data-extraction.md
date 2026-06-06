# Navigator Data Extraction Patterns

Patterns for extracting, validating, and processing web data.

---

## TEXT CONTENT EXTRACTION

```typescript
// Single element
const title = await page.locator('h1').textContent();

// Multiple elements
const items = await page.locator('.list-item').allTextContents();

// With filtering
const prices = await page.locator('.price')
  .filter({ hasText: /\d+/ })
  .allTextContents();
```

---

## STRUCTURED DATA EXTRACTION

```typescript
// Product list
const products = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.product-card')).map(card => ({
    name: card.querySelector('.product-name')?.textContent?.trim(),
    price: card.querySelector('.product-price')?.textContent?.trim(),
    rating: card.querySelector('.product-rating')?.getAttribute('data-rating'),
    imageUrl: card.querySelector('img')?.src,
    productUrl: card.querySelector('a')?.href,
  }));
});
```

---

## TABLE DATA EXTRACTION

```typescript
// Extract table to JSON
const tableData = await page.evaluate(() => {
  const table = document.querySelector('table');
  const headers = Array.from(table.querySelectorAll('thead th'))
    .map(th => th.textContent?.trim() || '');

  const rows = Array.from(table.querySelectorAll('tbody tr')).map(row => {
    const cells = Array.from(row.querySelectorAll('td'));
    return headers.reduce((obj, header, index) => {
      obj[header] = cells[index]?.textContent?.trim() || '';
      return obj;
    }, {} as Record<string, string>);
  });

  return rows;
});
```

---

## PAGINATION HANDLING

```typescript
// Collect data across multiple pages
async function collectPaginatedData(page: Page): Promise<any[]> {
  const allData: any[] = [];
  let hasNextPage = true;
  let pageNum = 1;

  while (hasNextPage) {
    // Extract data from current page
    const pageData = await extractPageData(page);
    allData.push(...pageData);

    // Screenshot current page
    await page.screenshot({
      path: `.navigator/screenshots/page_${pageNum}.png`
    });

    // Check for next page
    const nextButton = page.locator('[data-testid="next-page"]');
    hasNextPage = await nextButton.isVisible() && await nextButton.isEnabled();

    if (hasNextPage) {
      await nextButton.click();
      await page.waitForLoadState('networkidle');
      pageNum++;
    }
  }

  return allData;
}
```

---

## DATA VALIDATION

```typescript
// Validate extracted data
function validateData(data: any[]): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  data.forEach((item, index) => {
    // Required fields
    if (!item.name) errors.push(`Row ${index}: Missing name`);
    if (!item.price) errors.push(`Row ${index}: Missing price`);

    // Format validation
    if (item.price && !/^\d+(\.\d{2})?$/.test(item.price)) {
      warnings.push(`Row ${index}: Price format irregular`);
    }

    // Duplicate detection
    const duplicates = data.filter(d => d.name === item.name);
    if (duplicates.length > 1) {
      warnings.push(`Row ${index}: Duplicate name detected`);
    }
  });

  return {
    valid: errors.length === 0,
    errors,
    warnings,
    recordCount: data.length,
  };
}
```

---

## FORM OPERATIONS

### Form Analysis

```typescript
// Analyze form structure
async function analyzeForm(page: Page, formSelector: string) {
  return await page.evaluate((selector) => {
    const form = document.querySelector(selector);
    if (!form) return null;

    const fields = Array.from(form.querySelectorAll('input, select, textarea'));
    return fields.map(field => ({
      name: field.getAttribute('name'),
      type: field.getAttribute('type') || field.tagName.toLowerCase(),
      required: field.hasAttribute('required'),
      placeholder: field.getAttribute('placeholder'),
      options: field.tagName === 'SELECT'
        ? Array.from(field.querySelectorAll('option')).map(o => o.value)
        : undefined,
    }));
  }, formSelector);
}
```

### Form Filling

```typescript
// Fill form with validation
async function fillForm(page: Page, formData: Record<string, string>) {
  for (const [name, value] of Object.entries(formData)) {
    const field = page.locator(`[name="${name}"]`);
    const tagName = await field.evaluate(el => el.tagName);
    const inputType = await field.getAttribute('type');

    if (tagName === 'SELECT') {
      await field.selectOption(value);
    } else if (inputType === 'checkbox') {
      if (value === 'true') await field.check();
      else await field.uncheck();
    } else if (inputType === 'radio') {
      await page.locator(`[name="${name}"][value="${value}"]`).check();
    } else if (inputType === 'file') {
      await field.setInputFiles(value);
    } else {
      await field.fill(value);
    }

    // Brief pause to allow validation
    await page.waitForTimeout(100);
  }
}
```

### Form Submission (with confirmation)

```typescript
// Submit form with safeguards
async function submitForm(page: Page, formSelector: string): Promise<SubmitResult> {
  // Capture form state before submission
  const preSubmitScreenshot = `.navigator/screenshots/form_pre_submit.png`;
  await page.screenshot({ path: preSubmitScreenshot });

  // Get form data for logging
  const formData = await page.evaluate((selector) => {
    const form = document.querySelector(selector) as HTMLFormElement;
    return Object.fromEntries(new FormData(form));
  }, formSelector);

  // Log submission attempt
  console.log('Form submission:', JSON.stringify(formData, null, 2));

  // Submit and wait for response
  const [response] = await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle' }),
    page.locator(`${formSelector} [type="submit"]`).click(),
  ]);

  // Capture result
  const postSubmitScreenshot = `.navigator/screenshots/form_post_submit.png`;
  await page.screenshot({ path: postSubmitScreenshot });

  return {
    success: response?.ok() ?? false,
    status: response?.status(),
    url: page.url(),
    screenshots: {
      before: preSubmitScreenshot,
      after: postSubmitScreenshot,
    },
  };
}
```

---

## AUTHENTICATION HANDLING

### Session State Management

```typescript
// Save authentication state
async function saveAuthState(context: BrowserContext, path: string) {
  await context.storageState({ path });
  console.log(`Auth state saved to: ${path}`);
}

// Load authentication state
async function loadAuthState(browser: Browser, statePath: string) {
  const context = await browser.newContext({
    storageState: statePath,
  });
  return context;
}
```

### Login Flow

```typescript
// Execute login flow
async function login(page: Page): Promise<boolean> {
  const email = process.env.NAVIGATOR_USER_EMAIL;
  const password = process.env.NAVIGATOR_USER_PASSWORD;

  if (!email || !password) {
    throw new Error('Authentication credentials not found in environment variables');
  }

  // Navigate to login page
  await page.goto('/login');

  // Fill credentials
  await page.fill('[data-testid="email-input"]', email);
  await page.fill('[data-testid="password-input"]', password);

  // Submit
  await page.click('[data-testid="login-submit"]');

  // Wait for redirect or success indicator
  try {
    await page.waitForURL('**/dashboard', { timeout: 10000 });
    return true;
  } catch {
    // Check for error message
    const errorVisible = await page.locator('[data-testid="login-error"]').isVisible();
    if (errorVisible) {
      const errorText = await page.locator('[data-testid="login-error"]').textContent();
      console.error('Login failed:', errorText);
    }
    return false;
  }
}
```

### Authentication State Check

```typescript
// Check if currently authenticated
async function isAuthenticated(page: Page): Promise<boolean> {
  // Method 1: Check for user menu/avatar
  const userMenuVisible = await page.locator('[data-testid="user-menu"]').isVisible();
  if (userMenuVisible) return true;

  // Method 2: Check cookies
  const cookies = await page.context().cookies();
  const authCookie = cookies.find(c => c.name === 'session' || c.name === 'auth_token');
  if (authCookie) return true;

  // Method 3: Check localStorage
  const token = await page.evaluate(() => localStorage.getItem('auth_token'));
  if (token) return true;

  return false;
}
```

---

## ERROR HANDLING

### Error Classification

| Error Type | Cause | Action |
|------------|-------|--------|
| ElementNotFound | Selector changed/invalid | Update selector, retry |
| Timeout | Page slow, element hidden | Increase timeout, check visibility |
| NavigationFailed | Invalid URL, blocked | Verify URL, check access |
| NetworkError | Connection issue | Retry with backoff |
| AuthenticationFailed | Credentials invalid | Escalate to user |
| RateLimited | Too many requests | Wait and retry |
| CAPTCHABlocked | CAPTCHA present | Escalate to user |

### Error Recovery with Retry

```typescript
// Retry with exponential backoff
async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error as Error;
      const delay = baseDelay * Math.pow(2, attempt);
      console.log(`Attempt ${attempt + 1} failed, retrying in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}
```

### Error Logging

```typescript
// Log error with context
function logError(error: Error, context: ErrorContext) {
  const errorLog = {
    timestamp: new Date().toISOString(),
    type: error.name,
    message: error.message,
    stack: error.stack,
    context: {
      url: context.url,
      step: context.step,
      selector: context.selector,
      screenshot: context.screenshotPath,
    },
  };

  fs.appendFileSync(
    '.navigator/logs/errors.json',
    JSON.stringify(errorLog) + '\n'
  );
}
```

---

## Cross-Reference Links

| Reference | Content |
|-----------|---------|
| `execution-templates.md` | Execution phase templates, wait strategies, error handling |
| `playwright-cdp.md` | MCP server operations, CDP methods, connection patterns |
