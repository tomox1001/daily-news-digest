---
name: daily-news-digest
description: >
  毎朝の日次ニュースダイジェストをHTML形式で自動生成するスキル。5つの固定セクションでAI・ビジネス・政治のニュースを網羅し、
  各記事にLMビジネスへの影響とHR/組織への示唆の分析ボックスを付与する。
  Use this skill whenever the user asks for: ニュースダイジェスト, daily news digest, 今日のニュース,
  朝のブリーフィング, daily briefing, morning report, news summary, intelligence brief,
  or any request for a curated AI/business news summary. Also trigger when asked to
  "ダイジェストを作って", "ニュースまとめて", "run the digest", or similar.
  Output is a self-contained HTML file with a white-based light theme, responsive card layout, and embedded CSS.
---

# Daily News Digest Skill

毎朝24時間以内の鮮度の高いニュースを収集し、プロフェッショナルなHTMLダイジェストを生成する。
5セクション・12-16カードで構成され、全カードに定量データと2つの分析ボックスを付与する。

## 6つの固定セクション（この順番を維持する）

| # | セクション | カード目安 | アイコン | グラデーション |
|---|-----------|----------|---------|-------------|
| 1 | X(Twitter)で話題 — AI・テック最新バズ | 2-3 | 🔥 | gradient-4 |
| 2 | AI効率 → ビジネス価値変換 グローバル事例 | 2-3 | 💡 | gradient-3 |
| 3 | AI BPO — アウトソーシング革命 | 2 | 🏭 | gradient-2 |
| 4 | Product Hunt トレンド — 注目プロダクト | 2 | 🚀 | gradient-4 |
| 5 | AI・テクノロジー 最新ニュース | 3-5 | 🤖 | gradient-1 |
| 6 | 政治・国際動向 ｜ LMビジネス視点 | 2-3 | 🌏 | gradient-2 |

セクション順は意図的にこの順番に設定されている。Xのバズ投稿はリアルタイム性が最も高いため先頭に置き、
マクロな政治ニュースは参考情報として末尾に配置する。

## ワークフロー

### Step 1: 日付の取得

```bash
date "+%Y年%m月%d日（%a）"
```

日付は以下すべてに使用する：HTMLタイトル、ヒーローヘッダー、ファイル名（`news-digest-YYYY-MM-DD.html`）、検索クエリ。

### Step 1.5: Google Trends でトレンドキーワードを把握（検索前に必ず実行）

ニュース収集の前に、当日の急上昇AIキーワードを把握して検索クエリを最適化する。

```python
/usr/local/bin/python3 -c "
from pytrends.request import TrendReq
t = TrendReq(hl='ja-JP', tz=540)
# 主要AIキーワードの急上昇関連クエリ
t.build_payload(['Claude Code', 'ChatGPT', 'AIエージェント', 'Gemini'], timeframe='now 7-d', geo='JP')
rq = t.related_queries()
for kw in ['Claude Code', 'ChatGPT', 'AIエージェント', 'Gemini']:
    rising = rq.get(kw, {}).get('rising')
    if rising is not None and not rising.empty:
        print(f'=== {kw} 急上昇 ===')
        print(rising.head(5).to_string(index=False))
"
```

- 急上昇クエリに出てきたトピックはSection 1・Section 5の検索クエリに必ず組み込む
- 急上昇値が10,000%以上のキーワードは「今日の最重要トレンド」として優先的にカードを作る
- `trending_searches` は404になるため使用しない（`related_queries` で代替）

### Step 2: ニュース収集

`references/search-strategy.md` を読み、セクションごとの検索戦略に従う。

収集のルール：
- セクションごとに **3-4件の並列Web検索** を実行する
- 検索クエリには必ず **具体的な日付** を含め、24-48時間以内の記事を確保する
- **定量データ**（金額、割合、成長率、ROI）を含む記事を優先する
- 同じストーリーを複数ソースで裏取りする
- **記事の完全なURLを必ず記録する**（ドメインレベルではなく記事固有のパス。例: `nikkei.com/article/DGXZQO...` ）
- 検索結果のスニペットだけでなく、**元記事を実際に閲覧して数値・事実を確認する**
- Section 2では **英語・日本語・中国語の3言語** で検索を実行する（中国語ソース: 36Kr, 虎嗅 を必ず参照）

**Section 1（Xバズ）の補助ソース:**

HackerNews と YouTube は Section 1 の補足として使う。詳細な手順は `references/search-strategy.md` を参照。

```bash
# HackerNews トップ記事（AI関連をフィルタ）
python3 -c "
import urllib.request, json
ids = json.loads(urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/topstories.json').read())[:30]
for id in ids:
    item = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{id}.json').read())
    title = item.get('title','').lower()
    if any(kw in title for kw in ['ai','llm','gpt','claude','gemini','agent','openai']):
        print(f'[{item.get(\"score\",0)}pts] {item.get(\"title\")} | {item.get(\"url\",\"\")[:60]}')
"

# YouTube字幕取得（Step 1.5で見つかった急上昇キーワードで検索）
/Users/tomonori-kawano/Library/Python/3.11/bin/yt-dlp \
  "ytsearch3:[急上昇キーワード] 2026" \
  --print "%(id)s | %(view_count)s | %(title)s" --skip-download
# → 上位動画のIDで字幕取得
/Users/tomonori-kawano/Library/Python/3.11/bin/yt-dlp \
  "https://www.youtube.com/watch?v=[VIDEO_ID]" \
  --write-auto-subs --sub-lang en,ja --skip-download --output "/tmp/yt-digest"
```

### Step 2.5: 記事URL収集（Kawanoピックアップ）

ニュース検索と並行して、以下の **3つのソース** から当日〜前日のURLを収集する。

#### ソース①: Xブックマーク（最優先）

```bash
~/.local/bin/twitter bookmarks --max 30 --json | jq '[.data[] | select(.time >= "YYYY-MM-DDT00:00:00")] | .[:20]'
```

- **当日および前日** にブックマークした投稿を対象とする
- 投稿本文・添付リンク・引用元URLをすべて抽出する
- いいね数・RT数などエンゲージメント指標もメトリクスとして記録する

#### ソース②: Slack DM

| ソース | チャンネルID | 検索方法 |
|--------|------------|---------|
| 河野智則のDM | D014PLLHBCH | `slack_search_public_and_private` で `has:link in:<@U014B8E83NX> after:YYYY-MM-DD` |
| #times_kawano | C01529F00NP | `slack_read_channel` で直近メッセージからURL付きメッセージを抽出 |

#### 共通収集ルール：
- X(Twitter)リンク、note記事、ブログ記事、ニュース記事などすべてのURLを収集
- 各URLの内容をWebFetchまたはWebSearchで確認し、タイトルと概要を取得する
- 取得できない場合（403等）は検索でタイトル・概要を推定する
- 3ソース合計で重複するURLは1件にまとめる

収集した記事は、HTMLダイジェストの **最後のセクション（5つの固定セクションの後）** に
「📌 Kawano ピックアップ」セクションとして追加する。通常のニュースカードとは異なるが、
**読むだけで内容が把握できるレベル** まで充実させる：

#### 表示ルール
1. **タイトル** — 記事の核心が伝わる具体的なタイトルにする。アカウント名だけ・URLの貼り付けだけはNG。
   - ❌ `@ai_jitan — 業務効率化テック`
   - ✅ `えーたん(@ai_jitan) — NotebookLM×GPT-5「最高峰の推論術」、Gemini×スライド爆速作成20選`
   - ❌ `Paweł Huryn — PM向けAIエージェント`
   - ✅ `PM向け無料Deep Researchエージェント — 12並列リサーチャーが60サイトを30秒で調査`
2. **概要（3〜5行）** — 以下の情報を盛り込む：
   - **誰が**（発信者の経歴・フォロワー規模など文脈情報）
   - **何を主張/紹介しているか**（具体的な手法・数値・フレームワーク名）
   - **なぜ注目か**（バズった理由、閲覧数、他ニュースとの関連性など）
3. **タグ** — 内容に合わせたタグを使う（BLOG / AI AGENT / AI TIPS / 調査レポート / NEWSPICKS 等）。「X POST」一辺倒にしない。
4. **ソースURL** — 投稿の具体的パーマリンク（ステータスURL）を使用する。

#### 調査方法
- X投稿は `WebSearch` で `"アカウント名" site:x.com` を検索し、プロフィール・直近投稿内容を把握する
- ブログ記事は `WebFetch` で本文を取得。失敗時は `WebSearch` で記事タイトル・要約を収集する
- NewsPicks等の有料記事は `WebSearch` でタイトル・要旨を推定する

記事URLが1件も見つからなかった場合は、このセクション自体を省略する。

### Step 3: 市場データの収集

ヒーローヘッダーの市場ストリップに表示する **4つの指標** を収集する。固定指標：

| 指標 | 例 | 補足 |
|------|-----|------|
| 日経平均 | 57,650円 ▲1,500円高 | 前営業日の終値 |
| USD/JPY | 154.41 ▼円高進行 | 為替動向 |
| S&P 500 | 6,998 ▲7,000目前 | 米国市場の温度感 |
| AI BPO市場 | $49.6B ▲CAGR 34.3% | ダイジェストのテーマに直結する市場規模 |

市場データは当日or前営業日の最新値を使う。祝日・休場日は直近取引日のデータを使用し、その旨を記載する。

### Step 4: HTMLの構築

`references/html-structure.md` を読み、HTMLの完全な構造リファレンスに従う。

`assets/template.css` を読み、HTMLの `<style>` タグにCSSを埋め込む。

カード構成の必須要素（1枚も省略しない）：
- 左端アクセントバー（色分けグラデーション）
- 番号ウォーターマーク（01〜16、右上、薄い）
- カテゴリタグ（絵文字＋日付）
- **日本語の見出し**（20px、bold）
- **要約文**（3-5文、データリッチ、`<strong>` でキー数値を強調）
- **メトリクスピル**（2-4個の定量データ）
- **分析ボックス2つ**（全カード必須）：
  - 📊 LMビジネスへの影響 — コンサルティング/LM事業への具体的影響
  - 👥 HR／組織への示唆 — 人事・組織設計の観点からの示唆
- ソースリンク（外部リンクSVGアイコン付き）— **必ず記事固有のURL**を使用（ドメインルートNG）

分析ボックスは「一般論」ではなく **具体的なアクションアイテム** を書く。
「注目すべき」「重要である」のような抽象的な結論は避け、「〜すべき」「〜の検討が急務」のように
読者が翌日の会議で使える粒度にする。

### Step 4.5: ファクトチェック＆ソース検証（HTML生成後、保存前に必ず実行）

生成されたHTMLの品質を保証するため、以下の検証を行う。

**数値データの検証：**
- 各カードの **金額・割合・人数等の定量データ** を元ソースと照合する
- 検索結果に含まれていない数値（AIが推測・捏造した可能性のあるもの）は削除または修正する
- 特に「〇〇%削減」「〇〇社が導入」「〇〇億ドル規模」のような具体的数値は必ず裏取りする
- **数値の出典が特定できないものは使わない**。概算値を使う場合は「約」「推定」等を付記する

**ソースリンクの検証：**
- 全15カードのソースリンクが **記事固有のURL** であることを確認する（ドメインルート不可）
- 正しいパターン: `https://nikkei.com/article/DGXZQOUA0861M0Y6A200C2000000/`
- NGパターン: `https://nikkei.com` , `https://nikkei.com/business`
- Step 2の検索時に記録したURLをそのまま使用する
- URLが不明な記事は、タイトル＋メディア名で再検索して正確なURLを取得する

**事実の整合性チェック：**
- 企業名・人名・日付の表記ミスがないか確認する
- 「史上最高値」「過去最大」等の最上級表現は検索で裏取りしてから使う
- 同じイベントを扱う複数カード間でデータの矛盾がないか確認する

### Step 5: 保存・配信

ファイル名パターン：
```
news-digest-YYYY-MM-DD.html
```

ユーザーのdocs/ディレクトリに保存し、`computer://` リンクで即時プレビュー可能にする。

### Step 6: インデックスの更新

`news-digest-index.html` の `digests` 配列の **先頭** に新しいエントリを追加する。

```javascript
{
  date: "YYYY-MM-DD",
  weekday: "曜日",
  file: "news-digest-YYYY-MM-DD.html",
  cards: カード枚数,
  highlights: ["トップニュース1", "トップニュース2", "トップニュース3", "トップニュース4"],
  gradient: "g1"  // g1〜g4をローテーション
},
```

highlights には当日のダイジェストから特に重要な4件のトピックを短く抽出する。
gradient は日付ごとに g1→g2→g3→g4 のローテーションで割り当てる。

## 記述ガイドライン

### 言語
- 見出し・要約・分析ボックス：**日本語**
- 企業名・固有名詞・英語の技術用語：英語のまま保持（例：Product Hunt, Deloitte, CAGR）
- ソースリンクのテキスト：元記事の言語に合わせる
- メトリクスラベル：日本語または略語英語（混在OK）

### ビジュアルデザイン
- テーマ：**ホワイト基調のライトテーマ**（CSS変数 `--bg: #f5f7fa; --surface: #ffffff;`）
- ヒーローヘッダーのみダークネイビーグラデーション
- カードごとにグラデーションを変えて視覚的多様性を確保
- タグクラスの使い分け：tag-breaking（赤）, tag-market（青）, tag-policy（紫）, tag-tech（シアン）, tag-hr（緑）, tag-research（オレンジ）

## リソース

- `references/search-strategy.md` — セクション別の検索クエリ戦略、ソース優先度、鮮度フィルタリング
- `references/html-structure.md` — HTML構造の完全リファレンス（各コンポーネントのコード例付き）
- `assets/template.css` — HTMLに埋め込むCSSテンプレート
- `news-digest-index.html` — 全ダイジェストのアーカイブインデックス（同じdocs/ディレクトリに配置）
