# Horizon Code Standards

## Good Horizon Code

```typescript
// Modernizing - Using Native API instead of Library
// Before: import { format } from 'date-fns';
// After:
const formatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'full' });

// PoC Commenting
/**
 * @experiment Horizon PoC
 * Testing the new View Transitions API.
 * If this fails, fallback to CSS opacity.
 */
document.startViewTransition(() => updateDOM());
```

## Bad Horizon Code

```typescript
// Hype Driven - Installing a huge library just for one simple function
import { complexThing } from 'super-new-hype-lib';

// Bleeding Edge without guardrails
// Using a feature that only works in Chrome Canary
const x = new VeryExperimentalAPI();
```
