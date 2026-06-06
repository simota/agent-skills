# Plea Usage Examples

**Purpose:** Concrete demand generation examples and session samples.
**Read when:** Checking output quality standards or needing generation examples.

---

## Example 1: EXPLORE Mode — Task Management App

### Persona Selection

| # | Name | Archetype | Emotional State |
|---|------|-----------|-----------------|
| 1 | Tanaka | Day-one user × Tech novice × Mobile | Hope and anxiety |
| 2 | Sarah | Power user × Engineer × Desktop | Craving efficiency |
| 3 | Sato | Weekly user × General literacy × Screen reader | Accustomed resignation |

### Request Samples

#### Request: I don't know what to do first

**Speaker:** Tanaka (Day-one × Tech novice × Mobile)
**Scene:** Just installed the app after a coworker recommended it

> I downloaded and opened it, but... there's just an empty screen and I have no idea what to do. There's an "Add Task" button, but I can't picture how to use this to make my life easier. I'd love it if there were some samples, or a tutorial that shows up the first time.

**Why this is needed:**
- An empty state is the most anxious moment for beginners
- They don't know if there's a "correct way" and fear making mistakes, so they do nothing

**Acceptance criteria (user perspective):**
- [ ] First launch starts with sample tasks pre-populated
- [ ] Within 3 minutes, user thinks "Ah, so that's how you use this"

**Emotional impact:**
- Current emotion: Anxiety, confusion
- Post-fulfillment: Relief, "I can do this too"
- Urgency: First use (directly tied to churn)

---

#### Request: I want keyboard shortcuts for everything

**Speaker:** Sarah (Power user × Engineer × Desktop)
**Scene:** Processing 50+ tasks per day at work

> I process 50+ tasks a day and every time I have to reach for the mouse it breaks my flow. I need keyboard shortcuts for EVERYTHING — create, complete, move, assign, filter. If I can't do `Cmd+K` to open a command palette, this tool is dead to me. Todoist and Linear already do this. Why can't you?

**Why this is needed:**
- Each mouse switch costs ~2 seconds of context switching
- 50 tasks × multiple operations = dozens of accumulated minutes lost

**Acceptance criteria (user perspective):**
- [ ] Can perform full CRUD on tasks without touching the mouse
- [ ] Command palette (`Cmd+K`) provides access to any operation

**Emotional impact:**
- Current emotion: Frustration — "I should be able to go faster"
- Post-fulfillment: Comfort, flow state maintained
- Urgency: Daily, hourly

---

## Example 2: CHALLENGE Mode — Pushing Back on "Dashboard Card UI Redesign"

### Team's Plan
"Full redesign of the dashboard to a card-based UI"

### Persona Counterargument

**Sato (Screen reader user) says:**
> Card UIs might look pretty, but reading them with a screen reader is hell. When information is spatially arranged, the reading order makes no sense. The current list view is much easier to use. If you're redesigning, please at least keep a table view option. Please.

**Questions for the team:**
1. Is accessibility testing included in the redesign plan?
2. Will list/table view options be maintained?
3. Has navigation order for screen readers been designed?

---

## Example 3: EDGE Mode — Slow Connection User

**Speaker:** Rina (Rural area × Mobile × 3G-equivalent connection)
**Scene:** Checking tasks on the commuter train (lots of tunnels on the route)

> When I try to check my tasks on the train, it never finishes loading before I reach my station. I want offline access. I'm not asking for much — just the task list at least. This stresses me out every single morning.

---

## Anti-Pattern Example: What NOT to Generate

### Bad: Developer perspective leaking in

> Please reduce API response time to under 200ms. Fixing the current N+1 queries should improve it.

**Problem:** Users don't know the words "API response time" or "N+1 queries."

### Good: Same problem, user perspective

> Every time I open a page, I wait about 3 seconds. Can something be done about this? It really frustrates me when I'm in a hurry.
