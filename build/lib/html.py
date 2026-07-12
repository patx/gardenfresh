"""Small HTML helpers shared by all templates."""

_ESC = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}


def esc(text):
    """Escape text for safe interpolation into HTML content/attributes."""
    out = str(text)
    for ch, rep in _ESC.items():
        out = out.replace(ch, rep)
    return out


def attr(text):
    return esc(text)


def join(parts):
    return "".join(p for p in parts if p)
