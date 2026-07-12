"""Service pages (5): restaurants, hotels, schools, yachts, seasonal."""

from lib import layout, schema
from lib.html import esc
from lib.components import hero, btn, sec_head, card, card_grid, faq_list, \
    link_grid, cta_band, route_facts


def rotating_cities(service, ctx, count=12):
    """Deterministic spread of city links per service page."""
    slugs = ctx["city_slugs"]
    start = ctx["services"].index(service) * 7
    step = max(1, len(slugs) // count)
    return [slugs[(start + k * step) % len(slugs)] for k in range(count)]


def render(ctx, service_data):
    site = ctx["site"]
    path = service_data["file"]
    name = service_data["name"]

    hero_html = hero(
        ctx["images"], image=service_data["hero_image"],
        alt=f"Garden Fresh produce service — {name}",
        eyebrow="Wholesale produce service",
        h1=esc(service_data["h1"]),
        lead=esc(service_data["lead"]),
        buttons=(btn(site["catalog_url"], "Browse catalog", "light", "basket") +
                 btn("contact.html", "Request pricing", "outline-light", "clipboard")),
        chips=[("truck", "Refrigerated routes"), ("box", "Split cases"),
               ("calendar", "7-day delivery")])

    intro = "".join(f"<p>{esc(p)}</p>" for p in service_data["intro"])
    group_cards = card_grid(
        [card(g["t"], g["d"], ic="check") for g in service_data["groups"]], cols=4)

    seen = set()
    city_links = []
    for slug in rotating_cities(service_data, ctx):
        if slug in seen:
            continue
        seen.add(slug)
        city_links.append((f"{slug}-wholesale-produce.html",
                           ctx["cities"][slug]["name"], "pin"))
    city_links += [(c["page"], c["name"], "map") for c in ctx["counties"].values()]
    city_links.append(("wholesale-produce-delivery-areas.html", "All delivery areas", "map"))

    body = f"""{hero_html}
<section class="band">
  <div class="container container-narrow">
    {sec_head("How we support you", f"{name}: produce that fits the operation")}
    {intro}
  </div>
</section>
<section class="band band-mint">
  <div class="container">
    {sec_head("Service details", "What your kitchen gets", center=True)}
    {group_cards}
  </div>
</section>
<section class="band">
  <div class="container">
    {sec_head("Route promise", "Built around real kitchen schedules", center=True)}
    {route_facts(site)}
  </div>
</section>
<section class="band band-cream">
  <div class="container container-narrow">
    {sec_head("Service FAQ", "Common questions", center=True)}
    {faq_list(service_data["faqs"])}
  </div>
</section>
<section class="band">
  <div class="container">
    {sec_head("Cities we serve", "Local produce delivery routes", center=True)}
    {link_grid(city_links)}
  </div>
</section>
{cta_band(site, title=f"Talk to us about {name.lower()}.",
          text="Share your menu style, weekly volume, delivery window, and pressure points — we will build a produce program around your operation.")}"""

    title = service_data["title"]
    description = service_data["meta_description"]
    trail = [("Home", None), (name, path)]
    graph = [
        schema.webpage(site, path, title, description),
        schema.service(site, name=service_data["h1"],
                       service_type=service_data["service_type"],
                       area=[{"@type": "AdministrativeArea", "name": "Broward County, FL"},
                             {"@type": "AdministrativeArea", "name": "Palm Beach County, FL"}]),
        schema.business(site),
        schema.breadcrumbs(site, trail),
        schema.faq_page(service_data["faqs"]),
    ]
    return layout.page(ctx, path=path, title=title, description=description,
                       body=body, graph=graph, trail=trail)
