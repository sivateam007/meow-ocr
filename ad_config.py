"""
Adsterra ad configuration for Meow OCR.

Paste the Adsterra ad-unit codes you created in the Adsterra dashboard into the
corresponding variable below (or set them as environment variables on Render):

    ADSTERRA_LEADERBOARD  -> 728x90 / responsive banner (below hero on home, top of content pages)
    ADSTERRA_INPAGE       -> 300x250 in-page / banner (in the main content flow)
    ADSTERRA_POPUNDER     -> popunder script (last, once you have traffic)

Empty strings (the default) disable that slot, so the site renders no ad
placeholders at all until you add a code. Keep "Show adult ads" OFF in Adsterra.
"""

import os


def _env_or(name, default=""):
    val = os.environ.get(name)
    return val if val else default


# Each value is raw HTML/JS injected as-is into the template (use |safe).
ADSTERRA_CODES = {
    "leaderboard": _env_or("ADSTERRA_LEADERBOARD"),
    "inpage": _env_or("ADSTERRA_INPAGE"),
    "popunder": _env_or("ADSTERRA_POPUNDER"),
}


def ads_slots():
    """Map logical slots -> codes, so templates only render what's configured."""
    return {
        "leaderboard": ADSTERRA_CODES.get("leaderboard", ""),
        "inpage": ADSTERRA_CODES.get("inpage", ""),
        "popunder": ADSTERRA_CODES.get("popunder", ""),
    }
