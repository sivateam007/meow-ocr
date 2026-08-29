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
# Keys are public Adsterra ad keys (safe to embed); env vars can override.
_DEFAULT_CODES = {
    "leaderboard": """<script>
  atOptions = {
    'key' : '8e11da306a8403463a573608363e6d88',
    'format' : 'iframe',
    'height' : 90,
    'width' : 728,
    'params' : {}
  };
</script>
<script src="https://commercialhalftime.com/8e11da306a8403463a573608363e6d88/invoke.js"></script>""",
    "inpage": """<script>
  atOptions = {
    'key' : 'efba19609d11bf438955d5a5d2968d45',
    'format' : 'iframe',
    'height' : 250,
    'width' : 300,
    'params' : {}
  };
</script>
<script src="https://commercialhalftime.com/efba19609d11bf438955d5a5d2968d45/invoke.js"></script>""",
    "popunder": "",
}

ADSTERRA_CODES = {
    "leaderboard": _env_or("ADSTERRA_LEADERBOARD", _DEFAULT_CODES["leaderboard"]),
    "inpage": _env_or("ADSTERRA_INPAGE", _DEFAULT_CODES["inpage"]),
    "popunder": _env_or("ADSTERRA_POPUNDER", _DEFAULT_CODES["popunder"]),
}


def ads_slots():
    """Map logical slots -> codes, so templates only render what's configured."""
    return {
        "leaderboard": ADSTERRA_CODES.get("leaderboard", ""),
        "inpage": ADSTERRA_CODES.get("inpage", ""),
        "popunder": ADSTERRA_CODES.get("popunder", ""),
    }
