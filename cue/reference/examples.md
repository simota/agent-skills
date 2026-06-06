# Cue Examples

## Example 1: Product Demo Video (60s)

### Brief

```yaml
type: product-demo
product: TaskFlow (project management tool)
audience: Engineering managers
duration: 60s
platform: Product Hunt, landing page
goal: Drive free trial sign-ups
key_message: "Ship faster with AI-powered task management"
```

### Script

```markdown
## Scene 1: Hook (8s)
**Visual:** Counter animation: "Average team: 12 hours/week in status meetings"
**Narration:** "Your team spends 12 hours a week just talking about work. What if AI could handle that?"
**Tone:** Provocative
**Transition:** Zoom into product UI

## Scene 2: Problem (12s)
**Visual:** Split screen — cluttered Jira board vs. overflowing Slack
**Narration:** "Status updates scattered across tools. Blockers hidden in threads. Deadlines slipping quietly."
**Tone:** Empathetic
**Transition:** Fade to product

## Scene 3: Solution Intro (10s)
**Visual:** Clean TaskFlow dashboard with AI summary panel
**Narration:** "TaskFlow uses AI to surface what matters. No more asking 'what's the status?'"
**Tone:** Confident
**Transition:** Cut to feature demo

## Scene 4: Feature Demo (20s)
**Visual:** Screen recording — AI generates daily standup summary
**Narration:** "Every morning, your team gets an AI standup. Blockers flagged. Progress tracked. Zero meetings."
**Tone:** Professional, clear
**Notes:** [Director: record this segment with Playwright]
**Transition:** Morph to results

## Scene 5: Social Proof (5s)
**Visual:** "2,000+ teams shipped 40% faster"
**Narration:** "Two thousand teams already ship 40 percent faster."
**Tone:** Authoritative
**Transition:** Fade

## Scene 6: CTA (5s)
**Visual:** Logo + "Try free → taskflow.dev" + QR code
**Narration:** "Start free at taskflow.dev. Ship faster, starting today."
**Tone:** Warm, inviting
```

### Timing Budget

| Scene | Duration | Cumulative | Words |
|-------|----------|-----------|-------|
| Hook | 8s | 8s | 20 |
| Problem | 12s | 20s | 25 |
| Solution | 10s | 30s | 20 |
| Demo | 20s | 50s | 22 |
| Proof | 5s | 55s | 10 |
| CTA | 5s | 60s | 12 |
| **Total** | **60s** | — | **109** |

## Example 2: Tutorial Video (3 min)

### Brief

```yaml
type: tutorial
topic: "Setting up CI/CD with GitHub Actions"
audience: Junior developers
duration: 180s
platform: YouTube
goal: Viewer can create a basic CI pipeline
```

### Script Outline

| Scene | Time | Visual | Narration Focus |
|-------|------|--------|----------------|
| Intro | 0:00-0:15 | Title card + goal | What you'll learn |
| Prerequisites | 0:15-0:25 | Checklist animation | What you need |
| Step 1 | 0:25-0:55 | Code editor + terminal | Create workflow file |
| Step 2 | 0:55-1:25 | YAML editing | Define triggers and jobs |
| Step 3 | 1:25-1:55 | GitHub UI | Push and watch run |
| Step 4 | 1:55-2:25 | Green checkmark + logs | Verify success |
| Bonus | 2:25-2:45 | Code diff | Add caching for speed |
| Summary | 2:45-3:00 | Key takeaways + links | Recap and next steps |
