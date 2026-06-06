# GEO Packaging — Transcript + VideoObject for AI Citation

Purpose: Package every externally distributed demo so AI Overviews, ChatGPT, AI Mode, and YouTube search can **cite specific timestamped segments**. Used by the `geo` recipe.

## Why GEO Matters (2026)

- AI assistants quote **20–660 second segments** from videos — not whole files. Without a transcript and schema, your demo is invisible to citation.
- Combined YouTube + branded web mentions correlate strongest with brand visibility in ChatGPT / AI Overviews / AI Mode.
- Multi-channel distribution of a video can increase AI citation by **up to 325%**.
- VideoObject structured data correlates with up to **+41% CTR** on search.

If your demo is not transcribed and schema-tagged, it loses to competitors who do this for free.

---

## Deliverables

Every external demo ships with **all four**:

1. **WebVTT transcript** (`.vtt`) — same cue structure as captions, accessible to crawlers.
2. **Plaintext transcript** (`.txt`) — for blog embeds, social copy reuse, screen-reader fallback.
3. **VideoObject JSON-LD** — schema.org markup with `hasPart` clips, `transcript`, `thumbnailUrl`.
4. **Chapter cue map** — timestamp → topic, embeddable in YouTube description and on-page.

---

## WebVTT Transcript

Same shape as closed captions but optimized for search:

```
WEBVTT

NOTE
  Demo: Acme Migration Tool
  Duration: 0:60
  Locale: en-US

00:00:00.000 --> 00:00:03.000
Schema drift broke production. Again.

00:00:03.000 --> 00:00:10.500
Most teams manually diff three environments
and pray nothing else changed.

00:00:10.500 --> 00:00:40.000
With Acme, one click previews and applies
the migration across staging, canary, and prod.
```

Differences from captions:
- Longer cues are OK (this is for reading, not display).
- Cue text repeats narration verbatim — no `[music]` cues required.
- Speaker labels optional.

---

## Plaintext Transcript

Single-paragraph or paragraph-per-chapter prose. Used for:
- Blog post embeds
- Social copy reuse
- Screen-reader / accessibility fallback
- Direct AI ingestion (some models prefer plain text over VTT)

```
[0:00] Schema drift broke production. Again. Most teams manually
diff three environments and pray nothing else changed.

[0:10] With Acme, one click previews and applies the migration
across staging, canary, and prod.

[0:40] Result: zero manual SQL, zero overnight rollbacks. Acme
catches drift before it ships.

[0:55] Start free at acme.dev/migrate.
```

---

## VideoObject JSON-LD

Place this in the page that embeds the video, or alongside the video file as `demo.jsonld`.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Acme Migration Tool — 60s demo",
  "description": "One-click schema migration across staging, canary, and production with drift detection.",
  "thumbnailUrl": [
    "https://cdn.acme.dev/demos/migrate_thumb_1280x720.jpg",
    "https://cdn.acme.dev/demos/migrate_thumb_1080x1080.jpg",
    "https://cdn.acme.dev/demos/migrate_thumb_1080x1920.jpg"
  ],
  "uploadDate": "2026-05-15T09:00:00+09:00",
  "duration": "PT1M",
  "contentUrl": "https://cdn.acme.dev/demos/migrate_16x9_20260515.mp4",
  "embedUrl": "https://www.youtube.com/embed/EXAMPLE_ID",
  "transcript": "Schema drift broke production. Again. Most teams manually diff three environments...",
  "inLanguage": "en-US",
  "publisher": {
    "@type": "Organization",
    "name": "Acme",
    "logo": {
      "@type": "ImageObject",
      "url": "https://cdn.acme.dev/logo.png"
    }
  },
  "hasPart": [
    {
      "@type": "Clip",
      "name": "The schema-drift problem",
      "startOffset": 0,
      "endOffset": 10,
      "url": "https://cdn.acme.dev/demos/migrate_16x9_20260515.mp4#t=0,10"
    },
    {
      "@type": "Clip",
      "name": "Preview migration across environments",
      "startOffset": 10,
      "endOffset": 40,
      "url": "https://cdn.acme.dev/demos/migrate_16x9_20260515.mp4#t=10,40"
    },
    {
      "@type": "Clip",
      "name": "Apply with zero rollback risk",
      "startOffset": 40,
      "endOffset": 55,
      "url": "https://cdn.acme.dev/demos/migrate_16x9_20260515.mp4#t=40,55"
    }
  ]
}
```

### Required Fields

| Field | Notes |
|-------|-------|
| `name` | The discoverable title. Match it to the YouTube title and on-page heading. |
| `description` | One sentence; this is what AI Overviews will quote. |
| `thumbnailUrl` | All three aspects if multi-aspect (16:9, 1:1, 9:16). |
| `uploadDate` | ISO-8601. Update on re-shoots. |
| `duration` | ISO-8601 duration (`PT1M`, `PT2M30S`). |
| `contentUrl` OR `embedUrl` | At least one must be live. |
| `transcript` | Plaintext, full. **Critical for AI citation.** |
| `inLanguage` | BCP-47 (`en-US`, `ja-JP`). |
| `hasPart` (clips) | At least 2 chapters for any video > 30s. Enables timestamp citation. |

---

## Chapter Cue Map (YouTube Description Format)

Paste directly into YouTube description for native chapter navigation:

```
0:00 The schema-drift problem
0:10 Preview migration across environments
0:40 Apply with zero rollback risk
0:55 Try it free at acme.dev/migrate
```

Rules (YouTube enforces):
- First chapter must start at `0:00`.
- Chapters must be at least 10 seconds long.
- At least 3 chapters per video.

This unlocks YouTube "Key Moments" snippets that AI Overviews and Google Search use.

---

## Multi-Channel Distribution Plan

To maximize AI citation (up to +325%), distribute the same demo across multiple surfaces. AI models fuse citations across sources.

| Channel | Purpose | Required Artifacts |
|---------|---------|--------------------|
| YouTube long (16:9) | Primary indexable surface | VideoObject + chapters + transcript + thumbnail |
| LinkedIn (4:5) | B2B feed visibility | Burned-in captions + post body with transcript excerpt |
| Product Hunt (1:1) | Launch surface | YouTube embed + caption-burned variant |
| Website blog post | Owned-channel anchor | VideoObject JSON-LD + on-page transcript + chapter cues |
| Docs page | Long-tail organic | Inline embed + chapter cues + plaintext transcript |
| TikTok / Reels / Shorts (9:16) | Short-form discovery | Burned-in captions + 9:16 master + hook in first 3s |

AI models that crawl YouTube + your domain see the same video twice, which boosts citation confidence.

---

## Workflow

```
INPUT          →  finalized demo video + closed-caption .vtt
               →  brand metadata (name, description, publisher)

EXTRACT        →  parse .vtt cues → plaintext transcript
               →  identify chapter boundaries (≥10s each, ≥3 chapters)

SCHEMA         →  generate VideoObject JSON-LD
               →  populate hasPart[] with timestamped Clip objects
               →  attach thumbnailUrl per aspect

PUBLISH        →  upload video to YouTube + CDN
               →  paste chapter cues into YouTube description
               →  embed JSON-LD on hosting page
               →  add transcript section on the page (visible or collapsed)

VERIFY         →  Google Rich Results Test: search.google.com/test/rich-results
               →  YouTube chapters appear in player
               →  spot-check transcript matches narration

DISTRIBUTE     →  cross-post per Multi-Channel Distribution Plan

HANDOFF        →  Quill: doc-side embed + transcript
               →  Growth: A/B thumbnail + UTM tagging
               →  Builder: CDN upload + schema embed in templates
```

---

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Shipping without transcript | Block delivery; transcript is mandatory for external demos |
| Plaintext only (no VideoObject) | Add JSON-LD; AI crawlers prefer structured data |
| Chapters <10s or <3 chapters total | Re-cut chapters to meet YouTube rules |
| Embedding without `transcript` field in schema | Major citation loss — always include |
| Single hosting URL (no YouTube backup) | Cross-post to YouTube even if primary is self-hosted |
| Forgetting `inLanguage` | AI models can't route locale-specific citations |
| Old `uploadDate` after a reshoot | Update to fresh date; AI freshness signals matter |
| Generic thumbnail with no per-aspect variants | Generate one per aspect; supplied as array in JSON-LD |

---

## References

- schema.org VideoObject — schema.org/VideoObject
- Google Rich Results Test — search.google.com/test/rich-results
- YouTube chapter rules — support.google.com/youtube
- "VideoObject Schema" — AEO Expert (2026)
- "Video Citing AI Overviews" — Reel n Reel (2026)
- "YouTube Optimization for AI" — Am I Cited (2026)
