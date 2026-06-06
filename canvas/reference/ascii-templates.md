# ASCII Diagram Templates

Purpose: Read this when the diagram must work in terminals, comments, diffs, or plain-text-only environments.

## Contents

- When to use ASCII
- Canonical templates
- Styling rules

## When To Use ASCII

- Terminal or chat output only
- Code comment or README snippet
- Accessibility fallback
- The user explicitly asks for plain text

## Flowchart

```text
+---------+      +----------+      +---------+
| Start   | ---> | Validate | ---> | Success |
+---------+      +----------+      +---------+
                      |
                      v
                 +---------+
                 | Failure |
                 +---------+
```

## Sequence

```text
User        API        DB
 |           |         |
 | Request   |         |
 |---------> |         |
 |           | Query   |
 |           |-------> |
 |           | Result  |
 |           |<------- |
 | Response  |         |
 |<--------- |         |
```

## State

```text
[idle] --> [loading] --> [success]
   ^            |
   |            v
   +-------- [error]
```

## Tree / Hierarchy

```text
App
|- Layout
|  |- Header
|  `- Main
`- Providers
   |- AuthProvider
   `- ThemeProvider
```

## Box / Context

```text
+----------------------+
| External Actor       |
+----------+-----------+
           |
           v
+----------+-----------+
| System Boundary      |
| - API                |
| - Worker             |
| - Database           |
+----------------------+
```

## Styling Rules

- Use one box style consistently.
- Keep arrow direction stable inside one diagram.
- Prefer short labels.
- Use indentation or whitespace to encode grouping.
