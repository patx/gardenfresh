"""JSON-LD builders. All nodes are plain dicts; serialize once with dumps()."""

import json


def dumps(graph):
    blob = json.dumps({"@context": "https://schema.org", "@graph": graph},
                      separators=(",", ":"), ensure_ascii=True)
    # Prevent premature </script> termination inside JSON strings.
    return blob.replace("</", "<\\/")


def script(graph):
    return f'<script type="application/ld+json">{dumps(graph)}</script>'


def business(site):
    """The canonical LocalBusiness node, identical on every page."""
    base = site["base_url"]
    return {
        "@type": "LocalBusiness",
        "@id": f"{base}/#business",
        "name": site["name"],
        "legalName": site["legal_name"],
        "url": f"{base}/",
        "logo": f"{base}/{site['logo']}",
        "image": f"{base}/{site['default_social_image']}",
        "telephone": site["phone"],
        "email": site["email"],
        "priceRange": site["price_range"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": site["address"]["street"],
            "addressLocality": site["address"]["city"],
            "addressRegion": site["address"]["region"],
            "postalCode": site["address"]["zip"],
            "addressCountry": site["address"]["country"],
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": site["geo"]["lat"],
            "longitude": site["geo"]["lng"],
        },
        "hasMap": site["hasMap"],
        "openingHours": site["hours"],
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Broward County, FL"},
            {"@type": "AdministrativeArea", "name": "Palm Beach County, FL"},
        ],
        "description": site["description"],
    }


def webpage(site, path, title, description, image=None):
    base = site["base_url"]
    url = f"{base}/{path}" if path else f"{base}/"
    node = {
        "@type": "WebPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": title,
        "description": description,
        "isPartOf": {
            "@type": "WebSite",
            "@id": f"{base}/#website",
            "name": site["name"],
            "url": f"{base}/",
        },
    }
    if image:
        node["primaryImageOfPage"] = f"{base}/{image}"
    return node


def service(site, name, service_type, area=None):
    node = {
        "@type": "Service",
        "name": name,
        "serviceType": service_type,
        "provider": {"@id": f"{site['base_url']}/#business"},
    }
    if area:
        node["areaServed"] = area
    return node


def city_area(city, county_name):
    node = {
        "@type": "City",
        "name": f"{city['name']}, FL",
        "containedInPlace": {"@type": "AdministrativeArea",
                             "name": f"{county_name}, FL"},
    }
    if city.get("lat") and city.get("lng"):
        node["geo"] = {"@type": "GeoCoordinates",
                       "latitude": city["lat"], "longitude": city["lng"]}
    return node


def breadcrumbs(site, trail):
    """trail: list of (name, path-or-None). Last item is the current page."""
    base = site["base_url"]
    items = []
    for i, (name, path) in enumerate(trail, 1):
        item = {"@type": "ListItem", "position": i, "name": name}
        item["item"] = f"{base}/{path}" if path else f"{base}/"
        items.append(item)
    return {"@type": "BreadcrumbList", "itemListElement": items}


def faq_page(faqs):
    """faqs: list of {"q":..., "a":...} — the same list the visible FAQ renders."""
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"],
             "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in faqs
        ],
    }
