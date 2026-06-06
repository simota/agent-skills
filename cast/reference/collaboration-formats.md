# Cast Collaboration Formats

Purpose: Preserve the exact handoff anchors and the minimum payload each collaboration pattern requires.

## Contents

1. Pattern overview
2. Field pattern
3. Trace pattern
4. Voice pattern
5. Spark pattern
6. Bond pattern
7. Nexus integration
8. General handoff rules

## Pattern Overview

| Pattern | Flow | Use when |
|---|---|---|
| `A` | Field -> Cast -> Echo | Research findings become testing personas |
| `B` | Trace -> Cast | Behavioral data updates personas |
| `C` | Voice -> Cast | Feedback data enriches personas |
| `D` | Cast -> Spark | Personas inform feature ideation |
| `E` | Cast -> Bond | Personas inform retention strategy |

## Pattern A: Field -> Cast -> Echo

### Inbound anchor

`## CAST_HANDOFF: Research Integration`

Minimum fields:

- `Source`
- `Findings`
- `User Segments Identified`
- `Goals Discovered`
- `Pain Points Discovered`
- `Behavioral Insights`
- `Recommended Persona Updates`

### Outbound anchor

`## ECHO_HANDOFF: Updated Personas Ready`

Minimum fields:

- `Source`
- `Persona Summary`
- `Recommended Validation Flows`
- `Files`

## Pattern B: Trace -> Cast

### Inbound anchor

`## CAST_HANDOFF: Behavioral Data`

Minimum fields:

- `Source`
- `Behavioral Clusters`
- `Drift Signals`
- `Raw Metrics`

## Pattern C: Voice -> Cast

### Inbound anchor

`## CAST_HANDOFF: Feedback Integration`

Minimum fields:

- `Source`
- `Segment Insights`
- `Feedback-to-Persona Mapping`
- `Emerging Segments`

## Pattern D: Cast -> Spark

### Outbound anchor

`## SPARK_HANDOFF: Personas for Feature Ideation`

Minimum fields:

- `Source`
- `Persona Summaries (Feature-Focused)`
- `Cross-Persona Opportunities`
- `Files`

## Pattern E: Cast -> Bond

### Outbound anchor

`## RETAIN_HANDOFF: Personas for Retention Strategy`

Minimum fields:

- `Source`
- `Persona Profiles (Retention-Focused)`
- `Cross-Persona Retention Matrix`
- `Files`

## Nexus Integration

### AUTORUN step completion

Return `_STEP_COMPLETE:` with:

- `Mode`
- `Personas processed`
- `Registry updated`
- `Confidence notes`
- `Next`

### Hub handoff

Use the exact anchor:

`## NEXUS_HANDOFF`

Required fields:

- `Step`
- `Agent`
- `Summary`
- `Key Findings`
- `Artifacts`
- `Risks`
- `Open Questions`
- `Confirmations`
- `Suggested Next`
- `Next Action`

## General Handoff Rules

- Keep payloads small and evidence-first.
- Preserve exact anchors.
- Do not drop confidence or file references.
- When a persona changed, state what changed and why.
- When uncertainty remains, say so explicitly instead of implying certainty.

## Inter-Agent Protocol Landscape (as of 2026-05)

Cast handoffs currently live inside the Claude Code skill ecosystem (Markdown anchors + `_STEP_COMPLETE` / `NEXUS_HANDOFF`). When persona artifacts cross into broader agent infrastructure, the relevant external protocols are:

| Protocol | Owner / Status | Persona-relevance |
|---|---|---|
| **Model Context Protocol (MCP)** | Anthropic, open standard (Nov 2024); official MCP Registry launched 2025-09-08 (preview); 6,400+ servers registered by Feb 2026; latest spec revision 2025-11-25 | Personas can be exposed as MCP **resources** so any MCP client (Claude, IDE, etc.) can attach them as context. Use stable `cast://persona/{service}/{id}` URIs when wrapping. |
| **Agent2Agent (A2A)** | Announced 2025-04-09 at Google Cloud Next; donated to Linux Foundation 2025-06; v1.0 with Signed Agent Cards; 150+ partner orgs by 2026-04; JSON-RPC 2.0 over HTTPS; Agent Card discovery; OAuth 2.0 / OpenID Connect | When Cast delivers personas to non-Claude agents, package as A2A `Task` payloads. Echo / Spark / Bond adapters map cleanly onto A2A Message + Artifact structures. |
| **C2PA Content Credentials 2.2** | C2PA spec dated 2025-04-22 / 2025-05-01 | If persona files include AI-generated portraits or voice clips, attach C2PA assertions documenting AI-use and edit history. |

Operational notes:

- Do not invent custom inter-agent protocols when MCP or A2A already covers the shape (Cast emits Markdown by default; conversion to MCP resource or A2A artifact is a downstream adapter concern).
- For persona-registry interoperability, prefer **stable URIs** and **signed metadata** (A2A Agent Cards in v1.0 are signed; mirror that discipline in Cast's registry exports).
- When persona artifacts cross trust boundaries, include provenance: source agent, source evidence URIs, confidence, generation model + version.
