#!/usr/bin/env python3
"""
国内企業動向ウォッチリストから Feedly 用 OPML を生成し、RSS の新着記事を収集する。

使用例:
    python3 scripts/domestic_watch.py opml --out /tmp/domestic-watch.opml
    python3 scripts/domestic_watch.py fetch --hours 72 --markdown
"""

import argparse
import datetime
import email.utils
import json
from pathlib import Path
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


WATCHLIST_PATH = Path(__file__).resolve().parent.parent / "references" / "domestic-watchlist.json"
DEFAULT_OPML_PATH = "/tmp/domestic-watch.opml"
DEFAULT_JSON_PATH = "/tmp/domestic-watch.json"
GOOGLE_NEWS_BASE = "https://news.google.com"
GOOGLE_NEWS_PARAMS = "&hl=ja&gl=JP&ceid=JP:ja"
JST = datetime.timezone(datetime.timedelta(hours=9))


def load_watchlist():
    """正本のウォッチリストを読み込む。"""
    with WATCHLIST_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def google_news_urls(query):
    """検索語から Google News の RSS URL と閲覧用 URL を返す。"""
    encoded_query = urllib.parse.quote(query, safe="")
    rss_url = f"{GOOGLE_NEWS_BASE}/rss/search?q={encoded_query}{GOOGLE_NEWS_PARAMS}"
    html_url = f"{GOOGLE_NEWS_BASE}/search?q={encoded_query}{GOOGLE_NEWS_PARAMS}"
    return rss_url, html_url


def company_query(company):
    """企業名と別名を完全一致形式で結合し、除外語があれば末尾に付ける。"""
    names = [company["name"], *company.get("aliases", [])]
    query = " OR ".join(f'"{name}"' for name in names)
    excludes = company.get("exclude", [])
    if excludes:
        query = f"({query}) " + " ".join(f'-"{term}"' for term in excludes)
    return query


def build_feeds(watchlist):
    """OPML と記事取得で共用するフィード一覧を組み立てる。"""
    feeds = []

    for group in watchlist.get("groups", []):
        for company in group.get("companies", []):
            rss_url, html_url = google_news_urls(company_query(company))
            feeds.append(
                {
                    "group": group["label"],
                    "target": company["name"],
                    "url": rss_url,
                    "html_url": html_url,
                }
            )

    for keyword in watchlist.get("keyword_feeds", []):
        rss_url, html_url = google_news_urls(keyword["query"])
        feeds.append(
            {
                "group": "キーワード",
                "target": keyword["label"],
                "url": rss_url,
                "html_url": html_url,
            }
        )

    for media in watchlist.get("media_feeds", []):
        feeds.append(
            {
                "group": "メディア",
                "target": media["label"],
                "url": media["url"],
                "html_url": media["site"],
            }
        )

    return feeds


def add_feed_outline(parent, feed):
    """親フォルダへ RSS フィードの outline を追加する。"""
    ET.SubElement(
        parent,
        "outline",
        {
            "type": "rss",
            "text": feed["target"],
            "title": feed["target"],
            "xmlUrl": feed["url"],
            "htmlUrl": feed["html_url"],
        },
    )


def write_opml(watchlist, out_path):
    """Feedly に取り込める OPML 2.0 ファイルを書き出す。"""
    root = ET.Element("opml", {"version": "2.0"})
    head = ET.SubElement(root, "head")
    ET.SubElement(head, "title").text = "国内企業動向ウォッチリスト"
    body = ET.SubElement(root, "body")

    feed_by_target = {feed["target"]: feed for feed in build_feeds(watchlist)}

    for group in watchlist.get("groups", []):
        folder = ET.SubElement(body, "outline", {"text": group["label"]})
        for company in group.get("companies", []):
            add_feed_outline(folder, feed_by_target[company["name"]])

    keyword_folder = ET.SubElement(body, "outline", {"text": "キーワード"})
    for keyword in watchlist.get("keyword_feeds", []):
        add_feed_outline(keyword_folder, feed_by_target[keyword["label"]])

    media_folder = ET.SubElement(body, "outline", {"text": "メディア"})
    for media in watchlist.get("media_feeds", []):
        add_feed_outline(media_folder, feed_by_target[media["label"]])

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def local_name(tag):
    """名前空間を除いた XML 要素名を返す。"""
    return tag.rsplit("}", 1)[-1]


def direct_child(element, names):
    """指定した名前を持つ最初の直接の子要素を返す。"""
    for child in element:
        if local_name(child.tag) in names:
            return child
    return None


def element_text(element):
    """要素内の文字列を空白が連続しない形で取り出す。"""
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def parse_pub_date(value):
    """RFC 形式または ISO 8601 形式の日時を UTC に正規化する。"""
    if not value:
        return None

    try:
        parsed = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        parsed = None

    if parsed is None:
        try:
            parsed = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed.astimezone(datetime.timezone.utc)


def item_link(item):
    """RSS または Atom の記事リンクを返す。"""
    for child in item:
        if local_name(child.tag) != "link":
            continue
        href = child.get("href")
        relation = child.get("rel", "alternate")
        if href and relation == "alternate":
            return href.strip()
        text_value = element_text(child)
        if text_value:
            return text_value
    return ""


INVALID_XML_CHARS = re.compile(
    "[^\\t\\n\\r\\x20-\\uD7FF\\uE000-\\uFFFD\\U00010000-\\U0010FFFF]"
)


def parse_xml_lenient(xml_data):
    """XML として不正な制御文字を除いてから解析する。BRIDGE 等の壊れたフィード対策。"""
    try:
        return ET.fromstring(xml_data)
    except ET.ParseError:
        text = xml_data.decode("utf-8", errors="replace")
        text = INVALID_XML_CHARS.sub("", text)
        return ET.fromstring(text.encode("utf-8"))


def parse_feed(xml_data, feed, cutoff):
    """一つのフィードから期間内の記事を抽出する。"""
    root = parse_xml_lenient(xml_data)
    entries = [element for element in root.iter() if local_name(element.tag) in {"item", "entry"}]
    articles = []

    for entry in entries:
        title = element_text(direct_child(entry, {"title"}))
        link = item_link(entry)
        date_element = direct_child(entry, {"pubDate", "published", "updated", "date"})
        published_at = parse_pub_date(element_text(date_element))

        if not title or published_at is None or published_at < cutoff:
            continue

        source_element = direct_child(entry, {"source"})
        source = element_text(source_element) or feed["target"]
        publisher = source_element.get("url") if source_element is not None else None
        articles.append(
            {
                "title": title,
                "link": link,
                "pubDate": published_at.isoformat(),
                "source": source,
                "group": feed["group"],
                "target": feed["target"],
                "publisher": publisher,
                "_published_at": published_at,
            }
        )

    return articles


def fetch_feed(feed, cutoff):
    """一つの URL を取得して記事を解析する。"""
    request = urllib.request.Request(
        feed["url"],
        headers={"User-Agent": "domestic-watch/1.0"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return parse_feed(response.read(), feed, cutoff)


def collect_articles(feeds, hours):
    """全フィードを取得し、同一タイトルを除いて新しい順に返す。"""
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(hours=hours)
    articles = []

    for feed in feeds:
        try:
            articles.extend(fetch_feed(feed, cutoff))
        except Exception as error:
            message = " ".join(str(error).split())
            print(f"取得失敗: {feed['target']}: {message}", file=sys.stderr)

    articles.sort(key=lambda article: article["_published_at"], reverse=True)
    unique_articles = []
    seen_titles = set()

    for article in articles:
        if article["title"] in seen_titles:
            continue
        seen_titles.add(article["title"])
        article.pop("_published_at")
        unique_articles.append(article)

    return unique_articles


def write_json(articles, out_path):
    """記事一覧を UTF-8 の JSON 配列として書き出す。"""
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(articles, file, ensure_ascii=False, indent=2)
        file.write("\n")


def group_order(feeds):
    """フィード一覧に現れる順番で重複のないグループ名を返す。"""
    result = []
    for feed in feeds:
        if feed["group"] not in result:
            result.append(feed["group"])
    return result


def render_markdown(articles, groups):
    """記事一覧をグループ別の Markdown に変換する。"""
    sections = []

    for group in groups:
        group_articles = [article for article in articles if article["group"] == group]
        if not group_articles:
            continue

        lines = [f"## {group}", ""]
        for article in group_articles:
            published_at = datetime.datetime.fromisoformat(article["pubDate"]).astimezone(JST)
            jst_text = published_at.strftime("%Y-%m-%d %H:%M JST")
            publisher = article.get("publisher") or article["source"]
            lines.append(
                f"- [{jst_text}] {article['target']}｜{article['title']}"
                f"（{publisher}）{article['link']}"
            )
        sections.append("\n".join(lines))

    return "\n\n".join(sections)


def nonnegative_int(value):
    """0 以上の整数を argparse 用に検証する。"""
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("0以上の整数を指定してください")
    return number


def build_parser():
    """コマンドライン引数の解析器を作る。"""
    parser = argparse.ArgumentParser(
        description="国内企業動向ウォッチリストから OPML を生成し、RSS の新着記事を収集します。"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    opml_parser = subparsers.add_parser("opml", help="Feedly 用 OPML 2.0 を生成します。")
    opml_parser.add_argument("--out", default=DEFAULT_OPML_PATH, help="出力先のパス")

    fetch_parser = subparsers.add_parser("fetch", help="期間内の RSS 記事を収集します。")
    fetch_parser.add_argument("--hours", type=nonnegative_int, default=48, help="取得対象の時間数")
    fetch_parser.add_argument("--out", default=DEFAULT_JSON_PATH, help="JSON 出力先のパス")
    fetch_parser.add_argument(
        "--markdown",
        action="store_true",
        help="標準出力にもグループ別の Markdown を表示します。",
    )
    return parser


def main():
    """指定されたサブコマンドを実行する。"""
    parser = build_parser()
    args = parser.parse_args()
    watchlist = load_watchlist()

    if args.command == "opml":
        write_opml(watchlist, args.out)
        return 0

    feeds = build_feeds(watchlist)
    articles = collect_articles(feeds, args.hours)
    write_json(articles, args.out)
    if args.markdown:
        markdown = render_markdown(articles, group_order(feeds))
        if markdown:
            print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
