"""Product/category pages (8)."""

from lib import layout, schema
from lib.html import esc
from lib.components import split_hero, btn, sec_head, card, card_grid, faq_list, \
    link_grid, cta_band


def render(ctx, product):
    site = ctx["site"]
    path = product["file"]
    name = product["name"]

    hero_html = split_hero(
        ctx["images"], image=product["hero_image"],
        alt=f"{name} — wholesale produce for South Florida restaurants",
        eyebrow="Wholesale produce category",
        h1=esc(product["h1"]),
        lead=esc(product["lead"]),
        buttons=(btn(site["catalog_url"], "Browse catalog", "solid", "basket") +
                 btn("contact.html", "Request pricing", "ghost", "clipboard")),
        chips=[("truck", "Refrigerated routes"), ("box", "Split cases"),
               ("calendar", "7-day delivery")])

    intro = "".join(f"<p>{esc(p)}</p>" for p in product["intro"])
    variety_cards = card_grid(
        [card(g["t"], g["d"], ic="leaf") for g in product["groups"]], cols=4)

    by_slug = {p["slug"]: p for p in ctx["products"]}
    related = [(by_slug[s]["file"], by_slug[s]["name"], "leaf")
               for s in product["related"] if s in by_slug]
    related += [(c["page"], c["name"], "map") for c in ctx["counties"].values()]
    related += [("restaurant-wholesale-produce.html", "Restaurant produce", "utensils"),
                ("restaurant-produce-ordering-guide.html", "Ordering guide", "book")]

    body = f"""{hero_html}
<section class="band">
  <div class="container container-narrow">
    {sec_head("Chef-grade sourcing", f"{name} for working kitchens")}
    {intro}
  </div>
</section>
<section class="band band-mint">
  <div class="container">
    {sec_head("What to order", "Varieties and pack options", center=True)}
    {variety_cards}
  </div>
</section>
<section class="band">
  <div class="container container-narrow">
    {sec_head(f"{name} FAQ", "Questions chefs ask", center=True)}
    {faq_list(product["faqs"])}
  </div>
</section>
<section class="band band-cream">
  <div class="container">
    {sec_head("Keep exploring", "Related produce and delivery areas", center=True)}
    {link_grid(related)}
  </div>
</section>
{cta_band(site, title=f"Add {name.lower()} to your produce program.",
          text="Tell us your varieties, volumes, and ripeness preferences — we will set pars and delivery timing that fit your service.")}"""

    title = product["title"]
    description = product["meta_description"]
    trail = [("Home", None), (f"Wholesale {name}", path)]
    graph = [
        schema.webpage(site, path, title, description,
                       image=f"assets/images/r/{product['hero_image']}-1200.webp"),
        schema.service(site, name=product["h1"],
                       service_type=f"Wholesale {name.lower()} supplier",
                       area=[{"@type": "AdministrativeArea", "name": "Broward County, FL"},
                             {"@type": "AdministrativeArea", "name": "Palm Beach County, FL"}]),
        schema.business(site),
        schema.breadcrumbs(site, trail),
        schema.faq_page(product["faqs"]),
    ]
    return layout.page(ctx, path=path, title=title, description=description,
                       body=body, graph=graph, trail=trail,
                       og_image=f"assets/images/r/{product['hero_image']}-1200.webp")
