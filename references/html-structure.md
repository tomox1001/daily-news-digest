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
    <!-- SECTION 1: X(Twitter)で話題 -->            [2 cards]
    <!-- SECTION 2: Google Trends 急上昇 -->         [1 card]
    <!-- SECTION 3: YouTube AI動画 -->               [1 card]
    <!-- SECTION 4: 中国SNSトレンド -->              [1 card]
    <!-- SECTION 5: AI効率 → ビジネス価値変換 -->    [2 cards]
    <!-- SECTION 6: AI BPO -->                       [2 cards]
    <!-- SECTION 7: Product Hunt トレンド -->        [2 cards]
    <!-- SECTION 8: AI・テクノロジー 最新ニュース --> [2–3 cards]
    <!-- SECTION 9: 政策・規制動向 -->               [1–2 cards]
    <!-- SECTION 10: 国内企業動向 -->                [2–3 cards]
    <!-- SECTION 11: HBR -->                         [1–2 cards]
    <!-- SECTION 12: Weekly EM/Product（月曜のみ） --> [2–3 cards]
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
    <p class="date">[YYYY]年[M]月[D]日（[曜日]）｜ X バズ × Google Trends × YouTube × 中国SNS × AI ROI × AI BPO × Product Hunt × AI Tech × 政策・規制 × 国内企業動向 × HBR</p>

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
- Always exactly 4 items in the fixed order: 日経平均, USD/JPY, S&P 500, AI BPO市場（2026-09-05までは AI RPO市場）
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
| 2 | Google Trends 急上昇 — AIキーワード速報 | gradient-1 | 📈 | tag-tech, tag-breaking |
| 3 | YouTube AI動画 — 海外テック深掘り | gradient-3 | ▶️ | tag-tech |
| 4 | 中国SNSトレンド — 36Kr / 虎嗅 | gradient-2 | 🇨🇳 | tag-market, tag-tech |
| 5 | AI効率 → ビジネス価値変換 グローバル事例 | gradient-3 | 💡 | tag-research, tag-market |
| 6 | AI BPO — 納品の自動化とアウトカム型デリバリー | gradient-2 | 🏭 | tag-market, tag-research |
| 7 | Product Hunt トレンド — 今週使えるエージェント／自動化ツール | gradient-4 | 🚀 | tag-tech |
| 8 | AI・テクノロジー 最新ニュース ｜ 自動化・開発生産性・コスト | gradient-1 | 🤖 | tag-tech, tag-breaking, tag-market |
| 9 | 政策・規制動向 ｜ 顧客需要とAIガバナンス | gradient-2 | 🌏 | tag-policy |
| 10 | 国内企業動向 ｜ 競合・隣接・スタートアップ | gradient-1 | 🏢 | tag-market, tag-breaking |
| 11 | HBR — マネジメント・戦略インサイト | gradient-3 | 📚 | tag-research, tag-hr |
| 12 | Weekly EM/Product インテリジェンス（月曜のみ） | gradient-4 | 🌐 | tag-research, tag-tech |

（2026-09-02更新: 6セクション時代の旧表を現行12セクションに差し替え。Section 10 を新設）
（2026-09-05更新: Section 6 を AI RPO→AI BPO に改名、Section 7・8・9 の副題をKR接続の焦点に合わせて変更。CSSクラス・グラデーション・絵文字は変更なし）

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
      <div class="impact-label">📊 KRへの接続</div>
      <p class="impact-text"><strong>[KRラベル]</strong>｜[3本柱またはKR指標]：[どう効くか1文]。[河野の打ち手1文]</p>
    </div>
    <div class="impact-box hr-impact">
      <div class="impact-label">👥 チーム／育成への示唆</div>
      <p class="impact-text">[直下15名のどの層・どの課題に効くか、誰に何を渡すか。2文まで]</p>
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
    <button class="share-btn" onclick="var s=this.querySelector('span');var c=this.closest('.news-card');navigator.clipboard.writeText(c.querySelector('h3').textContent.trim()+'\n'+c.querySelector('.source-link').href).then(function(){s.textContent='✓ 完了';this.classList.add('copied');setTimeout(function(){s.textContent='コピー';this.classList.remove('copied');}.bind(this),2000);}.bind(this));"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg><span>コピー</span></button>
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

EVERY card must have both impact boxes (CSS classes unchanged since the 2026-09-05 redesign; only the labels and content rules changed):
1. **KRへの接続** (lm-impact): 先頭に SKILL.md Step 0 のKR接続ラベル（`KR1 AI BPO` / `KR2 営業生産性` / `KR3 中継業務` / `SRE-LT` / `SRE-マスク` / `AXL` / `結節` / `育成`）を `<strong>` で置く。次に「受注率・粗利率・設置率、またはKR指標のどれに、どう効くか」を1文。最後に河野が取る打ち手（ゲート判定への同席、外部依頼の遮断、BU長・経営との結節、メンバーへの直接介入のいずれか）を1文
2. **チーム／育成への示唆** (hr-impact): 直下15名（DXU 9名・SREイネ 6名）のどの層・どの課題に効くか。能力開発（強化選手、要件定義力、AI以前の業界インプット）、26卒2名の立ち上げ、会議時間の制約、探索と実行の物差しの使い分けに接続する。LMIの人事部門や「企業のHR一般」への示唆は書かない

Each box should be 1–2 sentences. Use `<strong>` for the KR label and the key number.

The analysis should be specific and actionable. Do not write「注目すべき」「重要である」「〜すべき」「〜の検討が急務」— these hide who changes what. Name the KR, the metric, and the concrete move. A card whose KRへの接続 box cannot start with a label is rejected (except in Sections 9–11, where `結節` / `育成` is the label).

Example:
```html
<p class="impact-text"><strong>KR1 AI BPO</strong>｜粗利率：Cognizantが請求時間からアウトカム課金へ転換した事実は、ルーフ（AEPS）の価格30%減試作案を「業界標準への追随」として説明する根拠になる。8月頭の方針決定資料に競合事例として1枚追加する。</p>
```

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
- Target: 18–21 cards total across 11 sections (Mon: +2–3 for Section 12)
- Sections 1–4 (速報系): 2+1+1+1 = 5 cards max
- Section 5 (AI ROI): 2 / Section 6 (AI BPO): 2 / Section 7 (Product Hunt): 2
- Section 8 (AI/Tech): 2–3 / Section 9 (政策・規制): 1–2 / Section 10 (国内企業): 2–3 / Section 11 (HBR): 1–2
- Adjust based on the day's news importance, but never exceed 22 on a non-Monday

### Card Numbering
- Cards are numbered sequentially 01–15 across all sections
- Section 1 starts at 01, Section 2 continues from where Section 1 ended, etc.
- The number appears as a large watermark in the top-right corner of each card
- Section comments in HTML follow the pattern: `<!-- SECTION N: [Title] -->`
- Card comments follow the pattern: `<!-- Card N: [Title] -->`
