---
name: daily-news-digest
description: >
  毎朝の日次ニュースダイジェストをHTML形式で自動生成するスキル。12の固定セクション（うち1つは月曜のみ）でAI・ビジネス・政治・国内企業動向・EM/組織のニュースを網羅し、
  各記事に「KRへの接続」（河野のKR・TopMTG3本柱への接続）と「チーム／育成への示唆」の分析ボックスを付与する。
  Use this skill whenever the user asks for: ニュースダイジェスト, daily news digest, 今日のニュース,
  朝のブリーフィング, daily briefing, morning report, news summary, intelligence brief,
  or any request for a curated AI/business news summary. Also trigger when asked to
  "ダイジェストを作って", "ニュースまとめて", "run the digest", or similar.
  Output is a self-contained HTML file with a white-based light theme, responsive card layout, and embedded CSS.
---

# Daily News Digest Skill

毎朝24時間以内の鮮度の高いニュースを収集し、プロフェッショナルなHTMLダイジェストを生成する。
12セクション（うちSection 12は月曜のみ）・18-21カードで構成され、全カードに定量データと2つの分析ボックスを付与する。

読者は河野智則（LMI プロダクトデザイン室 DX推進U・SREイネーブリングU UM、直下15名）1人。
ダイジェストの目的は「業界の動きを知ること」ではなく、**河野のKRとTopMTG報告の3本柱（受注率・粗利率・設置率）に効く情報を毎朝届けること**。
2026-09-05に見直し（B案）を実施した。それ以前は「LMビジネスへの影響／HR・組織への示唆」の2軸で、直近7日139カードのうち3本柱の語を含むカードが0枚、KR2（営業生産性）に触れるカードが1枚という偏りがあった。

## Step 0: 読者の役割とKRを読み込む（毎回・最初に実行）

以下のファイルを読み、当Qのミッション・KR・関与の型を把握する。このファイルが正本であり、SKILL.md側にKRの中身を書き写さない（四半期が変わっても自動で追従させるため）。

```
Read: /Users/tomonori-kawano/Documents/Obsidian Vault/memory/context/current-focus.md
```

読み取った内容から、その日の **KR接続ラベル** の一覧を作る。ラベルは分析ボックス（Step 4）で使う。2026 3Q時点の例:

| ラベル | 接続先 |
|-------|--------|
| `KR1 AI BPO` | 社員なしで回せる納品、粗利率向上、RPA/UiPath採否 |
| `KR2 営業生産性` | 営業MGRのアポ数・設置率、BU長PDCA |
| `KR3 中継業務` | 情報を届けるための仕事のエージェント代替、AIネイティブ度 |
| `SRE-LT` | 開発リードタイム削減、タスク管理・コーディングエージェント |
| `SRE-マスク` | 退会企業マスクの工数・頻度改善 |
| `AXL` | AIリスキリング新規事業、商品ライン3軸、検証顧客 |
| `結節` | BU長・経営との会話に使う他社動向・政策（KRに直接効かないが河野の役割として必要） |
| `育成` | 直下15名の能力開発、強化選手、要件定義力、26卒立ち上げ |

current-focus.md の内容が古い（更新日から3か月超）場合は、その旨をSlack通知の末尾に1行添える。

## 12の固定セクション（この順番を維持する）

| # | セクション | カード目安 | アイコン | グラデーション | 頻度 | 主なKR接続 |
|---|-----------|----------|---------|-------------|------|-----------|
| 1 | X(Twitter)で話題 — AI・テック最新バズ | 2 | 🔥 | gradient-4 | 毎日 | 結節・育成（メンバーが話題にするもの） |
| 2 | Google Trends 急上昇 — AIキーワード速報 | 1 | 📈 | gradient-1 | 毎日 | 結節 |
| 3 | YouTube AI動画 — 海外テック深掘り | 1 | ▶️ | gradient-3 | 毎日 | SRE-LT・KR3（実装手法の解説） |
| 4 | 中国SNSトレンド — 36Kr / 虎嗅 | 1 | 🇨🇳 | gradient-2 | 毎日 | 結節 |
| 5 | AI効率 → ビジネス価値変換 グローバル事例 | 2 | 💡 | gradient-3 | 毎日 | KR1・KR2（効率→収益の接続事例） |
| 6 | AI BPO — 納品の自動化とアウトカム型デリバリー | 2 | 🏭 | gradient-2 | 毎日 | KR1 |
| 7 | Product Hunt トレンド — 今週使えるエージェント／自動化ツール | 2 | 🚀 | gradient-4 | 毎日 | KR3・SRE-LT |
| 8 | AI・テクノロジー 最新ニュース ｜ 自動化・開発生産性・コスト | 2-3 | 🤖 | gradient-1 | 毎日 | KR1・KR3・SRE-LT |
| 9 | 政策・規制動向 ｜ 顧客需要とAIガバナンス | 1-2 | 🌏 | gradient-2 | 毎日 | 結節・AXL |
| 10 | 国内企業動向 ｜ 競合・隣接・スタートアップ | 2-3 | 🏢 | gradient-1 | 毎日 | 結節・KR1・KR2・AXL |
| 11 | HBR — マネジメント・戦略インサイト | 1-2 | 📚 | gradient-3 | 毎日 | 育成・結節 |
| 12 | Weekly EM/Product インテリジェンス | 2-3 | 🌐 | gradient-4 | **月曜のみ** | SRE-LT・育成 |

セクション順は意図的にこの順番に設定されている。Section 1-4はソース別の速報セクション（X・Google Trends・YouTube・中国SNS）で
リアルタイム性が高い順に配置。Section 5-10はトピック別の分析セクション。Section 11-12はEM/経営層向けの深掘りセクション。

**重要: Section 2-4（Google Trends・YouTube・中国SNS）は独立セクションであり、スキップ不可。ただし各1枚まで。**
速報系3セクションで合計3枚を超えない。ソースが取得不可の場合のみ、WebSearchで代替ソースを検索して補完する。

**カードの採用基準（2026-09-05から）**: 全カードにStep 0のKR接続ラベルを最低1つ付ける。ラベルが付けられないカードは、Section 9・10・11（結節・育成が主目的）以外では不採用にし、別候補に差し替える。「面白いが河野の判断を変えない」ニュース（モデルの新発表そのもの、マクロ経済の日次変動、著名人の一般論）は、価格・性能がツール選定やコスト計画を変える場合に限って採用する。

**Section 10（国内企業動向）もスキップ不可。** 2026-09-02に追加した。目的は、経営層がICC等の場で得ている「他社が今どう動いているか」の情報を、公開一次情報（プレスリリース・資金調達・決算・導入事例）で毎朝補うこと。
収集は `references/domestic-watchlist.json` を正本とし、`scripts/domestic_watch.py fetch` で Google News RSS と業界メディアRSSを機械的に取得してから、候補をWebFetchで裏取りする。
詳細は `references/search-strategy.md` の Section 10 を参照。

**Section 12は月曜日のみ生成する。** 火〜日はSection 11まで。月曜日かどうかは Step 1 の日付取得で曜日を判定する。

## ワークフロー

### Step 1: 日付の取得（Step 0の後に実行）

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

- 急上昇クエリに出てきたトピックはSection 1・Section 8の検索クエリに必ず組み込む
- 急上昇値が10,000%以上のキーワードは「今日の最重要トレンド」として優先的にカードを作る
- `trending_searches` は404になるため使用しない（`related_queries` で代替）
- **Google Trendsの実行結果はSection 2（Google Trends 急上昇）のカード生成に必ず使用する**

### Step 2: ニュース収集

`references/search-strategy.md` を読み、セクションごとの検索戦略に従う。

収集のルール：
- セクションごとに **3-4件の並列Web検索** を実行する
- 検索クエリには必ず **当日の具体的な日付** を含め、**24時間以内** の記事を最優先で採用する
- 48時間を超える記事は採用禁止（新たな続報がある場合のみ例外、その場合は「続報」タグを付ける）
- **各カードの元記事の公開日を必ず目視確認し、古い記事が混入しないようにする**
- **定量データ**（金額、割合、成長率、ROI）を含む記事を優先する
- 同じストーリーを複数ソースで裏取りする
- **記事の完全なURLを必ず記録する**（ドメインレベルではなく記事固有のパス。例: `nikkei.com/article/DGXZQO...` ）
- 検索結果のスニペットだけでなく、**元記事を実際に閲覧して数値・事実を確認する**
- Section 5では **英語・日本語・中国語の3言語** で検索を実行する

**Section 1（Xバズ）の補助ソース — HackerNews:**

HackerNews は Section 1 の補足として使う。詳細な手順は `references/search-strategy.md` を参照。

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
```

**Section 3（YouTube AI動画）の収集（スキップ不可）:**

Step 1.5で見つかった急上昇キーワードを使って海外AI動画を検索・字幕取得する。

```bash
# YouTube検索（急上昇キーワードで検索）
/Users/tomonori-kawano/Library/Python/3.11/bin/yt-dlp \
  "ytsearch5:[急上昇キーワード] 2026" \
  --print "%(id)s | %(view_count)s views | %(title)s" --skip-download
# → 再生数10万以上の上位動画のIDで字幕取得
/Users/tomonori-kawano/Library/Python/3.11/bin/yt-dlp \
  "https://www.youtube.com/watch?v=[VIDEO_ID]" \
  --write-auto-subs --sub-lang en,ja --skip-download --output "/tmp/yt-digest"
```

- 字幕（英語）の最初2,000文字を要約してカードにする
- yt-dlpが失敗した場合は `WebSearch "YouTube AI [急上昇キーワード] 2026"` で代替

**Section 4（中国SNSトレンド）の収集（スキップ不可）:**

36Kr と 虎嗅 から中国AI/テック市場の最新ニュースを取得する。

```
# 必須アクセス（WebFetchで直接取得）
WebFetch: https://36kr.com/information/AI/
WebFetch: https://www.huxiu.com/

# 補助検索（中国語クエリ）
"AI 商业价值 ROI [today's date]"
"AI效率 业务价值 案例 [today's date]"
"AI agent 中国 企业 [today's date]"
```

- WebFetchが失敗した場合は `WebSearch "36kr AI" OR "huxiu AI"` で代替
- 中国企業のAI活用事例・市場動向・規制を中心にカードを生成
- 最低1枚は必ず生成すること

**Section 10（国内企業動向）の収集（スキップ不可）:**

```bash
# ウォッチリスト全社と業界メディアの直近48時間分を機械取得（Markdown一覧を標準出力に出す）
python3 scripts/domestic_watch.py fetch --hours 48 --markdown --out /tmp/domestic-watch.json
```

- 出力の一覧から「資金調達・決算・新商品・大型導入・提携・経営層の人事」に該当する記事を選び、元記事をWebFetchで裏取りしてカード化する
- 同じ企業の複数記事は1枚にまとめる。1日2〜3枚、最低1枚
- 直接競合グループ（アトラエ・カオナビ・SmartHR・識学など）の動きは、他グループより優先して採用する
- 該当が薄い日はキーワードフィード（HRテック資金調達・AI面接導入）やメディアフィード（BRIDGE・HRzine）の記事で補う
- スクリプトが失敗した場合は、ウォッチリストの直接競合8社について `WebSearch "[企業名] [today's date]"` を実行して代替する

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
「📌 Kawano ピックアップ」セクションとして追加する（9つの固定セクションの後）。通常のニュースカードとは異なるが、
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
| AI BPO市場 | $XX.XB ▲CAGR XX% | KR1（AI BPO・粗利率）に直結する市場規模。「AI in BPO」「intelligent process automation」市場の最新推計を使い、出典を採用日ごとに記録する。同じ推計を使い続けてよいが、調査会社を変えるときはカード本文（Section 6）の出典と一致させる |

2026-09-05まで4つ目の指標は「AI RPO市場」（採用アウトソーシング）だった。KR1の対象はBPO（納品の自動化）であり別物のため差し替えた。過去ファイルのRPO表記は修正しない。

市場データは当日or前営業日の最新値を使う。祝日・休場日は直近取引日のデータを使用し、その旨を記載する。

### Step 4: HTMLの構築

`references/html-structure.md` を読み、HTMLの完全な構造リファレンスに従う。

`assets/template.css` を読み、HTMLの `<style>` タグにCSSを埋め込む。

カード構成の必須要素（1枚も省略しない）：
- 左端アクセントバー（色分けグラデーション）
- 番号ウォーターマーク（01〜22、右上、薄い）
- カテゴリタグ（絵文字＋日付）
- **日本語の見出し**（20px、bold）
- **要約文**（3-5文、データリッチ、`<strong>` でキー数値を強調）
- **メトリクスピル**（2-4個の定量データ）
- **分析ボックス2つ**（全カード必須。CSSクラスは従来の `lm-impact` / `hr-impact` をそのまま使う）：
  - 📊 KRへの接続（`lm-impact`）— 先頭にStep 0のラベルを `<strong>` で置き、続けて「3本柱（受注率・粗利率・設置率）またはKR指標のどれに、どう効くか」を1文、最後に河野が取る打ち手を1文。例: `<strong>KR1 AI BPO</strong>｜粗利率：Cognizantが請求時間からアウトカム課金へ転換した事実は、ルーフ（AEPS）の価格30%減試作案の根拠に使える。8月頭の方針決定資料に競合事例として1枚追加する。`
  - 👥 チーム／育成への示唆（`hr-impact`）— 直下15名（DXU 9名・SREイネ 6名）のどのメンバー層・どの課題に効くかを書く。対象は能力開発（強化選手、要件定義力、AI以前の業界インプット）、26卒2名の立ち上げ、会議時間の制約、探索と実行の物差しの使い分け。LMIの人事部門一般や「企業のHR」への示唆は書かない
- ソースリンク（外部リンクSVGアイコン付き）— **必ず記事固有のURL**を使用（ドメインルートNG）

分析ボックスは「一般論」ではなく **具体的なアクションアイテム** を書く。
「注目すべき」「重要である」「〜すべき」「〜の検討が急務」のような、誰の何が変わるか不明な結論は書かない。
「どのKRの、どの指標に、どう効くか」を先に書き、打ち手は河野の関与の型（ゲート判定への同席、フォーカスを壊す外部依頼の遮断、BU長・経営との結節、メンバーへの直接介入）のどれかに落とす。
柴戸室長の報告ルール「先頭に成果への接続1行、活動報告から始めない」をカード単位でも守る。

### Step 4.5: ファクトチェック＆ソース検証（HTML生成後、保存前に必ず実行）

生成されたHTMLの品質を保証するため、以下の検証を行う。

**数値データの検証：**
- 各カードの **金額・割合・人数等の定量データ** を元ソースと照合する
- 検索結果に含まれていない数値（AIが推測・捏造した可能性のあるもの）は削除または修正する
- 特に「〇〇%削減」「〇〇社が導入」「〇〇億ドル規模」のような具体的数値は必ず裏取りする
- **数値の出典が特定できないものは使わない**。概算値を使う場合は「約」「推定」等を付記する

**ソースリンクの検証：**
- 全カードのソースリンクが **記事固有のURL** であることを確認する（ドメインルート不可）
- 正しいパターン: `https://nikkei.com/article/DGXZQOUA0861M0Y6A200C2000000/`
- NGパターン: `https://nikkei.com` , `https://nikkei.com/business`
- Step 2の検索時に記録したURLをそのまま使用する
- URLが不明な記事は、タイトル＋メディア名で再検索して正確なURLを取得する

**事実の整合性チェック：**
- 企業名・人名・日付の表記ミスがないか確認する
- 「史上最高値」「過去最大」等の最上級表現は検索で裏取りしてから使う
- 同じイベントを扱う複数カード間でデータの矛盾がないか確認する

**過去ダイジェストとの重複チェック（機械的に実行）：**
- 生成したHTMLの全ソースリンクURLを抽出し、過去7日分のファイルのURL一覧と交差を取る。収集エージェントに既出リストを渡していても見落として提案してくることがある（2026-09-05にHBR記事の完全重複を公開直前に検出した）
```bash
for f in $(ls docs/news-digest-2026-*.html | tail -8 | head -7); do grep -oP '(?<=source-link" href=")[^"]*' "$f"; done | sort > /tmp/past_urls.txt
grep -oP '(?<=source-link" href=")[^"]*' docs/news-digest-YYYY-MM-DD.html | sort > /tmp/today_urls.txt
comm -12 /tmp/past_urls.txt /tmp/today_urls.txt
```
- 一致したURLは、①同一記事の完全重複（差し替え必須）か、②同一ページの続報利用（内容が更新されており「続報」タグで許容可）かを内容で判別する
- URL一致がなくても、企業名・人名・具体的数値で過去7日分を `grep -l` し、同一事象の別ソース再掲を弾く

**KRラベルの確認：**
- 全カードの「KRへの接続」ボックスがStep 0のラベルで始まっているか確認する。ラベルのないカードが残っていたら、その時点で差し替えるか不採用にする

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
- `references/domestic-watchlist.json` — Section 10 の監視対象企業・キーワード・メディアの正本（Feedly用OPMLもここから生成する）
- `scripts/domestic_watch.py` — ウォッチリストからのRSS取得（`fetch`）とFeedly用OPML生成（`opml`）
- `assets/template.css` — HTMLに埋め込むCSSテンプレート
- `news-digest-index.html` — 全ダイジェストのアーカイブインデックス（同じdocs/ディレクトリに配置）
