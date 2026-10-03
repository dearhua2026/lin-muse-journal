#!/usr/bin/env python3
"""Build the journal static site from articles/*.md into site/."""
import os
import re
import shutil
from datetime import datetime

import markdown

ROOT = os.path.expanduser("~/workspace/journal")
ARTICLES_DIR = os.path.join(ROOT, "articles")
OUT_DIR = os.path.join(ROOT, "site")
SITE_TITLE = "对话手记"
SITE_SUBTITLE = "Lin 与 Muse 的每一次沟通，都值得被记录"

CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#faf9f7;--card:#fff;--text:#2b2b2b;--muted:#8a8a8a;--accent:#b3541e;--border:#e8e4de;--code:#f4f1ec}
body{background:var(--bg);color:var(--text);font-family:"Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.9;font-size:17px}
.wrap{max-width:720px;margin:0 auto;padding:0 24px}
header.site{padding:72px 0 40px;text-align:center}
header.site h1{font-size:34px;letter-spacing:.14em;font-weight:700}
header.site h1 a{color:var(--text);text-decoration:none}
header.site p{color:var(--muted);margin-top:10px;font-size:15px;letter-spacing:.08em}
article.card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:28px 30px;margin:0 0 22px;transition:transform .15s ease,box-shadow .15s ease}
article.card:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,.06)}
article.card .date{color:var(--muted);font-size:13px;letter-spacing:.06em}
article.card h2{font-size:21px;margin:8px 0 10px;line-height:1.5}
article.card h2 a{color:var(--text);text-decoration:none}
article.card h2 a:hover{color:var(--accent)}
article.card p.excerpt{color:#555;font-size:15px;line-height:1.8}
.tags{margin-top:12px}
.tag{display:inline-block;font-size:12px;color:var(--accent);border:1px solid var(--accent);opacity:.85;border-radius:20px;padding:2px 12px;margin-right:8px}
.post{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:44px 46px;margin-bottom:30px}
.post .date{color:var(--muted);font-size:13px;letter-spacing:.06em}
.post h1{font-size:28px;margin:10px 0 6px;line-height:1.5}
.post h2{font-size:21px;margin:38px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--border)}
.post h3{font-size:18px;margin:28px 0 10px}
.post p{margin:14px 0}
.post ul,.post ol{margin:14px 0 14px 24px}
.post li{margin:6px 0}
.post code{font-family:ui-monospace,Menlo,Consolas,monospace;background:var(--code);padding:2px 7px;border-radius:6px;font-size:.88em}
.post pre{background:var(--code);border-radius:10px;padding:18px;overflow-x:auto;margin:16px 0}
.post pre code{background:none;padding:0}
.post blockquote{border-left:3px solid var(--accent);padding:4px 0 4px 18px;color:#666;margin:18px 0}
.post hr{border:none;border-top:1px solid var(--border);margin:34px 0}
.post em{color:#666}
.back{display:inline-block;margin:26px 0 60px;color:var(--muted);text-decoration:none;font-size:15px}
.back:hover{color:var(--accent)}
footer.site{text-align:center;color:var(--muted);font-size:13px;padding:20px 0 60px;letter-spacing:.06em}
.count{color:var(--muted);font-size:14px;margin:0 0 26px;text-align:center;letter-spacing:.08em}
@media(max-width:640px){.post{padding:28px 24px}header.site{padding:52px 0 30px}}
"""


def parse_article(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    meta, body = {}, text
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            front = text[3:end].strip()
            body = text[end + 3 :].strip()
            for line in front.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
    tags = []
    raw_tags = meta.get("tags", "").strip("[]")
    if raw_tags:
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
    slug = os.path.splitext(os.path.basename(path))[0]
    html = markdown.markdown(body, extensions=["fenced_code", "tables"])
    try:
        dt = datetime.strptime(meta.get("date", ""), "%Y-%m-%d")
    except ValueError:
        dt = datetime.fromtimestamp(os.path.getmtime(path))
    return {
        "slug": slug,
        "title": meta.get("title", slug),
        "date": dt,
        "date_str": dt.strftime("%Y 年 %-m 月 %-d 日"),
        "tags": tags,
        "excerpt": meta.get("excerpt", ""),
        "html": html,
    }


def tag_html(tags):
    return '<div class="tags">' + "".join(
        f'<span class="tag">{t}</span>' for t in tags
    ) + "</div>" if tags else ""


def build():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(os.path.join(OUT_DIR, "articles"))
    with open(os.path.join(OUT_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)

    articles = []
    for name in os.listdir(ARTICLES_DIR):
        if name.endswith(".md"):
            articles.append(parse_article(os.path.join(ARTICLES_DIR, name)))
    articles.sort(key=lambda a: a["date"], reverse=True)

    # article pages
    for a in articles:
        page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{a['title']} · {SITE_TITLE}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<div class="wrap">
<header class="site">
<h1><a href="../index.html">{SITE_TITLE}</a></h1>
<p>{SITE_SUBTITLE}</p>
</header>
<article class="post">
<div class="date">{a['date_str']}</div>
{a['html']}
{tag_html(a['tags'])}
</article>
<a class="back" href="../index.html">← 返回全部文章</a>
<footer class="site">{SITE_TITLE} · 由 Muse 整理发布</footer>
</div>
</body>
</html>"""
        with open(
            os.path.join(OUT_DIR, "articles", a["slug"] + ".html"), "w", encoding="utf-8"
        ) as f:
            f.write(page)

    # index page
    cards = []
    for a in articles:
        cards.append(f"""<article class="card">
<div class="date">{a['date_str']}</div>
<h2><a href="articles/{a['slug']}.html">{a['title']}</a></h2>
<p class="excerpt">{a['excerpt']}</p>
{tag_html(a['tags'])}
</article>""")
    index = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{SITE_TITLE} · {SITE_SUBTITLE}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="wrap">
<header class="site">
<h1>{SITE_TITLE}</h1>
<p>{SITE_SUBTITLE}</p>
</header>
<div class="count">共 {len(articles)} 篇</div>
{''.join(cards)}
<footer class="site">{SITE_TITLE} · 由 Muse 整理发布</footer>
</div>
</body>
</html>"""
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index)
    print(f"built {len(articles)} articles -> {OUT_DIR}")


if __name__ == "__main__":
    build()
