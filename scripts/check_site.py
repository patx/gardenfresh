#!/usr/bin/env python3
"""Post-build site verifier. Exit code 1 on any failure.

Checks: internal link/asset integrity, single H1, canonical matches filename,
JSON-LD parses and FAQ parity with visible text, unique titles/descriptions,
sitemap <-> built pages parity, legacy URL preservation, img alt/width/height,
and absence of legacy artifacts (Bootstrap, CDN, fake testimonials, old color).
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://gardenfreshwholesale.com"

LEGACY_FILES = [
    "index.html", "contact.html", "produce-delivery-faq.html",
    "restaurant-produce-ordering-guide.html", "wholesale-produce-delivery-areas.html",
    "broward-county-wholesale-produce.html", "palm-beach-county-wholesale-produce.html",
    "berries-wholesale-produce.html", "certified-organic-produce-wholesale.html",
    "citrus-tropical-fruit-wholesale-produce.html", "fresh-herbs-wholesale-produce.html",
    "leafy-greens-wholesale-produce.html", "roots-tubers-wholesale-produce.html",
    "specialty-produce-wholesale.html", "tomatoes-wholesale-produce.html",
    "restaurant-wholesale-produce.html", "hotel-resort-produce-supplier.html",
    "school-institutional-produce-delivery.html", "yacht-marine-provisioning.html",
    "seasonal-produce-for-restaurants-south-florida.html",
] + [f"{slug}-wholesale-produce.html" for slug in [
    "boca-raton", "boynton-beach", "coconut-creek", "coral-springs", "davie",
    "deerfield-beach", "delray-beach", "fort-lauderdale", "hollywood", "jupiter",
    "lake-worth-beach", "lantana", "miramar", "palm-beach", "palm-beach-gardens",
    "pembroke-pines", "plantation", "pompano-beach", "riviera-beach", "sunrise",
    "wellington", "west-palm-beach", "weston",
]]

FORBIDDEN = ["bi bi-", "cdn.jsdelivr", "Seaside Bistro", "#2e7d32",
             "bootstrap", "fonts.googleapis"]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.links = []
        self.imgs = []
        self.canonical = None
        self.title = ""
        self.description = None
        self.jsonld = []
        self._in_title = False
        self._in_script_ld = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag in ("img", "source"):
            self.imgs.append(a)
        elif tag == "use" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "link":
            if a.get("rel") == "canonical":
                self.canonical = a.get("href")
            elif a.get("href") and not a["href"].startswith("http"):
                self.links.append(a["href"])
        elif tag == "meta" and a.get("name") == "description":
            self.description = a.get("content")
        elif tag == "script":
            if a.get("type") == "application/ld+json":
                self._in_script_ld = True
                self._buf = ""
            elif a.get("src"):
                self.links.append(a["src"])

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_script_ld:
            self._buf += data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_script_ld:
            self._in_script_ld = False
            self.jsonld.append(self._buf)


def check_page(path, errors, titles, descriptions):
    html = path.read_text()
    p = PageParser()
    p.feed(html)
    name = path.name

    for needle in FORBIDDEN:
        if needle.lower() in html.lower():
            errors.append(f"{name}: legacy artifact {needle!r} found")

    if p.h1 != 1:
        errors.append(f"{name}: {p.h1} <h1> elements (want exactly 1)")

    expected = f"{BASE}/" if name == "index.html" else f"{BASE}/{name}"
    if p.canonical != expected:
        errors.append(f"{name}: canonical {p.canonical!r} != {expected!r}")

    if not p.title.strip():
        errors.append(f"{name}: empty <title>")
    elif p.title in titles:
        errors.append(f"{name}: duplicate title with {titles[p.title]}")
    titles[p.title] = name

    if not p.description:
        errors.append(f"{name}: missing meta description")
    elif p.description in descriptions:
        errors.append(f"{name}: duplicate description with {descriptions[p.description]}")
    descriptions[p.description] = name

    # Internal link + asset integrity
    for href in p.links:
        target = href.split("#")[0].split("?")[0]
        if not target or href.startswith(("http", "mailto:", "tel:", "#")):
            continue
        if not (ROOT / target).exists():
            errors.append(f"{name}: broken internal ref {href!r}")

    # Images: alt on <img>, dimensions, existing files
    for a in p.imgs:
        if "srcset" in a:
            for part in a["srcset"].split(","):
                src = part.strip().split(" ")[0]
                if src and not (ROOT / src).exists():
                    errors.append(f"{name}: missing srcset file {src!r}")
        src = a.get("src")
        if src:
            if not src.startswith("http") and not (ROOT / src).exists():
                errors.append(f"{name}: missing image {src!r}")
            if "alt" not in a:
                errors.append(f"{name}: <img src={src!r}> missing alt")
            # Ticker logos have varying aspect ratios and a fixed CSS height,
            # so they only carry a height attribute.
            if src.startswith("assets/logos/"):
                if "height" not in a:
                    errors.append(f"{name}: logo <img src={src!r}> missing height")
            elif "width" not in a or "height" not in a:
                errors.append(f"{name}: <img src={src!r}> missing width/height")

    # JSON-LD: parses; FAQPage questions appear in visible text
    visible = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", visible)
    for blob in p.jsonld:
        try:
            data = json.loads(blob.replace("<\\/", "</"))
        except json.JSONDecodeError as e:
            errors.append(f"{name}: JSON-LD parse error: {e}")
            continue
        nodes = data.get("@graph", [data])
        for node in nodes:
            if node.get("@type") == "FAQPage":
                for q in node["mainEntity"]:
                    qt = re.sub(r"\s+", " ", q["name"]).strip()
                    at = re.sub(r"\s+", " ", q["acceptedAnswer"]["text"]).strip()
                    if qt not in visible:
                        errors.append(f"{name}: FAQ question not in visible text: {qt[:60]!r}")
                    if at not in visible:
                        errors.append(f"{name}: FAQ answer not in visible text: {at[:60]!r}")
            if node.get("@type") == "LocalBusiness":
                for field in ("geo", "priceRange", "logo", "hasMap"):
                    if field not in node:
                        errors.append(f"{name}: LocalBusiness missing {field}")
                if node.get("address", {}).get("postalCode") != "33064":
                    errors.append(f"{name}: LocalBusiness missing/wrong postalCode")


def main():
    errors = []
    titles, descriptions = {}, {}

    pages = sorted(ROOT.glob("*.html"))
    if len(pages) < 60:
        errors.append(f"only {len(pages)} pages at root — expected 65")
    for legacy in LEGACY_FILES:
        if not (ROOT / legacy).exists():
            errors.append(f"legacy URL missing: {legacy}")

    for page in pages:
        check_page(page, errors, titles, descriptions)

    # sitemap parity
    sm = (ROOT / "sitemap.xml").read_text()
    sm_urls = set(re.findall(r"<loc>(.*?)</loc>", sm))
    built = {f"{BASE}/" if p.name == "index.html" else f"{BASE}/{p.name}" for p in pages}
    for missing in sorted(built - sm_urls):
        errors.append(f"sitemap missing {missing}")
    for extra in sorted(sm_urls - built):
        errors.append(f"sitemap lists non-built {extra}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        print(f"\n{len(errors)} problem(s)", file=sys.stderr)
        sys.exit(1)
    print(f"check_site: {len(pages)} pages OK — links, H1s, canonicals, schema, "
          f"sitemap parity, legacy URLs all verified")


if __name__ == "__main__":
    main()
