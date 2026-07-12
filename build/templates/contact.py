"""Contact page."""

from lib import layout, schema
from lib.html import esc
from lib.components import sec_head, contact_form, icon, btn

TITLE = "Contact Garden Fresh | Restaurant Produce Delivery in South Florida"
DESCRIPTION = ("Contact Garden Fresh for restaurant wholesale produce delivery, "
               "account setup, catalog access, and support across Broward and "
               "Palm Beach Counties.")


def render(ctx):
    site = ctx["site"]
    path = "contact.html"
    addr = site["address"]

    detail_cards = f"""<div class="aside-card">
        <div class="card-icon">{icon('phone')}</div>
        <h3>Call or text</h3>
        <p><a href="tel:{site['phone_tel']}">{esc(site['phone_display'])}</a><br>{esc(site['hours_display'])}</p>
      </div>
      <div class="aside-card">
        <div class="card-icon">{icon('envelope')}</div>
        <h3>Email sales</h3>
        <p><a href="mailto:{site['email']}">{esc(site['email'])}</a><br>Same-business-day response.</p>
      </div>
      <div class="aside-card">
        <div class="card-icon">{icon('pin')}</div>
        <h3>Warehouse</h3>
        <p>{esc(addr['street'])}<br>{esc(addr['city'])}, {esc(addr['region'])} {esc(addr['zip'])}<br>
        <a href="{site['hasMap']}" rel="noopener">View on Google Maps</a></p>
      </div>
      <div class="aside-card">
        <div class="card-icon">{icon('cart')}</div>
        <h3>Existing customers</h3>
        <p>Order online any time through our catalog.</p>
        {btn(site['order_url'], 'Place order', 'solid', 'cart')}
      </div>"""

    body = f"""<section class="band band-tight">
  <div class="container split">
    <div class="split-main">
      <div class="sec-head"><p class="eyebrow">Contact</p><h1>Contact Garden Fresh</h1></div>
      <p>New accounts, produce questions, route timing, marine provisioning — send a message and a local team member will get back to you the same business day. Prefer the phone? Call <a href="tel:{site['phone_tel']}">{esc(site['phone_display'])}</a> between 4 AM and 4 PM, any day of the week.</p>
      {contact_form(site, form_id="contactForm", msg_id="contactMsg", form_name="contact", subject="Contact form — gardenfreshwholesale.com")}
    </div>
    <div class="split-aside">
      {detail_cards}
    </div>
  </div>
</section>"""

    trail = [("Home", None), ("Contact", path)]
    webpage = schema.webpage(site, path, TITLE, DESCRIPTION)
    webpage["@type"] = "ContactPage"
    graph = [
        webpage,
        schema.business(site),
        schema.breadcrumbs(site, trail),
    ]
    return layout.page(ctx, path=path, title=TITLE, description=DESCRIPTION,
                       body=body, graph=graph, trail=trail)
