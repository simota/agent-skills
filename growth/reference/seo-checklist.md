# SEO Implementation Checklist

## Per-Page Requirements

- [ ] Unique `<title>` (50-60 chars, keyword first)
- [ ] Unique `<meta name="description">` (150-160 chars)
- [ ] Canonical URL: `<link rel="canonical" href="...">`
- [ ] Single H1 tag with primary keyword
- [ ] Heading hierarchy (H1 > H2 > H3, no skipping)
- [ ] Image alt text (descriptive, not stuffed)
- [ ] Internal links to related pages

## Technical SEO

- [ ] robots.txt configured
- [ ] XML sitemap submitted
- [ ] HTTPS everywhere
- [ ] Mobile responsive
- [ ] Core Web Vitals passing
- [ ] No duplicate content
- [ ] 301 redirects for moved pages

## AI Overview / AI Mode Optimization

Google's AI Overviews has scaled to 200+ countries and 40+ languages as of May 2025, and AI Mode (the new fully conversational AI Search experience launched at I/O 2025) became globally available across nearly 200 countries and 98 languages following Google I/O 2026 (2026-05). Gemini 3.5 Flash is the default model in AI Mode globally. The classic blue-link CTR for queries with AI Overviews dropped 61% (1.76% → 0.61%) per Seer Interactive's September 2025 study, but pages cited inside an AI Overview earn **35% more organic clicks** (and 91% more paid clicks) than uncited pages on the same SERP — citation is the new ranking. CTR is also recovering: Seer's follow-up showed AIO-query organic CTR rising from 1.3% (Dec 2025) to 2.4% (Feb 2026), an 85% rebound. Structured data + direct-answer formatting are now table stakes.

[Source: Search Engine Land — Google AI Overviews CTR shows early signs of recovery (2026-02), https://searchengineland.com/google-ai-overviews-ctr-recovery-study-475566]
[Source: Google blog — AI Mode expands languages and locations (2026-05), https://blog.google/products-and-platforms/products/search/ai-mode-expands-languages-locations/]
[Source: Ahrefs — AI Overviews Reduce Clicks by 58% (2025-12), https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/]

### E-E-A-T Signals

- Add author bios with credentials, publication dates, and update history
- Link to primary sources and cite first-hand experience
- Display qualifications, certifications, and organizational affiliations prominently

### Answer-First Structure

- Place a short, direct answer (2–3 sentences) at the top of the page before any preamble
- Follow with supporting detail, evidence, and nuance below

### Structured Data for AI Parsing

> **2026 update:** Google has fully dropped FAQ rich results from blue-link SERPs (FAQ search appearance, rich result report, and Rich Results Test support removed June 2026; Search Console API support removed August 2026 — [Search Engine Land, 2026, https://searchengineland.com/google-to-no-longer-support-faq-rich-results-476957]). HowTo rich results were already deprecated in 2023. **FAQPage and HowTo schema remain valid Schema.org types and are still parsed by AI Overviews / AI Mode / Perplexity / ChatGPT** — keep them for AI citation, not for rich snippets. Schema.org released **v30.0 on 2026-03-19** (823 types), adding properties for credentials, e-commerce, and supply-chain transparency optimized for AI verification [Source: Schema.org release notes, https://schema.org/docs/releases.html].

```html
<!-- FAQ schema is still parsed by AI engines for Q&A extraction (no longer triggers blue-link rich results) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the best way to improve Core Web Vitals?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Focus on LCP (image optimization, SSR), INP (reduce long tasks, use scheduler.yield), and CLS (reserve space for dynamic content)."
      }
    }
  ]
}
</script>

<!-- HowTo schema for step-by-step content -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to optimize LCP",
  "step": [
    { "@type": "HowToStep", "name": "Preload hero image", "text": "Add <link rel='preload'> for the LCP element." },
    { "@type": "HowToStep", "name": "Enable SSR", "text": "Use Next.js getStaticProps or generateStaticParams." }
  ]
}
</script>
```

### Semantic HTML + Entity Optimization

- Use `<article>`, `<section>`, `<aside>`, `<nav>` — avoid `<div>` for structural content
- Mention entities (people, places, concepts) consistently with their canonical names
- Build topic clusters: one pillar page + multiple supporting pages linked bidirectionally

## Next.js 15 / React 19 SEO

### Static Metadata

```typescript
// app/blog/page.tsx — static metadata via export const
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Blog | My Site',
  description: 'Latest articles on web performance and growth.',
  openGraph: {
    title: 'Blog | My Site',
    description: 'Latest articles on web performance and growth.',
    url: 'https://mysite.com/blog',
    siteName: 'My Site',
    images: [{ url: '/og/blog.png', width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Blog | My Site',
    description: 'Latest articles on web performance and growth.',
    images: ['/og/blog.png'],
  },
};
```

### Dynamic Metadata

```typescript
// app/blog/[slug]/page.tsx — dynamic metadata via generateMetadata
import type { Metadata } from 'next';

interface Props {
  params: Promise<{ slug: string }>;
}

// Only Server Components can export generateMetadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  // fetch is auto-memoized — same request won't be duplicated
  const post = await fetch(`/api/posts/${slug}`).then(r => r.json());

  return {
    title: `${post.title} | Blog`,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.coverImage, width: 1200, height: 630 }],
      type: 'article',
      publishedTime: post.publishedAt,
      authors: [post.author.name],
    },
  };
}

export default async function BlogPostPage({ params }: Props) {
  const { slug } = await params;
  const post = await fetch(`/api/posts/${slug}`).then(r => r.json()); // memoized hit
  return <article>{/* ... */}</article>;
}
```

### File-Based Metadata (App Router)

```
app/
  opengraph-image.jpg      → /og:image for all pages (fallback)
  blog/
    opengraph-image.jpg    → /blog og:image override
    [slug]/
      opengraph-image.tsx  → dynamic OG image via @vercel/og
  twitter-image.jpg
  robots.txt               → static robots rules
  sitemap.xml              → or sitemap.ts for dynamic generation
```

### layout.tsx vs page.tsx Pattern

```typescript
// app/layout.tsx — site-wide defaults
export const metadata: Metadata = {
  metadataBase: new URL('https://mysite.com'),
  title: { default: 'My Site', template: '%s | My Site' },
  description: 'Default site description.',
};

// app/blog/[slug]/page.tsx — per-page override (merges with layout)
export const metadata: Metadata = {
  title: 'Specific Post Title', // renders as "Specific Post Title | My Site"
};
```

## Structured Data (JSON-LD)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": { "@type": "Person", "name": "Author" },
  "datePublished": "2024-01-01"
}
</script>
```
