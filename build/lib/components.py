"""Reusable page components. Every function returns an HTML string."""

from .html import esc

WIDTH_STEPS = (480, 800, 1200, 1600, 1920)


def icon(name, cls="ic"):
    from .icons import ICONS
    return (f'<svg class="{cls}" aria-hidden="true" width="20" height="20" '
            f'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            f'{ICONS[name]}</svg>')


def _srcset(name, widths):
    return ", ".join(f"assets/images/r/{name}-{w}.webp {w}w" for w in widths)


def picture(images, name, alt, *, sizes="100vw", eager=False, cls=""):
    """Responsive <picture> from the generated-variants manifest."""
    meta = images[name]
    widths = meta["widths"]
    fallback = widths[min(len(widths) - 1, max(0, len(widths) - 2))]
    # Render intrinsic dimensions at the fallback width to avoid layout shift.
    w = fallback
    h = round(fallback * meta["h"] / meta["w"])
    loading = ('loading="eager" fetchpriority="high"' if eager
               else 'loading="lazy" decoding="async"')
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="{_srcset(name, widths)}" '
            f'sizes="{sizes}">'
            f'<img{cls_attr} src="assets/images/r/{name}-{fallback}.webp" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" {loading}></picture>')


def hero(images, *, image, alt, eyebrow, h1, lead, buttons, chips=None, tall=False):
    chips_html = ""
    if chips:
        chips_html = ('<ul class="fact-chips">' +
                      "".join(f'<li>{icon(i)}<span>{esc(t)}</span></li>'
                              for i, t in chips) + "</ul>")
    cls = "hero hero-tall" if tall else "hero"
    return f"""<section class="{cls}">
  {picture(images, image, alt, sizes="100vw", eager=True, cls="hero-img")}
  <div class="hero-scrim"></div>
  <div class="container hero-inner">
    <p class="eyebrow eyebrow-light">{esc(eyebrow)}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="btn-row">{buttons}</div>
    {chips_html}
  </div>
</section>"""


def split_hero(images, *, image, alt, eyebrow, h1, lead, buttons, chips=None):
    """Text-left, framed-photo-right hero for pages with smaller source images."""
    chips_html = ""
    if chips:
        chips_html = ('<ul class="fact-chips fact-chips-ink">' +
                      "".join(f'<li>{icon(i)}<span>{esc(t)}</span></li>'
                              for i, t in chips) + "</ul>")
    return f"""<section class="split-hero">
  <div class="container split split-media">
    <div class="split-main">
      <p class="eyebrow">{esc(eyebrow)}</p>
      <h1>{h1}</h1>
      <p class="lead lead-ink">{lead}</p>
      <div class="btn-row">{buttons}</div>
      {chips_html}
    </div>
    <div class="split-aside media-frame">
      {picture(images, image, alt, sizes="(min-width: 60rem) 44vw, 100vw", eager=True)}
    </div>
  </div>
</section>"""


def btn(href, label, style="solid", ic=None):
    ic_html = icon(ic) if ic else ""
    ext = ' rel="noopener"' if href.startswith("http") else ""
    return f'<a class="btn btn-{style}" href="{href}"{ext}>{ic_html}{esc(label)}</a>'


def sec_head(eyebrow, title, sub=None, center=False):
    cls = "sec-head sec-head-center" if center else "sec-head"
    sub_html = f'<p class="sec-sub">{esc(sub)}</p>' if sub else ""
    return (f'<div class="{cls}"><p class="eyebrow">{esc(eyebrow)}</p>'
            f'<h2>{esc(title)}</h2>{sub_html}</div>')


def card(title, text, ic=None, href=None, link_label=None):
    icon_html = f'<div class="card-icon">{icon(ic)}</div>' if ic else ""
    link = (f'<a class="card-link" href="{href}">{esc(link_label or "Learn more")}'
            f'{icon("arrow")}</a>' if href else "")
    return (f'<div class="card">{icon_html}<h3>{esc(title)}</h3>'
            f'<p>{esc(text)}</p>{link}</div>')


def card_grid(cards, cols=4):
    return f'<div class="card-grid" style="--cols:{cols}">' + "".join(cards) + "</div>"


def faq_list(faqs):
    """Render FAQ accordions. Must receive the same list given to schema.faq_page."""
    items = "".join(
        f'<details class="faq"><summary>{esc(f["q"])}</summary>'
        f'<div class="faq-a"><p>{esc(f["a"])}</p></div></details>'
        for f in faqs)
    return f'<div class="faq-list">{items}</div>'


def link_grid(links):
    """links: list of (href, label, icon_name)."""
    items = "".join(f'<a class="link-card" href="{href}">{icon(ic)}{esc(label)}</a>'
                    for href, label, ic in links)
    return f'<div class="link-grid">{items}</div>'


def cta_band(site, *, title, text, context_id="contact-cta"):
    return f"""<section id="{context_id}" class="band band-peach">
  <div class="container cta-band">
    <div class="cta-copy">
      <h2>{esc(title)}</h2>
      <p>{esc(text)}</p>
    </div>
    <div class="cta-actions">
      {btn('contact.html', 'Contact sales', 'solid', 'envelope')}
      {btn(f"tel:{site['phone_tel']}", f"Call {site['phone_display']}", 'ghost', 'phone')}
    </div>
  </div>
</section>"""


LOGOS = [
    ("racks", "Racks Fish House logo"),
    ("song", "Song restaurant logo"),
    ("islands", "Islands restaurant logo"),
    ("peters", "Peter's restaurant logo"),
    ("ethos", "Ethos Greek Bistro logo"),
    ("casablanca", "Casablanca Cafe logo"),
    ("papam", "Papa M restaurant logo"),
    ("spotos", "Spoto's Oyster Bar logo"),
    ("boatyard", "Boatyard restaurant logo"),
]


def logo_ticker():
    def row(hidden):
        aria = ' aria-hidden="true"' if hidden else ""
        imgs = "".join(
            f'<img src="assets/logos/{f}.png" alt="{"" if hidden else esc(alt)}" '
            f'loading="lazy" height="56">' for f, alt in LOGOS)
        return f'<div class="ticker-row"{aria}>{imgs}</div>'
    return (f'<div class="ticker" role="img" aria-label="Logos of South Florida '
            f'restaurants supplied by Garden Fresh"><div class="ticker-track">'
            f'{row(False)}{row(True)}</div></div>')


def contact_form(site, *, form_id="contactForm", msg_id="contactMsg",
                 form_name="contact", subject="New inquiry from gardenfreshwholesale.com"):
    return f"""<form id="{form_id}" class="gf-form" action="{site['formspree']}" method="POST" data-formspree-form>
  <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp-field">
  <input type="hidden" name="form_name" value="{esc(form_name)}">
  <input type="hidden" name="_subject" value="{esc(subject)}">
  <div class="form-row">
    <label>Name<input type="text" name="name" required autocomplete="name"></label>
    <label>Business<input type="text" name="company" autocomplete="organization"></label>
  </div>
  <div class="form-row">
    <label>Email<input type="email" name="email" required autocomplete="email"></label>
    <label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
  </div>
  <label>What does your kitchen need?<textarea name="message" rows="4" required placeholder="Prep list, delivery window, weekly volume, chef preferences…"></textarea></label>
  <button class="btn btn-solid" type="submit">{icon('envelope')}Send message</button>
  <p id="{msg_id}" data-form-message class="form-msg" role="status"></p>
</form>"""


def route_facts(site):
    facts = [
        ("clock", "4 AM dispatch", "Trucks leave our Pompano Beach warehouse before your first cook clocks in."),
        ("calendar", "7-day routes", "Refrigerated delivery across Broward and Palm Beach every day of the week."),
        ("box", "Split cases", "Full cases, split cases, and by-the-pound items to match real prep needs."),
        ("shield", "No fees, no minimums", "No delivery fees, no fuel charges, and no order minimums on local routes."),
    ]
    return card_grid([card(t, d, ic=i) for i, t, d in facts], cols=4)
