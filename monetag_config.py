"""
Monetag (Monetag.com) ad configuration for Meow OCR.

Each tag is the raw HTML/JS snippet provided by the Monetag dashboard
(below "Get tag"). They are injected into the <head> of every user-facing
page via templates/monetag.html.

You can override any value with a Render environment variable, e.g.:

    MONETAG_VIGNETTE  -> Vignette/Interstitial zone <script src="..."> snippet
    MONETAG_INPAGE    -> In-Page Push / Anchor zone snippet
    MONETAG_POPUNDER  -> OnClick (Popunder) zone snippet
    MONETAG_PUSH      -> Push Notifications zone snippet

Empty strings disable that slot. Keep unrubbed/unapproved codes OFF until the
zone is approved by Monetag to avoid blank ad space.
"""

import os


def _env_or(name, default=""):
    val = os.environ.get(name)
    return val if val else default


# Default codes (paste new Monetag tags here). Rail-safe: only put codes you
# actually want live. Env vars always override.
_DEFAULT = {
    "vignette": '<script src="https://quge5.com/88/tag.min.js" data-zone="274429" async data-cfasync="false"></script>',
    "inpage": "",
    "popunder": "",
    "push": "",
}

MONETAG = {
    "vignette": _env_or("MONETAG_VIGNETTE", _DEFAULT["vignette"]),
    "inpage": _env_or("MONETAG_INPAGE", _DEFAULT["inpage"]),
    "popunder": _env_or("MONETAG_POPUNDER", _DEFAULT["popunder"]),
    "push": _env_or("MONETAG_PUSH", _DEFAULT["push"]),
}

MONETAG_ENABLED = bool(MONETAG.get("vignette") or MONETAG.get("inpage")
                       or MONETAG.get("popunder") or MONETAG.get("push"))
