#!/usr/bin/env python3
"""Extract production HTML bodies (no chrome header/nav/footer) plus CSS."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path("/home/mukeysh/projects/gw/GROWIBES_PRODUCTION_MASTER")
THEME = Path("/home/mukeysh/projects/gw/drupal/web/themes/custom/growibes")
OUT = THEME / "components/html/examples"
ASSETS = THEME / "assets"
PAGES = json.loads((THEME / "scripts/pages.json").read_text())

EXTRA_LINKS = {
    "index.html": "/",
    "growibes-homepage-final-award.html": "/",
    "growibes-homepage-v2-master.html": "/",
    "growibes-digital-trust-security-performance-accessibility-award.html": "/capabilities/enterprise-engineering/security",
    "growibes-search-discovery-award.html": "/",
    "growibes-search-discovery-award-v2.html": "/",
}

NAV_RE = re.compile(r"<nav\b[^>]*>[\s\S]*?</nav>", re.I)
FOOTER_RE = re.compile(r"<footer\b[^>]*>[\s\S]*?</footer>", re.I)
HEADER_RE = re.compile(r"<header\b([^>]*)>([\s\S]*?)</header>", re.I)
CITE_RE = re.compile(r" ?cite[^]*")
STYLE_RE = re.compile(r"<style\b[^>]*>([\s\S]*?)</style>", re.I)
BODY_RE = re.compile(r"<body\b[^>]*>([\s\S]*)</body>", re.I)
DESC_RE = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', re.I)


def strip_chrome(body: str) -> str:
    body = NAV_RE.sub("", body)
    body = FOOTER_RE.sub("", body)

    def keep_hero(match: re.Match) -> str:
        attrs = match.group(1) or ""
        if re.search(r"\bhero\b", attrs, re.I):
            return match.group(0)
        return ""

    body = HEADER_RE.sub(keep_hero, body)
    body = CITE_RE.sub("", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip() + "\n"


def rewrite_links(html: str, links: dict[str, str]) -> str:
    def repl(match: re.Match) -> str:
        quote = match.group(1)
        url = match.group(2)
        name = url.split("/")[-1]
        if name in links:
            return f"href={quote}{links[name]}{quote}"
        return match.group(0)

    return re.sub(r'href=(["\'])([^"\']+\.html(?:#[^"\']*)?)\1', repl, html, flags=re.I)


def extract(source: Path, links: dict[str, str]) -> tuple[str, str, str]:
    raw = source.read_text(errors="replace")
    css_match = STYLE_RE.search(raw)
    css = (css_match.group(1).strip() + "\n") if css_match else ""
    body_match = BODY_RE.search(raw)
    body = body_match.group(1) if body_match else raw
    html = rewrite_links(strip_chrome(body), links)
    html = html.replace("src=\"yogi-emblem.png\"", 'src="/themes/custom/growibes/assets/yogi-emblem.png"')
    html = html.replace("src=\"himalayan-yogi-growibes.png\"", 'src="/themes/custom/growibes/assets/himalayan-yogi-growibes.png"')
    desc = ""
    desc_match = DESC_RE.search(raw)
    if desc_match:
        desc = desc_match.group(1).strip()
    return html, css, desc


def main() -> int:
    group = sys.argv[1] if len(sys.argv) > 1 else "all"
    OUT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    story = ROOT / "09_Himalayan_Story"
    for name in ("yogi-emblem.png", "himalayan-yogi-growibes.png"):
        src = story / name
        if src.exists():
            shutil.copy2(src, ASSETS / name)

    links = {Path(page["source"]).name: page["alias"] for page in PAGES}
    links.update(EXTRA_LINKS)

    selected = [p for p in PAGES if group == "all" or p["group"] == group]
    manifest = []
    for page in selected:
        source = ROOT / page["source"]
        if not source.exists():
            print(f"MISSING {page['source']}")
            continue
        html, css, desc = extract(source, links)
        (OUT / f"{page['slug']}.html").write_text(html)
        (OUT / f"{page['slug']}.css").write_text(css)
        leftover_nav = bool(re.search(r"<nav\b", html, re.I))
        leftover_footer = bool(re.search(r"<footer\b", html, re.I))
        chrome_header = bool(re.search(r"<header\b(?![^>]*hero)", html, re.I))
        print(
            f"{page['alias']:42} html={len(html):6d} css={len(css):5d} "
            f"nav={int(leftover_nav)} footer={int(leftover_footer)} chrome_header={int(chrome_header)}"
        )
        item = dict(page)
        item["description"] = desc
        item["html_file"] = f"{page['slug']}.html"
        item["css_file"] = f"{page['slug']}.css"
        manifest.append(item)

    (OUT / f"manifest-{group}.json").write_text(json.dumps(manifest, indent=2))
    print(f"extracted {len(manifest)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
