# Output Formats Reference

## Quick Answer (for simple existence checks)

```markdown
## [Feature] - [EXISTS/NOT FOUND]

- **Location:** `src/auth/loginService.ts:42`
- **Confidence:** High
- **Notes:** [Brief context]
```

---

## Investigation Report (for flow/structure questions)

```markdown
## Lens Investigation Report

### Question
[Original question]

### Summary
[2-3 sentence answer]

### Findings

#### [Finding 1]
- **Location:** `file:line`
- **Description:** [What was found]
- **Confidence:** [High/Medium/Low]

#### [Finding 2]
...

### Flow / Structure
[Diagram or table]

### What I Didn't Find
- [Expected but absent elements]
- [Areas that need deeper investigation]

### Recommendations
- [Suggested next steps]
- [Related questions to explore]
```

---

## Onboarding Report (for "understand this repo" requests)

```markdown
## Codebase Overview: [Project Name]

### Purpose
[What this project does]

### Tech Stack
| Layer | Technology |
|-------|-----------|

### Architecture
```
[Layer/module diagram]
```

### Key Modules
| Module | Path | Responsibility |
|--------|------|---------------|

### Key Flows
| Flow | Entry Point | Description |
|------|------------|-------------|

### Conventions
| Convention | Example |
|-----------|---------|

### Getting Started
- [How to run]
- [How to test]
- [Key files to read first]
```
