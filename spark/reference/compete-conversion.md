# Spark Compete-to-Spec Conversion Reference

Purpose: convert competitive analysis into concrete feature proposals without losing gap type, positioning, or differentiation logic.

## Contents
- Gap type strategy
- Proposal headers
- Matrix-to-story conversion
- Differentiation verification
- Competitive context block

## Gap Type Strategy

| Gap type | Definition | Strategy | Risk |
| --- | --- | --- | --- |
| `Parity Gap` | competitors have it and we do not | catch up where user expectation is clear | low to medium |
| `Blue Ocean` | nobody offers it yet | innovate where we have unfair advantage | high |
| `Our Advantage` | we have it and competitors do not | fortify and deepen the moat | low |
| `Threat Gap` | our lead is shrinking fast | defend, reposition, or refresh | medium to high |

## Proposal Headers

### `## CATCH_UP_PROPOSAL: [Feature Name]`

Use when:
- users explicitly expect the capability
- deals or retention are at risk without it
- the feature is now table stakes

Required sections:
- `Gap Source`
- `Gap Type`
- `Competitors with Feature`
- `Market Context`
- `Lost Opportunity Evidence`
- `Competitive Implementation Analysis`
- `Our Adaptation`

### `## INNOVATION_PROPOSAL: [Feature Name]`

Use when:
- the market has an unmet need
- we can exploit a technical or strategic edge
- the proposal opens a new segment or workflow

Required sections:
- `Gap Source`
- `Gap Type`
- `Competitor Coverage`
- `Market Opportunity`
- `Unmet Need`
- `Why Competitors Haven't Done This`
- `Risk Notes`

### `## FORTIFICATION_PROPOSAL: [Feature Name Enhancement]`

Use when:
- customers already choose us for this strength
- competitors are likely to copy it
- extending the lead is cheaper than starting a new category

Required sections:
- `Gap Source`
- `Gap Type`
- `Current Status`
- `Current Advantage Analysis`
- `Why It's An Advantage`
- `Fortification Moves`

### `## DEFENSIVE_PROPOSAL: [Feature Area]`

Use when:
- a former differentiator is collapsing
- a competitor launch narrowed the gap
- users perceive reduced distance between products

Required sections:
- `Gap Source`
- `Gap Type`
- `Threat Level`
- `Threat Analysis`
- `Previous Advantage`
- `Current State`
- `Defensive Response`

## Feature Matrix To User Story Conversion

### `## FEATURE_MATRIX_CONVERSION`

Required sections:
- `Source`
- `Total Gaps Identified`
- `Converted to Proposals`
- ranked proposal entries

Conversion steps:
1. identify the gap type
2. inspect how competitors implement it
3. assign a target persona
4. restate the user benefit in our product context
5. generate the user story
6. check whether to match, beat, or avoid

Compact example:

| Feature | Us | Comp A | Comp B | Priority |
| --- | --- | --- | --- | --- |
| Export to PDF | `❌` | `✅` | `✅` | `P1` |
| AI suggestions | `❌` | `❌` | `❌` | `P2 (Blue Ocean)` |
| Offline mode | `❌` | `✅` | `❌` | `P3` |

## Differentiated Spec

### `## DIFFERENTIATED_FEATURE_SPEC`

Required sections:
- `Feature`
- `Gap Type`
- `Baseline Requirements (Match Competition)`
- `Differentiation Requirements (Beat Competition)`
- `Evidence We Must Preserve`

Rule:
- parity work must still articulate where our version is clearer, faster, safer, or better integrated

## Differentiation Verification

### `## DIFFERENTIATION_VERIFICATION_REQUEST`

Use to validate whether the proposal still creates product distance.

Required fields:
- `Feature`
- `Gap Type`
- `Competitors to Check`
- `Claims To Verify`
- `Failure Condition`

Verification loop:
1. state the claim
2. check whether a competitor already matches it
3. decide `match`, `beat`, `fortify`, or `drop`

## Competitive Context Block

### `## COMPETITIVE_CONTEXT (Include in Proposal)`

Include:
- `Source Analysis`
- `Gap Type`
- `Competitors Compared`
- `What Users Already Expect`
- `What Makes Our Version Distinct`
- `What Would Invalidate This Proposal`

Use this block whenever a proposal came from `COMPETE_TO_SPARK_HANDOFF`.
