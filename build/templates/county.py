"""County hub pages — full city roster grouped by area."""

from lib import layout, schema
from lib.html import esc
from lib.components import hero, btn, sec_head, card, card_grid, faq_list, \
    link_grid, cta_band, route_facts

SHARED_COUNTY_FAQS = ["fees-minimums", "next-day-cutoff", "delivery-days", "cold-chain"]


def render(ctx, county):
    site = ctx["site"]
    name = county["name"]
    path = county["page"]

    faqs = []
    for fid in SHARED_COUNTY_FAQS:
        f = ctx["faqs"][fid]
        faqs.append({"q": f["q"].replace("{city}", name).replace("{county}", name),
                     "a": f["a"].replace("{city}", name).replace("{county}", name)})

    hero_html = hero(
        ctx["images"], image=county["hero_image"],
        alt=f"Wholesale produce for {name} restaurants",
        eyebrow="County service area",
        h1=f"{esc(name)} wholesale produce delivery",
        lead=(f"Refrigerated produce routes across {esc(name)} — restaurants, hotels, "
              f"schools, clubs, and caterers, seven days a week from our Pompano Beach warehouse."),
        buttons=(btn(site["catalog_url"], "Browse catalog", "light", "basket") +
                 btn("contact.html", "Request pricing", "outline-light", "clipboard")),
        chips=[("truck", "Refrigerated routes"), ("box", "Split cases"),
               ("calendar", "7-day delivery")])

    intro = "".join(f"<p>{esc(p)}</p>" for p in county["intro"])
    groups_html = ""
    for group_name, slugs in county["groups"].items():
        links = "".join(
            f'<li><a href="{slug}-wholesale-produce.html">{esc(ctx["cities"][slug]["name"])}</a></li>'
            for slug in slugs)
        groups_html += (f'<div class="roster-col"><h3>{esc(group_name)}</h3>'
                        f'<ul class="roster-list">{links}</ul></div>')

    body = f"""{hero_html}
<section class="band">
  <div class="container container-narrow">
    {sec_head("Local routes", f"Produce delivery across {name}")}
    {intro}
  </div>
</section>
<section class="band band-mint">
  <div class="container">
    {sec_head("City routes", f"Every {name} city we serve", center=True)}
    <div class="roster-grid">{groups_html}</div>
  </div>
</section>
<section class="band">
  <div class="container">
    {sec_head("How we work", "Built around real kitchen schedules", center=True)}
    {route_facts(site)}
  </div>
</section>
<section class="band band-cream">
  <div class="container container-narrow">
    {sec_head("Delivery FAQ", f"{name} produce delivery questions", center=True)}
    {faq_list(faqs)}
  </div>
</section>
<section class="band">
  <div class="container">
    {sec_head("Keep exploring", "Services and produce categories", center=True)}
    {link_grid([(s['file'], s['nav_label'], 'utensils') for s in ctx['services']] +
               [(p['file'], p['name'], 'leaf') for p in ctx['products'][:4]] +
               [('wholesale-produce-delivery-areas.html', 'All delivery areas', 'map')])}
  </div>
</section>
{cta_band(site, title=f"Set up wholesale produce delivery in {name}.",
          text="Tell us your city, receiving window, and weekly volume — we will match you to the right route and build an order guide around your menu.")}"""

    title = county["title"]
    description = county["meta_description"]
    trail = [("Home", None), (f"{name} Wholesale Produce", path)]
    graph = [
        schema.webpage(site, path, title, description),
        schema.service(site, name=f"Wholesale produce delivery in {name}, FL",
                       service_type="Wholesale produce supplier",
                       area={"@type": "AdministrativeArea", "name": f"{name}, FL"}),
        schema.business(site),
        schema.breadcrumbs(site, trail),
        schema.faq_page(faqs),
    ]
    return layout.page(ctx, path=path, title=title, description=description,
                       body=body, graph=graph, trail=trail)
