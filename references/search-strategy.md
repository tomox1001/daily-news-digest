# Search Strategy Reference

## Overview

This document defines the web search strategy for collecting fresh news (last 24–48 hours) across the 12 fixed sections. The goal is to find 18–21 high-quality articles with verifiable sources, quantitative data, and a clear connection to the reader's KRs (see SKILL.md Step 0: `memory/context/current-focus.md` が正本).

2026-09-05にB案の見直しを実施した。変更点: Section 6をAI RPO→AI BPOへ、Section 2と9を各1枚に縮小、Section 7・8・10の収集条件をKR語で再定義、分析ボックスを「KRへの接続」「チーム／育成への示唆」へ置き換え。

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

## Section 2: Google Trends 急上昇 — AIキーワード速報（スキップ不可・1枚まで）

Target cards: 1

日本の一般検索の関心は河野の判断材料になりにくいため、1枚に絞る。優先順は ①KRに関わるツール・ベンダー・モデル価格の急上昇（例: Claude Codeの既定モデル切替、UiPath、RPA） ②メンバーが翌日話題にしそうな急上昇語の「正体」解説 ③それ以外。①②に該当しない日は、急上昇語を複数まとめて1枚にする。

Step 1.5 で取得した Google Trends の急上昇クエリをカード化する。

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

カード構成:
- **タイトル**: 急上昇キーワード＋なぜバズっているかの文脈
- **概要**: 急上昇の背景（新製品発表、事件、規制等）をWebSearchで裏取りして3-5文で解説
- **メトリクス**: 急上昇率（例: +227,350%）、関連キーワード、検索ボリューム推移
- **ソースリンク**: 急上昇の元となったニュース記事のURL

選定基準:
- 急上昇値 **10,000%以上** でも1枚まで。複数ある場合はKR接続の強い方を選び、残りはメトリクスに併記する
- 急上昇値 **1,000〜9,999%** → 複数まとめて1カード
- 急上昇の正体が「既に別セクションで扱う事象」の場合は、Section 2側は検索行動の切り口（検索急増の規模・混同の有無）に限定し、事象の本体は担当セクションに譲る
- pytrends がレート制限エラーの場合は30秒待って再実行。それでも失敗したら `WebSearch "Google Trends AI 急上昇 today"` で代替

## Section 3: YouTube AI動画 — 海外テック深掘り（スキップ不可）

Target cards: 1

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

カード構成:
- **タイトル**: 動画の核心を日本語で要約（チャンネル名＋再生数を含む）
- **概要**: 字幕から抽出した具体的な知見・手法・数値を3-5文で解説
- **メトリクス**: 再生数、チャンネル登録者数、投稿日
- **ソースリンク**: `https://www.youtube.com/watch?v=[VIDEO_ID]`

選定基準:
- 再生数10万以上の動画を優先
- 字幕（英語）の最初2,000文字をClaudeに渡して日本語で要約する
- 「具体的なツール・手法・数値を紹介している動画」を採用する（概論・宣伝系は除外）
- yt-dlpが失敗した場合は `WebSearch "YouTube AI [急上昇キーワード] 2026"` で代替してカードを生成

## Section 4: 中国SNSトレンド — 36Kr / 虎嗅（スキップ不可）

Target cards: 1–2

中国テック/AI市場の最新ニュースを36Krと虎嗅から直接取得する。

```
# 必須アクセス（WebFetchで直接取得）
WebFetch: https://36kr.com/information/AI/
WebFetch: https://www.huxiu.com/

# 補助検索（中国語クエリ）
"AI 商业价值 ROI [today's date]"
"AI效率 业务价值 案例 [today's date]"
"AI agent 中国 企业 [today's date]"

# WebFetch失敗時の代替
WebSearch: "36kr AI" OR "huxiu AI" [today's date]
WebSearch: "中国 AI 企業 事例 [today's date]"
```

Key sources:
- **36Kr**（36kr.com）— 中国テック/AIビジネス専門メディア
- **虎嗅**（huxiu.com）— 中国テック企業の深掘り分析

Topics of interest:
- 中国企業のAI活用による事業変革事例
- ByteDance、Alibaba、Baidu、Tencent等のAI戦略
- 中国AIスタートアップの資金調達・新プロダクト
- 中国AI規制・政策動向
- 中国のAI BPO・業務自動化・エージェント実装事例（KR1・KR3に接続できるもの）

カード構成:
- **タイトル**: 中国語元記事のタイトルを日本語に翻訳＋要約
- **概要**: 記事の核心を日本語3-5文で解説（定量データを必ず含める）
- **メトリクス**: 売上・ROI・ユーザー数など定量指標
- **タグ**: `🇨🇳 36Kr` または `🇨🇳 虎嗅` を使用
- **ソースリンク**: 元記事の固有URL

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
- **Section 5（AI ROI）・Section 6（AI BPO）・Section 8（AI/テック）のネタ探しに特に有効**
- 各セクションの記事収集前にこのページを WebFetch して当週のトピックを把握してから検索クエリを設計する

## Section 5: AI効率 → ビジネス価値変換 グローバル事例

Target cards: 2–3

**2言語で並列検索する（英語・日本語）:**

（中国語ソースは Section 4 で独立収集する）

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
```

Key sources to prioritize:
- McKinsey, Deloitte, BCG, Accenture reports（AI ROI・バリュー計測レポート）
- Harvard Business Review, MIT Technology Review
- Nikkei, 日経ビジネス, ITmedia
- Bloomberg, Reuters, Financial Times
- SHRM, HR Dive, People Matters（HR/CHRO向け）

Topics of interest:
- **AI投資のROI計測事例**（定量効果が明示されているもの優先）
- **「効率化→企業価値変換」の成功・失敗パターン**
- AI導入後に売上・利益に接続できた/できなかった企業の差異分析
- CHRO・CFOが語るAI価値変換の実態（人事・財務視点）
- 「AI効率は上がったが収益に繋がっていない」という逆説事例
- 業界別ROI実績（金融、製造、ヘルスケア、小売）
- 調査レポートの新版リリース（State of AI, AI Index, Gartner等）

## Section 6: AI BPO — 納品の自動化とアウトカム型デリバリー

Target cards: 2
KR接続: `KR1 AI BPO`（社員なしで回せる納品、粗利率向上、RPA/UiPath採否、価格30%減試作）

2026-09-05までは「AI RPO（採用アウトソーシング）」だったが、KR1の対象はBPO（納品業務の自動化）なので改めた。RPO（採用代行）の市場データは扱わない。

Run 3–4 parallel searches:

```
"AI BPO outcome-based pricing [today's date month day year]"
"business process outsourcing AI agents delivery [today's date month day year]"
"agentic automation RPA UiPath OR "Automation Anywhere" [today's date month day year]"
"BPO provider AI margin headcount [today's date month day year]"
"BPO AI エージェント 納品 自動化 [今日の日付]"
```

Key sources to prioritize:
- Everest Group, HFS Research, Gartner, Forrester（契約構造・課金モデルの分析）
- Bloomberg, Reuters, Financial Times（大手BPO・ITサービスの決算・方針転換）
- Cognizant, Accenture, Genpact, TCS, Infosys, トランスコスモス, ベルシステム24 の一次発表
- UiPath, Automation Anywhere, Microsoft Power Automate の製品・価格発表

Topics of interest（KR1のゲート判断に使えるものを優先）:
- 請求時間・FTE課金からアウトカム課金への転換事例と、その価格水準・粗利への影響
- 「人を介さずに回る納品」を実現したBPO・ITサービスの実装構成（RPA＋エージェント、監督者の配置）
- RPA/UiPathと生成AIエージェントの役割分担、採否判断に使える比較データ
- BPO事業者の人員計画（新卒採用の維持・削減、監督職の新設）
- AI化に伴うBPO契約の構造変化（SLA、知財帰属、責任範囲）
- 市場規模データは「AI in BPO」「intelligent process automation」の最新推計を使い、ヘッダー指標（AI BPO市場）と出典を揃える

## Section 7: Product Hunt トレンド — 注目プロダクト

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

選定基準（KR接続: `KR3 中継業務`・`SRE-LT`）:
- 当日または直近24時間のTop Productsから、**今週メンバーが試せるエージェント／自動化ツール**を選ぶ。順位よりも「中継業務（情報を誰かに届けるために発生している仕事）を代替できるか」「開発フロー（タスク管理・コードレビュー・QA）に入れられるか」を優先する
- 次点は、河野が経営との会話で引ける「AIネイティブなプロダクトの作り方・課金モデル」の事例
- 純粋な消費者向けアプリ、動画生成、画像生成は原則除外（KRに接続しない）
- Upvote数、コメント数、価格モデル、無料枠の有無をメトリクスに含める。「試用可否」（無料枠・セルフサーブで今日試せるか）を1つ入れる
- ビジネスモデル（SaaS、API、従量課金）と、既存ツール（Slack、Notion、GitHub、Jira）との接続可否を概要に書く

## Section 8: AI・テクノロジー 最新ニュース ｜ 自動化・開発生産性・コスト

Target cards: 2–3
KR接続: `KR1 AI BPO`・`KR3 中継業務`・`SRE-LT`（モデルの新発表そのものは対象外。価格・性能がツール選定やコスト計画を変える場合のみ採用）

Run 3–4 parallel searches（3つの枝を必ず1本ずつ回す）:

```
# 枝A: エージェント実装・自動化プラットフォーム（KR1・KR3）
"AI agent deployment enterprise workflow results [today's date month day year]"
"agentic automation platform launch OR pricing [today's date month day year]"

# 枝B: 開発生産性・コーディング／タスク管理エージェントの実測（SRE-LT）
"coding agent productivity study lead time [today's date month day year]"
"Claude Code OR Codex OR Copilot enterprise adoption metrics [today's date month day year]"

# 枝C: APIコスト・価格変動・供給制約（事前検死: OpenAIコスト超過×費用圧縮）
"LLM API pricing change OR rate limit [today's date month day year]"
"GPU cloud capacity price AI compute [today's date month day year]"
```

Key sources to prioritize:
- Bloomberg, Reuters, CNBC, Financial Times
- Axios, The Information, TechCrunch
- ArsTechnica, The Verge, MIT Technology Review
- 各社の公式ドキュメント・価格ページ（価格変更は一次ソースで確認）

Topics of interest:
- エージェントの本番導入事例と実測値（処理件数、エラー率、監督者の人数、削減した中継工程）
- タスク管理・コーディングエージェントのリードタイム／レビュー工数への効果データ
- LLM API・GPUクラウドの価格変動、レート制限、供給制約（コスト計画の前提を変えるもの）
- 自律エージェントの逸脱・安全性インシデント（導入提案の監査項目に直結）
- AIモデルの新リリースは、価格または性能がClaude Code／UiPath等の採否・コスト試算を変える場合に限る。Big TechのCapEx・決算、AIスタートアップの資金調達は「結節」ネタとして1枚まで

## Section 9: 政策・規制動向 ｜ 顧客需要とAIガバナンス

Target cards: 1–2
KR接続: `結節`・`AXL`（日銀・為替・内閣人事などのマクロ政治は原則対象外。顧客である人事部門・経営層の需要や、AI導入のガバナンス要件を動かすものに絞る）

Run 3 parallel searches:

```
"AI規制 OR AI事業者ガイドライン 改定 [今日の日付]"
"労働法制 OR 人的資本開示 OR 賃上げ 政策 企業 対応 [今日の日付]"
"リスキリング 助成金 OR 人材開発支援助成金 生成AI [今日の日付]"
"AI regulation enterprise compliance [today's date month day year]"
```

Key sources to prioritize:
- 経産省・厚労省・デジタル庁・個人情報保護委員会の一次発表
- Japan Times, Nikkei Asia, NHK World
- Reuters, Bloomberg, Financial Times（海外AI規制）

Topics of interest:
- 顧客企業の人事部門・経営層の需要を直接動かす政策（人的資本開示、労働法制、賃上げ税制、106万円の壁のような就業調整）
- AIリスキリング・人材育成の助成金・補助金（AXLの販売条件に直結）
- AI規制・ガイドライン改定（導入支援提案に載せるガバナンス要件）
- 日銀・為替・内閣人事は、顧客の投資判断（研修予算・IT予算の凍結）を直撃する場合のみ1枚。その場合も「顧客予算への影響」を先頭に書く

## Freshness Filtering（厳格運用）

**記事の鮮度は最重要基準。古いニュースの混入は品質を著しく下げる。**

- **最優先**: 24時間以内に公開された記事
- **許容**: 48時間以内の記事（24時間以内で十分な記事数が確保できない場合のみ）
- **禁止**: 48時間を超える記事（新たな展開・続報がない限り採用不可）

Strategies:

1. Include the specific date in search queries (e.g., "April 9 2026") — **当日の日付を必ず含める**
2. Look for date indicators in search result snippets — **公開日が明示されていない記事は採用しない**
3. Cross-reference publication dates when visiting sources — **元記事の日付を必ず目視確認する**
4. If a story is older but has a **fresh update/development within 24h**, note both dates and「続報」タグを付ける
5. 検索結果に古い記事しか出ない場合は、そのトピックを諦めて別のトピックを探す

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
"AI in BPO market size 2026" OR "intelligent process automation market size 2026"
```

Fixed indicators:

| Indicator | Search Priority | Notes |
|-----------|----------------|-------|
| 日経平均 | 前営業日の終値 | 祝日・休場日は直近取引日 |
| USD/JPY | 直近の為替レート | 円高・円安の方向性を表示 |
| S&P 500 | 前営業日の終値 | 米国市場の温度感 |
| BPO市場 | 最新の市場規模推計（BPO全体） | CAGR等の成長率と「AI・クラウドが牽引」の旨を表示。Section 6の出典と揃える。2026-09-05までは「AI RPO市場」だった |

## Section 10: 国内企業動向 ｜ 競合・隣接・スタートアップ（毎日・スキップ不可）

Target cards: 2–3

**目的:** 経営層がICCサミット等のクローズドな場で得ている「他社が今どう動いているか」を、公開一次情報で毎朝補う。
対象は LMI の直接競合、隣接領域（採用・AI面接、AI/DX支援、研修・リスキリング）、国内スタートアップの資金調達。

**正本:** `references/domestic-watchlist.json`（企業6グループ、キーワード8本、業界メディア5本。2026-09-05にBPO・RPA事業者と営業AIの2グループ、研修グループへの追加を実施）。
企業の追加・削除はこのJSONだけを編集する。Feedly用OPMLも同じファイルから生成するため、二重管理しない。

**Step A: 機械取得（必須）**

```bash
python3 scripts/domestic_watch.py fetch --hours 48 --markdown --out /tmp/domestic-watch.json
```

- 企業名とエイリアスを Google News RSS（`hl=ja&gl=JP`）で検索し、業界メディアのRSSと合わせて直近48時間分を一覧化する
- 出力はグループ別Markdown。JSONには title / link / pubDate / publisher / group / target が入る

**Step B: 候補の選定**

採用する記事の種類（優先順）:
1. 資金調達・M&A・上場（金額、ラウンド、リード投資家）
2. 決算・業績修正（売上、ARR、顧客数、チャーン）
3. 新商品・新機能の提供開始（特にサーベイ、AI面接、AI研修）
4. 大型導入事例・提携（導入社数、対象規模）
5. 経営層の人事・組織変更
6. ICC / IVS等カンファレンスの登壇・受賞
7. KR直結の動き。BPO事業者のAI化・アウトカム課金（`KR1`）、営業AIツールの導入事例と成果数値（`KR2`）、AI研修・リスキリングの法人導入と助成金活用（`AXL`）は、種類1〜6に当たらなくても採用候補にする

除外するもの: セミナー告知、単発のメディア掲載告知、受賞歴の焼き直し、採用広報。

毎日の2〜3枚のうち、少なくとも1枚は `結節`（直接競合・経営が話題にする企業）、もう1枚は `KR1`・`KR2`・`AXL` のいずれかに接続させる。

**Step C: 裏取り**

- Google News のリンクはリダイレクトURLなので、WebFetchで元記事に到達し、記事固有URLと数値を確認する
- プレスリリースは PR TIMES の元リリース（`prtimes.jp/main/html/rd/p/...`）をソースリンクにする
- 上場企業の決算は適時開示（TDnet）か IR ページの資料URLを優先する

**Step D: フォールバック**

- スクリプトがネットワーク失敗した場合は、直接競合グループ8社について `WebSearch "[企業名] [today's date]"` を実行する
- それでも該当がない日は、キーワードフィード（HRテック 資金調達 / AI面接 導入）かメディアフィード（BRIDGE・HRzine・HR NOTE）から1枚を選ぶ

カード構成:
- **タイトル**: 企業名＋何をしたか＋規模（例: 「PeoX、累計78億円調達 AI面接をアルバイト採用から侵食」）
- **概要**: 3-5文。事実（誰が・何を・いくらで）の後に、LMIの該当商品（MC / MCEM / DXL / AXL）との位置関係を1文添える
- **メトリクス**: 調達額、ARR、導入社数、成長率など
- **タグ**: `🏢 競合` `🏢 隣接` `🏢 調達` を内容で使い分ける。tag-market を基本にし、資金調達は tag-breaking
- **分析ボックス**: KRへの接続は「どの商品（MC／MCEM／DXL／AXL）の、どの顧客層が取られるか／取れるか」と、河野がBU長・経営との結節で使う一言を具体的に。チーム／育成への示唆は、直下メンバーの誰が何を学ぶべきかへの含意
- **ソースリンク**: 元記事またはプレスリリースの固有URL

注意:
- Vault内の言及が多い企業（Unipos、松尾研、LayerX）は既知情報の重複を避け、新しい動きだけを採用する
- 「他社が10倍と言っている」系の自己申告は、数値の根拠（工程・計測方法）が記事内にない限りメトリクスに使わない

## Section 11: HBR — マネジメント・戦略インサイト（毎日）

Target cards: 1–2

Harvard Business Review の日本語版・英語版から、EM/経営層に直結するマネジメント・戦略記事を収集する。

**検索クエリ（3並列）:**

```
# 日本語版
WebFetch: https://dhbr.diamond.jp/
"Harvard Business Review 日本語 マネジメント [today's date month year]"

# 英語版（AI・組織・リーダーシップに絞る）
"Harvard Business Review AI leadership management [today's date month day year]"
"HBR organizational transformation digital [today's date month day year]"
```

Key sources:
- **dhbr.diamond.jp** — HBR日本語版（ダイヤモンド社）
- **hbr.org** — HBR英語版

Topics of interest（河野さんのミッションに直結するテーマを優先）:
- **AI前提での事業構造変革**（トランスフォーメーション、ビジネスモデル再設計）
- **組織にAIを浸透させるチェンジマネジメント**
- **ピープルマネジメント**（評価、育成、昇格判断、チームビルディング）
- **プラットフォーム型組織設計**（エンジニアリング組織、DevEx、生産性エコシステム）
- **コスト構造変革・生産性向上**の経営フレームワーク
- **リーダーシップ・意思決定**の研究知見

カード構成:
- **タイトル**: 記事の核心を日本語で要約（著者の肩書きを含む）
- **概要**: 3-5文で主要な主張・フレームワーク・数値を抽出
- **メトリクス**: 調査サンプル数、効果の定量データ、対象企業数など
- **分析ボックス**: KRへの接続は `育成` または `結節` ラベルで、河野の関与の型（強化選手への直接介入、探索と実行の物差しの使い分け）に落とす。チーム／育成への示唆は直下15名の具体的な課題（要件定義力、AI以前の業界インプット、26卒立ち上げ）に接続する
- **ソースリンク**: 記事固有のURL

注意:
- 有料記事の場合はWebSearchでタイトル・要旨を推定し、読者が判断できる程度の概要を書く
- 英語記事は日本語で要約する

## Section 12: Weekly EM/Product インテリジェンス（月曜日のみ）

Target cards: 2–3

**このセクションは月曜日のみ生成する。火〜日はスキップ。**

過去1週間に公開された、世界のEM/プロダクトリーダー向けニュースレター・ブログの最新記事を収集する。

**対象ソース（4つの固定ソース）:**

| ソース | URL | 著者 | テーマ |
|--------|-----|------|--------|
| The Pragmatic Engineer | newsletter.pragmaticengineer.com | Gergely Orosz | EM組織論・Big Techの内部事情・エンジニアのキャリア |
| Lenny's Newsletter | lennysnewsletter.com | Lenny Rachitsky | プロダクトマネジメント・事業成長・指標設計 |
| One Useful Thing | oneusefulthing.org | Ethan Mollick（ウォートンスクール教授） | AI活用の組織浸透・教育・業務変革 |
| platformengineering.org | platformengineering.org/blog | コミュニティ | プラットフォームエンジニアリング・Developer Experience |

**検索クエリ（4並列）:**

```
# 各ソースの最新記事を検索
"pragmatic engineer" site:newsletter.pragmaticengineer.com OR site:blog.pragmaticengineer.com
"Lenny Rachitsky" site:lennysnewsletter.com OR site:substack.com
"Ethan Mollick" site:oneusefulthing.org OR site:substack.com
site:platformengineering.org blog OR "platform engineering" "internal developer"
```

**補助検索（ソースのRSSが取れない場合）:**

```
"pragmatic engineer newsletter this week"
"lenny newsletter latest"
"one useful thing ethan mollick latest"
"platform engineering blog latest"
```

選定基準:
- 過去7日以内に公開された記事を対象
- 各ソースから最低1記事、合計2-3カード
- 4ソースすべてに新記事がある場合は、河野さんのミッション（AI×組織変革、EM、DX）との関連度で優先順位付け

カード構成:
- **タイトル**: 記事タイトルの日本語訳＋著者名
- **概要**: 3-5文で日本語要約。具体的なフレームワーク・数値・事例を抽出
- **メトリクス**: Substack購読者数、記事のいいね数など（取得可能な場合）
- **分析ボックス**:
  - 📊 KRへの接続 — `SRE-LT`（開発リードタイム、タスク管理エージェント）または `育成`・`結節` ラベルで、DX推進・SREイネーブリングの具体的な打ち手に落とす
  - 👥 チーム／育成への示唆 — 15名のチームマネジメント（DX推進U/SREイネーブリングU）への適用アイデア。誰に、いつ、何を渡すかまで書く
- **ソースリンク**: 記事固有のURL

注意:
- 英語記事は必ず **日本語で要約** する
- 有料コンテンツの場合は公開部分のみを要約し「全文は有料」と注記する
- 月曜が祝日の場合も生成する（情報の空白を作らない）
