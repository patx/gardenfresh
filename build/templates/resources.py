"""Resource pages: delivery FAQ, ordering guide, delivery areas."""

from lib import layout, schema
from lib.html import esc
from lib.components import sec_head, card, card_grid, faq_list, link_grid, \
    cta_band, btn, icon

FAQ_PAGE_FAQS = [
    {"q": "Does Garden Fresh have order minimums?",
     "a": "No. Local accounts have no order minimums, so restaurants and foodservice teams can order around actual prep needs."},
    {"q": "Does Garden Fresh charge delivery or fuel fees?",
     "a": "No. Garden Fresh offers no delivery fees and no fuel charges for local accounts in the service area."},
    {"q": "What is the cutoff for next-day delivery?",
     "a": "Most produce orders can be placed by 12 AM for next-day delivery, depending on item availability and route timing."},
    {"q": "Which counties do you serve?",
     "a": "Garden Fresh focuses on Broward County and Palm Beach County, with city route pages for major restaurant and foodservice areas."},
    {"q": "Can restaurants order split cases?",
     "a": "Yes. Restaurants can order full cases, split cases, and select by-the-pound items to control waste and food cost."},
    {"q": "Can Garden Fresh support standing orders?",
     "a": "Yes. Standing orders are available for weekly pars, staple produce, and planned menu needs."},
    {"q": "Do you offer specialty produce?",
     "a": "Yes. Specialty produce may include microgreens, edible flowers, specialty mushrooms, tropical fruit, organics, and seasonal items."},
    {"q": "How do new accounts get started?",
     "a": "Send your business name, delivery address, contact info, receiving window, and sample prep list through the contact form or by phone."},
]

GUIDE_FAQS = [
    {"q": "How should a restaurant start a produce order guide?",
     "a": "Start with staple prep items, weekly usage, delivery window, and any recurring specials. We can turn that list into an online order guide."},
    {"q": "When should restaurants use split cases?",
     "a": "Split cases help when volume is uncertain, when testing specials, or when a full case would create unnecessary waste."},
    {"q": "Can standing orders be changed?",
     "a": "Yes. Standing orders can be adjusted as menus, reservations, weather, and seasonal demand change."},
    {"q": "Can chefs request seasonal produce?",
     "a": "Yes. Chefs can request seasonal items, specialty produce, organics, microgreens, edible flowers, and tropical fruit when available."},
]


def _simple_page(ctx, *, path, title, description, h1, sub, body_sections,
                 faqs=None):
    site = ctx["site"]
    trail = [("Home", None), (h1, path)]
    graph = [schema.webpage(site, path, title, description),
             schema.business(site),
             schema.breadcrumbs(site, trail)]
    if faqs:
        graph.append(schema.faq_page(faqs))
    body = f"""<section class="band band-tight">
  <div class="container container-narrow">
    <div class="sec-head"><p class="eyebrow">Resources</p><h1>{esc(h1)}</h1>
    <p class="sec-sub">{esc(sub)}</p></div>
  </div>
</section>
{body_sections}"""
    return layout.page(ctx, path=path, title=title, description=description,
                       body=body, graph=graph, trail=trail)


def render_faq(ctx):
    site = ctx["site"]
    sections = f"""<section class="band band-top-tight">
  <div class="container container-narrow">
    {faq_list(FAQ_PAGE_FAQS)}
  </div>
</section>
<section class="band band-cream">
  <div class="container">
    {sec_head("Keep exploring", "More for foodservice buyers", center=True)}
    {link_grid([
        ('restaurant-produce-ordering-guide.html', 'Ordering guide', 'clipboard'),
        ('wholesale-produce-delivery-areas.html', 'Delivery areas', 'map'),
        ('restaurant-wholesale-produce.html', 'Restaurant produce', 'utensils'),
        ('seasonal-produce-for-restaurants-south-florida.html', 'Seasonal produce', 'sun'),
        ('contact.html', 'Contact sales', 'envelope'),
    ])}
  </div>
</section>
{cta_band(site, title="Still have a question?",
          text="Call or message us — a local team member who actually knows the routes will answer, any day of the week.")}"""
    return _simple_page(
        ctx, path="produce-delivery-faq.html",
        title="Produce Delivery FAQ | Broward & Palm Beach | Garden Fresh",
        description=("Answers about wholesale produce delivery in Broward and Palm "
                     "Beach Counties: order minimums, delivery fees, cutoff times, "
                     "split cases, standing orders, and account setup."),
        h1="Produce delivery FAQ",
        sub=("Straight answers about minimums, fees, cutoffs, routes, and account "
             "setup for South Florida foodservice kitchens."),
        body_sections=sections, faqs=FAQ_PAGE_FAQS)


def render_guide(ctx):
    site = ctx["site"]
    steps = card_grid([
        card("Set a baseline", "Build weekly pars for staple items that rarely change.", ic="clipboard"),
        card("Add specials", "Layer in seasonal and event items without rebuilding the entire order.", ic="sun"),
        card("Review waste", "Use split cases and by-the-pound items when volume is uncertain.", ic="box"),
    ], cols=3)
    sections = f"""<section class="band band-top-tight">
  <div class="container container-narrow">
    <p>A good order guide turns produce ordering from a nightly chore into a two-minute check. Here is how we build them with chefs across Broward and Palm Beach — and how to keep yours tight as menus and seasons change.</p>
  </div>
</section>
<section class="band band-mint">
  <div class="container">
    {sec_head("The method", "Three habits of low-waste kitchens", center=True)}
    {steps}
  </div>
</section>
<section class="band">
  <div class="container container-narrow">
    {sec_head("Ordering FAQ", "Questions chefs ask about order guides", center=True)}
    {faq_list(GUIDE_FAQS)}
  </div>
</section>
{cta_band(site, title="Want us to build your order guide?",
          text="Send your prep list and weekly volume — we will turn it into an online order guide with your pars, staples, and standing orders ready to go.")}"""
    return _simple_page(
        ctx, path="restaurant-produce-ordering-guide.html",
        title="Restaurant Produce Ordering Guide | South Florida",
        description=("How South Florida restaurants build produce order guides: "
                     "weekly pars, split cases, standing orders, and seasonal "
                     "specials — with help from Garden Fresh."),
        h1="Restaurant produce ordering guide",
        sub=("Build pars, split cases, standing orders, and seasonal requests "
             "that protect food cost."),
        body_sections=sections, faqs=GUIDE_FAQS)


def render_areas(ctx):
    site = ctx["site"]
    county_blocks = ""
    for county in ctx["counties"].values():
        groups_html = ""
        for group_name, slugs in county["groups"].items():
            links = "".join(
                f'<li><a href="{slug}-wholesale-produce.html">{esc(ctx["cities"][slug]["name"])}</a></li>'
                for slug in slugs)
            groups_html += (f'<div class="roster-col"><h3>{esc(group_name)}</h3>'
                            f'<ul class="roster-list">{links}</ul></div>')
        county_blocks += f"""<section class="band band-top-tight">
  <div class="container">
    {sec_head("County routes", county["name"], center=False)}
    <p><a href="{county['page']}">See the {esc(county['name'])} overview page</a> for route details, or jump straight to your city:</p>
    <div class="roster-grid">{groups_html}</div>
  </div>
</section>"""
    sections = f"""{county_blocks}
<section class="band band-cream">
  <div class="container">
    {sec_head("Not just restaurants", "Produce programs by kitchen type", center=True)}
    {link_grid([(s['file'], s['nav_label'], 'utensils') for s in ctx['services']])}
  </div>
</section>
{cta_band(site, title="Don't see your city?",
          text="Our routes cover all of Broward and Palm Beach Counties — if your kitchen is here, we deliver to it. Call and we will confirm your route and receiving window.")}"""
    return _simple_page(
        ctx, path="wholesale-produce-delivery-areas.html",
        title="Wholesale Produce Delivery Areas | Broward & Palm Beach",
        description=("Every Garden Fresh wholesale produce delivery area across "
                     "Broward and Palm Beach Counties — find your city's local "
                     "restaurant produce route."),
        h1="Wholesale produce delivery areas",
        sub=("Refrigerated routes across Broward and Palm Beach Counties, "
             "seven days a week from Pompano Beach."),
        body_sections=sections)
