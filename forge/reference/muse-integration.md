# Forge Muse Integration

> Purpose: hand functional prototypes to Muse for token-driven polish without losing implementation context.

## Contents

- `MUSE_HANDOFF`
- Style migration guide
- Common conversion patterns

Design handoff templates for polish and styling.

---

## Design Handoff Template

```markdown
## MUSE_HANDOFF

### Task: Design Polish for Prototype
- Component: `components/prototypes/[name].tsx`
- Current status: Functional but unstyled

### Current Styling
- Using inline styles for rapid prototyping
- No design tokens applied
- Basic layout only

### Design Requirements
1. **Color Scheme**
   - Apply brand colors
   - Ensure proper contrast

2. **Typography**
   - Apply font family from design system
   - Set proper heading hierarchy
   - Adjust line heights

3. **Spacing**
   - Apply consistent margins/padding
   - Use design system spacing scale

4. **Components**
   - Style buttons consistently
   - Style form inputs
   - Add hover/focus states

5. **Responsive**
   - Mobile-first approach
   - Breakpoints for tablet/desktop

### Visual Reference
[Link to Figma/design mockup if available]

### Priority Elements
1. [Most important element]
2. [Second priority]
3. [Third priority]
```

---

## Style Migration Guide

### Before (Prototype - Inline Styles)

```tsx
<button style={{
  padding: '8px 16px',
  background: '#3498db',
  color: 'white',
  border: 'none',
  borderRadius: 4,
  cursor: 'pointer',
}}>
  Submit
</button>
```

### After (Production - Tailwind)

```tsx
<button className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark transition-colors">
  Submit
</button>
```

### After (Production - CSS Modules)

```tsx
import styles from './Button.module.css';
<button className={styles.primary}>Submit</button>
```

### After (Production - styled-components)

```tsx
const PrimaryButton = styled.button`
  ${buttonBase}
  background: var(--color-primary);
  &:hover { background: var(--color-primary-dark); }
`;
<PrimaryButton>Submit</PrimaryButton>
```

---

## Common Style Patterns to Convert

| Prototype Pattern | Production Approach |
|-------------------|---------------------|
| `style={{ marginBottom: 16 }}` | `className="mb-4"` or spacing tokens |
| `style={{ color: '#666' }}` | `className="text-gray-500"` or color tokens |
| `style={{ display: 'flex' }}` | `className="flex"` |
| `style={{ border: '1px solid #ccc' }}` | `className="border border-gray-300"` |
| Inline conditional styles | CSS class toggles or CSS-in-JS |
