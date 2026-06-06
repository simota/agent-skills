# Onboarding Copy Patterns

段階的開示テンプレート、初回体験テキストのリファレンス。

---

## Progressive Disclosure

### Disclosure Levels

| Level | Content | When |
|-------|---------|------|
| **Essential** | What user must know to proceed | Always visible |
| **Helpful** | What improves understanding | On hover/expand |
| **Detailed** | Deep configuration or explanation | Behind "Learn more" |

### Progressive Disclosure Pattern

```
Step 1: Show the minimum needed
  "Create your first project"
  [Project name field]
  [Create button]

Step 2: Reveal more when relevant
  ↓ After project creation
  "Nice! Now invite your team"
  [Email invite field]
  "Skip for now" (always offer escape)

Step 3: Advanced options on demand
  ⚙️ "Advanced settings"
  → Expands to show additional options
```

---

## Welcome Screens

### First Launch Template

```markdown
## Template Structure
1. Greeting (personal, brief)
2. Value proposition (what they can do, not what the product is)
3. First action (single, clear CTA)
4. Skip option (never trap the user)

## Example
"Welcome to [Product], [Name]! 👋

Here you can [primary value: "manage your projects and
collaborate with your team in real-time"].

Let's set up your first project."

[Create a project]          [Take a tour]
```

### Post-Signup Flow

| Step | Purpose | Copy Pattern |
|------|---------|-------------|
| **1. Welcome** | Orient and motivate | "Welcome! Let's get you set up." |
| **2. Profile** | Personalize experience | "Tell us about yourself so we can customize your experience." |
| **3. First action** | Deliver value quickly | "Create your first [item] — it takes less than a minute." |
| **4. Quick win** | Reinforce value | "Great job! You've just [accomplishment]." |
| **5. Next steps** | Expand engagement | "Here's what you can do next:" |

---

## Setup Wizard Copy

### Step Indicator Text

```
Good: "Step 2 of 4 — Connect your account"
Bad:  "Step 2 of 4"

Include:
- Step number and total
- What this step does (brief)
- Progress bar or indicator
```

### Setup Step Patterns

| Element | Pattern | Example |
|---------|---------|---------|
| **Heading** | Action verb + outcome | "Connect your calendar" |
| **Subheading** | Why this matters | "So we can schedule meetings for you" |
| **Help text** | Reassurance | "You can change this anytime in settings" |
| **CTA** | Specific action | "Connect Google Calendar" |
| **Skip** | Permission to opt out | "Skip — I'll do this later" |

---

## Tooltip Tours

### Tour Best Practices

```markdown
## Rules
1. Max 5 steps (users abandon longer tours)
2. Each step teaches ONE concept
3. Show benefit, not feature
4. Allow skip at every step
5. Don't block critical actions
6. Show step count: "2 of 5"

## Step Template
Heading: [Feature name]
Body: [What it does + why it helps — 1-2 sentences]
CTA: [Next / Got it / Try it]
```

### Tour Step Examples

```markdown
## Step 1: Dashboard
"This is your dashboard — a quick overview of all your
active projects and upcoming deadlines."
[Next →]  [Skip tour]

## Step 2: Quick Actions
"Use the + button to create projects, tasks, or notes
from anywhere in the app."
[Next →]  [Skip tour]

## Step 3: Collaboration
"Invite team members to collaborate in real-time.
Everyone's changes sync instantly."
[Got it!]
```

---

## Onboarding Emails

### Email Sequence Pattern

| Day | Type | Subject Line Pattern | Content Focus |
|-----|------|---------------------|---------------|
| 0 | Welcome | "Welcome to [Product]!" | Quick start guide |
| 1 | Quick win | "Try this: [specific action]" | One feature, one benefit |
| 3 | Value | "Did you know you can [feature]?" | Expand usage |
| 7 | Check-in | "How's it going with [Product]?" | Support offer, feedback ask |
| 14 | Upgrade | "[Feature] is waiting for you" | Premium value (if freemium) |

### Email Copy Template

```markdown
Subject: [Action-oriented, specific, under 50 chars]

Hi [Name],

[1 sentence connecting to their goal/pain point]

[1-2 sentences about the feature and its benefit]

[CTA button: specific action verb]

[1 sentence of reassurance or alternative]

Cheers,
[Human name from team]
```

---

## Checklist Onboarding

### Setup Checklist Pattern

```markdown
## Getting Started

Complete these steps to get the most out of [Product]:

☑ Create your account — Done!
☐ Set up your profile
☐ Create your first project
☐ Invite a team member
☐ Connect your tools

Progress: 1 of 5 complete

[Continue setup →]
```

### Checklist Copy Guidelines

| Element | Guidelines |
|---------|-----------|
| **Task text** | Verb + object (action-oriented) |
| **Completion text** | Past tense + emoji/check |
| **Progress** | Show X of Y, not just percentage |
| **Reward** | Celebrate completion: "All set! You're ready to go." |
| **Persistence** | Dismissable but accessible from settings |
