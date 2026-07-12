"""Home page."""

from lib import layout, schema
from lib.html import esc
from lib.components import (picture, hero, btn, sec_head, card, card_grid,
                            faq_list, link_grid, cta_band, icon, logo_ticker,
                            contact_form, route_facts)

TITLE = "Restaurant Produce Delivery | Garden Fresh"
DESCRIPTION = ("We supply local restaurants in Broward and Palm Beach Counties with "
               "wholesale produce, split cases, no minimums, and 7-day delivery.")

HOW_STEPS = [
    ("clipboard", "1. Request an account", "Send your business info, receiving window, and a sample prep list — by form or phone."),
    ("basket", "2. Build your order", "We turn your prep list into an online order guide with your staples and pars."),
    ("calendar", "3. Choose delivery days", "Daily, weekdays, or around events — routes run seven days a week."),
    ("truck", "4. Receive before prep", "Trucks leave Pompano Beach at 4 AM so produce lands before your line fires up."),
]


def render(ctx):
    site = ctx["site"]

    hero_html = hero(
        ctx["images"], image="restaurant-hero",
        alt="Chef preparing fresh produce in a South Florida restaurant kitchen",
        eyebrow="Wholesale produce · Broward & Palm Beach Counties",
        h1="Restaurant wholesale produce delivery for Broward and Palm Beach kitchens",
        lead=("We supply restaurants, chefs, cafes, bars, caterers, and hospitality "
              "kitchens with consistent produce, refrigerated delivery, split cases, "
              "and online ordering across South Florida."),
        buttons=(btn(site["order_url"], "Place order", "light", "cart") +
                 btn("contact.html", "Request pricing", "outline-light", "clipboard")),
        chips=[("truck", "4 AM dispatch"), ("calendar", "7-day routes"),
               ("box", "Split cases"), ("shield", "No minimums or fees")],
        tall=True)

    ticker_section = f"""<section class="band band-slim" id="proof">
  <div class="container">
    {sec_head("Kitchens we deliver to", "Trusted by South Florida restaurants", center=True)}
  </div>
  {logo_ticker()}
</section>"""

    about_section = f"""<section class="band" id="about">
  <div class="container split split-media">
    <div class="split-main">
      {sec_head("Why Garden Fresh", "A produce partner that runs on chef time")}
      <p>We partner with regional farms and national growers to source peak-fresh produce across seasons. Chefs and restaurant owners get cold-chain handling, practical pack sizes, and a local team in Pompano Beach that understands prep schedules, receiving windows, and what happens when a menu changes at 10 PM.</p>
      <ul class="check-list">
        <li>Refrigerated warehouse handling and delivery vehicles.</li>
        <li>Case, split case, and by-the-pound options.</li>
        <li>Order by 12 AM for next-day delivery on most items.</li>
        <li>GAP/HACCP-conscious handling and cold-chain delivery.</li>
      </ul>
      <div class="btn-row">{btn('contact.html', 'Talk to sales', 'solid', 'envelope')}{btn('produce-delivery-faq.html', 'Delivery FAQ', 'ghost')}</div>
    </div>
    <div class="split-aside media-frame">
      {picture(ctx["images"], "produce-display", "Fresh produce display of seasonal fruits and vegetables", sizes="(min-width: 60rem) 40vw, 100vw")}
    </div>
  </div>
</section>"""

    product_cards = card_grid(
        [card(p["name"], p["card_blurb"], href=p["file"], link_label="See varieties")
         for p in ctx["products"]], cols=4)
    catalog_section = f"""<section class="band band-mint" id="catalog">
  <div class="container">
    {sec_head("The catalog", "Wholesale produce categories", center=True)}
    {product_cards}
    <div class="band-foot">{btn(site["catalog_url"], "Browse the full catalog", "solid", "basket")}</div>
  </div>
</section>"""

    how_section = f"""<section class="band" id="how">
  <div class="container">
    {sec_head("How it works", "From prep list to loading dock", center=True)}
    {card_grid([card(t, d, ic=i) for i, t, d in HOW_STEPS], cols=4)}
  </div>
</section>"""

    service_cards = card_grid(
        [card(s["name"], s["card_blurb"], href=s["file"], link_label="How we help",
              ic=i) for s, i in zip(ctx["services"],
                                    ["utensils", "building", "book", "anchor", "sun"])],
        cols=3)
    services_section = f"""<section class="band band-citrus" id="services">
  <div class="container">
    {sec_head("Who we serve", "Wholesale produce programs for every kitchen", center=True)}
    {service_cards}
  </div>
</section>"""

    area_cols = ""
    for county in ctx["counties"].values():
        links = "".join(
            f'<li><a href="{slug}-wholesale-produce.html">{esc(ctx["cities"][slug]["name"])}</a></li>'
            for group in county["groups"].values() for slug in group[:3])
        area_cols += f"""<div class="roster-col">
      <h3><a href="{county['page']}">{esc(county['name'])}</a></h3>
      <ul class="roster-list">{links}</ul>
      <a class="card-link" href="{county['page']}">All {esc(county['name'])} routes{icon('arrow')}</a>
    </div>"""
    areas_section = f"""<section class="band" id="service-area">
  <div class="container">
    {sec_head("Where we deliver", "Local routes across two counties", center=True)}
    <div class="roster-grid roster-grid-2">{area_cols}</div>
    <div class="band-foot">{btn('wholesale-produce-delivery-areas.html', 'See every delivery area', 'ghost', 'map')}</div>
  </div>
</section>"""

    marine_section = f"""<section class="band band-deep" id="marine">
  <div class="container split">
    <div class="split-main">
      {sec_head("Marine division", "Yacht and marine provisioning")}
      <p>Dockside produce provisioning for yachts, charters, and crew kitchens from Fort Lauderdale to Palm Beach marinas — hand-selected produce, pack-out suited to marine refrigeration, and delivery timed to your departure.</p>
      <div class="btn-row">{btn('yacht-marine-provisioning.html', 'Marine provisioning', 'light', 'anchor')}<a class="btn btn-outline-light" href="#contact" data-prefill="Marine Provisioning: Please send your itinerary, headcount, departure marina, and dates.">Get a quote</a></div>
    </div>
    <div class="split-aside media-frame">
      {picture(ctx["images"], "yacht-provisioning-crates", "Produce crates staged for yacht provisioning", sizes="(min-width: 60rem) 40vw, 100vw")}
    </div>
  </div>
</section>"""

    resources_section = f"""<section class="band band-cream" id="seo-resources">
  <div class="container">
    {sec_head("Resources", "Guides for foodservice buyers", center=True)}
    {card_grid([
        card("Delivery FAQ", "Minimums, cutoff times, delivery fees, routes, and account setup.", ic="book", href="produce-delivery-faq.html", link_label="Read the FAQ"),
        card("Ordering guide", "Build pars, split cases, standing orders, and seasonal requests.", ic="clipboard", href="restaurant-produce-ordering-guide.html", link_label="Read the guide"),
        card("Delivery areas", "Every wholesale produce route across Broward and Palm Beach.", ic="map", href="wholesale-produce-delivery-areas.html", link_label="Find your city"),
        card("Seasonal produce", "Plan specials around South Florida seasons and availability.", ic="sun", href="seasonal-produce-for-restaurants-south-florida.html", link_label="Plan the season"),
    ], cols=4)}
  </div>
</section>"""

    contact_section = f"""<section class="band" id="contact">
  <div class="container split">
    <div class="split-main">
      {sec_head("Get started", "Set up wholesale produce delivery")}
      <p>Send your prep list, delivery window, and weekly volume. A local team member will reach out the same business day to build your order guide and set up online ordering.</p>
      <address class="contact-nap">
        {icon('pin')}550 NE 28th Ct, Pompano Beach, FL 33064<br>
        {icon('phone')}<a href="tel:{site['phone_tel']}">{esc(site['phone_display'])}</a><br>
        {icon('clock')}{esc(site['hours_display'])}
      </address>
    </div>
    <div class="split-aside">
      {contact_form(site, form_id="signupForm", msg_id="signupMsg", form_name="account_signup", subject="New account request — gardenfreshwholesale.com")}
    </div>
  </div>
</section>"""

    body = "\n".join([hero_html, ticker_section, about_section, catalog_section,
                      how_section, services_section, areas_section, marine_section,
                      resources_section, contact_section])

    graph = [
        schema.webpage(site, "", TITLE, DESCRIPTION),
        schema.business(site),
    ]
    return layout.page(ctx, path="", title=TITLE, description=DESCRIPTION,
                       body=body, graph=graph)
