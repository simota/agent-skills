# Forge UI Component Templates

> Purpose: provide minimal starter templates for the most common prototype UI shapes.

## Contents

### Quick-Start Visual Patterns

**Bento Grid** — Asymmetric grid for feature showcases and dashboards:
```css
.bento { display: grid; grid-template-columns: 2fr 1fr 1fr; grid-template-areas: "hero side1 side1" "hero side2 side3"; gap: 1rem; }
```

**Glassmorphism Card** — Frosted glass overlay:
```css
.glass { background: rgba(255,255,255,0.15); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.2); border-radius: 16px; }
```

**Claymorphism Card** — Soft 3D for playful/educational UI:
```css
.clay { background: #f0e6ff; border-radius: 24px; box-shadow: inset 4px 4px 6px rgba(255,255,255,0.6), inset -4px -4px 6px rgba(130,100,180,0.25), 8px 8px 20px rgba(130,100,180,0.3); }
```

**Skeleton Shimmer** — Content-aware loading:
```css
.skeleton { background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%); background-size: 200% 100%; animation: shimmer 1.8s ease-in-out infinite; }
```

**Magnetic Button** — Cursor-attracted interaction:
```css
.magnetic-wrapper { padding: 40px; display: inline-block; }
.magnetic-wrapper:hover .btn { transform: translate(var(--x,0), var(--y,0)); transition: transform 0.3s cubic-bezier(0.33,1,0.68,1); }
```

- Basic form
- List with search and pagination
- Modal / dialog
- Card layout
- Async content states

Rapid prototyping UI templates for common patterns.

---

## Basic Form Component

```tsx
// components/prototypes/ContactForm.tsx
import { useState, FormEvent } from 'react';

interface FormData {
  name: string;
  email: string;
  message: string;
}

const INITIAL_STATE: FormData = {
  name: '',
  email: '',
  message: '',
};

// ...
```

---

## List with Search and Pagination

```tsx
// components/prototypes/UserList.tsx
import { useState, useMemo } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

// Mock data - replace with API call later
const MOCK_USERS: User[] = [
  { id: '1', name: 'Alice Johnson', email: 'alice@example.com', role: 'Admin' },
  { id: '2', name: 'Bob Smith', email: 'bob@example.com', role: 'User' },
  { id: '3', name: 'Carol Williams', email: 'carol@example.com', role: 'User' },
// ...
```

---

## Modal/Dialog Component

```tsx
// components/prototypes/Modal.tsx
import { ReactNode, useEffect } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
// ...
```

---

## Card Layout

```tsx
// components/prototypes/ProductCard.tsx
interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
  description: string;
}

const MOCK_PRODUCTS: Product[] = [
  { id: '1', name: 'Wireless Headphones', price: 99.99, image: 'https://via.placeholder.com/200', description: 'High-quality wireless headphones' },
  { id: '2', name: 'Smart Watch', price: 199.99, image: 'https://via.placeholder.com/200', description: 'Feature-rich smart watch' },
  { id: '3', name: 'Laptop Stand', price: 49.99, image: 'https://via.placeholder.com/200', description: 'Ergonomic laptop stand' },
];

// ...
```

---

## Composition-Aware Page Template

Use this template instead of the default card layout when prototyping landing pages or marketing sites.

```tsx
// components/prototypes/LandingPage.tsx
interface LandingPageProps {
  hero: {
    headline: string;
    subline: string;
    ctaLabel: string;
    ctaHref: string;
    imageSrc: string;
    imageAlt: string;
  };
  sections: Array<{
    purpose: string;
    headline: string;
    content: React.ReactNode;
    background?: 'base' | 'raised';
  }>;
  finalCta: {
    headline: string;
    ctaLabel: string;
    ctaHref: string;
  };
}

// Structure: Hero → Support → Detail → Final CTA
// Each section has a named purpose
// No default card grids — use spacing and typography for hierarchy
```

### Card Usage Note

**Cards are NOT a layout tool.** In prototypes:
- Use cards only for interactive, actionable items (products, projects, settings)
- Do NOT wrap static features or benefits in cards
- Use spacing (`py-12` / `py-16`) and background color (`bg-gray-50`) for section separation
- Default to text sections with clear typography hierarchy

When a card grid seems like the answer, ask: "Is each item individually clickable or comparable?" If not, cards are wrong.

→ Full composition principles: `vision/reference/composition-principles.md`

---

## Loading and Error States

```tsx
// components/prototypes/AsyncContent.tsx
import { useState, useEffect, ReactNode } from 'react';

type Status = 'loading' | 'success' | 'error';

interface AsyncContentProps<T> {
  fetchFn: () => Promise<T>;
  children: (data: T) => ReactNode;
}

export function AsyncContent<T>({ fetchFn, children }: AsyncContentProps<T>) {
  const [status, setStatus] = useState<Status>('loading');
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string>('');

// ...
```
