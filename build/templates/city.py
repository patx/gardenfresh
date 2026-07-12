"""City page template — the core local-SEO unit (~45 pages)."""

from lib import layout, schema
from lib.html import esc
from lib.components import (picture, hero, btn, sec_head, card, card_grid,
                            faq_list, link_grid, cta_band, icon)

HERO_CHIPS = [("truck", "Refrigerated routes"), ("box", "Split cases"),
              ("calendar", "7-day delivery")]


def resolve_faqs(city, ctx, county_name):
    """Unique FAQs + deterministic rotation of shared pool entries."""
    faqs = list(city["faqs_unique"])
    pool = ctx["faq_pool"]
    idx = ctx["city_index"][city["slug"]]
    if "faq_shared" in city:
        shared = [ctx["faqs"][fid] for fid in city["faq_shared"]]
    else:
        shared = [pool[idx % len(pool)], pool[(idx + 3) % len(pool)]]
    for f in shared:
        faqs.append({
            "q": f["q"].replace("{city}", city["name"]).replace("{county}", county_name),
            "a": f["a"].replace("{city}", city["name"]).replace("{county}", county_name),
        })
    return faqs


def rotating_products(city, ctx):
    idx = ctx["city_index"][city["slug"]]
    n = len(ctx["products"])
    return [ctx["products"][(idx + k) % n] for k in (0, 2, 4, 6)]


def render(ctx, city):
    site = ctx["site"]
    county = ctx["counties"][city["county"]]
    county_name = county["name"]
    name = city["name"]
    path = f"{city['slug']}-wholesale-produce.html"
    idx = ctx["city_index"][city["slug"]]

    title = f"{name} Restaurant Wholesale Produce Delivery | Garden Fresh"
    profile = city["kitchen_profile"]
    description = (f"Restaurant wholesale produce delivery in {name}, FL — serving "
                   f"{', '.join(profile[:3])}. Split cases, no minimums, "
                   f"7-day refrigerated routes from Pompano Beach.")
    lead = (f"We supply {profile[0]}, {profile[1]}, and kitchens across {name} with "
            f"refrigerated wholesale produce — split cases, standing orders, "
            f"no order minimums, and 7-day next-day delivery.")

    faqs = resolve_faqs(city, ctx, county_name)
    products = rotating_products(city, ctx)
    rot_service = ctx["services"][idx % len(ctx["services"])]

    hero_html = hero(
        ctx["images"], image=city["hero_image"],
        alt=f"Fresh wholesale produce delivered to {name} restaurants",
        eyebrow=f"{county_name} · Refrigerated daily routes",
        h1=f"Restaurant wholesale produce delivery in {esc(name)}, FL",
        lead=esc(lead),
        buttons=(btn(site["catalog_url"], "Browse catalog", "light", "basket") +
                 btn("contact.html", "Request pricing", "outline-light", "clipboard")),
        chips=HERO_CHIPS)

    districts = "".join(f"<li>{esc(d)}</li>" for d in city["dining_districts"])
    intro = "".join(f"<p>{esc(p)}</p>" for p in city["intro"])
    intro_section = f"""<section class="band">
  <div class="container split">
    <div class="split-main">
      {sec_head(f"{county_name} restaurant routes", f"Produce built for {name} kitchens")}
      {intro}
      <ul class="check-list">
        <li>Order by 12 AM for next-day delivery on most restaurant produce items.</li>
        <li>Use standing orders for prep staples and update specials as menus change.</li>
        <li>No order minimums, no delivery fees, and no fuel charges on local routes.</li>
      </ul>
    </div>
    <div class="split-aside">
      <div class="aside-card">
        <div class="card-icon">{icon('truck')}</div>
        <h3>From our Pompano Beach warehouse</h3>
        <p>{esc(city['route_note'])}</p>
      </div>
      <div class="aside-card">
        <div class="card-icon">{icon('pin')}</div>
        <h3>Where we deliver in {esc(name)}</h3>
        <ul class="district-list">{districts}</ul>
      </div>
      <div class="aside-card aside-card-deep">
        <h3>Set up delivery in {esc(name)}</h3>
        <p>Send your prep list, delivery window, and weekly volume. We will build an order guide and get your account ready for online ordering.</p>
        {btn('contact.html', 'Talk to sales', 'light')}
      </div>
    </div>
  </div>
</section>"""

    product_cards = card_grid(
        [card(p["name"], p["card_blurb"], href=p["file"], link_label="See varieties")
         for p in products], cols=4)
    products_section = f"""<section class="band band-mint">
  <div class="container">
    {sec_head("Restaurant-first service", f"What {name} kitchens order", center=True)}
    {product_cards}
  </div>
</section>"""

    faq_section = f"""<section class="band">
  <div class="container container-narrow">
    {sec_head("Local delivery FAQ", f"{name} produce delivery questions", center=True)}
    {faq_list(faqs)}
  </div>
</section>"""

    nearby_links = [(f"{slug}-wholesale-produce.html",
                     ctx["cities"][slug]["name"], "pin")
                    for slug in city["nearby"]]
    nearby_links += [
        (county["page"], county_name, "map"),
        (rot_service["file"], rot_service["nav_label"], "utensils"),
        ("restaurant-produce-ordering-guide.html", "Ordering guide", "book"),
    ]
    nearby_section = f"""<section class="band band-cream">
  <div class="container">
    {sec_head("Nearby routes", "Related local produce pages", center=True)}
    {link_grid(nearby_links)}
  </div>
</section>"""

    body = "\n".join([hero_html, intro_section, products_section, faq_section,
                      nearby_section,
                      cta_band(site,
                               title=f"Let us build a {name} produce order around your service.",
                               text=city["cta_text"])])

    trail = [("Home", None),
             (f"{county_name} Wholesale Produce", county["page"]),
             (f"{name}", path)]
    graph = [
        schema.webpage(site, path, title, description),
        schema.service(site,
                       name=f"Restaurant wholesale produce delivery in {name}, FL",
                       service_type="Restaurant wholesale produce supplier",
                       area=schema.city_area(city, county_name)),
        schema.business(site),
        schema.breadcrumbs(site, trail),
        schema.faq_page(faqs),
    ]
    return layout.page(ctx, path=path, title=title, description=description,
                       body=body, graph=graph, trail=trail)
