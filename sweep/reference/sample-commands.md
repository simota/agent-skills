# Sample Commands

Purpose: quick command reference for dependency analysis, file analysis, and project-tool discovery.

## Dependency Analysis

```bash
# TypeScript/JavaScript - unused exports
npx ts-prune

# Unused dependencies
npx depcheck

# Comprehensive unused-code scan
npx knip

# Inspect installed production packages
npm ls --all --production
```

## File Analysis

```bash
# Detect duplicate files by hash
find . -type f -not -path '*/node_modules/*' -exec md5 -r {} \; | sort | uniq -d -w32

# Find files larger than 100 KB
find . -type f -size +100k -not -path '*/node_modules/*' -not -path '*/.git/*'

# Find files not modified for 90+ days
find . -type f -mtime +90 -not -path '*/node_modules/*'

# Find orphan TypeScript file candidates
for f in $(find src -name "*.ts" -not -name "*.d.ts"); do
  base=$(basename "$f" .ts)
  grep -rq "from.*['\"].*$base['\"]" src/ || echo "Orphan: $f"
done
```

## Project-Specific Tool Discovery

```bash
# Inspect package.json scripts
cat package.json | jq '.scripts'

# Inspect lint/format config files
ls -la .*rc* .*.js .*.json 2>/dev/null

# Inspect tools referenced by GitHub Actions
cat .github/workflows/*.yml 2>/dev/null | grep -E "npm|yarn|pnpm"
```
