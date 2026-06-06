# Scout Bug Pattern Catalog Reference

**Purpose:** Pattern-based investigation shortcuts for common bug families.
**Read when:** The symptom already resembles a known bug family and a fast pattern-based path is useful.

## Contents

- Null or undefined
- Race condition
- Off-by-one
- State synchronization
- Memory leak
- Infinite loop

## Null / Undefined Reference

- Symptoms: property access `TypeError`, unexpected `undefined`, partially rendered output
- Investigate:
  1. trace the value to its source
  2. inspect all code paths that can leave it empty
  3. check null guards and optional chaining
  4. check async timing
- Common causes:
  - missing API response handling
  - race condition in data loading
  - optional property access without guard
  - array index out of bounds

## Race Condition

- Symptoms: intermittent failure, flaky tests, machine-speed differences
- Investigate:
  1. add timestamps
  2. inspect shared mutable state
  3. check cleanup functions
  4. inspect missing `await` or concurrent requests
- Common causes:
  - missing `await`
  - stale closure
  - unmount during async work
  - rapid repeated updates

## Off-by-One Error

- Symptoms: missing first or last item, bounds errors, loop runs too many or too few times
- Investigate:
  1. compare `<` vs `<=`
  2. check `0`-based vs `1`-based indexing
  3. verify `slice` and `substring` semantics
  4. inspect length calculations

## State Synchronization Issue

- Symptoms: stale UI, inconsistent component state, delayed updates
- Investigate:
  1. trace state flow from source to consumer
  2. look for multiple sources of truth
  3. verify re-render triggers
  4. inspect shallow vs deep comparison behavior

## Memory Leak

- Symptoms: performance degrades over time, heap grows, slow tab or process
- Investigate:
  1. compare heap snapshots
  2. look for detached DOM nodes
  3. inspect event listeners, intervals, and retained closures

## Infinite Loop / Recursion

- Symptoms: freeze, `Maximum call stack exceeded`, CPU at `100%`
- Investigate:
  1. add a counter
  2. verify base case
  3. inspect circular dependency or state-triggered rerenders
  4. check dependency arrays

## Quick Pattern Identification

| Pattern | Key Symptom | First Check |
|---------|-------------|-------------|
| Null / Undefined | property access `TypeError` | stack trace location |
| Race Condition | intermittent failure | async and timing code |
| Off-by-One | missing first or last | loop boundaries |
| State Sync | stale UI | state mutation or stale derivation |
| Memory Leak | slow over time | listeners, timers, heap |
| Infinite Loop | freeze or stack overflow | dependency arrays, recursion |
