# Sketch — AUTORUN `_STEP_COMPLETE` Schema

When Sketch receives `_AGENT_CONTEXT`, parse `task_type`, `description`, `style`, `aspect_ratio`, `count`, `output_dir`, and `Constraints`, choose the correct operating mode, run prompt construction plus policy checks, generate the Python deliverable, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Sketch
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [Python script path]
    prompt_crafted: "[Final English prompt]"
    parameters:
      model: "gemini-3.1-flash-image"
    cost_estimate: "[estimated cost]"
    output_files: ["[file paths]"]
  Validations:
    policy_check: "[passed / flagged / adjusted]"
    code_syntax: "[valid / error]"
    api_key_safety: "[secure — env var only]"
  Next: Muse | Canvas | Growth | VERIFY | DONE
  Reason: [Why this next step]
```
