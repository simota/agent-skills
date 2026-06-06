# Echo Analysis Frameworks

Detailed workflow and analysis target definitions for Echo's advanced features.

---

## Persona Generation

### Generation Workflow

```
1. ANALYZE  - Analyze README, docs, src
2. EXTRACT  - Extract user types, goals, pain points
3. GENERATE - Generate personas following template
4. SAVE     - Save to .agents/personas/{service}/
```

### Auto-Suggestion

Auto-suggests generation when starting review without defined personas.

### Analysis Targets (User Persona)

| File | Extraction Target |
|------|-------------------|
| README.md | Target users, usage scenarios |
| docs/**/* | User guide target readers |
| src/**/user*, auth* | User models, role definitions |
| tests/**/* | Test scenarios → use cases |

### Analysis Targets (Internal Persona)

| File | Extraction Target |
|------|-------------------|
| CODEOWNERS | Team structure, responsibility areas |
| .github/workflows/* | CI/CD workflows |
| docs/CONTRIBUTING.md | Development flow |
| .vscode/**, .editorconfig | Development environment |
| docs/runbook*, docs/onboarding* | Operations/onboarding docs |

### Output Structure

Generated personas are saved to `.agents/personas/{service}/`:

```
.agents/personas/
└── ec-platform/
    ├── first-time-buyer.md      # User persona
    ├── power-shopper.md         # User persona
    ├── enterprise-admin.md      # User persona
    └── internal/
        ├── frontend-developer.md  # Internal persona
        └── ops-manager.md         # Internal persona
```

---

## Service-Specific Review

### Review Process

1. **LOAD** - Load personas from `.agents/personas/{service}/`
2. **SELECT** - Select review target flow and persona
3. **WALK** - Apply persona-specific Emotion Triggers
4. **SCORE** - Score in service-specific context
5. **REPORT** - Generate report based on Testing Focus

### Benefits Comparison

| Aspect | Standard Personas | Service-Specific Personas |
|--------|------------------|---------------------------|
| Accuracy | Generic | Reflects service-specific context |
| Triggers | General | Real user response patterns |
| Focus | Wide range | Concentrated on key flows |
| JTBD | Assumed | Based on code/documentation |

### Internal Persona Review Targets

| Target | Recommended Persona | Purpose |
|--------|---------------------|---------|
| Admin Panel | Ops Manager, CS Rep | Operations usability |
| Dev Tools/CI/CD | Frontend/Backend Dev | Developer experience (DX) |
| Documentation | New Engineer, PdM | Comprehensibility |
| Error Messages/Logs | QA Engineer, Ops | Debugging usefulness |
| API/SDK | Backend Developer | Interface design |

### Cross-Persona Analysis

Compare flows across multiple saved personas:

```markdown
| Step | First-Time | Power | Enterprise | Issue Type |
|------|------------|-------|------------|------------|
| 1    | +1         | +2    | +1         | Non-Issue  |
| 2    | -2         | +1    | -1         | Segment    |
| 3    | -3         | -2    | -3         | Universal  |
```

---

## Context-Aware Simulation

### Environmental Context Dimensions

| Dimension | Variables | Impact on UX |
|-----------|-----------|--------------|
| **Physical** | One-hand/two-hand, walking/sitting, lighting | Touch accuracy, screen visibility |
| **Temporal** | Rushed/relaxed, deadline pressure | Patience threshold, error tolerance |
| **Social** | Alone/public/meeting, being watched | Privacy awareness, embarrassment risk |
| **Cognitive** | Multitasking/focused, fatigue level | Information processing capacity |
| **Technical** | Connection speed, device capability | Performance expectations |
