# Documentation Types & Templates

Purpose: Read this when Quill must scaffold or update changelogs, contributing guides, OpenAPI examples, or ADR-style documentation.

Contents:
- `CHANGELOG.md (Keep a Changelog format)`: release-note structure
- `CONTRIBUTING.md (Essential sections)`: contribution guide checklist
- `OpenAPI/Swagger Documentation`: response and example template
- `Architecture Decision Record (ADR)`: decision log template

## CHANGELOG.md (Keep a Changelog format)

```markdown
## [Unreleased]
### Added
- New feature description (#PR)

### Changed
- Modified behavior description

### Fixed
- Bug fix description (#issue)

### Deprecated
- Feature to be removed in future version
```

## CONTRIBUTING.md (Essential sections)

```markdown
## Getting Started
[Dev environment setup]

## Development Workflow
1. Fork and clone
2. Create feature branch
3. Make changes with tests
4. Submit PR

## Code Style
[Linting rules, naming conventions]

## Testing
[How to run tests, coverage requirements]

## PR Guidelines
[Title format, description template, review process]
```

## OpenAPI/Swagger Documentation

```yaml
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
          example: "usr_123"
      responses:
        200:
          description: User found
          content:
            application/json:
              example:
                id: "usr_123"
                name: "John Doe"
        404:
          description: User not found
```

## Architecture Decision Record (ADR)

```markdown
# ADR-001: [Decision Title]

## Status
Accepted | Deprecated | Superseded by ADR-XXX

## Context
[Why we needed to make this decision]

## Decision
[What we decided to do]

## Consequences
[Trade-offs and implications]
```
