#!/usr/bin/env python3
"""Generates blog post pages and the blog index from markdown files in posts/."""

import html
import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"

PFP_MARKER_FILE = ROOT / "index.html"


def get_pfp_img_tag():
    """Return the <img class="pfp"> tag from index.html."""
    text = PFP_MARKER_FILE.read_text(encoding="utf-8")
    m = re.search(r'<img class="pfp".*?>', text, re.S)
    if not m:
        sys.exit("Could not find the pfp <img> tag in index.html — aborting.")
    return m.group(0)


def slugify(title):
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug or "post"


def parse_post(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"{path.name}: missing --- frontmatter block at the top of the file.")
    frontmatter, body = m.group(1), m.group(2)

    meta = {}
    for line in frontmatter.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip().lower()] = value.strip()

    for required in ("title", "date", "summary"):
        if required not in meta:
            sys.exit(f"{path.name}: frontmatter is missing '{required}:'")

    try:
        date_obj = datetime.strptime(meta["date"], "%Y-%m-%d")
    except ValueError:
        sys.exit(f"{path.name}: date '{meta['date']}' isn't in YYYY-MM-DD format.")

    return {
        "title": meta["title"],
        "date_str": date_obj.strftime("%B %-d, %Y") if sys.platform != "win32"
                    else date_obj.strftime("%B %#d, %Y"),
        "date_sort": date_obj,
        "summary": meta["summary"],
        "slug": slugify(meta["title"]),
        "body_md": body.strip(),
    }


INLINE_PATTERNS = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)"), r"<em>\1</em>"),
    (re.compile(r"`(.+?)`"), r"<code>\1</code>"),
    (re.compile(r"\[(.+?)\]\((https?://[^\s)]+)\)"), r'<a href="\2" target="_blank" rel="noopener">\1</a>'),
]


def render_inline(text):
    text = html.escape(text, quote=False)
    for pattern, repl in INLINE_PATTERNS:
        text = pattern.sub(repl, text)
    return text


def render_markdown(md_text):
    blocks = re.split(r"\n\s*\n", md_text.strip())
    html_parts = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith("## "):
            html_parts.append(f"<h3>{render_inline(block[3:].strip())}</h3>")
        elif block.startswith("# "):
            html_parts.append(f"<h2>{render_inline(block[2:].strip())}</h2>")
        else:
            # collapse hard-wrapped lines within a paragraph into one line
            joined = " ".join(line.strip() for line in block.splitlines())
            html_parts.append(f"<p>{render_inline(joined)}</p>")
    return "\n      ".join(html_parts)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Originalboy2 — {title}</title>
<meta name="description" content="{summary}">
<link rel="icon" type="image/x-icon" href="ogb2.ico">
<link rel="stylesheet" href="style.css">
</head>

<body>
<div class="page-bg page-bg-blog" aria-hidden="true"></div>
<div class="wrap">

  <header>
    {pfp_tag}
    <h1>Originalboy2</h1>
  </header>

  <a class="back-btn" href="blog.html"><span class="sigil">&lt;</span>blog</a>

  <article class="post">
    <p class="post-date">{date_str}</p>
    <h2 class="post-heading">{title}</h2>
    <div class="post-body">
      {body_html}
    </div>
  </article>

</div>

<footer class="footer footer-left">
  <p>&copy; Originalboy2 2026 (website)</p>
  <p>&copy; zuki.awu 2026 (pfp)</p>
</footer>

</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Originalboy2 — Blog</title>
<meta name="description" content="Originalboy2 — blog.">
<link rel="icon" type="image/x-icon" href="ogb2.ico">
<link rel="stylesheet" href="style.css">
</head>

<body>
<div class="page-bg page-bg-blog" aria-hidden="true"></div>
<div class="wrap">

  <header>
    {pfp_tag}
    <h1>Originalboy2</h1>
  </header>

  <a class="back-btn" href="index.html"><span class="sigil">&lt;</span>index</a>

  <div class="blog-list">
{rows}
  </div>

</div>

<footer class="footer footer-left">
  <p>&copy; Originalboy2 2026 (website)</p>
  <p>&copy; zuki.awu 2026 (pfp)</p>
</footer>

</body>
</html>
"""

ROW_TEMPLATE = """    <a class="blog-row" href="blog-{slug}.html">
      <div class="blog-row-head">
        <span class="blog-title"><span class="sigil">&gt;</span>{title}</span>
        <span class="blog-date">{date_str}</span>
      </div>
      <p class="blog-summary">{summary}</p>
    </a>"""

EMPTY_STATE = '    <p class="blog-empty">No posts yet — add one to posts/ and rerun this script.</p>'


def main():
    if not POSTS_DIR.exists():
        sys.exit(f"posts/ folder not found at {POSTS_DIR}")

    pfp_tag = get_pfp_img_tag()

    posts = [parse_post(p) for p in sorted(POSTS_DIR.glob("*.md"))]
    posts.sort(key=lambda p: p["date_sort"], reverse=True)

    if not posts:
        print("No .md files found in posts/ — writing an empty blog.html.")

    for post in posts:
        page_html = PAGE_TEMPLATE.format(
            title=post["title"],
            summary=post["summary"],
            pfp_tag=pfp_tag,
            date_str=post["date_str"],
            body_html=render_markdown(post["body_md"]),
        )
        out_path = ROOT / f"blog-{post['slug']}.html"
        out_path.write_text(page_html, encoding="utf-8")
        print(f"wrote {out_path.name}")

    rows = "\n\n".join(
        ROW_TEMPLATE.format(
            slug=post["slug"],
            title=post["title"],
            date_str=post["date_str"],
            summary=post["summary"],
        )
        for post in posts
    ) or EMPTY_STATE

    index_html = INDEX_TEMPLATE.format(pfp_tag=pfp_tag, rows=rows)
    (ROOT / "blog.html").write_text(index_html, encoding="utf-8")
    print("wrote blog.html")


if __name__ == "__main__":
    main()
