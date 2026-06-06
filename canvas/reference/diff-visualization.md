# Diff Visualization Reference

Purpose: Read this when you need to visualize what changed between two versions, commits, schemas, or architectures.

## Contents

- Commands
- Diff styles
- Color semantics
- Output rules
- Clarification triggers

## Commands

```text
/Canvas diff [file1] [file2]
/Canvas diff --before [commit]
/Canvas diff schema
/Canvas diff architecture
/Canvas history [diagram-name]
```

## Diff Styles

| Style | Use When |
|-------|----------|
| Side-by-Side | Compare two snapshots directly |
| Overlay | Show additions/removals in one picture |
| Timeline | Show evolution across several revisions |

## Color Semantics

| Meaning | Recommended Color |
|---------|-------------------|
| Added | Green / teal |
| Removed | Coral / red |
| Modified | Yellow / orange |
| Unchanged | Gray |

## Output Rules

- State the baseline and target versions.
- Tell the viewer what changed first.
- Keep one diff diagram focused on one change domain.
- Save to the diagram library only when the diff is reusable.

### ON_DIFF_SCOPE

- File-level diff
- Schema diff
- Architecture diff
- Multi-step timeline

### ON_DIFF_FORMAT

- Side-by-side
- Overlay
- Timeline

### ON_DIFF_SAVE

- Save diff to library
- Show once only
