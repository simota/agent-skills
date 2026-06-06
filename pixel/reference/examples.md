# Usage Examples

**Purpose:** Practical examples of Pixel agent usage patterns.
**Read when:** You need to understand how to invoke Pixel or what to expect from its output.

## Contents
- Example 1: Full LP Reproduction
- Example 2: Single Section Reproduction
- Example 3: Verification Only
- Example 4: Responsive Conversion
- Example 5: Nexus Chain (Pixel → Growth → Artisan)

---

## Example 1: Full LP Reproduction

### User Request

```
このモックアップ画像からLPをHTML/CSSで再現してください。
[mockup-lp.png を添付]
```

### Pixel's Execution

**Phase 1: SCAN**
```
モックアップを分析しました。以下のセクションを識別:
1. Navigation (固定ヘッダー、ロゴ + 3リンク + CTAボタン)
2. Hero (フルブリード背景画像、見出し + サブライン + CTA)
3. Features (3カラムグリッド、アイコン + タイトル + 説明)
4. Pricing (3プランカード、中央がハイライト)
5. FAQ (6つのQ&A、アコーディオン形式)
6. CTA (コントラスト背景、見出し + ボタン)
7. Footer (4カラム、リンクグループ + コピーライト)
```

**Phase 2: EXTRACT**
```markdown
## Design Extraction Report

### Color Palette
| Role | Value | Confidence |
|------|-------|------------|
| bg-base | #ffffff | HIGH |
| bg-surface | #f8fafc | MEDIUM |
| bg-dark | #0f172a | HIGH |
| text-primary | #1e293b | MEDIUM |
| text-secondary | #64748b | MEDIUM |
| accent | #6366f1 | MEDIUM |
| accent-hover | #4f46e5 | LOW: inferred |

### Typography
| Element | Size | Weight | Confidence |
|---------|------|--------|------------|
| Hero h1 | 3.5rem | 800 | MEDIUM |
| Section h2 | 2rem | 700 | MEDIUM |
| Body | 1rem | 400 | HIGH |

### Layout
| Property | Value | Confidence |
|----------|-------|------------|
| Max-width | 72rem | MEDIUM |
| Feature grid | 3 columns | HIGH |
| Section padding | 5rem | MEDIUM |
```

**Phase 3: COMPOSE**

Generates `index.html` and `styles.css` with all sections.

**Phase 4: VERIFY**
```markdown
## Visual Comparison Report
- Fidelity Score: 87%
- CRITICAL: Hero gradient overlay missing (background appears flat)
- MODERATE: Pricing card shadow intensity too low
- MINOR: Feature icon size slightly larger than mockup
```

**Phase 5: REFINE (Iteration 1)**
```markdown
## Changes Applied
- Added linear-gradient overlay to hero background
- Increased box-shadow spread on pricing cards
- Adjusted feature icon size from 3rem to 2.5rem

## Updated Score: 93%
- No remaining CRITICAL differences
- 1 MODERATE: FAQ accordion indicator style differs
- 2 MINOR: subtle spacing differences
```

### Final Output

```markdown
## 完了報告

LP全体のHTML/CSS再現が完了しました。

### 生成ファイル
- `index.html` — 7セクション構成のLP
- `styles.css` — レスポンシブ対応CSS（モバイルファースト）

### 忠実度スコア: 93%
- 2回のイテレーションで最適化
- 残存差異: FAQ アコーディオンインジケーター形状（MODERATE）、微細な余白差（MINOR x2）

### デザイン値
- HIGH信頼度: 5値
- MEDIUM信頼度: 12値
- LOW信頼度: 3値（フォントファミリー、ホバー色、影の正確な値）

### 推奨次ステップ
- → **Artisan**: React/Tailwindコンポーネントに変換
- → **Growth**: SEOメタタグ追加、CTA最適化
- → **Muse**: 抽出した色・余白をデザイントークン体系化
```

---

## Example 2: Single Section Reproduction

### User Request

```
このスクリーンショットのPricingセクションだけをHTML/CSSで再現してください。
React + Tailwindで出力してください。
[pricing-section.png を添付]
```

### Pixel's Output

```tsx
// PricingSection.tsx
interface PricingPlan {
  name: string;
  price: number;
  period: string;
  features: string[];
  cta: string;
  featured?: boolean;
}

interface PricingSectionProps {
  heading: string;
  plans: PricingPlan[];
}

function PricingSection({ heading, plans }: PricingSectionProps) {
  return (
    <section className="py-20 px-6" id="pricing">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center text-gray-900">
          {heading}
        </h2>
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-2xl p-8 text-center ${
                plan.featured
                  ? 'bg-indigo-600 text-white shadow-xl scale-105' /* MEDIUM: accent color */
                  : 'border border-gray-200 bg-white'
              }`}
            >
              {plan.featured && (
                <span className="inline-block text-xs font-semibold uppercase tracking-wide bg-white/20 text-white px-3 py-1 rounded-full mb-4">
                  Most Popular
                </span>
              )}
              <h3 className={`text-xl font-semibold ${plan.featured ? 'text-white' : 'text-gray-900'}`}>
                {plan.name}
              </h3>
              <div className="mt-4">
                <span className="text-5xl font-bold">${plan.price}</span>
                <span className={`text-base ${plan.featured ? 'text-white/70' : 'text-gray-500'}`}>
                  /{plan.period}
                </span>
              </div>
              <ul className="mt-6 space-y-3 text-left">
                {plan.features.map((feature) => (
                  <li key={feature} className={`text-sm ${plan.featured ? 'text-white/90' : 'text-gray-600'}`}>
                    ✓ {feature}
                  </li>
                ))}
              </ul>
              <a
                href="#"
                className={`mt-8 block w-full py-3 rounded-lg font-semibold transition-colors ${
                  plan.featured
                    ? 'bg-white text-indigo-600 hover:bg-gray-100'
                    : 'bg-indigo-600 text-white hover:bg-indigo-700'
                }`}
              >
                {plan.cta}
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

```markdown
## 忠実度スコア: 91%
- MEDIUM: アクセント色 #6366f1 推定、正確な値は要確認
- MINOR: カードのborder-radius 微差（1rem vs 推定）
```

---

## Example 3: Verification Only

### User Request

```
既存のindex.htmlとこのモックアップを比較して、差分を教えてください。
[mockup.png を添付]
```

### Pixel's Output

```markdown
## Visual Comparison Report

### Overview
- **モックアップ**: mockup.png
- **実装**: index.html
- **忠実度スコア**: 78%

### CRITICAL (要修正)
| # | 箇所 | モックアップ | 実装 | 修正方法 |
|---|------|------------|------|---------|
| 1 | Hero背景 | グラデーション(紺→紫) | 単色(#1a1a2e) | `background: linear-gradient(135deg, #1e1b4b, #4c1d95)` |
| 2 | Featuresレイアウト | 3カラム均等 | 2カラム + 余白 | `grid-template-columns: repeat(3, 1fr)` |

### MODERATE (改善推奨)
| # | 箇所 | モックアップ | 実装 | 修正方法 |
|---|------|------------|------|---------|
| 1 | Section間余白 | ~96px | 64px | `padding: 6rem 0` |
| 2 | CTAボタン角丸 | ~12px | 4px | `border-radius: 0.75rem` |
| 3 | 見出しサイズ | ~36px | 30px | `font-size: 2.25rem` |

### MINOR (微細)
| # | 箇所 | 差異 |
|---|------|------|
| 1 | Footer背景 | 微妙な色味差 (#111827 vs #0f172a) |
| 2 | テキスト行間 | わずかに異なる (1.5 vs 1.6) |

### 推奨アクション
CRITICALを修正すれば90%+に到達可能です。修正しますか？
```

---

## Example 4: Responsive Conversion

### User Request

```
このデスクトップモックアップをモバイルファーストで実装してください。
[desktop-mockup.png を添付]
```

### Pixel's Output

```markdown
## レスポンシブ変換レポート

### ブレークポイント設計 (MEDIUM confidence)
| Breakpoint | 幅 | 主な変更 |
|------------|-----|---------|
| Mobile (base) | ~375px | 1カラム、縮小タイポ、縦積みCTA |
| Tablet (md) | 768px+ | 2カラムグリッド、サイドナビ表示 |
| Desktop (lg) | 1024px+ | 3カラム、フルモックアップレイアウト |

### 変換判断 (モックアップにないため推定)
- ナビゲーション: 768px未満でハンバーガーメニュー
- Hero CTAボタン: 768px未満で縦並び
- Pricingカード: 768px未満で1カラムスタック、ハイライトカードのscale解除
- Footer: 768px未満で1カラム

### 注意事項
⚠️ モバイルビューはモックアップに含まれていないため、
全てのモバイル固有の判断はMEDIUM以下の信頼度です。
デザイナーとの確認を推奨します。
```

---

## Example 5: Nexus Chain (Pixel → Growth → Artisan)

### Nexus AUTORUN Context

```yaml
_AGENT_CONTEXT:
  Role: Pixel
  Task: LP mockup reproduction with SEO optimization
  Mode: AUTORUN
  Chain: [Vision]
  Input: "/path/to/lp-mockup.png"
  Constraints:
    - React + Tailwind
    - Fidelity target: 90%
  Expected_Output: HTML/CSS code ready for Growth optimization
```

### Pixel's _STEP_COMPLETE

```yaml
_STEP_COMPLETE:
  Agent: Pixel
  Status: SUCCESS
  Output:
    deliverable: "/project/src/pages/landing.tsx"
    artifact_type: "HTML/CSS Reproduction"
    parameters:
      framework: "React + Tailwind"
      fidelity_score: "92%"
      iterations_used: 2
      confidence_breakdown:
        high_values: 6
        medium_values: 14
        low_values: 3
    files_changed:
      - path: "src/pages/landing.tsx"
        type: created
        changes: "Full LP page component with 7 sections"
      - path: "src/styles/landing.css"
        type: created
        changes: "Custom CSS for non-Tailwind values"
  Handoff:
    Format: PIXEL_TO_GROWTH_HANDOFF
    Content:
      page_type: "Landing Page"
      sections: ["nav", "hero", "features", "pricing", "testimonials", "faq", "cta", "footer"]
      headings:
        - { level: "h1", text: "Transform Your Workflow" }
        - { level: "h2", text: "Features", "Pricing", "FAQ" }
      cta_buttons:
        - { text: "Get Started Free", location: "hero" }
        - { text: "Start Your Trial", location: "final-cta" }
  Artifacts:
    - "src/pages/landing.tsx"
    - "src/styles/landing.css"
    - "screenshots/comparison-report.md"
  Risks:
    - "Font family unconfirmed (LOW confidence: Inter assumed)"
    - "Mobile layout assumptions without mobile mockup"
  Next: Growth
  Reason: "LP code ready — needs SEO meta tags, JSON-LD, heading optimization"
```
