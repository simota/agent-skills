# Dependency Health Scan

## Scan Commands

```bash
# Check for outdated packages
npm outdated

# Check for security vulnerabilities
npm audit

# Find unused dependencies
npx depcheck

# Check bundle size impact
npx bundlephobia <package-name>

# Analyze package size
npx cost-of-modules

# Check for deprecated packages
npx npm-check
```

## Automated Health Check Script

```bash
#!/bin/bash
# dependency-health.sh

echo "=== Dependency Health Check ==="

echo "\n📦 Outdated Packages:"
npm outdated --json | jq -r 'to_entries[] | "\(.key): \(.value.current) → \(.value.latest)"'

echo "\n🔒 Security Vulnerabilities:"
npm audit --json | jq '.metadata.vulnerabilities'

echo "\n🗑️ Unused Dependencies:"
npx depcheck --json | jq '.dependencies, .devDependencies'

echo "\n📊 Bundle Size (top 10):"
npx cost-of-modules --less --no-install | head -15
```

## Health Check Matrix

| Check | Tool | Frequency | Action |
|-------|------|-----------|--------|
| Outdated (patch) | `npm outdated` | Weekly | Auto-update |
| Outdated (minor) | `npm outdated` | Monthly | Review + update |
| Outdated (major) | `npm outdated` | Quarterly | Plan migration |
| Security (low/moderate) | `npm audit` | Weekly | Review |
| Security (high/critical) | `npm audit` | Immediate | Fix now |
| Unused dependencies | `depcheck` | Monthly | Remove |
| Deprecated packages | `npm-check` | Monthly | Plan replacement |

## Package.json Analysis Checklist

### Direct Dependencies
- [ ] All packages actively maintained (last commit < 1 year)
- [ ] No known security vulnerabilities
- [ ] No deprecated packages
- [ ] Bundle size reasonable for use case

### DevDependencies
- [ ] Build tools up to date
- [ ] Linters/formatters consistent
- [ ] Test frameworks current

### Potential Issues
- [ ] Duplicate functionality (e.g., lodash + ramda)
- [ ] Heavy packages for simple tasks
- [ ] Packages with native alternatives
