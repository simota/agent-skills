# README Scaffolding Templates

Templates for different project types to ensure consistent documentation.

Purpose: Read this when Quill must create or repair README structure for a library, application, or CLI project.

Contents:
- `Library/Package README`: package-oriented installation, API, and config template
- `Application README`: app onboarding, project structure, scripts, and deployment template
- `CLI Tool README`: command-focused installation, usage, config, and examples template
- `AI-readability companion files`: `llms.txt` / `llms-full.txt` baseline for 2026 documentation

## AI Consumer is Now ~50% of Documentation Traffic (2026)

By 2026 the published analytics from documentation platforms put **roughly half of documentation traffic on AI agents** — Cursor, Claude Code, ChatGPT, Perplexity, GitHub Copilot, Windsurf, Antigravity — not human browsers. Two practical rules for every README authored in 2026:

1. **Lead with the *what* + the canonical install command in the first 10 lines.** AI scrapers truncate aggressively; a README that buries the install command behind a marketing intro is a `pip install`/`npm install` an AI agent will hallucinate.
2. **Ship the `llms.txt` companion** at the repository root (and at the docs-site root for hosted docs). Mintlify / Fern / Docusaurus all auto-generate it; for hand-rolled docs use [`docusaurus-plugin-llms`](https://github.com/rachfop/docusaurus-plugin-llms) or write it by hand from the README headings.

### Minimal `llms.txt`

```markdown
# Package Name

> Brief description (one sentence).

## Docs
- [Quick Start](./README.md#quick-start): canonical install + first call
- [API Reference](./docs/api.md): every public symbol with @param, @returns, @throws
- [Migration Guide](./docs/MIGRATION.md): version-to-version breaking changes
- [Examples](./examples/): runnable code samples

## Optional
- [Architecture](./docs/architecture.md): internal design — for contributors only
```

The companion `llms-full.txt` inlines the same documents concatenated for full-context retrieval. Treat both as **first-class artefacts** that the build pipeline regenerates on every release — stale `llms.txt` is worse than no `llms.txt` because AI agents trust what is there.

## Library/Package README

```markdown
# Package Name

Brief description of what this package does.

## Installation

\`\`\`bash
npm install package-name
# or
yarn add package-name
\`\`\`

## Quick Start

\`\`\`typescript
import { mainFunction } from 'package-name';

const result = mainFunction({ option: 'value' });
\`\`\`

## API Reference

### `mainFunction(options)`

Description of the main function.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `option` | `string` | - | Required option |
| `timeout` | `number` | `5000` | Optional timeout in ms |

**Returns**: `ResultType` - Description of return value

**Example**:
\`\`\`typescript
const result = mainFunction({ option: 'value', timeout: 10000 });
\`\`\`

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `PACKAGE_API_KEY` | API key for service | - |
| `PACKAGE_TIMEOUT` | Request timeout | `5000` |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup.

## License

MIT
```

## Application README

```markdown
# Application Name

Brief description of the application.

## Prerequisites

- Node.js >= 18
- PostgreSQL >= 14
- Redis >= 6

## Getting Started

### 1. Clone and Install

\`\`\`bash
git clone https://github.com/org/repo.git
cd repo
npm install
\`\`\`

### 2. Environment Setup

\`\`\`bash
cp .env.example .env
# Edit .env with your values
\`\`\`

### 3. Database Setup

\`\`\`bash
npm run db:migrate
npm run db:seed  # Optional: seed test data
\`\`\`

### 4. Run Development Server

\`\`\`bash
npm run dev
# Open http://localhost:3000
\`\`\`

## Project Structure

\`\`\`
src/
├── api/          # API routes
├── components/   # React components
├── lib/          # Shared utilities
├── pages/        # Page components
└── types/        # TypeScript types
\`\`\`

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run test` | Run tests |
| `npm run lint` | Run linter |

## Deployment

See [docs/deployment.md](./docs/deployment.md) for deployment instructions.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT
```

## CLI Tool README

```markdown
# CLI Tool Name

Brief description of the CLI tool.

## Installation

\`\`\`bash
npm install -g cli-tool-name
# or
npx cli-tool-name
\`\`\`

## Usage

\`\`\`bash
cli-tool <command> [options]
\`\`\`

## Commands

### `init`

Initialize a new project.

\`\`\`bash
cli-tool init [project-name]

Options:
  --template <name>  Use a specific template
  --force            Overwrite existing files
\`\`\`

### `build`

Build the project.

\`\`\`bash
cli-tool build [options]

Options:
  --watch    Watch for changes
  --minify   Minify output
\`\`\`

## Configuration

Create `cli-tool.config.js` in your project root:

\`\`\`javascript
module.exports = {
  input: './src',
  output: './dist',
  plugins: [],
};
\`\`\`

## Examples

### Basic Usage

\`\`\`bash
cli-tool init my-project
cd my-project
cli-tool build
\`\`\`

### With Options

\`\`\`bash
cli-tool build --watch --minify
\`\`\`

## License

MIT
```
