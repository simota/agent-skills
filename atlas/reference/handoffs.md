# Atlas Handoffs

Use `_common/HANDOFF.md` for transport and routing. Atlas supplies evidence and an approved proposal; it does not implement the structural change or bypass the hub. Fill only the selected recipient's payload from actual analysis.

## ZEN_HANDOFF

Required: task and target file/modules; observed responsibilities/coupling and dependency evidence; proposed split or interface/seam; current versus desired state; acceptance criteria; and constraints on behavior, public API and migration order. State which consumers must keep working and which tests establish preservation. Do not convert sample LOC counts or imaginary import counts into acceptance criteria.

God-class split, mixed-responsibility separation and coupling reduction use this same payload. Public API remains compatible initially; any later deprecation/change needs the approved migration plan.

## CANVAS_REQUEST

Required: diagram type, purpose, scope/entities and directed relationships. Add only the applicable data:

| Diagram | Additional payload |
|---------|--------------------|
| System context (C4 L1) | System name/description, external actors/systems and interactions |
| Component (C4 L3) | Internal components, responsibilities and dependency edges |
| Dependency graph | Actual module edges; cycles/concentrated dependency issues to highlight |
| Migration timeline/Gantt | Phases, ordering/duration constraints and verified milestones |

Canvas owns diagram syntax/rendering. Do not invent an architecture or roadmap to fill a sample.
