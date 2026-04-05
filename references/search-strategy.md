# Search Strategy Reference

## Overview

This document defines the web search strategy for collecting fresh news (last 24–48 hours) across the 6 fixed sections. The goal is to find 14–18 high-quality articles with verifiable sources, quantitative data, and analytical depth.

Run searches **section by section**, with 3–4 parallel web searches per section. Always include a concrete date string (e.g., "February 11 2026") in every query to ensure freshness.

## Step 1.5: Google Trends（検索前に必ず実行）

**ツール:** `/usr/local/bin/python3` + `pytrends`（インストール済み）

```python
/usr/local/bin/python3 -c "
from pytrends.request import TrendReq
t = TrendReq(hl='ja-JP', tz=540)
t.build_payload(['Claude Code', 'ChatGPT', 'AIエージェント', 'Gemini', 'OpenAI'], timeframe='now 7-d', geo='JP')
rq = t.related_queries()
for kw in ['Claude Code', 'ChatGPT', 'AIエージェント', 'Gemini', 'OpenAI']:
    rising = rq.get(kw, {}).get('rising')
    if rising is not None and not rising.empty:
        print(f'=== {kw} 急上昇クエリ ===')
        print(rising.head(5).to_string(index=False))
        print()
"
```

活用方法:
- 急上昇値 **10,000%以上** → Section 1・Section 5の最優先トピック
- 急上昇値 **1,000〜9,999%** → 各セクションの検索クエリに組み込む
- 急上昇クエリに知らないキーワードが出た場合 → WebSearchで即確認してカード候補にする
- `trending_searches()` は404エラーになるため使用しない（`related_queries()` で代替）

注意: pytrendsはレート制限に引っかかることがある。エラーが出た場合は30秒待って再実行。

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

### Section 1 補助ソース①: HackerNews API

Section 1 の補足として、開発者コミュニティで話題のAIトピックを取得する。

```python
python3 -c "
import urllib.request, json
ids = json.loads(urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/topstories.json').read())[:30]
ai_kws = ['ai','llm','gpt','claude','gemini','agent','openai','anthropic','model','neural']
results = []
for id in ids:
    item = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{id}.json').read())
    title = item.get('title','').lower()
    if any(kw in title for kw in ai_kws):
        results.append({'score': item.get('score',0), 'title': item.get('title'), 'url': item.get('url',''), 'id': id})
results.sort(key=lambda x: x['score'], reverse=True)
for r in results[:5]:
    print(f'[{r[\"score\"]}pts] {r[\"title\"]}')
    print(f'  {r[\"url\"] or \"https://news.ycombinator.com/item?id=\"+str(r[\"id\"])}')
"
```

- スコア200pt以上は単独カード候補として扱う
- ソースリンクは `https://news.ycombinator.com/item?id=XXXXX` を使う
- HNで話題 → 1〜2週間後に日本のXでバズるパターンが多いため「先取りネタ」として有効

### Section 1 補助ソース②: YouTube字幕

Step 1.5（Google Trends）で把握した急上昇キーワードを使って海外AI動画を検索し、字幕を取得する。

```bash
# Step 1: 動画を検索して再生数TOP3を取得
/Users/tomonori-kawano/Library/Python/3.11/bin/yt-dlp \
  "ytsearch5:[急上昇キーワード e.g. claude code tutorial] 2026" \
  --print "%(id)s | %(view_count)s views | %(title)s" \
  --skip-download 2>/dev/null

# Step 2: 最も再生数の多い動画の字幕を取得
/Users/tomonori-kawano/Library/Python/3.11/bin/yt-dlp \
  "https://www.youtube.com/watch?v=[VIDEO_ID]" \
  --write-auto-subs --sub-lang en,ja --skip-download \
  --output "/tmp/yt-digest" 2>/dev/null

# Step 3: VTTをテキストに変換して要約
python3 -c "
import re, glob
for f in glob.glob('/tmp/yt-digest*.vtt'):
    content = open(f).read()
    text = re.sub(r'<[^>]+>', '', content)
    text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> .*\n', '', text)
    text = re.sub(r'\n+', ' ', text).strip()
    print(text[:2000])
"
```

選定基準:
- 再生数10万以上の動画を優先
- 字幕（英語）の最初2,000文字をClaudeに渡して日本語で要約する
- 「具体的なツール・手法・数値を紹介している動画」を採用する（概論・宣伝系は除外）

## Kawanoピックアップ — Xブックマーク収集

Step 2.5 で使用するXブックマーク取得コマンド：

```bash
# 直近30件のブックマークを取得（JSON形式）
~/.local/bin/twitter bookmarks --max 30 --json

# 日付フィルタリング（前日以降）
~/.local/bin/twitter bookmarks --max 30 --json | jq '[.data[] | select(.time >= "YYYY-MM-DDT00:00:00Z")]'

# コンパクト表示（LLMコンテキスト節約）
~/.local/bin/twitter -c bookmarks --max 30
```

選定基準：
- ブックマーク日時が **当日または前日** のものを対象とする
- 投稿本文に含まれるURLを優先的に抽出し、WebFetch/WebSearchで内容を確認する
- X投稿そのものがコンテンツの場合（スレッド・長文等）は投稿URLをソースリンクとして使用する
- 重複URL（Slack DM側にも同じURLがある場合）は1件に統合する

注意：
- `~/.local/bin/twitter` はフルパスで指定する（PATH未設定のため）
- 認証はブラウザCookieから自動取得（Chrome/Arc等でx.comにログイン済みであること）

## AIエージェント専門ニュースソース（全セクション共通）

**必ずアクセスするソース:**

```
WebFetch: https://aiagentstore.ai/ai-agent-news/this-week
```

- 毎週（月〜日）のAIエージェント関連ニュースを日次更新で集約
- エンタープライズAI導入・セキュリティ・市場動向・技術革新・規制政策を横断カバー
- ROI・コスト・導入規模などの具体的数値を含む実装志向の記事が多い
- **Section 2（企業AI活用）・Section 3（AI BPO）・Section 5（AI/テック）のネタ探しに特に有効**
- 各セクションの記事収集前にこのページを WebFetch して当週のトピックを把握してから検索クエリを設計する

## Section 2: AI効率 → ビジネス価値変換 グローバル事例

Target cards: 2–3

**3言語で並列検索する（英語・日本語・中国語）:**

```
# 英語
"AI ROI business value [today's date month day year]"
"AI productivity to revenue conversion [today's date month day year]"
"AI business value realization enterprise [today's date month day year]"
"AI efficiency ROI measurement [today's date month day year]"

# 日本語
"AI ROI 成果 事例 [今日の日付]"
"AI 生産性 価値変換 [今日の日付]"
"AI投資 効果 ビジネス成果 [今日の日付]"

# 中国語（必須アクセスソース）
WebFetch: https://36kr.com/information/AI/
WebFetch: https://www.huxiu.com/
"AI 商业价值 ROI [today's date]"
"AI效率 业务价值 案例 [today's date]"
```

Key sources to prioritize:
- McKinsey, Deloitte, BCG, Accenture reports（AI ROI・バリュー計測レポート）
- Harvard Business Review, MIT Technology Review
- Nikkei, 日経ビジネス, ITmedia
- Bloomberg, Reuters, Financial Times
- **36Kr**（36kr.com）— 中国テック/AIビジネス専門メディア
- **虎嗅**（huxiu.com）— 中国テック企業の深掘り分析
- SHRM, HR Dive, People Matters（HR/CHRO向け）

Topics of interest:
- **AI投資のROI計測事例**（定量効果が明示されているもの優先）
- **「効率化→企業価値変換」の成功・失敗パターン**
- AI導入後に売上・利益に接続できた/できなかった企業の差異分析
- CHRO・CFOが語るAI価値変換の実態（人事・財務視点）
- 「AI効率は上がったが収益に繋がっていない」という逆説事例
- 中国企業のAI活用による事業変革事例（英語・中国語問わず）
- 業界別ROI実績（金融、製造、ヘルスケア、小売）
- 調査レポートの新版リリース（State of AI, AI Index, Gartner等）

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
