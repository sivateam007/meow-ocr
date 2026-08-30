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


# Strictly env-var driven: no code is baked in. A Monetag script only loads when
# the matching Render environment variable is set. Set these in the Render
# dashboard (Environment -> Add Environment Variable) to the FULL script tag:
#
#     MONETAG_VIGNETTE  -> Vignette/Interstitial zone <script src="..."> snippet
#     MONETAG_INPAGE    -> In-Page Push / Anchor zone snippet
#     MONETAG_POPUNDER  -> OnClick (Popunder) zone snippet
#     MONETAG_PUSH      -> Push Notifications zone snippet
#
# Empty (unset) means the slot is OFF — no script loads.

_VIGNETTE_DEFAULT = '<script src="https://quge5.com/88/tag.min.js" data-zone="274429" async data-cfasync="false"></script>'

MONETAG = {
    "vignette": _env_or("MONETAG_VIGNETTE", _VIGNETTE_DEFAULT),
    "inpage": _env_or("MONETAG_INPAGE", ""),
    "popunder": _env_or("MONETAG_POPUNDER", ""),
    "push": _env_or("MONETAG_PUSH", ""),
}

MONETAG_ENABLED = bool(MONETAG.get("vignette") or MONETAG.get("inpage")
                       or MONETAG.get("popunder") or MONETAG.get("push"))
