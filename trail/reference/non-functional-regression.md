# Non-Functional Regression Investigation

Investigation methodology for non-functional regressions combining git bisect with specialized tools.

## Performance Regression

### Benchmark-Driven Bisect

```bash
# Use semantic names with bisect terms
git bisect start --term-old=fast --term-new=slow

# Automate verdict with a benchmark script
git bisect run ./scripts/perf-bisect.sh
```

### perf-bisect.sh Template

```bash
#!/bin/bash
# Build
npm run build 2>/dev/null || exit 125  # skip if build fails

# Run benchmark
RESULT=$(npm run bench -- --json 2>/dev/null | jq '.results[0].mean')

# Compare against threshold (e.g., 200ms)
THRESHOLD=200
if (( $(echo "$RESULT > $THRESHOLD" | bc -l) )); then
  exit 1  # slow (new/bad)
else
  exit 0  # fast (old/good)
fi
```

### CI/CD Performance Test Integration

- Identify regression point from historical performance test result graphs in CI
- Narrow candidate commits with `git log --after="regression-date" --before="regression-date+1d"`
- Retrieve benchmark results from GitHub Actions artifacts: `gh run download`

## Memory Regression

### Heap Growth Bisect

```bash
#!/bin/bash
# Memory bisect script
npm run build 2>/dev/null || exit 125

# Run with memory profiling
node --max-old-space-size=512 --expose-gc scripts/memory-test.js

# Check peak RSS
PEAK_RSS=$(cat /tmp/peak-rss.txt)
THRESHOLD=256  # MB

if [ "$PEAK_RSS" -gt "$THRESHOLD" ]; then
  exit 1  # leak (new/bad)
else
  exit 0  # ok (old/good)
fi
```

### Memory Leak Onset Identification

1. Use blame on the leak location detected by Specter to identify the last modifier
2. Use bisect to identify the commit where the leak started
3. Compare heap snapshots before and after the commit

## Bundle Size Regression

### Bundle Size Bisect

```bash
#!/bin/bash
npm run build 2>/dev/null || exit 125
SIZE=$(stat -f%z dist/bundle.js 2>/dev/null || stat -c%s dist/bundle.js)
THRESHOLD=500000  # 500KB
[ "$SIZE" -gt "$THRESHOLD" ] && exit 1 || exit 0
```

## Startup Time Regression

- Distinguish cold start vs warm start
- Container environment: measure wall time with `time docker run --rm app`
- Node.js: identify bottleneck modules with `--prof` + `--prof-process`
- Python: profile import time with `python -X importtime`

## Specter Escalation Criteria

When bisect result falls into any of the following, use `TRAIL_TO_SPECTER_HANDOFF` (`_common/INVESTIGATION_ESCALATION.md`):

- Changes to concurrency control (lock, mutex, semaphore, channel)
- Changes to resource management (connection pool, file handle, socket)
- Changes to async processing patterns (Promise chain, async/await, event listener)
- Changes to memory management (cache, buffer, stream)
