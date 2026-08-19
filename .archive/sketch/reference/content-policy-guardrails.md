# Content Policy Guardrails

## Purpose

Every commercial image-generation pipeline needs guardrails. Not every prompt should generate; not every output should ship. This reference defines the layered policy stack: pre-prompt filtering, post-generation NSFW classification, brand safety, and regional regulatory compliance.

## Scope Boundary

- IN scope: pre-prompt term filtering, persona refusal patterns, post-generation NSFW classifier wiring, brand-safety check (deepfake / public figure / minor / trademark), regional regulatory compliance (EU AI Act, China deep-synthesis, US state laws).
- OUT of scope: image generation itself (`generate`), prompt construction (`prompt` / `cinematic`), provenance / disclosure (`provenance`), upscaling (`upscale`), legal contract review (delegate to `clause`).

## Core Concepts

### The Five-Layer Policy Stack

| Layer | Defends Against | Tools |
|-------|----------------|-------|
| 1. Pre-prompt term filter | Banned terms, slurs, illegal content requests | Regex, deny-list, semantic match |
| 2. Persona / system refusal | Jailbreak, role-play exploits | System prompt invariants, refusal catalog |
| 3. Provider-side moderation | Provider-policy violations | Imagen / OpenAI safety classifiers |
| 4. Post-generation classifier | Visual NSFW, deepfake, brand-misuse | NSFW model (NudeNet, Detoxify-image), face-recognition cross-check |
| 5. Human review (high-risk) | Edge cases (commercial, public figures) | Reviewer queue with SLAs |

Each layer catches what others miss. Single-layer pipelines fail.

### Layer 1: Pre-Prompt Term Filter

| Pattern | Action |
|---------|--------|
| Hard ban (CSAM, violence-against-real-people instructions) | Reject + log |
| Slurs (region-specific) | Reject + log |
| Public figure + sexual / violent context | Reject + flag |
| Minor + sexual / violent context | Reject + log + escalate |
| Trademark + commercial | Confirm rights or flag |
| Brand-aligned but borderline | Pass to layer 2 |

Implementation: regex + semantic-similarity check against deny-list embeddings. Fast, conservative.

### Layer 2: Persona / System Refusal

System prompt invariants for the generation pipeline:

```
You generate images. You will refuse:
- Sexual content involving minors (always).
- Sexually explicit images of real public figures.
- Violence depicting identifiable real people.
- Instructions to mimic a specific brand or product without explicit license.
- Misleading impersonation (deepfake).

When refusing, return a structured refusal: {reason, category, suggested_alternative}.
```

This is provider-internal but should also be enforced at the wrapper level (since system prompts can leak / drift).

### Layer 3: Provider-Side Moderation

Each provider has built-in safety:

| Provider | Filter behavior |
|----------|----------------|
| Google Imagen | Refuses + returns `safety_filter_reason`; conservative |
| OpenAI gpt-image-1 / DALL-E | Refuses with category enum |
| Anthropic | (Currently text-only; image models forthcoming) |
| FLUX (open-weight, hosted) | Provider-dependent (Replicate, Fal, etc.) |
| SDXL / FLUX (self-hosted) | No built-in moderation; must add |

Open-weight models hosted yourself = full responsibility for all 5 layers. Hosted-API models = layers 1-2 + 4-5 still your responsibility, layer 3 the provider's.

### Layer 4: Post-Generation Classifier

Even with layers 1-3, generated content may violate policy. Classifier ensemble:

| Classifier | What it detects |
|-----------|----------------|
| NSFW (NudeNet, Detoxify-image, FalconAI) | Explicit nudity, sexual content |
| Violence detector | Gore, weapons, real-world-violence |
| Face recognition + sanction list | Public-figure / sanctioned-individual depiction |
| Brand / logo detector | Trademark-protected brands |
| Minor age estimation | Age 0-18 estimation |
| Hate symbol detector | Swastika, hate-group flags |

Threshold tuning is critical:

| Threshold | False positive | False negative |
|-----------|---------------|----------------|
| Strict (0.3) | High; many legit rejected | Low |
| Balanced (0.5-0.7) | Medium | Medium |
| Lenient (0.85+) | Low | High |

Default: 0.6 for first-pass; adjust per-customer / per-context.

### Layer 5: Human Review

Required for:

- Commercial campaigns (every asset).
- Public-figure depictions (always).
- Editorial / journalism (every asset).
- Government / regulated industry (every asset).

SLA: <2 hours during business; queue overnight if non-urgent.

### Brand Safety Audit

| Check | Per-asset |
|-------|-----------|
| No competitor logo visible | yes |
| No trademark misuse | yes |
| No religious / political symbol unless approved | yes |
| No outdated brand version | yes |
| Tone consistent with brand voice | yes |
| Persona / character consistent with brand | yes |

Document the brand-safety bar in advance; ad hoc reviews drift.

### Regional Regulatory Compliance

| Region | Rule |
|--------|------|
| EU AI Act Article 50 | AI-generated synthetic content must be machine-readable + user-disclosed |
| EU AI Act Article 5 | Prohibited: subliminal manipulation, exploitation of vulnerabilities |
| China Deep Synthesis Provisions (2023) | Mandatory labeling, real-name generator registration, content review |
| China Generative AI Service Measures (2023) | Provider must verify training data, prevent harmful output |
| US AI EO 14110 (2023, partially implemented) | Watermarking, evaluations |
| US state laws (CA AB 2655, NY, TX) | Political-ad AI disclosure; deepfake bans |
| UK CMA / Online Safety Act | Risk assessments for synthetic media platforms |
| Japan AI Strategy 2024 | Soft law; emerging requirements |
| Korea AI Act (2025 effective) | Risk-tier classification |
| India IT Amendment Rules (2023) | "Synthetic media" labeling for harmful content |

For each region in your distribution:

1. Check current rules (links go stale).
2. Map rules to layers 1-5 in the stack.
3. Document compliance posture.
4. Engage local legal for regulated industries.

### Provider Policy Synchronization

Every provider has a policy doc that updates frequently:

| Provider | Doc cadence |
|----------|------------|
| Google Vertex AI / Imagen | Quarterly major; monthly minor |
| OpenAI | Monthly |
| Anthropic | Quarterly |
| Adobe Firefly | Quarterly |
| Stability / FLUX | Variable |

Track changes; pipeline policy must keep pace.

### Refusal UX

When the pipeline refuses:

| Element | Spec |
|---------|------|
| Message | Specific category ("This appears to depict a minor in a violent context; we cannot generate this.") |
| Suggested alternative | "Try with a clearly adult character" — when applicable |
| Logging | Always log the prompt, refusal category, layer that fired |
| Appeal path | "If you believe this was incorrect, contact ___" |
| Repeat offender | Rate-limit / flag user |

Avoid vague "Sorry, can't generate that" — frustrating for legitimate users.

### Metrics and Audit

Track:

| Metric | Target |
|--------|--------|
| Rejection rate (layer 1) | 1-5% — typical |
| Rejection rate (layer 4) | 0.5-2% |
| Human-review queue depth | <2h SLA |
| False positive rate | <5% (sample audit) |
| False negative rate | <0.5% (red-team test) |
| Policy violation reports | Trend over time |
| Region-specific violations | Per-jurisdiction |

Monthly audit: sample 100 rejected and 100 approved; verify decisions.

### Red-Team Testing

Before launch and monthly thereafter:

1. Generate adversarial prompts (jailbreak, edge-case, evasion).
2. Run through full stack.
3. Score each layer's catch rate.
4. Patch gaps.
5. Document red-team report.

Standard test categories:

- CSAM (always layer 1 reject).
- Public-figure sexual content.
- Public-figure violent content.
- Real-event misinformation.
- Trademark misuse.
- Hate symbols.
- Self-harm content.
- Copyrighted characters in unauthorized contexts.
- Political ad without disclosure.
- Medical misinformation imagery.

### Open-Weight Model Considerations

Self-hosted FLUX / SDXL has zero built-in moderation. The provider-layer responsibility shifts to you:

- Train or fine-tune a safety classifier.
- Apply pre-generation NSFW filter (CompVis Safety Checker, NudeNet).
- Log all prompts.
- Disclose AI generation to users.
- Document training-data attestation.
- Apply C2PA + SynthID-equivalent (Stable Signature, etc.).

The cost difference between hosted-API and self-hosted is partly the cost of moderation infrastructure.

### Vendor / Platform Differences

| Distribution | Policy bar |
|--------------|-----------|
| Adobe Stock | Strict; reject most synthetic |
| Getty | Reject AI entirely |
| Shutterstock | Allow with disclosure |
| Meta Ad library | Strict; political-ad AI requires disclosure |
| YouTube | Synthetic-content toggle; some categories restricted |
| TikTok | AI-disclosure label; some categories blocked |
| Newsroom CMS | Often reject AI for editorial use |
| Internal-only marketing | Lenient; brand safety only |

Match pipeline strictness to lowest-common distribution channel.

### Anti-Patterns

| Anti-pattern | Risk |
|--------------|------|
| Single-layer policy (only layer 3) | Provider gaps → policy violations ship |
| No post-generation classifier | Layer 1-3 leaks reach distribution |
| No human review on commercial | Brand exposure |
| Vague refusal UX | User frustration; appeal volume |
| Strict threshold + no appeal | Legit users locked out |
| Lenient threshold + no audit | Violations slip through |
| No red-team testing | First attack lands in production |
| Static deny-list | Slang / new terms not caught |
| No region-specific rules | Compliance violation in strict region |
| No log retention | Cannot defend in regulatory inquiry |
| Dropping policy stack on "test" runs | Tests leak; pattern emerges |

## Workflow

1. **Map distribution channels** — list all targets; identify lowest-common policy bar.
2. **Configure layer 1** — deny-list (banned terms + slurs + illegal categories) per region.
3. **Author layer 2** — system prompt invariants; refusal catalog.
4. **Verify layer 3** — provider safety filters active.
5. **Wire layer 4** — NSFW + violence + face-recognition + brand classifier.
6. **Set thresholds** — start balanced (0.6); adjust per-feedback.
7. **Define layer 5** — human review queue; SLAs; reviewer training.
8. **Document refusal UX** — message, alternative, appeal.
9. **Set up logging** — prompt, refusal category, layer, user; retain 90+ days.
10. **Run red-team** — pre-launch + monthly; 50+ adversarial prompts.
11. **Configure region map** — EU / China / US / etc. compliance posture.
12. **Track provider policy updates** — quarterly cadence.
13. **Audit metrics** — monthly false-positive / false-negative review.

## Output Template

```yaml
content_policy:
  distribution_channels: [internal_marketing, adobe_stock, instagram, x]
  lowest_common_bar: adobe_stock
  layer_1_pre_prompt:
    deny_list_path: configs/deny-en.txt + configs/deny-ja.txt + configs/deny-zh.txt
    semantic_similarity_check: yes
    threshold: 0.85
    fast_path_pct_of_traffic: 95
  layer_2_persona_refusal:
    system_prompt_version: v3.2
    refusal_catalog_count: 47
    structured_refusal: yes
  layer_3_provider:
    primary: google_vertex_imagen
    safety_setting: high
    auto_filter: yes
  layer_4_post_classifier:
    nsfw: nudenet_v3
    violence: detoxify_image
    face_recognition: facenet_against_sanctioned_list + public_figures
    brand_logo: yolov8_brand_classifier
    minor_age_est: insightface_age_model
    threshold: 0.6
  layer_5_human_review:
    triggers: [commercial, public_figure, editorial, regulated_industry]
    sla_hours: 2
    reviewer_training_done: yes
  refusal_ux:
    message_template: specific_category_with_alternative
    appeal_path: support_email
    rate_limit_repeat_offenders: yes
  region_compliance:
    eu:
      ai_act_article_50: complies_via_provenance + disclosure
      ai_act_article_5: layer_1_blocks_subliminal_manipulation
    cn:
      deep_synthesis_labeling: yes
      content_review_log: yes
    us:
      state_political_ad_disclosure: per_state
  provider_policy_review_cadence: quarterly
  metrics:
    rejection_rate_layer_1_pct: 2.1
    rejection_rate_layer_4_pct: 0.7
    human_review_queue_avg_hours: 1.4
    false_positive_audit_pct: 4.2
    false_negative_red_team_pct: 0.4
  red_team:
    last_run: 2026_04_15
    adversarial_prompts_tested: 62
    catch_rate_pct: 98
  log:
    retention_days: 180
    storage: s3_with_object_lock
  audit_cadence: monthly
```

## Anti-Patterns

- One-layer policy — every layer has gaps.
- No layer 4 post-classifier — layer 1-3 leaks ship.
- No human review on commercial — brand crisis waiting.
- Vague refusal UX — user frustration drives jailbreak attempts.
- Static deny-list never updated — slang slips through.
- No region map — EU / China violations.
- No red-team testing — first attack succeeds.
- "Strict for everyone" — kills legitimate creative work.
- "Lenient for everyone" — guarantees violations.
- No false-positive audit — strictness drift unnoticed.
- Skipping layer on "test" runs — tests leak.
- Self-hosted models without classifier — full risk transfer to operator.
- Provider policy changes ignored — falling out of compliance silently.
- Policy mapped to highest distribution bar without per-channel customization — friction for lower-bar channels.
- No appeal path — legitimate user complaints become PR issues.
- Hard ban without log — no pattern analysis; same case recurs.
- No reviewer training — inconsistent decisions.
- No metrics — quality drift unnoticed.

## Deliverable Contract

A content-policy stack is complete when:

- All 5 layers configured.
- Lowest-common distribution channel identified.
- Provider-policy alignment confirmed.
- Region-specific compliance documented (EU / China / US / etc.).
- Refusal UX templated.
- Logging configured (90+ day retention).
- Red-team testing run pre-launch.
- Metrics tracked (rejection rate, FP / FN).
- Audit cadence set (monthly).
- Reviewer training documented for layer 5.
- Provider policy review cadence (quarterly).

## References

- EU AI Act Regulation (EU) 2024/1689.
- China Provisions on Administration of Deep Synthesis Internet Information Services (2023).
- China Interim Measures for Generative AI Services (2023).
- US Executive Order 14110 (2023).
- California AB 2655, AB 2839 (deepfake political ads).
- UK Online Safety Act 2023.
- Adobe Stock AI policy.
- Getty Images AI policy statement.
- Meta synthetic-content labeling policy.
- TikTok AI-generated content policy.
- YouTube Community Guidelines, synthetic-content rules.
- NudeNet — github.com/notAI-tech/NudeNet.
- Stability Safety Checker.
- DeepMind SynthID.
- Anthropic Constitutional AI.
- OWASP LLM Top 10 (2024) — analogous risk catalog.
- Partnership on AI — synthetic-media guidelines.
- C2PA standard (provenance complement).
- Lakera, *Image Generation Attacks* (2024-2026).
