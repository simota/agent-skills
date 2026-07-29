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

AI Overviews and AI Mode now sit at or near-global reach; citation inside an AI Overview earns significantly more clicks than an uncited result on the same SERP, and structured data + direct-answer formatting are table stakes. Full CTR figures, rollout timeline, and sources → `reference/geo-optimization.md`.

### E-E-A-T Signals

- Add author bios with credentials, publication dates, and update history
- Link to primary sources and cite first-hand experience
- Display qualifications, certifications, and organizational affiliations prominently

### Answer-First Structure

- Place a short, direct answer (2–3 sentences) at the top of the page before any preamble
- Follow with supporting detail, evidence, and nuance below

### Structured Data for AI Parsing

> **2026 update:** FAQ rich results were retired from blue-link SERPs (Jun/Aug 2026); FAQPage and HowTo schema remain valid and are still parsed by AI engines for citation — keep them. Full detail and sources → `reference/json-ld-templates.md`.

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
