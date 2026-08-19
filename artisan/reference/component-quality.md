# Component Quality

Accessibility, error/loading states, form validation, styling strategy, and component checklist.

---

## 1. Accessibility Patterns

### Semantic HTML First

```tsx
// DO: semantic elements
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/home">Home</a></li>
    <li><a href="/about" aria-current="page">About</a></li>
  </ul>
</nav>

// DON'T: divs for everything
<div class="nav">
  <div onclick="navigate('/home')">Home</div>
</div>
```

### ARIA Attributes

```tsx
// Live regions for dynamic content
<div aria-live="polite" aria-atomic="true">{statusMessage}</div>

// Dialog/Modal
<dialog role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm Action</h2>
</dialog>

// Toggle button
<button aria-pressed={isActive} aria-label="Toggle dark mode">
  {isActive ? 'On' : 'Off'}
</button>
```

### Keyboard Navigation

```tsx
function useKeyboardNavigation(items: HTMLElement[]) {
  const handleKeyDown = (e: KeyboardEvent, currentIndex: number) => {
    let nextIndex: number;
    switch (e.key) {
      case 'ArrowDown': case 'ArrowRight':
        e.preventDefault();
        nextIndex = (currentIndex + 1) % items.length;
        items[nextIndex]?.focus();
        break;
      case 'ArrowUp': case 'ArrowLeft':
        e.preventDefault();
        nextIndex = (currentIndex - 1 + items.length) % items.length;
        items[nextIndex]?.focus();
        break;
      case 'Home': e.preventDefault(); items[0]?.focus(); break;
      case 'End': e.preventDefault(); items[items.length - 1]?.focus(); break;
    }
  };
  return { handleKeyDown };
}
```

### Focus Trap

```tsx
function useFocusTrap(containerRef: React.RefObject<HTMLElement>) {
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const focusable = container.querySelectorAll(
      'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusable[0] as HTMLElement;
    const last = focusable[focusable.length - 1] as HTMLElement;
    first?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last?.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first?.focus(); }
    };
    container.addEventListener('keydown', handleKeyDown);
    return () => container.removeEventListener('keydown', handleKeyDown);
  }, [containerRef]);
}
```

### WCAG 2.2 Requirements (October 2023)

| Criterion | Level | Requirement | Implementation |
|-----------|-------|-------------|----------------|
| 2.4.11 Focus Not Obscured (Minimum) | AA | Focused element not fully hidden by sticky headers/footers | `scroll-padding-top` for sticky headers; z-index management |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | Focused element not even partially hidden | Scroll-into-view logic on focus |
| 2.5.7 Dragging Movements | AA | Any drag operation must have a single-pointer alternative | Add click/tap alternative for all drag interactions |
| 2.5.8 Target Size (Minimum) | AA | Interactive targets ≥ 24×24 CSS px (or ≥ 24px spacing) | `min-w-6 min-h-6` or `gap-2` between small targets |
| 3.3.7 Redundant Entry | A | Don't re-ask info already provided in same session | Pre-fill from earlier steps; use session storage |
| 3.3.8 Accessible Authentication (Minimum) | AA | No cognitive function test for auth (unless alternative exists) | Support paste in password fields; allow password managers |
| 3.3.9 Accessible Authentication (Enhanced) | AAA | No cognitive function test at all for auth | Passkeys, WebAuthn, or copy-paste friendly flows |

```tsx
// Target size: minimum 24×24px (WCAG 2.5.8 AA), recommended 44×44px
<button className="min-w-[44px] min-h-[44px] p-2">
  <TrashIcon className="w-5 h-5" />
</button>

// Focus not obscured: scroll-padding for sticky headers (WCAG 2.4.11)
// In global CSS:
// html { scroll-padding-top: 80px; } /* height of sticky header */
```

---

## 2. Error State Patterns

### Error Boundary with Recovery

```tsx
function ErrorFallback({ error, resetErrorBoundary }: {
  error: Error; resetErrorBoundary: () => void;
}) {
  return (
    <div role="alert" className="error-container">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

<ErrorBoundary FallbackComponent={ErrorFallback} onReset={() => queryClient.clear()}>
  <MyComponent />
</ErrorBoundary>
```

### Inline Error Display

```tsx
function FieldError({ error, fieldId }: { error?: string; fieldId: string }) {
  if (!error) return null;
  return (
    <p id={`${fieldId}-error`} role="alert" className="text-sm text-destructive mt-1">
      {error}
    </p>
  );
}

<input id="email" aria-invalid={!!errors.email}
  aria-describedby={errors.email ? 'email-error' : undefined} />
<FieldError error={errors.email} fieldId="email" />
```

---

## 3. Loading State Patterns

### Skeleton Loading

```tsx
function Skeleton({ width, height, className }: {
  width?: string; height?: string; className?: string;
}) {
  return (
    <div className={cn("animate-pulse rounded-md bg-muted", className)}
      style={{ width, height }} aria-hidden="true" />
  );
}

function CardSkeleton() {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading content">
      <Skeleton height="200px" />
      <Skeleton height="20px" width="80%" />
      <Skeleton height="16px" width="60%" />
    </div>
  );
}
```

### Async State Component

```tsx
function AsyncContent<T>({ data, isLoading, error, skeleton, empty, children }: {
  data: T | null | undefined; isLoading: boolean; error: Error | null;
  skeleton: React.ReactNode; empty?: React.ReactNode;
  children: (data: T) => React.ReactNode;
}) {
  if (isLoading) return <>{skeleton}</>;
  if (error) return <ErrorDisplay error={error} />;
  if (!data || (Array.isArray(data) && data.length === 0)) return <>{empty ?? <EmptyState />}</>;
  return <>{children(data)}</>;
}
```

---

## 4. Form Validation

```tsx
function FormField({ label, name, type = 'text', required, error, helpText }: {
  label: string; name: string; type?: string;
  required?: boolean; error?: string; helpText?: string;
}) {
  const inputId = `field-${name}`;
  const errorId = `${inputId}-error`;
  const helpId = `${inputId}-help`;
  const describedBy = [error ? errorId : null, helpText ? helpId : null]
    .filter(Boolean).join(' ') || undefined;

  return (
    <div className="form-field">
      <label htmlFor={inputId}>
        {label}
        {required && <span aria-hidden="true"> *</span>}
        {required && <span className="sr-only"> (required)</span>}
      </label>
      <input id={inputId} name={name} type={type} required={required}
        aria-invalid={!!error} aria-describedby={describedBy} />
      {helpText && <p id={helpId} className="text-sm text-muted">{helpText}</p>}
      {error && <p id={errorId} role="alert" className="text-sm text-destructive">{error}</p>}
    </div>
  );
}
```

---

## 5. Styling Strategy

| Approach | Best For | Trade-offs |
|----------|----------|------------|
| **Tailwind CSS v4** | Rapid development, utility-first | CSS-first config (`@theme`), fast builds (100x+), Container Queries built-in |
| **CSS Modules** | Component isolation | True scoping, familiar CSS; more files |
| **Zero-runtime CSS-in-JS** | Type-safe styles, no runtime cost | Vanilla Extract (stable), StyleX (Meta), Panda CSS |
| **Vanilla CSS** | Simple projects | No dependencies; manual organization |

### Tailwind CSS v4 Changes

| v3 | v4 | Notes |
|----|-----|-------|
| `tailwind.config.js` | `@theme` in CSS | CSS-first configuration |
| `@apply` in config | `@utility` directive | Custom utilities in CSS |
| `shadow-sm` | `shadow-xs` | Size scale shifted down |
| `rounded-sm` | `rounded-xs` | Size scale shifted down |
| `ring` | `ring-3` | Explicit width required |
| `@screen md` | `@media (width >= 768px)` | Standard CSS media queries |

```tsx
// cn() utility pattern (unchanged)
import { cn } from '@/lib/utils';

const Button = ({ variant = 'primary', size = 'md', className, children }: ButtonProps) => (
  <button className={cn(
    'inline-flex items-center justify-center rounded-md font-medium transition-colors',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
    'disabled:pointer-events-none disabled:opacity-50',
    { 'bg-primary text-primary-foreground hover:bg-primary/90': variant === 'primary',
      'bg-secondary text-secondary-foreground hover:bg-secondary/80': variant === 'secondary' },
    { 'h-8 px-3 text-sm': size === 'sm', 'h-10 px-4 text-base': size === 'md',
      'h-12 px-6 text-lg': size === 'lg' },
    className
  )}>{children}</button>
);
```

---

## 5b. Modern CSS Features (2025-2026)

### CSS `@scope` — Native Style Scoping

```css
@scope (.card) to (.card__content) {
  h2 { font-size: 1.25rem; }
  p { color: var(--text-secondary); }
}
```

- Replaces CSS Modules / CSS-in-JS for component-level scoping.
- `to` canon creates a "donut scope" — styles apply within `.card` but stop at `.card__content`.
- **Rule**: Prefer `@scope` for new components when project targets modern browsers.

### Anchor Positioning

```css
.tooltip {
  position: fixed;
  position-anchor: --trigger;
  position-area: top;
  position-try-fallbacks: bottom, right, left;
}

.trigger {
  anchor-name: --trigger;
}
```

- Declarative tooltip/dropdown/popover placement — no JS positioning libraries.
- Combine with **Popover API** for complete accessible overlay patterns.

### Popover API

```html
<button popovertarget="menu">Open</button>
<div id="menu" popover>
  <!-- Top layer, light dismiss, focus management built-in -->
</div>
```

- Replaces custom modal/dropdown implementations with native behavior.
- **Rule**: Use `popover` for non-modal overlays. Use `<dialog>` for modal overlays.

### Text Wrapping

```css
h1, h2, h3 { text-wrap: balance; }  /* Balanced line lengths — max 6 lines */
p { text-wrap: pretty; }            /* Prevents orphaned last words */
```

### CSS `if()` (Emerging)

```css
.component {
  gap: if(style(--density: compact): 4px; else: 8px);
}
```

- Chrome Canary only. Always provide `@supports` fallback.

### Grid Lanes (CSS Masonry)

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-template-rows: masonry;
}
```

- WebKit implementation in progress. Use JS fallback (Masonry.js) with `@supports` check.

### `sibling-index()` / `sibling-count()`

```css
.item {
  animation-delay: calc(sibling-index() * 50ms);  /* Staggered entrance */
  opacity: calc(1 - (sibling-index() / sibling-count()) * 0.3);  /* Fade gradient */
}
```

---

## 5c. Production UI Patterns (2025-2026)

### Split-View / Three-Panel Layout

The dominant SaaS navigation pattern (Linear, Notion, Slack, VS Code):

```css
.layout {
  display: grid;
  grid-template-columns: 240px minmax(300px, 1fr) minmax(400px, 2fr);
  height: 100dvh;
}
```

**Rule**: Use `react-resizable-panels` for drag-to-resize. Persist widths in localStorage. Collapse sidebar to 56px icons-only mode on narrow viewports. Keyboard shortcut `[`/`]` to toggle panels.

### Inline Editing (Click-to-Edit)

```tsx
function InlineEdit({ value, onSave }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);
  if (!editing) return (
    <span onClick={() => setEditing(true)} className="cursor-pointer hover:bg-muted px-1 rounded">{value}</span>
  );
  return (
    <input autoFocus value={draft} onChange={e => setDraft(e.target.value)}
      onBlur={() => { onSave(draft); setEditing(false); }}
      onKeyDown={e => {
        if (e.key === 'Enter') { onSave(draft); setEditing(false); }
        if (e.key === 'Escape') { setDraft(value); setEditing(false); }
      }} />
  );
}
```

**Rule**: Show hover indicator (background change). Use `contentEditable` for rich text. Validate on blur. Products: Notion, Jira, Asana, Airtable.

### Optimistic UI (React 19)

```tsx
const [optimisticItems, addOptimistic] = useOptimistic(items,
  (state, newItem) => [...state, { ...newItem, pending: true }]
);
```

**Rule**: Show subtle visual distinction for pending items (lower opacity). Always implement rollback. Only for high-confidence ops (>99% success). Never for payments or destructive actions.

### Drag-and-Drop (2025 Libraries)

| Library | Best For | Size |
|---------|----------|------|
| `@dnd-kit/react` | Flexible, accessible, customizable | ~10KB |
| `pragmatic-drag-and-drop` (Atlassian) | Headless, HTML5 DnD API | ~5KB |
| `@hello-pangea/dnd` | Drop-in react-beautiful-dnd replacement | ~30KB |

**Rule**: Always support keyboard DnD (Space to pick up, arrows to move). Show clear drop indicators. Animate shifting items.

### Context Menu (Right-Click)

```tsx
<ContextMenu>
  <ContextMenuTrigger>{children}</ContextMenuTrigger>
  <ContextMenuContent>
    <ContextMenuItem>Copy <ContextMenuShortcut>⌘C</ContextMenuShortcut></ContextMenuItem>
    <ContextMenuSeparator />
    <ContextMenuItem className="text-destructive">Delete</ContextMenuItem>
  </ContextMenuContent>
</ContextMenu>
```

**Rule**: Use Radix `ContextMenu` or shadcn/ui. Group with separators. Show shortcuts. Destructive actions last, in red. ≤10 items per level.

### Multi-Select & Bulk Actions

```tsx
function handleClick(index, event) {
  if (event.shiftKey && lastSelected !== null) {
    // Shift+click selects range
    const [min, max] = [Math.min(lastSelected, index), Math.max(lastSelected, index)];
    setSelected(prev => { const next = new Set(prev); for (let i = min; i <= max; i++) next.add(i); return next; });
  } else {
    // Toggle individual
    setSelected(prev => { const next = new Set(prev); next.has(index) ? next.delete(index) : next.add(index); return next; });
  }
}
```

**Rule**: Floating action bar with count ("3 selected") + bulk actions. Support "Select all". Confirm destructive bulk ops.

### AI Streaming Text

```tsx
import { useChat } from 'ai/react'; // Vercel AI SDK
const { messages, input, handleInputChange, handleSubmit } = useChat();
```

**Rule**: Show typing indicator for first token. Render at consistent ~200 chars/sec regardless of chunk size. Allow scroll during streaming. Support stop generation. Products: ChatGPT, Claude, Gemini.

### AI Prompt Input

```tsx
<div className="border rounded-2xl p-3 flex flex-col gap-2">
  <div className="flex flex-wrap gap-1">
    {attachments.map(a => <Chip key={a.id} label={a.name} onRemove={() => remove(a.id)} />)}
  </div>
  <textarea rows={1} className="resize-none"
    onInput={e => { e.target.style.height = 'auto'; e.target.style.height = e.target.scrollHeight + 'px'; }}
    style={{ maxHeight: '200px' }} />
  <div className="flex justify-between">
    <div className="flex gap-2"><IconButton icon={<Paperclip />} /><IconButton icon={<Image />} /></div>
    <button className="bg-primary rounded-full p-2"><ArrowUp /></button>
  </div>
</div>
```

**Rule**: Auto-expand to max height then scroll. Submit with Enter, newline with Shift+Enter. Support paste for images. Products: ChatGPT, Claude.

### AI Response Actions

```tsx
<div className="group relative">
  <div className="prose">{content}</div>
  <div className="opacity-0 group-hover:opacity-100 flex gap-1 mt-2">
    <IconButton icon={<Copy />} tooltip="Copy" />
    <IconButton icon={<RefreshCw />} tooltip="Regenerate" />
    <IconButton icon={<Edit />} tooltip="Edit" />
    <IconButton icon={<GitBranch />} tooltip="Branch" />
    <IconButton icon={<ThumbsUp />} tooltip="Good" />
  </div>
</div>
```

**Rule**: Copy shows "Copied!" briefly. Regenerate creates branch, not overwrite. Show loading during regeneration.

### Content Preview on Hover

```tsx
<HoverCard openDelay={300} closeDelay={100}>
  <HoverCardTrigger asChild><a href={url}>{text}</a></HoverCardTrigger>
  <HoverCardContent className="w-80 p-4 rounded-lg shadow-lg">
    <img src={ogImage} /><h3>{title}</h3><p>{desc}</p>
  </HoverCardContent>
</HoverCard>
```

**Rule**: 300ms open delay, 100ms close grace period. Fetch OG metadata server-side, cache aggressively. Products: Wikipedia, GitHub, Slack, Notion.

### Key Library Map (2025-2026)

| Category | Library |
|----------|---------|
| Command Palette | `cmdk` |
| Drag & Drop | `@dnd-kit/react` |
| Context Menu | Radix `ContextMenu` |
| Hover Cards | Radix `HoverCard` |
| Bottom Sheet (web) | `vaul` |
| AI Chat | Vercel AI SDK (`ai`) |
| Virtual Lists | `@tanstack/virtual` |
| Resizable Panels | `react-resizable-panels` |
| Toast | `sonner` |
| Forms | React Hook Form + Zod |

---

## 5d. Visual UI Pattern Knowledge Base

### Bento Grid Layout

Asymmetric grid inspired by Japanese bento boxes. Apple product pages popularized it.

```css
.bento {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  grid-template-areas:
    "hero  side1 side1"
    "hero  side2 side3";
  gap: 1rem;
}
@media (max-width: 768px) {
  .bento { grid-template-columns: 1fr; grid-template-areas: "hero" "side1" "side2" "side3"; }
}
```

**Rule**: Bento grids are for feature showcases, dashboards, and portfolios. Not for content-heavy pages. Visual hierarchy comes from cell size — largest cell = highest priority.

### Glassmorphism → Liquid Glass

Evolution: Glassmorphism (2020) → Acrylic/Fluent (Microsoft) → **Liquid Glass** (Apple WWDC25, physics-based refraction):

```css
/* Glassmorphism base */
.glass { background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 16px; }
```

**Rule**: `backdrop-filter: blur()` is Baseline (97% support). Keep blur 8-15px (GPU cost scales exponentially). Liquid Glass uses SVG `feDisplacementMap` for refraction — progressive enhancement only.

### Command Palette (⌘K Pattern)

Keyboard-driven universal search/action interface (VSCode, Linear, Slack, Notion):

```tsx
<Command>
  <Command.Input placeholder="Type a command or search..." />
  <Command.List>
    <Command.Group heading="Navigation">
      <Command.Item onSelect={() => navigate('/dashboard')}>Go to Dashboard</Command.Item>
    </Command.Group>
  </Command.List>
</Command>
```

**Rule**: Use `cmdk` (pacocoursey) or shadcn/ui `<Command />`. Combine fuzzy search + section grouping + keyboard-first navigation. Benefits both power users (O(1) access) and beginners (discoverable).

### Notification Hierarchy

| Level | Component | Auto-dismiss | Action | Use For |
|-------|-----------|-------------|--------|---------|
| Ambient | Status bar | No | View | Ongoing state (uploading, syncing) |
| Informational | Toast | 3-5s | None | Success confirmation |
| Actionable | Snackbar | 5-10s | Undo/Retry | Reversible actions |
| Critical | Dialog/Banner | No | Acknowledge | Errors, destructive confirmations |

**Rule**: `role="status"` + `aria-live="polite"` for toast/snackbar. Never stack >3 notifications. Error toasts: never auto-dismiss.

### Claymorphism

Soft 3D aesthetic using dual inner shadows:

```css
.clay { background: #f0e6ff; border-radius: 24px; box-shadow: inset 4px 4px 6px rgba(255,255,255,0.6), inset -4px -4px 6px rgba(130,100,180,0.25), 8px 8px 20px rgba(130,100,180,0.3); }
```

**Rule**: Suitable for playful/educational contexts. Avoid for data-heavy or professional tools (contrast issues). Always verify WCAG contrast.

---

## 6. Layout Restraint Rules

When building page-level components or landing pages, enforce these composition constraints to avoid generic AI-generated layouts.

### Card Usage

- **Do NOT default to card grids** for features, benefits, or static content
- Cards are for **interactive, actionable, comparable items** only (products, projects, settings groups)
- If content is static text, use sections with spacing and typography hierarchy instead

### Section Purpose

- **1 section = 1 purpose** — if a section serves two jobs, split it
- Every `<section>` should have a nameable purpose (e.g., "hero", "social-proof", "features", "final-cta")
- Use `data-purpose` attribute for auditability

```tsx
// DO: Named purpose, no unnecessary card wrapper
<section data-purpose="features" className="py-16 px-6">
  <div className="max-w-5xl mx-auto space-y-12">
    <h2>Features that matter</h2>
    {/* Feature descriptions as text sections, NOT cards */}
  </div>
</section>

// DON'T: Card grid default
<section className="py-16 px-6">
  <div className="grid grid-cols-3 gap-6">
    <div className="rounded-lg border p-6">Feature 1</div>
    <div className="rounded-lg border p-6">Feature 2</div>
    <div className="rounded-lg border p-6">Feature 3</div>
  </div>
</section>
```

### Layout Anti-Patterns to Reject

| Pattern | Code Signal | Fix |
|---------|------------|-----|
| Card grid in hero | `grid grid-cols-3` at page top | Single hero composition |
| Pill cluster | `flex flex-wrap gap-2` with short text | Categorized list or text group |
| Stat strip | 3-4 sibling `<div>` with large numbers | Stats in narrative context |
| Icon row | `grid grid-cols-4` with icon + text | Feature sections with descriptions |

→ Full patterns: `reference/ai-frontend-patterns.md`

---

## 7. Component Checklist

### Functionality
- [ ] All props typed with TypeScript
- [ ] Sensible default props
- [ ] Edge cases handled (empty, loading, error states)
- [ ] Form validation with clear feedback

### Accessibility
- [ ] Semantic HTML elements
- [ ] ARIA attributes where needed
- [ ] Keyboard navigation works
- [ ] Focus management correct
- [ ] Color contrast meets WCAG AA
- [ ] Touch targets ≥ 24×24px (WCAG 2.5.8)
- [ ] Focus not obscured by sticky elements (WCAG 2.4.11)
- [ ] Drag operations have single-pointer alternative (WCAG 2.5.7)
- [ ] Auth flows allow paste / password managers (WCAG 3.3.8)

### Performance
- [ ] No unnecessary re-renders
- [ ] Large lists virtualized
- [ ] Images optimized (next/image, lazy loading)
- [ ] Code splitting for large components

### Testing
- [ ] Testable in isolation
- [ ] Key interactions have test coverage
- [ ] Accessibility tests pass

### Code Quality
- [ ] No `any` types
- [ ] Consistent naming conventions
- [ ] Single responsibility principle

**Source:** [WCAG 2.2 W3C Recommendation](https://www.w3.org/TR/WCAG22/) · [WCAG 2.2 New Success Criteria](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) · [Tailwind CSS v4 Upgrade Guide](https://tailwindcss.com/docs/upgrade-guide) · [ARIA APG Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/) · [Zod v4 Release Notes](https://zod.dev/v4) · [TanStack Form v1 Announcement](https://tanstack.com/blog/announcing-tanstack-form-v1)


---

## Per-Recipe Behavior Notes and VERIFY Gates (SKILL.md excerpt)

Each `**VERIFY**:` is the recipe-specific gate **in addition to** Artisan's universal discipline (TypeScript strict no `any`, error boundary + loading/error/empty states, a11y built-in, semantic HTML, ≤50 lines per change, INP < 200ms target).
- `component`: Single component implementation. Always include type safety, a11y, and error/loading states. Target <50 lines. **VERIFY**: TS strict with zero `any` (`unknown` + narrow); error/loading/empty states all handled; a11y wired (ARIA + keyboard + WCAG 2.2 target ≥24×24px); semantic HTML; testable in isolation; no manual `memo`/`useMemo`/`useCallback` when React Compiler is on.
- `state`: Classify state (Remote/URL/Local/Shared) during DESIGN, then select the optimal library. **VERIFY**: state explicitly classified (Remote/URL/Local/Shared) before library choice; state lives close to its usage; zero direct mutation; library-choice / new-dependency gated Ask First; primitives map to the signals model (atomic get/set, derived, effects) for migration safety.
- `form`: RHF + Zod v4 validation (or TanStack Form v1 for cross-framework/type-safe paths). Include error display, submission state, and accessibility. **VERIFY**: validation via RHF+Zod v4 (or TanStack Form v1); accessible error display (associated to fields, announced); submission/pending state shown; `useFormStatus` placed in a **child** of the `<form>` (never the same component — else `pending` stays false); errors user-friendly.
- `fetch`: TanStack Query v5 or SWR. Design caching strategy and error/loading states. **VERIFY**: data fetched via TanStack Query v5 / SWR / Server Components / React 19 `use()` — NEVER `useEffect` fetch (waterfalls + races); caching strategy defined; loading/error/empty states handled; no client-side storage of sensitive data.
- `rsc`: Lock Server/Client boundaries during DESIGN. Consider selective hydration and streaming. **VERIFY**: Server/Client boundary locked at DESIGN; `"use client"` only on interactive leaves (never wrapper/layout); React pinned to a CVE-2025-55182-patched version (19.0.1+/19.1.2+/19.2.1+, Next.js 15.1.4+) before shipping Server Actions; streaming / selective hydration considered.
- `a11y`: Tactical WCAG 2.2 AA hardening of an Artisan-owned component or page — wire ARIA roles/labels, keyboard paths, focus management, and screen reader affordances. Verify target size (≥24×24px), focus appearance, and dragging alternatives. Scope is a single component/page; route to `Palette` for product-level usability/interaction redesign, and route to `Canon` for repo-wide WCAG gap audits. **VERIFY**: ARIA roles/labels + full keyboard path + focus management + SR affordances all present; WCAG 2.2 AA new criteria checked (target ≥24×24px, focus appearance, dragging alternative); scope held to one component/page (product redesign → Palette, repo-wide audit → Canon).
- `i18n`: Component-level i18n wiring inside a production frontend file — extract hardcoded strings to `t()`, use ICU MessageFormat for plurals/selects, apply `Intl.DateTimeFormat`/`NumberFormat` for locale-aware formatting, and switch physical properties to logical ones (`margin-inline-start`, `text-align: start`) for RTL safety. Stop at single-component scope; hand off to `Polyglot` for full i18n/l10n specialist work (extraction tooling, locale pipelines, translator workflow, ICU message catalogs at repo scale). **VERIFY**: zero hardcoded user-facing strings (all via `t()`); plurals/selects use ICU MessageFormat (not string concat); dates/numbers/currency via `Intl`; physical L/R properties switched to logical (RTL-safe); scope held to one component (repo-scale → Polyglot).
- `perf`: Frontend-component tuning inside a single component/page — apply memoization only when React Compiler is off or the compiler opts out, virtualize lists > ~100 rows with TanStack Virtual or react-window, split non-critical chunks with `next/dynamic` or `React.lazy`, and audit the route's bundle size. Measure INP/LCP before and after. Scope is one component or page; hand off to `Bolt` for cross-cutting frontend+backend performance work (rendering pipeline, server response, DB-backed waterfalls). **VERIFY**: INP/LCP measured before AND after (improvement shown, no regression); memoization added only when Compiler off / opts-out; lists >~100 rows virtualized; non-critical chunks dynamically imported; route bundle audited; scope held to one component/page (cross-cutting → Bolt).

