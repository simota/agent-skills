# OGP & Social Sharing Templates

> **2026 platform notes:**
> - **X (Twitter)** still supports `summary` and `summary_large_image` cards; preferred image is **1200×675** (1.91:1, ≤5MB). Twitter's official Card Validator at `cards-dev.twitter.com` has been deprecated since 2022 — verify cards by posting from a private/scheduled draft instead. [Source: og-image.org / moda.app Twitter card 2026 guides]
> - **Bluesky** parses standard `og:title` / `og:description` / `og:image` (no custom AT-Protocol record needed) and renders them similar to X's `summary_large_image` layout. There is an open social-app issue (#5012) tracking a future small/`summary` card variant. [Source: github.com/bluesky-social/social-app/issues/5012]
> - **LinkedIn / Facebook / Slack / Discord** continue to consume standard OGP; LinkedIn now uses 1200×627 as the canonical share image dimension.

## Open Graph (Facebook/LinkedIn)

```html
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="Description" />
<meta property="og:image" content="https://example.com/image.jpg" />
<meta property="og:url" content="https://example.com/page" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Site Name" />
```

Image requirements: 1200x630px, < 8MB

## Twitter Cards

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Page Title" />
<meta name="twitter:description" content="Description" />
<meta name="twitter:image" content="https://example.com/image.jpg" />
```

## Next.js Metadata API

```typescript
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Description',
  openGraph: {
    title: 'Page Title',
    description: 'Description',
    images: [{ url: '/og-image.jpg', width: 1200, height: 630 }],
  },
  twitter: { card: 'summary_large_image' },
};
```
