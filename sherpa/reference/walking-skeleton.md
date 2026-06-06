# Walking Skeleton Reference

Purpose: Design the thinnest end-to-end slice of a new system — Alistair Cockburn's Walking Skeleton. Exercises every architectural layer (UI → API → DB → auth → deploy) with placeholder logic before investing in any single layer. Validates integration before broadening features.

## Scope Boundary

- **sherpa `walking-skeleton`**: Thinnest end-to-end slice design (this document).
- **sherpa `atomic` (elsewhere)**: ≤15-minute step breakdown. The walking skeleton is typically the first 3-10 atomic steps.
- **sherpa `vertical-slice` (elsewhere)**: End-to-end feature slices. Walking skeleton is the *first* vertical slice; subsequent slices broaden it.
- **forge (elsewhere)**: Prototype / spike. Walking skeleton ships to production on Day 1; a forge prototype does not.

## Definition (Cockburn)

> "A Walking Skeleton is a tiny implementation of the system that performs a small end-to-end function. It need not use the final architecture, but it should link together the main architectural components. The architecture and the functionality can then evolve in parallel."
> — Alistair Cockburn, *Agile Software Development: The Cooperative Game*

Key properties:
1. **Thinnest possible** — one happy path, no edge cases.
2. **End-to-end** — every layer from user input to persistent state.
3. **Production-deployed** — lives on the real infrastructure on Day 1, not in a branch.
4. **Testable** — has at least one automated test covering the full path.

## Layer-Coverage Checklist

A walking skeleton must touch each layer. Missing any layer means integration risk is still ahead.

| Layer | Walking-skeleton level |
|-------|-----------------------|
| UI | 1 screen with 1 button |
| API | 1 endpoint, hardcoded output allowed |
| Auth | Session or token, real auth provider (not bypass) |
| DB | 1 table, 1 row insert or read |
| Cache | If part of architecture, 1 key |
| Queue / async | If part of architecture, 1 job roundtrip |
| Deployment | CI → staging → prod pipeline runs green |
| Monitoring | At least 1 metric emitted, 1 log line, 1 trace |
| Error path | 1 error handled (e.g., 404) |
| Test | 1 E2E test covering the path |

Check off every layer. If any is missing, extend the skeleton before building horizontally.

## Typical Scope

For a "user can sign up, create a widget, and view it" epic:

### Walking skeleton (minimal end-to-end)
- UI: home page with "Sign up" form, one input field.
- API: `POST /signup` that creates a user record.
- DB: `users` table, 2 columns (id, email).
- Deploy: pushes to staging, then prod.
- Test: E2E that signs up and asserts row.

No widgets yet. No password. No validation. **That's the point.**

### After walking skeleton: broadening
- Add password field and hash.
- Add widget model.
- Add widget-creation UI.
- Add widget-list UI.

Each broadening step is its own vertical slice on top of the walking skeleton.

## Walking Skeleton Anti-Patterns

| Anti-pattern | Why it breaks | Fix |
|--------------|--------------|-----|
| Skipping the DB layer with a mock | Defers integration risk | Real DB row insert on Day 1 |
| Running only in local dev | Deferral of deployment risk | Must ship to staging/prod |
| Using a feature flag that prevents production exposure | Cheats layer coverage | Ship to production; control exposure via auth instead |
| "Skeleton sprint" that runs 4 weeks | Not a skeleton anymore | Target ≤ 1 week for first deploy; ≤ 3 days preferred |
| No automated test | Regression risk immediate | Minimum one E2E test |
| Multiple features in skeleton | Not thinnest | One happy path only |
| Placeholder auth ("admin/admin") left in | Insecurity | Real auth from Day 1, even if minimal |
| Skipping observability | Deferred ops work | At minimum one log + one metric |

## When Not to Use Walking Skeleton

- **Well-understood architecture extension**: adding a feature to a mature system — use vertical slice directly, skeleton already exists.
- **Pure refactor**: no new end-to-end path; use atomic decomposition.
- **Research spike**: if the goal is learning, use forge (prototype) instead; a walking skeleton ships.

## Output Template

```markdown
## Walking Skeleton: [Epic Name]

### Scope
- **End-to-end function**: [one sentence — "user can X"]
- **Target deploy**: [staging / production]
- **Target deadline**: [≤ 1 week, ideally ≤ 3 days]

### Layer Coverage
| Layer | Skeleton implementation | Owner |
|-------|-------------------------|-------|
| UI | [description] | Builder / Artisan |
| API | [description] | Builder |
| Auth | [description] | Builder |
| DB | [description] | Schema / Builder |
| Deployment | [pipeline description] | Gear / Scaffold |
| Observability | [log + metric + trace] | Beacon |
| Test | [1 E2E test path] | Voyager / Radar |

### Explicitly Deferred
- [List everything intentionally left out — ensures team doesn't re-add scope]

### Atomic Steps (call `atomic`)
1. [Step 1 — ≤15 min]
2. ...

### Success Criteria
- [ ] Deployed to production
- [ ] E2E test green in CI
- [ ] At least one real user traversed the path (internal dogfood OK)
- [ ] Observability emits expected signals

### Next (after skeleton)
- [list of vertical slices that broaden from here]
```

## Example: Three-Day Skeleton

Day 1:
- Scaffold repo, CI, deploy to staging (skeleton step 1-4).

Day 2:
- Wire login (OAuth placeholder with one provider) + session (step 5-8).
- Wire one protected endpoint returning hardcoded data (step 9-11).

Day 3:
- Wire UI page that shows the endpoint data (step 12-14).
- Ship to production (step 15).
- Add E2E test covering login → view protected page (step 16).

End of Day 3: production URL lives, E2E test green, team can broaden from here.

## Relationship to Other Agents

- **forge** is for throwaway prototypes; walking skeleton is the real thing, minimal.
- **titan** may run the skeleton-first pattern for S/M scopes automatically.
- **builder** executes each step; **voyager** writes the E2E test; **beacon** wires observability.
- **ripple** evaluates blast radius of the skeleton to production (usually minimal).

## Deliverable Contract

When `walking-skeleton` completes, emit:

- **End-to-end function** (one sentence).
- **Layer-coverage table** (every layer named, with implementation level and owner).
- **Explicitly deferred list** (what is *not* in the skeleton, to defend against scope creep).
- **Atomic step list** (hand off to `atomic` for execution).
- **Success criteria** (deployed + E2E test + observability).
- **Next steps** (vertical slices that broaden from here).
- **Handoffs**: Builder, Voyager/Radar, Beacon, Gear/Scaffold.

## References

- Alistair Cockburn — *Agile Software Development: The Cooperative Game* (origin of the term)
- Growing Object-Oriented Software, Guided by Tests (Freeman & Pryce) — walking skeleton as TDD entry
- Dave Farley — Continuous Delivery (skeleton ships to prod)
- Kent Beck — "Tidy First?" (smallest step that could possibly work)
