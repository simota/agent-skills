# Motion Tokens

Purpose: Use this file when you need a tokenized motion system, semantic aliases, or Muse-aligned motion distances.

## Contents
- Duration and easing tokens
- Semantic aliases
- Reduced-motion overrides
- Muse alignment
- Tailwind mapping

## Core Tokens

```css
:root {
  --duration-instant: 50ms;
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 400ms;
  --duration-spinner: 1000ms;
  --duration-skeleton: 1500ms;

  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-soft: cubic-bezier(0.25, 0.1, 0.25, 1);
}
```

## Semantic Aliases

| Alias | Token Mapping | Use For |
|-------|---------------|---------|
| `--motion-micro` | `--duration-instant` + `--ease-out` | Press and tiny confirmation |
| `--motion-fast` | `--duration-fast` + `--ease-out` | Hover and quick feedback |
| `--motion-normal` | `--duration-normal` + `--ease-out` | Default transitions |
| `--motion-enter` | `--duration-slow` + `--ease-out` | Entry animations |
| `--motion-exit` | `--duration-normal` + `--ease-in` | Exit animations |
| `--motion-state` | `--duration-normal` + `--ease-in-out` | State changes |

## Reduced-Motion Override

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-instant: 0ms;
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --duration-slow: 0ms;
    --duration-slower: 0ms;
  }
}
```

## Muse Alignment

```css
:root {
  --motion-distance-sm: var(--space-2); /* 8px */
  --motion-distance-md: var(--space-4); /* 16px */
  --motion-distance-lg: var(--space-6); /* 24px */
}
```

## Tailwind Mapping

```js
module.exports = {
  theme: {
    extend: {
      transitionDuration: {
        instant: '50ms',
        fast: '100ms',
        normal: '200ms',
        slow: '300ms',
        slower: '400ms',
      },
      transitionTimingFunction: {
        out: 'cubic-bezier(0, 0, 0.2, 1)',
        in: 'cubic-bezier(0.4, 0, 1, 1)',
        'in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
    },
  },
};
```
