# Native API Replacement Guide

## Internationalization (Intl API)

Replace formatting libraries with native Intl:

```typescript
// Date Formatting (replaces moment/date-fns for display)
const dateFormatter = new Intl.DateTimeFormat('ja-JP', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  weekday: 'long',
});
dateFormatter.format(new Date()); // "2024年1月15日月曜日"

// Number Formatting (replaces numeral.js)
const currencyFormatter = new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY',
});
currencyFormatter.format(1234567); // "￥1,234,567"

// Relative Time (replaces timeago.js)
const relativeFormatter = new Intl.RelativeTimeFormat('ja', { numeric: 'auto' });
relativeFormatter.format(-1, 'day'); // "昨日"
relativeFormatter.format(3, 'hour'); // "3時間後"

// List Formatting
const listFormatter = new Intl.ListFormat('ja', { style: 'long', type: 'conjunction' });
listFormatter.format(['りんご', 'バナナ', 'オレンジ']); // "りんご、バナナ、オレンジ"

// Plural Rules
const pluralRules = new Intl.PluralRules('en-US');
pluralRules.select(1); // "one"
pluralRules.select(2); // "other"
```

## Fetch API (replaces HTTP libraries)

```typescript
// Basic GET
const response = await fetch('/api/users');
const data = await response.json();

// POST with JSON
const response = await fetch('/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'John' }),
});

// With timeout (AbortController)
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch('/api/data', { signal: controller.signal });
  clearTimeout(timeoutId);
  return await response.json();
} catch (error) {
  if (error.name === 'AbortError') {
    throw new Error('Request timed out');
  }
  throw error;
}

// Retry logic
async function fetchWithRetry(url: string, options = {}, retries = 3): Promise<Response> {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;
      if (response.status < 500) throw new Error(`HTTP ${response.status}`);
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
    }
  }
  throw new Error('Max retries reached');
}
```

## Dialog API (replaces modal libraries)

```typescript
// Native dialog element
const dialog = document.querySelector<HTMLDialogElement>('#myDialog');

// Show as modal (with backdrop, traps focus)
dialog.showModal();

// Show as non-modal
dialog.show();

// Close
dialog.close();

// Handle close
dialog.addEventListener('close', () => {
  console.log('Dialog closed with:', dialog.returnValue);
});

// Click outside to close
dialog.addEventListener('click', (e) => {
  if (e.target === dialog) dialog.close();
});
```

```html
<dialog id="myDialog">
  <form method="dialog">
    <h2>Confirm Action</h2>
    <p>Are you sure?</p>
    <button value="cancel">Cancel</button>
    <button value="confirm">Confirm</button>
  </form>
</dialog>
```

## Intersection Observer (replaces scroll libraries)

```typescript
// Lazy loading images
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target as HTMLImageElement;
      img.src = img.dataset.src!;
      observer.unobserve(img);
    }
  });
}, { rootMargin: '100px' });

document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));

// Infinite scroll
const sentinel = document.querySelector('#sentinel');
const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    loadMoreItems();
  }
}, { threshold: 1.0 });
observer.observe(sentinel);

// Section tracking for navigation
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      setActiveSection(entry.target.id);
    }
  });
}, { threshold: 0.5 });
```

## Resize Observer (replaces resize libraries)

```typescript
const observer = new ResizeObserver((entries) => {
  for (const entry of entries) {
    const { width, height } = entry.contentRect;
    console.log(`Element resized: ${width}x${height}`);
  }
});

observer.observe(document.querySelector('#container'));
```

## Mutation Observer (replaces DOM change libraries)

```typescript
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    if (mutation.type === 'childList') {
      console.log('Children changed');
    }
  });
});

observer.observe(document.querySelector('#dynamic'), {
  childList: true,
  subtree: true,
});
```

## Broadcast Channel (replaces cross-tab libraries)

```typescript
// Tab 1: Send message
const channel = new BroadcastChannel('app-channel');
channel.postMessage({ type: 'logout' });

// Tab 2: Receive message
const channel = new BroadcastChannel('app-channel');
channel.onmessage = (event) => {
  if (event.data.type === 'logout') {
    window.location.href = '/login';
  }
};
```

## Crypto API (replaces crypto libraries)

```typescript
// UUID generation (replaces uuid package)
const id = crypto.randomUUID();

// Random values
const array = new Uint32Array(10);
crypto.getRandomValues(array);

// Hashing (SHA-256)
async function sha256(message: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hash))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}
```
