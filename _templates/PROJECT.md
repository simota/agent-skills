# Project Knowledge Base

> This file contains shared knowledge that ALL agents should reference.
> Individual agent journals (`.agents/{agent}.md`) are for agent-specific learnings.
> This file is for cross-cutting project knowledge.

---

## Architecture Decisions

<!-- Key architectural choices that affect multiple agents -->

| Decision | Choice | Rationale | Date |
|----------|--------|-----------|------|
| State Management | (e.g., Zustand) | (why chosen) | YYYY-MM-DD |
| Styling | (e.g., Tailwind) | (why chosen) | YYYY-MM-DD |
| Testing | (e.g., Vitest) | (why chosen) | YYYY-MM-DD |

---

## Domain Glossary

<!-- Shared terminology to ensure consistent naming across agents -->

| Term | Definition | Notes |
|------|------------|-------|
| User | Authenticated account holder | Not "Customer" or "Member" |
| Visitor | Unauthenticated browser | Before signup/login |

---

## API & External Services

<!-- Rate limits, endpoints, known issues with external dependencies -->

| Service | Constraint | Notes |
|---------|------------|-------|
| (API name) | (rate limit, etc.) | (discovered by, date) |

---

## Known Gotchas

<!-- Cross-cutting issues that multiple agents should be aware of -->

- **Area**: Description of the gotcha
  - Discovered by: (Agent name)
  - Impact: (What breaks if ignored)

---

## Browser / Environment Support

<!-- Target environments that affect multiple agents -->

- **Browsers**: (e.g., Chrome 90+, Safari 14+, Firefox 88+)
- **Node.js**: (e.g., 18.x LTS)
- **Mobile**: (e.g., iOS 14+, Android 10+)

---

## Security Considerations

<!-- Security constraints that all agents must respect -->

- Authentication method: (e.g., JWT, Session)
- Sensitive data handling: (what to never log/expose)
- Required headers: (e.g., CSP, CORS policies)

---

## Performance Budgets

<!-- Constraints that Bolt and others should respect -->

| Metric | Budget | Current |
|--------|--------|---------|
| Bundle size (JS) | < 200KB | - |
| LCP | < 2.5s | - |
| FID | < 100ms | - |

---

## Activity Log

<!--
All agents MUST add an entry here after completing significant work.
Keep last 30 entries. Delete oldest when adding new.
Format: YYYY-MM-DD | Agent | Action | Files/Scope | Outcome
-->

| Date | Agent | Action | Scope | Outcome |
|------|-------|--------|-------|---------|
| YYYY-MM-DD | (Agent) | (What was done) | (Files affected) | (Result/Status) |

---

## Cross-Agent Discoveries

<!-- Important findings that affect multiple agents - keep last 10 entries -->

### YYYY-MM-DD - [Title]
- **Discovered by**: (Agent name)
- **Affects**: (List of agents impacted)
- **Summary**: (Brief description)

---

## Update Guidelines

**Every agent MUST update this file after completing work:**

1. **Activity Log** (REQUIRED): Add a row after every task completion
2. **Cross-Agent Discoveries**: Add when finding something that affects other agents
3. **Domain sections**: Update when discovering new constraints or decisions

| Section | When to Update | Primary Agents |
|---------|----------------|----------------|
| Activity Log | After every task | ALL |
| Architecture Decisions | New tech choices | Atlas, Horizon |
| Domain Glossary | New term definitions | Builder, Quill |
| API & External Services | New integrations, rate limits | Builder, Gear |
| Known Gotchas | Tricky issues discovered | Scout, Any |
| Security Considerations | Security-related changes | Sentinel |
| Performance Budgets | Metrics updates | Bolt, Growth |
| Cross-Agent Discoveries | Findings affecting multiple agents | Any |

Keep entries concise. This is a living document.
