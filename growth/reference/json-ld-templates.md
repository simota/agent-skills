# JSON-LD Structured Data Templates

Schema.org JSON-LD templates for rich snippets in search results **and AI citation (AI Overviews / ChatGPT / Perplexity / Claude / Copilot)**.

> **2026 status:**
> - **Schema.org v30.0** released 2026-03-19 — 823 distinct types. New properties expanded for professional credentials, e-commerce, and digital supply-chain transparency, optimized for AI verification. [Source: https://schema.org/docs/releases.html]
> - **FAQ rich results retired** in Google blue-link SERPs (Jun 2026 — Rich Results Test support removed; Aug 2026 — Search Console API removed). HowTo rich results were already retired in 2023. **FAQPage and HowTo schema remain valid Schema.org types and are still parsed by AI engines** for citation — keep them. [Source: Search Engine Land, https://searchengineland.com/google-to-no-longer-support-faq-rich-results-476957]
> - **Use the most specific subtype**: `BlogPosting` ⊂ `Article`, `NewsArticle` ⊂ `Article`, `LocalBusiness` ⊂ `Organization`, `OnlineStore` ⊂ `LocalBusiness`. Specificity strengthens AI citation signals.
> - **Triple-stack (`Article` + `ItemList` + `FAQPage`)** in a single `@graph` array yields the strongest AI citation lift in the Princeton GEO methodology.

## Product

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg"
  ],
  "description": "Product description here",
  "sku": "SKU-12345",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "JPY",
    "price": "9800",
    "priceValidUntil": "2025-12-31",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Seller Name"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "123"
  }
}
</script>
```

## Article / Blog Post (prefer `BlogPosting` for blog content)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Article Title (max 110 characters)",
  "image": [
    "https://example.com/photos/1x1/photo.jpg"
  ],
  "datePublished": "2026-01-15T08:00:00+09:00",
  "dateModified": "2026-05-20T10:00:00+09:00",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author",
    "jobTitle": "Senior Engineer",
    "hasCredential": {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "certification",
      "name": "AWS Solutions Architect Professional"
    }
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "description": "Article description for search results"
}
</script>
```

`author.hasCredential` / `jobTitle` strengthen E-E-A-T signals — important after the **Google March 2026 Core Update** which weights author credential evidence more heavily on YMYL content (73% of top YMYL pages now show detailed author credentials vs 58% pre-update).

## FAQ

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is your return policy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "You can return any item within 30 days of purchase."
      }
    },
    {
      "@type": "Question",
      "name": "How long does shipping take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Standard shipping takes 3-5 business days."
      }
    }
  ]
}
</script>
```

## Breadcrumb

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://example.com/category"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Current Page",
      "item": "https://example.com/category/page"
    }
  ]
}
</script>
```

## Organization

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/company",
    "https://www.linkedin.com/company/company",
    "https://github.com/company"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+81-3-1234-5678",
    "contactType": "customer service",
    "availableLanguage": ["Japanese", "English"]
  }
}
</script>
```

## LocalBusiness

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "image": "https://example.com/photo.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "1-2-3 Shibuya",
    "addressLocality": "Shibuya-ku",
    "addressRegion": "Tokyo",
    "postalCode": "150-0001",
    "addressCountry": "JP"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 35.6595,
    "longitude": 139.7004
  },
  "telephone": "+81-3-1234-5678",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "18:00"
    }
  ]
}
</script>
```

## SoftwareApplication

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "App Name",
  "operatingSystem": "Web, iOS, Android",
  "applicationCategory": "ProductivityApplication",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "1000"
  }
}
</script>
```
