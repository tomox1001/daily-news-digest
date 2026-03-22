# Search Strategy Reference

## Overview

This document defines the web search strategy for collecting fresh news (last 24–48 hours) across the 6 fixed sections. The goal is to find 14–18 high-quality articles with verifiable sources, quantitative data, and analytical depth.

Run searches **section by section**, with 3–4 parallel web searches per section. Always include a concrete date string (e.g., "February 11 2026") in every query to ensure freshness.

## Section 1: X(Twitter)で話題 — AI・テック最新バズ

Target cards: 2–3

`twitter-cli` を使ってAI・テック関連のバズ投稿を収集する。

```bash
# AI関連のバズ投稿を検索（いいね数でソート）
twitter search "AI" -t Latest --max 20 --json | jq '[.data[] | select(.metrics.likes > 500)] | sort_by(.metrics.likes) | reverse | .[:10]'

# エージェント・LLM関連
twitter search "AI agent OR LLM OR GPT" -t Latest --max 20 --json | jq '[.data[] | select(.metrics.likes > 300)]'

# 日本語のAIバズ
twitter search "AI 活用 OR 生成AI OR AIエージェント" -t Latest --max 20 --json | jq '[.data[] | select(.metrics.likes > 100)]'
```

選定基準:
- **エンゲージメント重視**: いいね数500以上、またはRT数100以上のバズ投稿を優先
- **情報の質**: 単なる感想ではなく、具体的な知見・データ・新発表を含む投稿
- **発信者の信頼性**: AI研究者、テック企業CEO、著名エンジニア、アナリストの投稿を優先
- 投稿内容が外部記事やスレッドの場合、元ソースもWebFetch/WebSearchで確認する

カード構成:
- **タイトル**: 投稿の核心を日本語で要約（発信者名を含む）
- **概要**: 投稿の内容＋文脈（なぜバズったか、背景情報）を3-5文で
- **メトリクス**: いいね数、RT数、表示数、フォロワー数
- **ソースリンク**: 投稿の固有URL（`https://x.com/username/status/ID`）

注意:
- `twitter-cli` が利用できない場合は、WebSearchで `site:x.com "AI" OR "GPT"` 等で代替する
- 個人の日常投稿・宣伝は除外し、業界知見を含む投稿のみ採用する

## Section 2: 企業・開発組織のAI活用 最新事例

Target cards: 2–3

Run 3–4 parallel searches:

```
"enterprise AI adoption case study [today's date month day year]"
"企業 AI活用 事例 [今日の日付]"
"AI transformation enterprise [today's date month day year]"
"developer tools AI coding [today's date month day year]"
```

Key sources to prioritize:
- McKinsey, Deloitte, BCG, Accenture reports
- Harvard Business Review, MIT Technology Review
- Nikkei, 日経ビジネス, ITmedia
- TechCrunch, The Information, VentureBeat

Topics of interest:
- 大企業のAI導入事例と成果（ROI、コスト削減率、生産性向上）
- 開発組織のAIツール活用（Copilot, Cursor, Devin等）
- AI導入の組織変革（CoE設立、データ戦略）
- 業界別の横展開パターン（金融、製造、ヘルスケア）
- 調査レポートの新版リリース（State of AI, AI Index等）

## Section 3: AI BPO — アウトソーシング革命

Target cards: 2

Run 3–4 parallel searches:

```
"AI BPO outsourcing [today's date month day year]"
"BPO automation artificial intelligence [today's date month day year]"
"business process outsourcing AI transformation [today's date month day year]"
"AI BPO market size growth [today's date month day year]"
```

Key sources to prioritize:
- Gartner, Forrester, Everest Group, HFS Research
- Bloomberg, Reuters, Financial Times
- a16z, Bain & Company, McKinsey
- Astute Analytica, Grand View Research (market data)

Topics of interest:
- AI BPO市場規模と成長予測（CAGR、TAM）
- 従来型BPOベンダーのAIピボット事例
- AIネイティブBPOスタートアップの台頭
- コスト削減と品質向上の定量データ
- 業界別BPO×AI（カスタマーサポート、経理、法務）
- アウトソーシングの「アンバンドリング→リバンドリング」トレンド

## Section 4: Product Hunt トレンド — 注目プロダクト

Target cards: 2

Run 2–3 parallel searches:

```
"Product Hunt trending [today's date month day year]"
"Product Hunt top products [this week/today]"
"Product Hunt AI tools launch [today's date month day year]"
```

Key sources to prioritize:
- Product Hunt (producthunt.com) — 直接アクセスが理想
- TechCrunch, TheNextWeb
- BetaList, HackerNews
- 各プロダクトの公式サイト

Topics of interest:
- 当日または直近24時間のTop Productsからピックアップ
- AI関連プロダクトを優先（ただし非AI有望プロダクトも可）
- Upvote数、コメント数など定量指標をメトリクスに含める
- プロダクトのユニークな差別化ポイントに注目
- ビジネスモデル（SaaS、API、フリーミアム等）
- LMビジネスやコンサルティング業への応用可能性

## Section 5: AI・テクノロジー 最新ニュース

Target cards: 3–5

Run 3–4 parallel searches:

```
"AI technology news [today's date month day year]"
"artificial intelligence [today's date month day year]"
"tech industry news [today's date month day year]"
"AI investment capex [today's date month day year]"
```

Key sources to prioritize:
- Bloomberg, Reuters, CNBC, Financial Times
- Axios, The Information, TechCrunch
- Fortune, Wired, MIT Technology Review
- ArsTechnica, The Verge

Topics of interest:
- AIモデルの新リリース、ベンチマーク、新機能
- Big TechのCapEx、投資動向、決算
- SaaS/ソフトウェア市場の動き
- AI規制とガバナンス
- AIインフラ（データセンター、チップ、エネルギー）
- AIスタートアップの資金調達

## Section 6: 政治・国際動向 ｜ LMビジネス視点

Target cards: 2–3

Run 3–4 parallel searches:

```
"Japan politics policy [today's date month day year]"
"Japan economy business [today's date month day year]"
"global politics business impact [today's date month day year]"
"regulation policy technology [today's date month day year]"
```

Key sources to prioritize:
- Japan Times, Nikkei Asia, NHK World
- Nippon.com, Mainichi English
- Al Jazeera, BBC, Reuters
- Bloomberg, Financial Times

Topics of interest:
- 日本の国内政治、選挙、内閣
- 財政・金融政策（日銀、予算、税制）
- 通商政策、日米関係
- ESG/サステナビリティ規制（SSBJ、ISSB）
- コーポレートガバナンス（CGコード改訂）
- 防衛・安全保障政策のビジネスへの影響

## Freshness Filtering

Every article must have a publication date within the last 24–48 hours. Strategies:

1. Include the specific date in search queries (e.g., "February 11 2026")
2. Look for date indicators in search result snippets
3. Cross-reference publication dates when visiting sources
4. If a story is older but has a fresh update/development, note both dates

## Quality Criteria

Each selected article should have:
- **Quantitative data**: At least 1–2 specific numbers, percentages, or metrics
- **Named sources**: Analyst quotes, official reports, or institutional data
- **Business relevance**: Clear connection to LM business or HR/organizational implications
- **Analytical depth**: Goes beyond headline-level reporting

## Market Data Collection

For the hero header market strip, search for the **4 fixed indicators**:

```
"日経平均 今日 終値 [today's date]"
"USD JPY exchange rate today [today's date]"
"S&P 500 closing price today [today's date]"
"AI BPO market size 2025 2026"
```

Fixed indicators:

| Indicator | Search Priority | Notes |
|-----------|----------------|-------|
| 日経平均 | 前営業日の終値 | 祝日・休場日は直近取引日 |
| USD/JPY | 直近の為替レート | 円高・円安の方向性を表示 |
| S&P 500 | 前営業日の終値 | 米国市場の温度感 |
| AI BPO市場 | 最新の市場規模推計 | CAGR等の成長率も表示 |
