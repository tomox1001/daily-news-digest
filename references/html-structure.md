# HTML Structure Reference

## Overview

This document describes the exact HTML structure for the news digest output. The output is a single self-contained HTML file with embedded CSS (no external dependencies except Google Fonts).

## File Structure

```
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Daily News Digest — [DATE]</title>
  <style>[CSS from assets/template.css]</style>
</head>
<body>
  <header class="hero">...</header>
  <main class="container">
    <!-- SECTION 1: 企業・開発組織のAI活用 最新事例 -->
    [Cards 01–03]
    <!-- SECTION 2: AI BPO — アウトソーシング革命 -->
    [Cards 04–05]
    <!-- SECTION 3: Product Hunt トレンド — 注目プロダクト -->
    [Cards 06–07]
    <!-- SECTION 4: AI・テクノロジー 最新ニュース -->
    [Cards 08–12]
    <!-- SECTION 5: 政治・国際動向 ｜ LMビジネス視点 -->
    [Cards 13–15]
  </main>
  <footer class="footer">...</footer>
</body>
</html>
```

## Hero Header

```html
<header class="hero">
  <div class="hero-content">
    <div class="hero-badge">
      <span class="pulse"></span>
      DAILY INTELLIGENCE BRIEF
    </div>
    <h1>News Digest</h1>
    <p class="date">[YYYY]年[M]月[D]日（[曜日]）｜ 企業AI活用 × AI BPO × AI・テクノロジー × 政治・政策 × Product Hunt</p>

    <div class="market-strip">
      <!-- Fixed 4 market indicators -->
      <div class="market-item">
        <div>
          <div class="label">日経平均</div>
          <div class="value">[VALUE]円</div>
        </div>
        <span class="change up|down">[CHANGE TEXT]</span>
      </div>
      <div class="market-item">
        <div>
          <div class="label">USD/JPY</div>
          <div class="value">[VALUE]</div>
        </div>
        <span class="change up|down">[CHANGE TEXT]</span>
      </div>
      <div class="market-item">
        <div>
          <div class="label">S&amp;P 500</div>
          <div class="value">[VALUE]</div>
        </div>
        <span class="change up|down">[CHANGE TEXT]</span>
      </div>
      <div class="market-item">
        <div>
          <div class="label">AI BPO市場</div>
          <div class="value">[VALUE]</div>
        </div>
        <span class="change up|down">[CHANGE TEXT]</span>
      </div>
    </div>
  </div>
</header>
```

Market strip guidelines:
- Always exactly 4 items in the fixed order: 日経平均, USD/JPY, S&P 500, AI BPO市場
- Use class "up" (green) for positive, "down" (red) for negative
- Values should be concise (use abbreviations like $49.6B, ¥57,650)
- 祝日・休場日は直近取引日のデータを使い、その旨を記載する

## Section Header

```html
<!-- SECTION N: [Section Title] -->
<div class="section-header">
  <div class="section-icon" style="background: var(--gradient-N);">[EMOJI]</div>
  <div>
    <h2>[Section Title in Japanese]</h2>
    <span class="sub">[English subtitle] — [Date range] Sources</span>
  </div>
</div>
```

Section assignments (this order is fixed and intentional):

| # | Section | Gradient | Emoji | Tag Classes |
|---|---------|----------|-------|-------------|
| 1 | X(Twitter)で話題 — AI・テック最新バズ | gradient-4 | 🔥 | tag-breaking, tag-tech |
| 2 | AI効率 → ビジネス価値変換 グローバル事例 | gradient-3 | 💡 | tag-research, tag-market |
| 3 | AI BPO — アウトソーシング革命 | gradient-2 | 🏭 | tag-market, tag-research |
| 4 | Product Hunt トレンド — 注目プロダクト | gradient-4 | 🚀 | tag-tech |
| 5 | AI・テクノロジー 最新ニュース | gradient-1 | 🤖 | tag-tech, tag-breaking, tag-market |
| 6 | 政治・国際動向 ｜ LMビジネス視点 | gradient-2 | 🌏 | tag-policy |

## News Card

```html
<article class="news-card">
  <div class="card-accent" style="background: var(--gradient-N);"></div>
  <span class="number">[01–15]</span>
  <div class="card-tag [tag-class]">[EMOJI] [Date]</div>
  <h3>[Headline in Japanese]</h3>
  <p class="summary">
    [3–5 sentence summary with <strong> tags on key data points and phrases]
  </p>
  <div class="metrics">
    <!-- 2–4 metric pills -->
    <div class="metric">
      <span class="metric-label">[Label]</span>
      <span class="metric-value [up|down]">[Value]</span>
    </div>
  </div>
  <div class="impact-grid">
    <div class="impact-box lm-impact">
      <div class="impact-label">📊 LMビジネスへの影響</div>
      <p class="impact-text">[2–3 sentences with <strong> on key insights]</p>
    </div>
    <div class="impact-box hr-impact">
      <div class="impact-label">👥 HR／組織への示唆</div>
      <p class="impact-text">[2–3 sentences with <strong> on key insights]</p>
    </div>
  </div>
  <div class="card-footer">
    <a class="source-link" href="[URL]" target="_blank">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
        <polyline points="15,3 21,3 21,9"/>
        <line x1="10" y1="14" x2="21" y2="3"/>
      </svg>
      [Source Name] — [Article title abbreviated] ([Date])
    </a>
    <button class="share-btn" onclick="(function(b){var card=b.closest('.news-card');var h3=card.querySelector('h3').textContent.trim();var link=card.querySelector('.source-link').href;navigator.clipboard.writeText(h3+' '+link).then(()=>{b.textContent='✓ Copied!';b.classList.add('copied');setTimeout(()=>{b.textContent='Share';b.classList.remove('copied')},2000)});})(this)">Share</button>
  </div>
</article>
```

### Product Hunt Card Notes

Product Hunt cards follow the same structure but with these specifics:
- Tag class: `tag-tech`
- Gradient: `gradient-4`
- Metrics should include: Upvote数, コメント数, カテゴリ, 価格モデル
- Summary should cover: what the product does, its differentiator, pricing model
- Source link should point to the Product Hunt page or the product's official site

### Tag Classes

| Tag Class | Color | Use Case |
|-----------|-------|----------|
| tag-breaking | Red | Breaking/urgent news |
| tag-market | Blue | Market/financial data |
| tag-policy | Purple | Policy/regulation |
| tag-tech | Cyan | Technology/innovation |
| tag-hr | Green | HR/labor/workforce |
| tag-research | Orange | Research/reports |

### Gradient Assignments

Vary gradients across cards for visual diversity:
- gradient-1: Blue → Purple (primary, AI/tech)
- gradient-2: Orange → Red (alerts, market, BPO)
- gradient-3: Green → Cyan (positive, growth, enterprise)
- gradient-4: Purple → Red (policy, Product Hunt)

### Impact Analysis Boxes

EVERY card must have both impact boxes:
1. **LMビジネスへの影響** (lm-impact): How this news affects the consulting/LM business specifically
2. **HR／組織への示唆** (hr-impact): Implications for HR strategy, workforce, organization design

Each box should be 2–3 sentences. Use `<strong>` to highlight the key takeaway.

The analysis should be specific and actionable — not generic observations. Write at a level of granularity where the reader can bring the insight into a meeting the next day. Avoid phrases like「注目すべき」「重要である」and instead use concrete recommendations like「〜すべき」「〜の検討が急務」.

### Metrics Pills

Each card should have 2–4 metrics. Guidelines:
- Use specific numbers from the article
- Add "up" or "down" class to metric-value when directional
- Keep labels short (3–5 characters Japanese, or abbreviated English)
- Values should be formatted consistently (use ¥, $, %, etc.)

## Footer

```html
<footer class="footer">
  <div class="disclaimer">
    <p style="margin-bottom: 12px; color: var(--text); font-weight: 600; font-size: 14px;">
      Daily Intelligence Brief
    </p>
    <p>本レポートは公開情報源に基づくAI生成サマリーであり、
    投資助言や法的助言を構成するものではありません。
    正確性については各出典をご確認ください。</p>
    <p style="margin-top: 12px; opacity: 0.5;">
      Generated by Claude — [YYYY]年[M]月[D]日 — For internal use
    </p>
  </div>
</footer>
```

## Content Guidelines

### Language
- Headlines: Japanese
- Summaries: Japanese (with English terms/names kept as-is)
- Impact analysis: Japanese
- Source links: Match the original article language
- Metric labels: Japanese or abbreviated English

### Writing Style
- Summaries should be dense with data points, not vague
- Use bold (`<strong>`) for: dollar amounts, percentages, key statistics, company names in context, key phrases
- Each summary should tell a complete story in 3–5 sentences
- Impact boxes should be actionable, not just descriptive

### Card Count
- Target: 12–16 cards total across all 5 sections
- Section 2 (AI効率→価値変換): 2–3 cards
- Section 2 (AI BPO): 2 cards
- Section 3 (Product Hunt): 2 cards
- Section 4 (AI/Tech): 3–5 cards
- Section 5 (政治): 2–3 cards
- Adjust based on the day's news importance

### Card Numbering
- Cards are numbered sequentially 01–15 across all sections
- Section 1 starts at 01, Section 2 continues from where Section 1 ended, etc.
- The number appears as a large watermark in the top-right corner of each card
- Section comments in HTML follow the pattern: `<!-- SECTION N: [Title] -->`
- Card comments follow the pattern: `<!-- Card N: [Title] -->`
