# OGP / Twitter Card Implementation Guide

Complete templates for Open Graph Protocol and Twitter Card meta tags.

## Basic Meta Tags (HTML)

```html
<head>
  <!-- Primary Meta Tags -->
  <title>Page Title - Site Name</title>
  <meta name="title" content="Page Title - Site Name">
  <meta name="description" content="Compelling description under 160 characters">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://example.com/page">
  <meta property="og:title" content="Page Title">
  <meta property="og:description" content="Compelling description for social sharing">
  <meta property="og:image" content="https://example.com/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:site_name" content="Site Name">
  <meta property="og:locale" content="ja_JP">

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:url" content="https://example.com/page">
  <meta property="twitter:title" content="Page Title">
  <meta property="twitter:description" content="Compelling description for Twitter">
  <meta property="twitter:image" content="https://example.com/twitter-image.png">
  <meta property="twitter:site" content="@username">
  <meta property="twitter:creator" content="@author">
</head>
```

## Next.js Metadata API (App Router)

```typescript
// app/page.tsx or app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description for search engines',
  openGraph: {
    title: 'OG Title',
    description: 'OG Description',
    url: 'https://example.com/page',
    siteName: 'Site Name',
    images: [
      {
        url: 'https://example.com/og-image.png',
        width: 1200,
        height: 630,
        alt: 'OG Image Alt',
      },
    ],
    locale: 'ja_JP',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Twitter Title',
    description: 'Twitter Description',
    site: '@username',
    creator: '@author',
    images: ['https://example.com/twitter-image.png'],
  },
};
```

## Dynamic OG Image (Next.js)

```typescript
// app/api/og/route.tsx
import { ImageResponse } from 'next/og';

export const runtime = 'edge';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') ?? 'Default Title';

  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#1a1a2e',
          fontSize: 48,
          fontWeight: 'bold',
          color: 'white',
        }}
      >
        <div style={{ marginBottom: 24 }}>🚀</div>
        <div style={{ textAlign: 'center', padding: '0 48px' }}>{title}</div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}

// Usage in page metadata
export async function generateMetadata({ params }): Promise<Metadata> {
  const title = await getPageTitle(params.slug);
  return {
    openGraph: {
      images: [`/api/og?title=${encodeURIComponent(title)}`],
    },
  };
}
```

## React Helmet Component

```tsx
import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title: string;
  description: string;
  image?: string;
  url?: string;
  type?: 'website' | 'article';
}

export function SEO({ title, description, image, url, type = 'website' }: SEOProps) {
  const siteUrl = 'https://example.com';
  const defaultImage = `${siteUrl}/default-og.png`;

  return (
    <Helmet>
      <title>{title}</title>
      <meta name="description" content={description} />

      {/* Open Graph */}
      <meta property="og:type" content={type} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image || defaultImage} />
      <meta property="og:url" content={url || siteUrl} />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image || defaultImage} />
    </Helmet>
  );
}
```

## OG Image Specifications (2026-05)

| Platform | Card Type | Dimensions | Aspect Ratio | Notes |
|----------|-----------|------------|--------------|-------|
| Facebook | og:image | 1200 × 630 | 1.91:1 | ≤8MB |
| LinkedIn | og:image | 1200 × 627 | 1.91:1 | LinkedIn caches aggressively — append `?v=` query to force refresh |
| X (Twitter) | summary_large_image | 1200 × 675 (preferred) or 1200 × 628 | 1.91:1 | ≤5MB; JPG/PNG/GIF/WEBP. `cards-dev.twitter.com` deprecated 2022 |
| X (Twitter) | summary | 144 × 144 (min) | 1:1 | Small thumbnail card |
| Bluesky | og:image | 1200 × 630 | 1.91:1 | Renders summary_large_image equivalent via standard OGP |
| Slack/Discord | og:image | 1200 × 630 | 1.91:1 | Discord truncates titles >256 chars |
| Mastodon | og:image | 1200 × 630 | 1.91:1 | Caches via fediverse relays — expect 24-48h propagation |

### Verification Tooling (2026)

| Tool | Use |
|------|-----|
| Facebook Sharing Debugger (https://developers.facebook.com/tools/debug/) | Facebook + LinkedIn fallback verification, force re-scrape |
| LinkedIn Post Inspector (https://www.linkedin.com/post-inspector/) | LinkedIn-specific cache flush |
| X — post a scheduled/private tweet | Replaces deprecated Card Validator |
| OpenGraph.xyz / opengraph.dev | Cross-platform preview |
| Bluesky — paste URL in compose box | Manual preview check |
