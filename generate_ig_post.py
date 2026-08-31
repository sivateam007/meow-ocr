"""Generate attractive Instagram post for Meow OCR — v2 (gradients, better design)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "static", "images")

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REGULAR = r"C:\Windows\Fonts\arial.ttf"
FONT_IMPACT = r"C:\Windows\Fonts\impact.ttf"

OUT_SQ = os.path.join(BASE_DIR, "ig_post_square.jpg")
OUT_STORY = os.path.join(BASE_DIR, "ig_post_story.jpg")


def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2*radius, y0 + 2*radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2*radius, y0, x1, y0 + 2*radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2*radius, x0 + 2*radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2*radius, y1 - 2*radius, x1, y1], 0, 90, fill=fill)


def make_gradient(w, h, color_top, color_bottom):
    img = Image.new("RGB", (w, h))
    for y in range(h):
        ratio = y / h
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        ImageDraw.Draw(img).line([(0, y), (w, y)], fill=(r, g, b))
    return img


def text_with_shadow(draw, pos, text, font, fill, shadow_color=(0, 0, 0), shadow_offset=3):
    x, y = pos
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)


def text_center_shadow(draw, cy, text, font, fill, W, shadow_color=(0, 0, 0), shadow_offset=3):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    text_with_shadow(draw, (x, cy), text, font, fill, shadow_color, shadow_offset)
    return bbox[3] - bbox[1]


def make_square_post():
    W, H = 1080, 1080

    # === Background: deep purple-to-blue gradient ===
    bg = make_gradient(W, H, (25, 10, 60), (10, 30, 80))

    # === Add a decorative circle (top-right) ===
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([W-300, -150, W+100, 250], fill=(255, 100, 50, 40))
    od.ellipse([-100, H-400, 300, H+50], fill=(100, 200, 255, 30))
    bg = bg.convert("RGBA")
    bg = Image.alpha_composite(bg, overlay).convert("RGB")

    # === Load and place cat (smaller, bottom-left corner) ===
    cat = Image.open(os.path.join(ASSETS, "meow-hero.jpg")).convert("RGBA")
    cat = cat.resize((380, 380), Image.LANCZOS)
    cat_mask = Image.new("L", cat.size, 0)
    ImageDraw.Draw(cat_mask).ellipse([0, 0, 380, 380], fill=255)
    cat.putalpha(cat_mask)
    # Soft glow behind cat
    glow = Image.new("RGBA", (420, 420), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([0, 0, 420, 420], fill=(255, 140, 50, 50))
    bg.paste(glow, (20, H - 420), glow)
    bg.paste(cat, (40, H - 400), cat)

    draw = ImageDraw.Draw(bg)

    # === Top bar: brand name ===
    try:
        font_brand = ImageFont.truetype(FONT_BOLD, 38)
    except:
        font_brand = ImageFont.load_default()

    # Brand pill
    brand = "MEOW OCR"
    bbox = draw.textbbox((0, 0), brand, font=font_brand)
    bw = bbox[2] - bbox[0] + 40
    bh = bbox[3] - bbox[1] + 20
    draw_rounded_rect(draw, (30, 30, 30 + bw, 30 + bh), 20, (255, 140, 50))
    draw.text((50, 38), brand, font=font_brand, fill=(0, 0, 0))

    # === Main headline area ===
    try:
        font_big = ImageFont.truetype(FONT_IMPACT, 110)
    except:
        font_big = ImageFont.load_default()

    # "SCAN" in yellow
    text_center_shadow(draw, 160, "SCAN", font_big, (255, 210, 80), W, (0, 0, 0), 4)

    # Arrow
    try:
        font_arrow = ImageFont.truetype(FONT_BOLD, 70)
    except:
        font_arrow = ImageFont.load_default()
    arrow = ">>>>>"
    bbox = draw.textbbox((0, 0), arrow, font=font_arrow)
    tw = bbox[2] - bbox[0]
    text_with_shadow(draw, ((W - tw) // 2, 285), arrow, font_arrow, (255, 255, 255), (0, 0, 0), 3)

    # "TEXT" in white
    text_center_shadow(draw, 360, "TEXT", font_big, (255, 255, 255), W, (0, 0, 0), 4)

    # === Feature pills ===
    try:
        font_pill = ImageFont.truetype(FONT_BOLD, 30)
    except:
        font_pill = ImageFont.load_default()

    pills = ["FREE", "NO SIGNUP", "NO CARD"]
    pill_colors = [(46, 204, 113), (52, 152, 219), (155, 89, 182)]
    x_start = 160
    for i, (pill, color) in enumerate(zip(pills, pill_colors)):
        bbox = draw.textbbox((0, 0), pill, font=font_pill)
        pw = bbox[2] - bbox[0] + 30
        ph = bbox[3] - bbox[1] + 16
        draw_rounded_rect(draw, (x_start, 490, x_start + pw, 490 + ph), 12, color)
        draw.text((x_start + 15, 496), pill, font=font_pill, fill=(255, 255, 255))
        x_start += pw + 15

    # === Language line ===
    try:
        font_lang = ImageFont.truetype(FONT_BOLD, 34)
    except:
        font_lang = ImageFont.load_default()
    lang = "Tamil + 19 Languages"
    text_center_shadow(draw, 560, lang, font_lang, (200, 200, 255), W, (0, 0, 0), 2)

    # === Separator line ===
    draw.line([(100, 620), (W - 100, 620)], fill=(255, 255, 255, 80), width=2)

    # === Supported formats ===
    try:
        font_fmt = ImageFont.truetype(FONT_REGULAR, 26)
    except:
        font_fmt = ImageFont.load_default()
    fmts = ["PDF", "Images", "Documents", "Scans", "Photos"]
    fmt_text = "  |  ".join(fmts)
    text_center_shadow(draw, 645, fmt_text, font_fmt, (180, 180, 200), W, (0, 0, 0), 2)

    # === CTA Button ===
    try:
        font_cta = ImageFont.truetype(FONT_BOLD, 36)
    except:
        font_cta = ImageFont.load_default()
    cta = "TRY NOW FREE"
    bbox = draw.textbbox((0, 0), cta, font=font_cta)
    cta_w = bbox[2] - bbox[0] + 50
    cta_h = bbox[3] - bbox[1] + 28
    cta_x = (W - cta_w) // 2
    cta_y = 700
    draw_rounded_rect(draw, (cta_x, cta_y, cta_x + cta_w, cta_y + cta_h), 16, (255, 100, 50))
    draw.text((cta_x + 25, cta_y + 12), cta, font=font_cta, fill=(255, 255, 255))

    # === URL at bottom ===
    try:
        font_url = ImageFont.truetype(FONT_BOLD, 28)
    except:
        font_url = ImageFont.load_default()
    url = "www.meowocr.work.gd"
    bbox = draw.textbbox((0, 0), url, font=font_url)
    tw = bbox[2] - bbox[0]
    text_with_shadow(draw, ((W - tw) // 2, 790), url, font_url, (200, 200, 200), (0, 0, 0), 2)

    # === Bottom decorative dots ===
    for i in range(5):
        x = W // 2 - 40 + i * 20
        draw.ellipse([x, 840, x + 8, 848], fill=(255, 140, 50, 150))

    # === Corner accents ===
    draw.line([(0, 0), (80, 0)], fill=(255, 140, 50), width=4)
    draw.line([(0, 0), (0, 80)], fill=(255, 140, 50), width=4)
    draw.line([(W, H), (W - 80, H)], fill=(255, 140, 50), width=4)
    draw.line([(W, H), (W, H - 80)], fill=(255, 140, 50), width=4)

    bg.save(OUT_SQ, "JPEG", quality=95)
    print(f"Saved: {OUT_SQ} ({os.path.getsize(OUT_SQ)//1024} KB)")


def make_story_post():
    W, H = 1080, 1920

    # === Background: deep dark gradient ===
    bg = make_gradient(W, H, (15, 5, 40), (5, 15, 50))

    # Decorative circles
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([W-250, -100, W+50, 200], fill=(255, 100, 50, 35))
    od.ellipse([-80, 200, 220, 500], fill=(100, 200, 255, 25))
    od.ellipse([W-200, H-500, W+50, H-250], fill=(155, 89, 182, 20))
    bg = bg.convert("RGBA")
    bg = Image.alpha_composite(bg, overlay).convert("RGB")

    # Cat circle (top area)
    cat = Image.open(os.path.join(ASSETS, "meow-hero.jpg")).convert("RGBA")
    cat = cat.resize((300, 300), Image.LANCZOS)
    cat_mask = Image.new("L", cat.size, 0)
    ImageDraw.Draw(cat_mask).ellipse([0, 0, 300, 300], fill=255)
    cat.putalpha(cat_mask)
    # Glow
    glow = Image.new("RGBA", (340, 340), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([0, 0, 340, 340], fill=(255, 140, 50, 50))
    bg.paste(glow, (W // 2 - 170, 80), glow)
    bg.paste(cat, (W // 2 - 150, 100), cat)

    draw = ImageDraw.Draw(bg)

    # === Brand pill (top) ===
    try:
        font_brand = ImageFont.truetype(FONT_BOLD, 36)
    except:
        font_brand = ImageFont.load_default()
    brand = "MEOW OCR"
    bbox = draw.textbbox((0, 0), brand, font=font_brand)
    bw = bbox[2] - bbox[0] + 40
    bh = bbox[3] - bbox[1] + 18
    draw_rounded_rect(draw, ((W - bw) // 2, 420, (W + bw) // 2, 420 + bh), 18, (255, 140, 50))
    draw.text(((W - (bbox[2] - bbox[0])) // 2, 428), brand, font=font_brand, fill=(0, 0, 0))

    # === Main headline ===
    try:
        font_huge = ImageFont.truetype(FONT_IMPACT, 130)
    except:
        font_huge = ImageFont.load_default()

    text_center_shadow(draw, 510, "SCAN", font_huge, (255, 210, 80), W, (0, 0, 0), 5)

    # Arrow with animation feel
    try:
        font_arrow = ImageFont.truetype(FONT_BOLD, 80)
    except:
        font_arrow = ImageFont.load_default()
    arrow = ">>>>>"
    bbox = draw.textbbox((0, 0), arrow, font=font_arrow)
    tw = bbox[2] - bbox[0]
    text_with_shadow(draw, ((W - tw) // 2, 655), arrow, font_arrow, (255, 255, 255), (0, 0, 0), 3)

    text_center_shadow(draw, 750, "TEXT", font_huge, (255, 255, 255), W, (0, 0, 0), 5)

    # === Feature pills ===
    try:
        font_pill = ImageFont.truetype(FONT_BOLD, 32)
    except:
        font_pill = ImageFont.load_default()

    pills = [("FREE", (46, 204, 113)), ("NO SIGNUP", (52, 152, 219)), ("NO CARD", (155, 89, 182))]
    y_pill = 920
    for pill, color in pills:
        bbox = draw.textbbox((0, 0), pill, font=font_pill)
        pw = bbox[2] - bbox[0] + 36
        ph = bbox[3] - bbox[1] + 18
        px = (W - pw) // 2
        draw_rounded_rect(draw, (px, y_pill, px + pw, y_pill + ph), 14, color)
        draw.text((px + 18, y_pill + 8), pill, font=font_pill, fill=(255, 255, 255))
        y_pill += ph + 14

    # === Language ===
    try:
        font_lang = ImageFont.truetype(FONT_BOLD, 38)
    except:
        font_lang = ImageFont.load_default()
    text_center_shadow(draw, 1100, "Tamil + 19 Languages", font_lang, (200, 200, 255), W, (0, 0, 0), 3)

    # === Separator ===
    draw.line([(150, 1170), (W - 150, 1170)], fill=(255, 255, 255), width=2)

    # === Formats ===
    try:
        font_fmt = ImageFont.truetype(FONT_REGULAR, 28)
    except:
        font_fmt = ImageFont.load_default()
    fmts = ["PDF", "Images", "Documents", "Scans", "Photos"]
    y_fmt = 1195
    for fmt in fmts:
        text_center_shadow(draw, y_fmt, fmt, font_fmt, (170, 170, 190), W, (0, 0, 0), 2)
        y_fmt += 40

    # === CTA Button ===
    try:
        font_cta = ImageFont.truetype(FONT_BOLD, 40)
    except:
        font_cta = ImageFont.load_default()
    cta = "TRY NOW FREE"
    bbox = draw.textbbox((0, 0), cta, font=font_cta)
    cta_w = bbox[2] - bbox[0] + 55
    cta_h = bbox[3] - bbox[1] + 30
    cta_x = (W - cta_w) // 2
    cta_y = 1430
    draw_rounded_rect(draw, (cta_x, cta_y, cta_x + cta_w, cta_y + cta_h), 18, (255, 100, 50))
    draw.text((cta_x + 28, cta_y + 14), cta, font=font_cta, fill=(255, 255, 255))

    # === URL ===
    try:
        font_url = ImageFont.truetype(FONT_BOLD, 30)
    except:
        font_url = ImageFont.load_default()
    url = "www.meowocr.work.gd"
    bbox = draw.textbbox((0, 0), url, font=font_url)
    tw = bbox[2] - bbox[0]
    text_with_shadow(draw, ((W - tw) // 2, 1520), url, font_url, (200, 200, 200), (0, 0, 0), 2)

    # Swipe
    try:
        font_sw = ImageFont.truetype(FONT_REGULAR, 26)
    except:
        font_sw = ImageFont.load_default()
    swipe = "Swipe up to try"
    bbox = draw.textbbox((0, 0), swipe, font=font_sw)
    tw = bbox[2] - bbox[0]
    text_with_shadow(draw, ((W - tw) // 2, 1580), swipe, font_sw, (150, 150, 170), (0, 0, 0), 2)

    # Corner accents
    draw.line([(0, 0), (100, 0)], fill=(255, 140, 50), width=5)
    draw.line([(0, 0), (0, 100)], fill=(255, 140, 50), width=5)
    draw.line([(W, H), (W - 100, H)], fill=(255, 140, 50), width=5)
    draw.line([(W, H), (W, H - 100)], fill=(255, 140, 50), width=5)

    bg.save(OUT_STORY, "JPEG", quality=95)
    print(f"Saved: {OUT_STORY} ({os.path.getsize(OUT_STORY)//1024} KB)")


if __name__ == "__main__":
    make_square_post()
    make_story_post()
    print("Done!")
