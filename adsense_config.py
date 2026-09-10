"""
Google AdSense configuration for Meow OCR.

The publisher ID below is the one from your own AdSense account
(ca-pub-XXXXXXXXXXXXXXXX). It can be overridden via the ADSENSE_CLIENT
environment variable on Render; set ADSENSE_OFF=1 to disable the loader.
"""

import os


def _env_or(name, default=""):
    val = os.environ.get(name)
    return val if val else default


ADSENSE_CLIENT = os.environ.get("ADSENSE_CLIENT", "ca-pub-2878912285255336").strip()

_OFF = os.environ.get("ADSENSE_OFF", "").strip().lower() in ("1", "true", "yes", "on")

ADSENSE_ENABLED = bool(ADSENSE_CLIENT) and not _OFF


def adsense_tag():
    """Return the AdSense page-level loader script (raw HTML)."""
    if not ADSENSE_ENABLED:
        return ""
    return (
        '<script async src="https://pagead2.googlesyndication.com/pagead/js/'
        'adsbygoogle.js?client=' + ADSENSE_CLIENT + '" crossorigin="anonymous"></script>'
    )