# Weave Usage Examples

**Purpose:** Sample outputs and use cases for Weave.
**Read when:** You need concrete examples of Weave's usage and output format.

---

## Example 1: E-commerce Order State Machine

### Input

```
Design the state transitions for an order.
Cart -> confirmed -> payment -> shipped -> delivered -> completed. Support cancellations and returns.
```

### Output

```yaml
STATE_MACHINE:
  name: OrderLifecycle
  initial: cart
  states:
    cart:
      on:
        CHECKOUT: { target: confirmed, guard: cartNotEmpty }
    confirmed:
      on:
        PAY: { target: payment_processing }
        CANCEL: { target: cancelled }
      after:
        1800000: { target: cancelled, actions: [notifyTimeout] }  # 30min timeout
    payment_processing:
      invoke:
        src: processPayment
        onDone: { target: paid }
        onError: { target: payment_failed }
    payment_failed:
      on:
        RETRY_PAY: { target: payment_processing, guard: canRetry }
        CANCEL: { target: cancelled }
    paid:
      on:
        SHIP: { target: shipped }
        CANCEL: { target: refunding }
    shipped:
      on:
        DELIVER: { target: delivered }
        RETURN_REQUEST: { target: return_requested }
    delivered:
      on:
        RETURN_REQUEST: { target: return_requested, guard: withinReturnPeriod }
        COMPLETE: { target: completed }
      after:
        604800000: { target: completed }  # 7 days auto-complete
    return_requested:
      on:
        APPROVE_RETURN: { target: returning }
        REJECT_RETURN: { target: delivered }
    returning:
      on:
        RETURN_RECEIVED: { target: refunding }
    refunding:
      invoke:
        src: processRefund
        onDone: { target: refunded }
        onError: { target: refund_failed }
    refund_failed:
      on:
        RETRY_REFUND: { target: refunding }
    refunded:
      type: final
    cancelled:
      type: final
    completed:
      type: final

VALIDATION_REPORT:
  reachability: PASS (all 13 states reachable from cart)
  deadlock_free: PASS (all non-final states have outgoing transitions)
  determinism: PASS (no ambiguous transitions)
  completeness: PASS (all state x event combinations handled)
  final_states: [refunded, cancelled, completed]
  unreachable_states: []
  potential_issues:
    - "payment_failed: canRetry guard needs max retry count"
    - "return_requested: consider timeout for approval"
```

---

## Example 2: Saga Design (Travel Booking)

### Input

```
Design a Saga for travel booking.
Reserve flight -> hotel -> rental car in order.
If any step fails, roll back with compensating transactions.
```

### Output

```yaml
SAGA_ORCHESTRATION:
  name: TravelBookingSaga
  timeout: "10m"
  correlation_id: "booking:{booking_id}"
  steps:
    - name: reserve_flight
      service: FlightService
      action:
        command: ReserveFlight
        payload: { flight_id, passenger, date }
        timeout: "30s"
      compensation:
        command: CancelFlightReservation
        payload: { reservation_id }
        timeout: "30s"
      on_success: reserve_hotel
      on_failure: COMPENSATE

    - name: reserve_hotel
      service: HotelService
      action:
        command: ReserveHotel
        payload: { hotel_id, guest, check_in, check_out }
        timeout: "30s"
      compensation:
        command: CancelHotelReservation
        payload: { reservation_id }
        timeout: "30s"
      on_success: reserve_car
      on_failure: COMPENSATE

    - name: reserve_car
      service: CarService
      action:
        command: ReserveRentalCar
        payload: { car_type, pickup_date, return_date }
        timeout: "30s"
      compensation:
        command: CancelCarReservation
        payload: { reservation_id }
        timeout: "30s"
      on_success: COMMIT
      on_failure: COMPENSATE

  compensation_order: reverse
  # Failure at Step 3: cancel car -> cancel hotel -> cancel flight
  # Failure at Step 2: cancel hotel -> cancel flight
  # Failure at Step 1: cancel flight

  idempotency:
    strategy: idempotency_key
    key_format: "saga:{saga_id}:step:{step_name}:{attempt}"
```

---

## Example 3: Approval Flow

### Input

```
Design an approval flow for expense claims.
Under 100,000 JPY: manager only. 100,000 JPY and above: manager + department head. 500,000 JPY and above: also CFO.
```

### Output

```yaml
APPROVAL_FLOW:
  name: ExpenseApproval
  trigger:
    event: expense_submitted
  routing:
    - condition: "amount < 100000"
      levels: [manager]
    - condition: "amount >= 100000 AND amount < 500000"
      levels: [manager, department_head]
    - condition: "amount >= 500000"
      levels: [manager, department_head, cfo]
  levels:
    manager:
      approvers: { type: role, value: "submitter.direct_manager" }
      quorum: 1
      timeout: "24h"
      escalation: department_head
    department_head:
      approvers: { type: role, value: "submitter.department.head" }
      quorum: 1
      timeout: "48h"
      escalation: cfo
    cfo:
      approvers: { type: user, value: "cfo@company.com" }
      quorum: 1
      timeout: "72h"
      escalation: notify_and_wait
  delegation:
    enabled: true
    max_depth: 2
  recall:
    allowed_before: "first_approval"

STATE_MACHINE:
  name: ExpenseApprovalFSM
  initial: draft
  states:
    draft:
      on:
        SUBMIT: { target: pending_manager }
    pending_manager:
      on:
        APPROVE:
          - target: pending_dept_head
            guard: requiresDeptHead
          - target: approved
        REJECT: { target: rejected }
        RECALL: { target: draft }
    pending_dept_head:
      on:
        APPROVE:
          - target: pending_cfo
            guard: requiresCFO
          - target: approved
        REJECT: { target: rejected }
    pending_cfo:
      on:
        APPROVE: { target: approved }
        REJECT: { target: rejected }
    approved:
      type: final
      entry: [processPayment, notifySubmitter]
    rejected:
      on:
        AMEND: { target: draft }
      entry: [notifySubmitter]
```

---

## Example 4: Subscription Lifecycle

### Input

```
Design the lifecycle of a SaaS subscription.
Trial -> paid -> renewal / cancellation / pause. Include dunning (past-due) handling.
```

### Output

```yaml
STATE_MACHINE:
  name: SubscriptionLifecycle
  initial: trial
  context:
    retry_count: 0
    grace_period_days: 7
  states:
    trial:
      on:
        CONVERT: { target: active, actions: [startBilling] }
        EXPIRE: { target: expired }
      after:
        1209600000: { target: trial_ending }  # 14 days
    trial_ending:
      entry: [sendTrialEndingNotice]
      on:
        CONVERT: { target: active, actions: [startBilling] }
      after:
        86400000: { target: expired }  # 1 day grace
    active:
      on:
        PAYMENT_DUE: { target: payment_processing }
        CANCEL: { target: cancelling }
        PAUSE: { target: paused, guard: pauseAllowed }
        UPGRADE: { actions: [changePlan] }
        DOWNGRADE: { target: downgrade_scheduled }
    payment_processing:
      invoke:
        src: chargeSubscription
        onDone: { target: active, actions: [recordPayment] }
        onError: { target: payment_retry }
    payment_retry:
      entry: [incrementRetry, sendPaymentFailedNotice]
      on:
        PAYMENT_UPDATED: { target: payment_processing }
      after:
        259200000:  # 3 days
          - target: payment_processing
            guard: canRetry
          - target: past_due
    past_due:
      entry: [sendPastDueNotice, restrictFeatures]
      on:
        PAYMENT_UPDATED: { target: payment_processing }
      after:
        604800000: { target: suspended }  # 7 day grace
    suspended:
      entry: [suspendAccess, sendSuspensionNotice]
      on:
        PAYMENT_UPDATED: { target: payment_processing }
      after:
        2592000000: { target: churned }  # 30 days
    paused:
      on:
        RESUME: { target: active }
      after:
        7776000000: { target: churned }  # 90 days max pause
    cancelling:
      entry: [scheduleEndOfPeriod]
      on:
        REACTIVATE: { target: active }
        PERIOD_END: { target: cancelled }
    downgrade_scheduled:
      on:
        PERIOD_END: { target: active, actions: [applyDowngrade] }
        CANCEL_DOWNGRADE: { target: active }
    expired:
      on:
        CONVERT: { target: active, actions: [startBilling] }
      type: final
    cancelled:
      on:
        RESUBSCRIBE: { target: active }
      type: final
    churned:
      type: final
      entry: [archiveData, sendWinbackEmail]
```
