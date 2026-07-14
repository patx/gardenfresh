"""Page shell: header/nav, breadcrumb strip, footer."""

from . import head, schema
from .html import esc
from .components import icon

FLAGSHIP_CITIES = [
    "pompano-beach", "fort-lauderdale", "hollywood",
    "boca-raton", "delray-beach", "west-palm-beach",
]


def nav(ctx):
    products = "".join(
        f'<a href="{p["file"]}">{esc(p["name"])}</a>' for p in ctx["products"])
    services = "".join(
        f'<a href="{s["file"]}">{esc(s["nav_label"])}</a>' for s in ctx["services"])
    counties = "".join(
        f'<a href="{c["page"]}">{esc(c["name"])}</a>'
        for c in ctx["counties"].values())
    cities = "".join(
        f'<a href="{slug}-wholesale-produce.html">{esc(ctx["cities"][slug]["name"])}</a>'
        for slug in FLAGSHIP_CITIES)
    return f"""<header class="site-header">
  <div class="container header-bar">
    <a class="brand" href="index.html"><img src="assets/gardenfresh_logo_clear.png" alt="Garden Fresh logo" width="150" height="60"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="siteNav"><span class="nav-toggle-bars" aria-hidden="true"></span>Menu</button>
    <nav class="site-nav" id="siteNav" aria-label="Main">
      <details class="nav-group"><summary>Produce</summary><div class="nav-drop">{products}</div></details>
      <details class="nav-group"><summary>Services</summary><div class="nav-drop">{services}</div></details>
      <details class="nav-group"><summary>Service areas</summary><div class="nav-drop">{counties}<hr>{cities}<hr><a href="wholesale-produce-delivery-areas.html">All delivery areas</a></div></details>
      <details class="nav-group"><summary>Resources</summary><div class="nav-drop"><a href="produce-delivery-faq.html">Delivery FAQ</a><a href="restaurant-produce-ordering-guide.html">Ordering guide</a><a href="seasonal-produce-for-restaurants-south-florida.html">Seasonal produce</a></div></details>
      <a class="nav-link" href="contact.html">Contact</a>
      <a class="btn btn-solid btn-nav" href="{ctx['site']['order_url']}" rel="noopener">{icon('cart')}Place order</a>
    </nav>
  </div>
</header>"""


def breadcrumb_ui(trail):
    """Same trail as schema.breadcrumbs: list of (name, path-or-None)."""
    items = []
    for i, (name, path) in enumerate(trail):
        if i == len(trail) - 1:
            items.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            href = path if path else "index.html"
            items.append(f'<li><a href="{href}">{esc(name)}</a></li>')
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><div class="container">'
            f'<ol>{"".join(items)}</ol></div></nav>')


def footer(ctx):
    site = ctx["site"]
    services = "".join(
        f'<li><a href="{s["file"]}">{esc(s["nav_label"])}</a></li>'
        for s in ctx["services"])
    products = "".join(
        f'<li><a href="{p["file"]}">{esc(p["name"])}</a></li>'
        for p in ctx["products"])
    areas = "".join(
        f'<li><a href="{c["page"]}">{esc(c["name"])}</a></li>'
        for c in ctx["counties"].values()) + "".join(
        f'<li><a href="{slug}-wholesale-produce.html">{esc(ctx["cities"][slug]["name"])}</a></li>'
        for slug in FLAGSHIP_CITIES) + (
        '<li><a href="wholesale-produce-delivery-areas.html">All delivery areas</a></li>')
    addr = site["address"]
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <img src="assets/gardenfresh_logo_clear.png" alt="Garden Fresh logo" width="150" height="60" loading="lazy">
      <p>Wholesale produce delivery for restaurants, hotels, schools, and yachts across Broward and Palm Beach Counties.</p>
      <address>
        {icon('pin')}{esc(addr['street'])}, {esc(addr['city'])}, {esc(addr['region'])} {esc(addr['zip'])}<br>
        {icon('phone')}<a href="tel:{site['phone_tel']}">{esc(site['phone_display'])}</a><br>
        {icon('envelope')}<a href="mailto:{site['email']}">{esc(site['email'])}</a><br>
        {icon('clock')}{esc(site['hours_display'])}
      </address>
    </div>
    <nav class="footer-col" aria-label="Produce"><h3>Produce</h3><ul>{products}</ul></nav>
    <nav class="footer-col" aria-label="Services"><h3>Services</h3><ul>{services}<li><a href="produce-delivery-faq.html">Delivery FAQ</a></li><li><a href="restaurant-produce-ordering-guide.html">Ordering guide</a></li></ul></nav>
    <nav class="footer-col" aria-label="Service areas"><h3>Service areas</h3><ul>{areas}</ul></nav>
  </div>
  <div class="container footer-base">
    <p>&copy; <span id="year">2026</span> {esc(site['legal_name'])} &middot; {esc(addr['city'])}, Florida</p>
    <a class="btn btn-light btn-sm" href="{site['order_url']}" rel="noopener">{icon('cart')}Place order</a>
  </div>
</footer>"""


def sticky_cta(ctx):
    site = ctx["site"]
    return f"""<div class="sticky-cta">
  <div class="container sticky-cta-inner">
    <p class="sticky-cta-text"><strong>Ready to order?</strong> Same-day wholesale delivery across Broward &amp; Palm Beach.</p>
    <a class="btn btn-light btn-sm" href="tel:{site['phone_tel']}">{icon('phone')}Call {esc(site['phone_display'])}</a>
  </div>
</div>"""


def page(ctx, *, path, title, description, body, graph, og_image=None, trail=None):
    """Assemble a complete HTML document."""
    head_html = head.render(ctx["site"], path=path, title=title,
                            description=description, og_image=og_image,
                            extra="\n  " + schema.script(graph))
    crumbs = breadcrumb_ui(trail) if trail else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  {head_html}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  {nav(ctx)}
  {crumbs}
  <main id="main">
{body}
  </main>
  {footer(ctx)}
  {sticky_cta(ctx)}
  <script src="assets/site.js" defer></script>
</body>
</html>
"""
