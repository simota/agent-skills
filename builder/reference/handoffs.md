# Builder Handoff Directions

Moved out of `builder/SKILL.md` so it loads when it is needed rather than on
every invocation. The text is unchanged.

---

| Direction | Handoff | Purpose |
|-----------|---------|---------|
| Forge → Builder | `FORGE_TO_BUILDER` | Prototype conversion to production code |
| Scout → Builder | `SCOUT_TO_BUILDER` | Bug fix based on investigation results |
| Guardian → Builder | `GUARDIAN_TO_BUILDER` | Commit structure guidance |
| Tuner → Builder | `TUNER_TO_BUILDER` | Apply optimization recommendations |
| Sentinel → Builder | `SENTINEL_TO_BUILDER` | Security fix implementation |
| Builder → Radar | `BUILDER_TO_RADAR` | Test skeleton handoff |
| Builder → Guardian | `BUILDER_TO_GUARDIAN` | PR preparation |
| Builder → Judge | `BUILDER_TO_JUDGE` | Code review request |
| Builder → Tuner | `BUILDER_TO_TUNER` | Performance analysis request |
| Builder → Sentinel | `BUILDER_TO_SENTINEL` | Security review request |
| Builder → Canvas | `BUILDER_TO_CANVAS` | Domain diagram request |
| Vision → Builder | `VISION_TO_BUILDER` | Art direction for image-generation code |
| Growth → Builder | `GROWTH_TO_BUILDER` | Marketing asset-generation requirements |
| Quill → Builder | `QUILL_TO_BUILDER` | Documentation illustration requirements |
| Builder → Muse | `BUILDER_TO_MUSE` | Generated-asset design-system integration |
| Builder → Vitrine | `BUILDER_TO_VITRINE` | Generated assets for catalogs or stories |
