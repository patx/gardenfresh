#!/usr/bin/env python3
"""Garden Fresh static site generator.

Usage:  python3 build/build.py [--check]

Reads build/data/*, renders every page in the registry to the repo root,
and regenerates sitemap.xml and assets/manifest.json. Only registry-owned
files are ever written. The build is deterministic: rebuilding with
unchanged inputs produces a byte-identical site.
"""

import json
import sys
from pathlib import Path

BUILD_DIR = Path(__file__).resolve().parent
ROOT = BUILD_DIR.parent
sys.path.insert(0, str(BUILD_DIR))

from templates import home, contact, city, county, product, service, resources  # noqa: E402

DATA = BUILD_DIR / "data"


def load_json(name):
    with open(DATA / name) as fh:
        return json.load(fh)


def load_context():
    site = load_json("site.json")
    counties = load_json("counties.json")
    faq_pool = load_json("faqs.json")
    products = load_json("products.json")
    services = load_json("services.json")
    images = load_json("images_generated.json")

    cities = {}
    for path in sorted((DATA / "cities").glob("*.json")):
        with open(path) as fh:
            c = json.load(fh)
        if c["slug"] != path.stem:
            raise SystemExit(f"{path.name}: slug {c['slug']!r} != filename")
        cities[c["slug"]] = c

    city_slugs = sorted(cities)
    return {
        "site": site,
        "counties": counties,
        "faq_pool": faq_pool,
        "faqs": {f["id"]: f for f in faq_pool},
        "products": products,
        "services": services,
        "cities": cities,
        "city_slugs": city_slugs,
        "city_index": {slug: i for i, slug in enumerate(city_slugs)},
        "images": images,
    }


def validate(ctx):
    """Anti-thin-content and link-integrity guardrails. Failures stop the build."""
    errors, warnings = [], []
    roster = {slug for c in ctx["counties"].values()
              for g in c["groups"].values() for slug in g}
    inbound = {slug: 0 for slug in ctx["cities"]}

    for slug, c in ctx["cities"].items():
        where = f"cities/{slug}.json"
        if len(c.get("intro", [])) < 2:
            errors.append(f"{where}: intro needs >= 2 paragraphs")
        if len(c.get("faqs_unique", [])) < 2:
            errors.append(f"{where}: needs >= 2 unique FAQs")
        for field in ("route_note", "cta_text", "hero_image"):
            if not c.get(field):
                errors.append(f"{where}: missing {field}")
        if len(c.get("dining_districts", [])) < 2:
            errors.append(f"{where}: needs >= 2 dining_districts")
        if len(c.get("kitchen_profile", [])) < 2:
            errors.append(f"{where}: needs >= 2 kitchen_profile entries")
        if c.get("county") not in ctx["counties"]:
            errors.append(f"{where}: unknown county {c.get('county')!r}")
        if c.get("hero_image") not in ctx["images"]:
            errors.append(f"{where}: unknown hero_image {c.get('hero_image')!r}")
        if not (3 <= len(c.get("nearby", [])) <= 6):
            errors.append(f"{where}: nearby should have 3-6 cities")
        for n in c.get("nearby", []):
            if n not in ctx["cities"]:
                errors.append(f"{where}: nearby city {n!r} has no data file")
            else:
                inbound[n] += 1
        if slug not in roster:
            errors.append(f"{where}: city missing from counties.json groups")

    for slug in roster:
        if slug not in ctx["cities"]:
            errors.append(f"counties.json lists {slug!r} but no data file exists")
    for slug, n in inbound.items():
        if n == 0:
            warnings.append(f"{slug}: no inbound nearby links from other cities")

    for w in warnings:
        print(f"  warning: {w}")
    if errors:
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        raise SystemExit(f"build aborted: {len(errors)} data error(s)")


def build_registry(ctx):
    """filename -> callable returning the page HTML."""
    registry = {
        "index.html": lambda: home.render(ctx),
        "contact.html": lambda: contact.render(ctx),
        "produce-delivery-faq.html": lambda: resources.render_faq(ctx),
        "restaurant-produce-ordering-guide.html": lambda: resources.render_guide(ctx),
        "wholesale-produce-delivery-areas.html": lambda: resources.render_areas(ctx),
    }
    for c in ctx["counties"].values():
        registry[c["page"]] = lambda c=c: county.render(ctx, c)
    for p in ctx["products"]:
        registry[p["file"]] = lambda p=p: product.render(ctx, p)
    for s in ctx["services"]:
        registry[s["file"]] = lambda s=s: service.render(ctx, s)
    for slug, c in sorted(ctx["cities"].items()):
        registry[f"{slug}-wholesale-produce.html"] = lambda c=c: city.render(ctx, c)
    return registry


def sitemap(ctx, registry):
    base = ctx["site"]["base_url"]

    def priority(fname):
        if fname == "index.html":
            return "1.0"
        if fname.endswith("county-wholesale-produce.html") or \
                fname == "wholesale-produce-delivery-areas.html":
            return "0.9"
        if any(s["file"] == fname for s in ctx["services"]):
            return "0.85"
        if any(p["file"] == fname for p in ctx["products"]):
            return "0.78"
        if fname == "contact.html":
            return "0.75"
        if fname in ("produce-delivery-faq.html",
                     "restaurant-produce-ordering-guide.html"):
            return "0.7"
        return "0.8"  # city pages

    urls = []
    for fname in sorted(registry, key=lambda f: (f != "index.html", f)):
        loc = f"{base}/" if fname == "index.html" else f"{base}/{fname}"
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n"
                    f"    <priority>{priority(fname)}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def manifest(ctx):
    site = ctx["site"]
    return json.dumps({
        "name": "Garden Fresh Wholesale Produce",
        "short_name": "Garden Fresh",
        "description": site["description"],
        "start_url": "/",
        "scope": "/",
        "display": "browser",
        "theme_color": site["theme_color"],
        "background_color": site["background_color"],
        "icons": [
            {"src": "/assets/icon192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icon512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, indent=2) + "\n"


def write_if_changed(path, content):
    if path.exists() and path.read_text() == content:
        return False
    path.write_text(content)
    return True


def main():
    ctx = load_context()
    validate(ctx)
    registry = build_registry(ctx)

    changed = 0
    for fname, render in sorted(registry.items()):
        changed += write_if_changed(ROOT / fname, render())
    changed += write_if_changed(ROOT / "sitemap.xml", sitemap(ctx, registry))
    changed += write_if_changed(ROOT / "assets" / "manifest.json", manifest(ctx))

    print(f"built {len(registry)} pages + sitemap + manifest "
          f"({changed} file(s) changed)")

    if "--check" in sys.argv:
        import subprocess
        raise SystemExit(subprocess.call(
            [sys.executable, str(ROOT / "scripts" / "check_site.py")]))


if __name__ == "__main__":
    main()
