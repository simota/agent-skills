# Daily Process Checklists

## 1. SURVEY - Map the Territory

### Dependency Analysis
- [ ] Are there "God Objects" or "God Files" (500+ lines) doing too much?
- [ ] Are there circular dependencies? (Module A → Module B → Module A)
- [ ] Is the project relying on "Deprecated" or "Abandoned" libraries?
- [ ] Are layer boundaries respected? (UI → App → Domain → Infra)

### Structural Integrity
- [ ] Does the folder structure reflect the domain (Features) or just technology (Components/Containers)?
- [ ] Is business logic leaking into the UI layer?
- [ ] Is the API layer tightly coupled to the database schema?

### Scalability Risks
- [ ] Is the current state management solution scalable?
- [ ] Are we fetching too much data due to poor schema design?
- [ ] Is the build pipeline becoming too slow/complex?

## 2. PLAN - Draw the Blueprint

- Draft an RFC (Request for Comments) or ADR
- Define the "Current State" vs "Desired State"
- List the "Pros/Cons" of the change
- Outline a "Migration Strategy" (How to get there without breaking everything)

## 3. VERIFY - Stress Test the Plan

- Does this add unnecessary complexity? (YAGNI check)
- Is this standard practice? (Least Surprise Principle)
- Can the team actually maintain this?

## 4. PRESENT - Roll Out the Map

Create a PR (Documentation only) with:
- Title: `docs(arch): RFC for [Architecture Change]`
- Description:
  - Proposal: High-level summary of the architectural change
  - Motivation: The pain point we are solving (Tech Debt/Scalability)
  - Plan: Step-by-step migration path
  - Trade-offs: What we gain vs what we lose (cost/complexity)
