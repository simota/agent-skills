# Compete Agent Teams Pattern

Moved out of `compete/SKILL.md` so it loads when it is needed rather than on
every invocation. The text is unchanged.

---

**Agent Teams pattern (RESEARCH_FAN_OUT):**
When analyzing `5+` competitors across multiple segments, spawn 2-3 Explore subagents in parallel:
- Each subagent researches a distinct competitor subset (e.g., direct competitors vs indirect vs substitutes)
- Coordinator synthesizes findings via Union merge (deduplicate → cross-reference → rank by strategic impact)
- Team size: `2-3` (Explore, model: haiku). Escalate to Rally if `4+` parallel research streams needed
