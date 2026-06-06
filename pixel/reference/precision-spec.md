# Precision Spec — 完全再現のためのデザイン値仕様システム

**Purpose:** マージン、余白、フォントサイズ、フォントウェイト、フォントカラーなど全デザイン値を体系的に抽出・カタログ化・検証し、ピクセル単位の完全再現を実現する。
**Read when:** モックアップから高忠実度のコードを生成する際、EXTRACT フェーズ直後に必ず読む。

## Contents
- Design Spec Sheet（仕様書フォーマット）
- Element-by-Element Extraction Protocol
- Precision Prompts
- CSS Variable System（全値のCSS変数化）
- Per-Property Verification Checklist
- Auto-Correction Loop

---

## Design Spec Sheet

モックアップから抽出した全デザイン値を**1つの構造化された仕様書**にまとめる。この仕様書がコード生成とVERIFYの唯一の正（Ground Truth）となる。

### フォーマット

```yaml
DESIGN_SPEC:
  meta:
    source: "[mockup filename]"
    viewport: "[width]px"
    extracted_at: "[ISO timestamp]"
    base_font_size: "16px"

  colors:
    # role: { value, confidence, used_in }
    bg-base:        { value: "#ffffff",  confidence: HIGH,   used_in: "page background" }
    bg-surface:     { value: "#f8fafc",  confidence: MEDIUM, used_in: "features section, footer" }
    bg-hero:        { value: "#0f172a",  confidence: HIGH,   used_in: "hero section" }
    text-heading:   { value: "#0f172a",  confidence: MEDIUM, used_in: "h1, h2, h3" }
    text-body:      { value: "#334155",  confidence: MEDIUM, used_in: "paragraph, list items" }
    text-muted:     { value: "#94a3b8",  confidence: MEDIUM, used_in: "meta, placeholder, caption" }
    text-inverse:   { value: "#ffffff",  confidence: HIGH,   used_in: "text on dark bg" }
    accent-primary: { value: "#6366f1",  confidence: MEDIUM, used_in: "CTA buttons, links" }
    accent-hover:   { value: "#4f46e5",  confidence: LOW,    used_in: "button hover (inferred)" }
    border-default: { value: "#e2e8f0",  confidence: MEDIUM, used_in: "card borders, dividers" }
    border-strong:  { value: "#cbd5e1",  confidence: LOW,    used_in: "pricing card outline" }

  typography:
    # element: { size, weight, line_height, letter_spacing, color_ref, confidence }
    hero-headline:
      size: "3.5rem"         # 56px
      weight: 800
      line_height: 1.1
      letter_spacing: "-0.02em"
      color_ref: "text-inverse"
      confidence: MEDIUM
    section-heading:
      size: "2.25rem"        # 36px
      weight: 700
      line_height: 1.2
      letter_spacing: "-0.01em"
      color_ref: "text-heading"
      confidence: MEDIUM
    sub-heading:
      size: "1.25rem"        # 20px
      weight: 600
      line_height: 1.4
      letter_spacing: "normal"
      color_ref: "text-heading"
      confidence: MEDIUM
    body:
      size: "1rem"           # 16px — baseline
      weight: 400
      line_height: 1.6
      letter_spacing: "normal"
      color_ref: "text-body"
      confidence: HIGH        # baseline assumption
    body-large:
      size: "1.125rem"       # 18px
      weight: 400
      line_height: 1.6
      letter_spacing: "normal"
      color_ref: "text-body"
      confidence: MEDIUM
    small:
      size: "0.875rem"       # 14px
      weight: 400
      line_height: 1.5
      letter_spacing: "normal"
      color_ref: "text-muted"
      confidence: MEDIUM
    button:
      size: "1rem"           # 16px
      weight: 600
      line_height: 1
      letter_spacing: "normal"
      color_ref: "text-inverse"
      confidence: MEDIUM
    nav-link:
      size: "0.875rem"       # 14px
      weight: 500
      line_height: 1
      letter_spacing: "normal"
      color_ref: "text-body"
      confidence: MEDIUM

  spacing:
    # name: { value, confidence, used_in }
    section-padding-y:     { value: "5rem",    confidence: MEDIUM, used_in: "section top/bottom padding" }
    section-padding-x:     { value: "1.5rem",  confidence: MEDIUM, used_in: "section left/right padding" }
    container-max-width:   { value: "72rem",   confidence: MEDIUM, used_in: "content container" }
    heading-to-body:       { value: "1rem",    confidence: MEDIUM, used_in: "h2 → paragraph gap" }
    heading-to-grid:       { value: "3rem",    confidence: MEDIUM, used_in: "h2 → grid/list gap" }
    grid-gap:              { value: "2rem",    confidence: MEDIUM, used_in: "feature grid, pricing grid" }
    card-padding:          { value: "2rem",    confidence: MEDIUM, used_in: "pricing card internal" }
    stack-gap:             { value: "0.5rem",  confidence: MEDIUM, used_in: "title → description inside card" }
    cta-padding-y:         { value: "0.75rem", confidence: MEDIUM, used_in: "button vertical padding" }
    cta-padding-x:         { value: "1.5rem",  confidence: MEDIUM, used_in: "button horizontal padding" }
    nav-height:            { value: "4rem",    confidence: MEDIUM, used_in: "navigation bar height" }
    nav-link-gap:          { value: "2rem",    confidence: MEDIUM, used_in: "space between nav links" }

  borders:
    # name: { radius, width, style, color_ref, confidence }
    button:    { radius: "0.5rem",   width: "0",   style: "none",  color_ref: null,             confidence: MEDIUM }
    card:      { radius: "1rem",     width: "1px", style: "solid", color_ref: "border-default", confidence: MEDIUM }
    input:     { radius: "0.375rem", width: "1px", style: "solid", color_ref: "border-default", confidence: MEDIUM }
    badge:     { radius: "9999px",   width: "0",   style: "none",  color_ref: null,             confidence: MEDIUM }

  shadows:
    # name: { value, confidence, used_in }
    card-featured: { value: "0 4px 24px rgba(0,0,0,0.1)", confidence: LOW, used_in: "featured pricing card" }
    nav:           { value: "0 1px 3px rgba(0,0,0,0.05)", confidence: LOW, used_in: "sticky nav shadow" }

  layout:
    # element: { type, columns, gap_ref, align, confidence }
    features-grid: { type: "grid", columns: 3, gap_ref: "grid-gap", align: "center", confidence: HIGH }
    pricing-grid:  { type: "grid", columns: 3, gap_ref: "grid-gap", align: "start",  confidence: HIGH }
    footer-grid:   { type: "grid", columns: "2fr 1fr 1fr 1fr", gap_ref: "grid-gap", align: "start", confidence: MEDIUM }
    hero-content:  { type: "flex",  columns: 1, gap_ref: null,      align: "center", confidence: HIGH }
```

---

## Element-by-Element Extraction Protocol

要素単位で値を特定する手順。各要素に対して**7つのプロパティ**を必ず記録する。

### The 7 Properties (全要素共通)

| # | Property | CSS対応 | 抽出方法 |
|---|----------|---------|---------|
| 1 | **Font Size** | `font-size` | ベースライン(16px)に対する比率で推定 |
| 2 | **Font Weight** | `font-weight` | 線の太さと対照比で判定: Thin(100)〜Black(900) |
| 3 | **Font Color** | `color` | 背景との対比から抽出。常にHEXで記録 |
| 4 | **Line Height** | `line-height` | テキスト行間の比率: 1.0(密)〜2.0(広) |
| 5 | **Margin** | `margin` | 隣接要素との外側距離。4方向を個別に記録 |
| 6 | **Padding** | `padding` | 要素内部の内側余白。4方向を個別に記録 |
| 7 | **Background** | `background` | 背景色、グラデーション、画像の有無 |

### 補助プロパティ（必要に応じて）

| Property | CSS対応 | いつ記録するか |
|----------|---------|--------------|
| Letter Spacing | `letter-spacing` | 見出しで明らかな文字間隔がある場合 |
| Text Transform | `text-transform` | 全大文字表記の場合 |
| Border Radius | `border-radius` | カード、ボタン、バッジ等 |
| Box Shadow | `box-shadow` | 浮いて見える要素 |
| Opacity | `opacity` | 半透明のオーバーレイ等 |
| Max Width | `max-width` | テキストコンテンツの折返し幅 |

### 抽出テンプレート（セクション別）

```
## [Section Name] の Design Spec

### 要素: [element name]
- font-size: [value] ([confidence])
- font-weight: [value] ([confidence])
- color: [hex] ([confidence])
- line-height: [value] ([confidence])
- margin-top: [value] ([confidence])
- margin-bottom: [value] ([confidence])
- padding: [top right bottom left] ([confidence])
- background: [value] ([confidence])
- border-radius: [value] ([confidence])   ← if applicable
- letter-spacing: [value] ([confidence])  ← if applicable
```

---

## Precision Prompts

### Master Extraction Prompt

以下のプロンプトをSCAN→EXTRACTの際にClaude Visionに使用する:

```
この画像は幅[VIEWPORT_WIDTH]pxのモックアップです。

以下の全要素について、指定プロパティをJSON形式で抽出してください。
本文テキストのfont-sizeを16pxとして、他の値を相対的に推定してください。
値は4pxグリッド（4の倍数）にスナップしてください。

対象要素:
1. ナビゲーションバー
2. ヒーローセクション見出し
3. ヒーローセクションサブテキスト
4. ヒーローCTAボタン
5. セクション見出し（h2）
6. 本文テキスト
7. カードコンポーネント
8. 小テキスト/メタテキスト
[...対象要素を全て列挙]

各要素について以下を記録:
{
  "element": "要素名",
  "font_size_px": 数値,
  "font_weight": 数値(100-900),
  "color": "#hex",
  "line_height": 数値(比率),
  "letter_spacing": "normal" or "値em",
  "margin_top_px": 数値,
  "margin_bottom_px": 数値,
  "padding": "top right bottom left (px)",
  "background": "#hex or gradient or none",
  "border_radius_px": 数値 or null,
  "confidence": "HIGH/MEDIUM/LOW"
}

推測できない値は null とし、confidence を LOW にしてください。
4pxグリッドに合わない値は最も近い4の倍数に丸めてください。
```

### 要素間スペーシング特化プロンプト

```
この画像の要素間距離を正確に測定してください。
本文テキストを16px、画像幅を[VIEWPORT_WIDTH]pxとして計算してください。

以下の間隔をpx単位で推定してください:
1. ナビバー下端 → ヒーロー見出し上端: ___px
2. ヒーロー見出し下端 → サブテキスト上端: ___px
3. サブテキスト下端 → CTAボタン上端: ___px
4. ヒーローセクション下端 → 次セクション上端: ___px
5. セクション見出し下端 → グリッド上端: ___px
6. グリッドアイテム間の水平ギャップ: ___px
7. グリッドアイテム間の垂直ギャップ: ___px
8. カード内: アイコン下端 → タイトル上端: ___px
9. カード内: タイトル下端 → 説明文上端: ___px
10. セクション内部パディング（上下左右）: ___px

全ての値を4pxグリッドに丸め、信頼度(HIGH/MEDIUM/LOW)を付けてください。
```

### フォントプロパティ特化プロンプト

```
この画像内の全てのテキスト要素について、フォントプロパティを詳細に分析してください。
画像幅は[VIEWPORT_WIDTH]pxです。本文テキストは16pxと仮定します。

各テキスト要素について:
1. font-size (px → rem換算も記載)
2. font-weight (100-900の数値。以下を目安に:
   - 400=Regular: 標準的な太さ
   - 500=Medium: やや太い
   - 600=SemiBold: 明らかに太い
   - 700=Bold: 太字
   - 800=ExtraBold: 非常に太い)
3. color (#HEX)
4. line-height (行間比率: テキストのサイズに対する行間の倍率)
5. letter-spacing (文字間隔: normal / 値em)
6. text-transform (none / uppercase / capitalize)
7. text-decoration (none / underline)
8. text-align (left / center / right)
9. max-width (テキストの折返し幅が制限されている場合)

特に以下の違いに注目してください:
- 見出しとサブ見出しの太さの差
- 本文とメタテキスト/キャプションの色の差
- CTA内テキストと通常テキストの違い
- ナビリンクのフォントサイズと太さ
```

### カラー差分特化プロンプト

```
この画像に含まれる全ての異なる色をリストアップしてください。

分類:
1. テキスト色（全て）:
   - 最も暗いテキスト色 → 見出し用
   - 標準的なテキスト色 → 本文用
   - 最も薄いテキスト色 → メタ/補足用
   - リンク色
   - CTA内テキスト色

2. 背景色（全て）:
   - メイン背景
   - 交互背景（セクション背景が切り替わる場合）
   - カード背景
   - CTA背景
   - ヒーロー/ダーク背景

3. ボーダー/ディバイダー色:
   - カード枠線
   - 水平線/区切り線
   - 入力フィールド枠線

4. アクセント色:
   - プライマリ（CTA）
   - セカンダリ（あれば）
   - ホバー状態（推定）

各色を#HEX形式で記録し、類似の色がある場合は同一色か別の色か明記してください。
例: text-heading(#0f172a) と text-body(#334155) は別の色です。
```

---

## CSS Variable System

Design Spec Sheet の全値を CSS Custom Properties として出力する。
**全てのマジックナンバーをCSS変数化**し、一括調整を可能にする。

### Generated Output Template

```css
/* ============================================
   DESIGN SPEC: CSS Variables
   Source: [mockup filename]
   Extracted: [timestamp]
   ============================================ */

:root {
  /* ── Colors ── */
  --color-bg-base:        #ffffff;         /* HIGH */
  --color-bg-surface:     #f8fafc;         /* MEDIUM */
  --color-bg-hero:        #0f172a;         /* HIGH */
  --color-text-heading:   #0f172a;         /* MEDIUM */
  --color-text-body:      #334155;         /* MEDIUM */
  --color-text-muted:     #94a3b8;         /* MEDIUM */
  --color-text-inverse:   #ffffff;         /* HIGH */
  --color-accent-primary: #6366f1;         /* MEDIUM */
  --color-accent-hover:   #4f46e5;         /* LOW */
  --color-border-default: #e2e8f0;         /* MEDIUM */
  --color-border-strong:  #cbd5e1;         /* LOW */

  /* ── Typography: Sizes ── */
  --text-hero:        3.5rem;    /* 56px  MEDIUM */
  --text-section:     2.25rem;   /* 36px  MEDIUM */
  --text-sub:         1.25rem;   /* 20px  MEDIUM */
  --text-body-lg:     1.125rem;  /* 18px  MEDIUM */
  --text-body:        1rem;      /* 16px  HIGH (baseline) */
  --text-sm:          0.875rem;  /* 14px  MEDIUM */
  --text-xs:          0.75rem;   /* 12px  LOW */

  /* ── Typography: Weights ── */
  --weight-regular:   400;
  --weight-medium:    500;
  --weight-semibold:  600;
  --weight-bold:      700;
  --weight-extrabold: 800;

  /* ── Typography: Line Heights ── */
  --leading-tight:    1.1;   /* hero headings */
  --leading-snug:     1.2;   /* section headings */
  --leading-normal:   1.4;   /* sub-headings */
  --leading-relaxed:  1.6;   /* body text */
  --leading-loose:    1.7;   /* long-form text */

  /* ── Typography: Letter Spacing ── */
  --tracking-tight:   -0.02em;  /* hero headline */
  --tracking-snug:    -0.01em;  /* section heading */
  --tracking-normal:  0;        /* body */
  --tracking-wide:    0.05em;   /* badges, uppercase labels */

  /* ── Spacing ── */
  --space-1:   0.25rem;  /* 4px  */
  --space-2:   0.5rem;   /* 8px  */
  --space-3:   0.75rem;  /* 12px */
  --space-4:   1rem;     /* 16px */
  --space-5:   1.25rem;  /* 20px */
  --space-6:   1.5rem;   /* 24px */
  --space-8:   2rem;     /* 32px */
  --space-10:  2.5rem;   /* 40px */
  --space-12:  3rem;     /* 48px */
  --space-16:  4rem;     /* 64px */
  --space-20:  5rem;     /* 80px */
  --space-24:  6rem;     /* 96px */

  /* ── Semantic Spacing ── */
  --section-padding-y: var(--space-20);  /* MEDIUM */
  --section-padding-x: var(--space-6);   /* MEDIUM */
  --container-max:     72rem;            /* MEDIUM */
  --heading-gap:       var(--space-4);   /* h → p gap MEDIUM */
  --heading-to-grid:   var(--space-12);  /* h → grid gap MEDIUM */
  --grid-gap:          var(--space-8);   /* MEDIUM */
  --card-padding:      var(--space-8);   /* MEDIUM */
  --stack-gap:         var(--space-2);   /* MEDIUM */
  --nav-height:        var(--space-16);  /* MEDIUM */

  /* ── Borders ── */
  --radius-sm:    0.375rem;  /* 6px — inputs */
  --radius-md:    0.5rem;    /* 8px — buttons */
  --radius-lg:    1rem;      /* 16px — cards */
  --radius-full:  9999px;    /* pills, badges */

  /* ── Shadows ── */
  --shadow-sm:   0 1px 3px rgba(0,0,0,0.05);
  --shadow-md:   0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg:   0 4px 24px rgba(0,0,0,0.1);
}
```

### 使用ルール

1. **マジックナンバー禁止**: コード内に直接 `16px` や `#334155` を書かない。必ず CSS 変数を参照する。
2. **変数名は意味で命名**: `--space-4` (汎用) と `--heading-gap` (セマンティック) の2層構造。
3. **信頼度コメント**: 各変数の横にHIGH/MEDIUM/LOWのコメントを残す。
4. **一括修正可能**: VERIFYで色が違うと判明したら、`:root` の1箇所を修正するだけで全要素に反映。

---

## Per-Property Verification Checklist

VERIFYフェーズで、Design Spec Sheet の各値が実装に正しく反映されているか検証する。

### Verification Prompt

スクリーンショット撮影後、以下のプロンプトでClaude Visionに検証を依頼:

```
モックアップ（1枚目）と実装スクリーンショット（2枚目）を比較し、
以下の各プロパティが一致しているか検証してください。

## テキスト検証
各テキスト要素について:
- [ ] font-size: モックアップと同じ大きさか？
- [ ] font-weight: 同じ太さか？（特にsemibold vs boldの区別に注意）
- [ ] color: 同じ色か？（特にheading色 vs body色の区別）
- [ ] line-height: 行間は同じか？
- [ ] letter-spacing: 文字間隔は同じか？（特に見出し）

## スペーシング検証
- [ ] セクション間の距離: 一致しているか？
- [ ] 見出しと本文の間隔: 一致しているか？
- [ ] カード内の余白: 一致しているか？
- [ ] グリッドアイテム間のギャップ: 一致しているか？
- [ ] CTAボタンのパディング: 一致しているか？

## カラー検証
- [ ] 背景色: セクションごとに正しいか？
- [ ] テキスト色: heading/body/mutedが正しく区別されているか？
- [ ] CTA色: ボタン背景色が正しいか？
- [ ] ボーダー色: カードや区切り線が正しいか？

差異がある項目について、実装のCSS修正値を具体的に提示してください。
例: "hero headline の font-weight を 700 → 800 に変更"
```

### Automated Check Script

```javascript
// verify-design-spec.js
// Design Spec Sheet の値と実装CSSを自動比較

const { chromium } = require('playwright');

async function verifyDesignSpec(htmlPath, designSpec) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(`file://${require('path').resolve(htmlPath)}`);
  await page.waitForLoadState('networkidle');

  const results = [];

  // CSS変数の実際の計算値を取得
  const computedVars = await page.evaluate(() => {
    const style = getComputedStyle(document.documentElement);
    return {
      colors: {
        'bg-base': style.getPropertyValue('--color-bg-base').trim(),
        'text-heading': style.getPropertyValue('--color-text-heading').trim(),
        'text-body': style.getPropertyValue('--color-text-body').trim(),
        'accent-primary': style.getPropertyValue('--color-accent-primary').trim(),
      }
    };
  });

  // 特定要素の計算済みスタイルを取得
  for (const selector of ['h1', 'h2', 'p', '.cta-button', '.nav__link']) {
    const computed = await page.evaluate((sel) => {
      const el = document.querySelector(sel);
      if (!el) return null;
      const cs = getComputedStyle(el);
      return {
        selector: sel,
        fontSize: cs.fontSize,
        fontWeight: cs.fontWeight,
        color: cs.color,
        lineHeight: cs.lineHeight,
        letterSpacing: cs.letterSpacing,
        marginTop: cs.marginTop,
        marginBottom: cs.marginBottom,
        paddingTop: cs.paddingTop,
        paddingBottom: cs.paddingBottom,
        paddingLeft: cs.paddingLeft,
        paddingRight: cs.paddingRight,
      };
    }, selector);

    if (computed) results.push(computed);
  }

  await browser.close();
  return results;
}
```

---

## Auto-Correction Loop

VERIFYで差異が検出された場合、Design Spec Sheet を参照して自動修正する。

### 修正フロー

```
1. VERIFY差分レポートを受け取る
2. 差異の種類を分類:
   a. CSS変数の値が間違い → :root の変数値を修正
   b. CSS変数の参照漏れ → マジックナンバーを変数参照に置換
   c. プロパティ自体の欠落 → プロパティを追加
3. 修正適用
4. 再スクリーンショット → 再比較
```

### 修正の優先順位

| Priority | Type | Impact | Fix Method |
|----------|------|--------|-----------|
| P0 | 色の間違い | 全体の印象が変わる | `--color-*` 変数値を修正 |
| P0 | font-weight の間違い | テキストの印象が変わる | `--weight-*` 変数値を修正 |
| P1 | font-size の間違い | 階層構造が崩れる | `--text-*` 変数値を修正 |
| P1 | セクション余白の間違い | ページリズムが崩れる | `--section-padding-*` を修正 |
| P2 | line-height の間違い | テキストの読みやすさ | `--leading-*` 変数値を修正 |
| P2 | 要素間スペーシングの間違い | 微細な配置ズレ | `--*-gap` / `margin` を修正 |
| P3 | letter-spacing | 見出しの印象 | `--tracking-*` を修正 |
| P3 | border-radius | コンポーネント形状 | `--radius-*` を修正 |
| P4 | box-shadow | 奥行き感 | `--shadow-*` を修正 |

### 修正プロンプト（REFINEフェーズ用）

```
以下の差異が検出されました。CSSの修正内容を具体的に出力してください。

差異リスト:
[差異のリストをここに挿入]

修正ルール:
1. :root のCSS変数値のみを変更する（個別セレクタのスタイルは変更しない）
2. 各修正について、変更前 → 変更後 を明記する
3. 1回の修正で複数の差異が解消される場合はまとめて記載する

例:
:root {
  --color-text-heading: #0f172a;  /* 変更前: #111827 → 変更後: #0f172a */
  --text-hero: 3.75rem;           /* 変更前: 3.5rem → 変更後: 3.75rem (60px) */
}
```

---

## Integration with SKILL.md Workflow

Design Spec Sheet は以下のフェーズで使用される:

| Phase | 役割 |
|-------|------|
| **EXTRACT** | Design Spec Sheet を作成する（このファイルの主な使用場面） |
| **COMPOSE** | Design Spec Sheet → CSS Variables → HTML/CSS コード生成 |
| **VERIFY** | Per-Property Verification Checklist で各値を検証 |
| **REFINE** | Auto-Correction Loop で CSS変数値を修正 |

### Required Output

EXTRACT完了時に以下を必ず生成:
1. **Design Spec Sheet** (YAML形式)
2. **CSS Variables file** (`:root { ... }`)
3. **Extraction confidence summary** (HIGH: N個, MEDIUM: N個, LOW: N個)
