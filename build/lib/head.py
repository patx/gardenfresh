"""<head> builder shared by every page."""

from .html import esc


def render(site, *, path, title, description, og_image=None, extra=""):
    base = site["base_url"]
    url = f"{base}/{path}" if path else f"{base}/"
    image = f"{base}/{og_image or site['default_social_image']}"
    return f"""<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{url}">
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
  <link rel="apple-touch-icon" href="assets/icon192.png">
  <link rel="manifest" href="assets/manifest.json">
  <meta name="theme-color" content="{site['theme_color']}">
  <meta property="og:site_name" content="{esc(site['name'])}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{image}">
  <link rel="preload" href="assets/fonts/Fraunces-Variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/Inter-Variable.woff2" as="font" type="font/woff2" crossorigin>
  <link href="assets/site.css" rel="stylesheet">{extra}"""
