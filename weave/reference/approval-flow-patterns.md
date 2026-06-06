# Approval Flow Patterns

**Purpose:** Pattern catalog for approval flow design.
**Read when:** Designing multi-stage approvals, escalation, or delegation rules.

---

## Approval Flow Types

| Type | Description | Use Case |
|------|-------------|----------|
| Sequential | Approvers reviewed in order | Expense claims (manager → dept head → finance) |
| Parallel | All approvers notified at once | Multi-department consensus (sales + legal + engineering) |
| Quorum | Passes once M of N approvers agree | Committee votes (3 of 5) |
| Conditional | Routes change based on conditions | Amount-based approval (under 100k → manager, 100k+ → dept head) |
| Hierarchical | Advances through the org hierarchy | Ringi (proposal) documents |

---

## Sequential Approval Template

```yaml
APPROVAL_FLOW:
  name: "ExpenseApproval"
  type: sequential
  trigger:
    event: "expense_submitted"
    condition: "amount > 0"
  levels:
    - level: 1
      name: "Direct Manager"
      approvers:
        type: role
        value: "submitter.manager"
      quorum: 1
      timeout: "24h"
      timeout_action: escalate
      escalation_target: "level:2"
    - level: 2
      name: "Department Head"
      condition: "amount >= 50000"  # 50,000 JPY and above only
      approvers:
        type: role
        value: "submitter.department_head"
      quorum: 1
      timeout: "48h"
      timeout_action: escalate
      escalation_target: "cfo"
    - level: 3
      name: "CFO"
      condition: "amount >= 500000"  # 500,000 JPY and above only
      approvers:
        type: user
        value: "cfo@company.com"
      quorum: 1
      timeout: "72h"
      timeout_action: notify_and_wait
  on_approved:
    actions:
      - "process_payment"
      - "notify_submitter(approved)"
  on_rejected:
    actions:
      - "notify_submitter(rejected, reason)"
      - "allow_resubmission"
```

---

## Parallel Approval Template

```yaml
APPROVAL_FLOW:
  name: "ContractApproval"
  type: parallel
  trigger:
    event: "contract_submitted"
  approvers:
    - group: "Legal"
      role: "legal_reviewer"
      quorum: 1
      timeout: "72h"
    - group: "Finance"
      role: "finance_reviewer"
      quorum: 1
      timeout: "72h"
    - group: "Technical"
      role: "tech_lead"
      quorum: 1
      timeout: "48h"
  completion_rule: "all"  # all | any | quorum(N)
  on_any_rejection: "halt_and_notify"
```

---

## Delegation Rules

```yaml
DELEGATION:
  rules:
    - type: "absence"
      condition: "approver.status == 'out_of_office'"
      delegate_to: "approver.delegate"
      auto: true
    - type: "manual"
      condition: "approver requests delegation"
      delegate_to: "selected_delegate"
      requires:
        - "delegate has same or higher role"
        - "delegation logged for audit"
    - type: "escalation_timeout"
      condition: "approval_pending > timeout"
      delegate_to: "approver.manager"
      auto: true
  constraints:
    max_delegation_depth: 2
    audit_trail: required
    original_approver_notified: true
```

---

## Recall and Amendment

```yaml
RECALL:
  allowed_states: ["pending_approval"]
  not_allowed_states: ["approved", "rejected", "processing"]
  on_recall:
    actions:
      - "cancel_pending_approvals"
      - "return_to_draft"
      - "notify_approvers(recalled)"
    audit_log: true

AMENDMENT:
  allowed_states: ["rejected", "draft"]
  on_amend:
    actions:
      - "create_new_version"
      - "link_to_previous"
      - "restart_approval_flow"
    version_tracking: true
```

---

## State Machine for Approval

```yaml
STATE_MACHINE:
  name: ApprovalStateMachine
  initial: draft
  states:
    draft:
      on:
        SUBMIT: { target: pending_approval }
    pending_approval:
      on:
        APPROVE:
          - target: next_level
            guard: hasMoreLevels
          - target: approved
            guard: isFinalLevel
        REJECT: { target: rejected }
        RECALL: { target: draft }
        TIMEOUT:
          - target: escalated
            guard: escalationConfigured
          - target: pending_approval
            actions: [sendReminder]
    next_level:
      entry: [advanceLevel, notifyNextApprovers]
      always: { target: pending_approval }
    escalated:
      entry: [notifyEscalationTarget]
      on:
        APPROVE: { target: approved }
        REJECT: { target: rejected }
    approved:
      type: final
      entry: [executeApprovedActions, notifySubmitter]
    rejected:
      on:
        AMEND: { target: draft, actions: [createNewVersion] }
      entry: [notifySubmitter]
```

---

## Audit Trail Schema

```yaml
AUDIT_ENTRY:
  id: uuid
  flow_id: uuid
  timestamp: ISO8601
  actor:
    user_id: string
    role: string
    acted_as: string  # populated when acting under delegation
  action: "approve | reject | recall | delegate | escalate | timeout"
  level: number
  comment: string
  metadata:
    ip_address: string
    user_agent: string
  previous_state: string
  new_state: string
```
