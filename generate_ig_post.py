"""Generate Instagram post image for Meow OCR (1080x1080 square)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "static", "images")

# Fonts
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REGULAR = r"C:\Windows\Fonts\arial.ttf"

# Output
OUT_SQ = os.path.join(BASE_DIR, "ig_post_square.jpg")
OUT_STORY = os.path.join(BASE_DIR, "ig_post_story.jpg")


def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)


def make_square_post():
    W, H = 1080, 1080
    # Load hero cat
    cat = Image.open(os.path.join(ASSETS, "meow-hero.jpg")).convert("RGB")
    # Resize to fill
    cat_ratio = cat.width / cat.height
    if cat_ratio > 1:
        new_h = H
        new_w = int(new_h * cat_ratio)
    else:
        new_w = W
        new_h = int(new_w / cat_ratio)
    cat = cat.resize((new_w, new_h), Image.LANCZOS)
    # Center crop
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    cat = cat.crop((left, top, left + W, top + H))

    # Apply slight blur for text readability
    bg = cat.filter(ImageFilter.GaussianBlur(radius=3))

    # Dark gradient overlay
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        # Stronger at top and bottom, lighter in middle
        if y < H * 0.45:
            alpha = int(180 * (1 - y / (H * 0.45)))
        elif y > H * 0.55:
            alpha = int(180 * ((y - H * 0.55) / (H * 0.45)))
        else:
            alpha = 80
        alpha = max(0, min(200, alpha))
        od.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    bg = bg.convert("RGBA")
    bg = Image.alpha_composite(bg, overlay)
    bg = bg.convert("RGB")

    draw = ImageDraw.Draw(bg)

    # === TOP: Cat emoji + "MEOW OCR" ===
    try:
        font_brand = ImageFont.truetype(FONT_BOLD, 52)
    except Exception:
        font_brand = ImageFont.load_default()
    brand_text = "MEOW OCR"
    bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 50), brand_text, fill=(255, 255, 255), font=font_brand)

    # === CENTER: Big emoji arrow ===
    try:
        font_emoji = ImageFont.truetype(FONT_BOLD, 100)
    except Exception:
        font_emoji = ImageFont.load_default()
    emoji_text = "SCAN  >  TEXT"
    bbox = draw.textbbox((0, 0), emoji_text, font=font_emoji)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 340), emoji_text, fill=(255, 255, 255), font=font_emoji)

    # === CENTER-BOTTOM: Subtitle ===
    try:
        font_sub = ImageFont.truetype(FONT_BOLD, 42)
    except Exception:
        font_sub = ImageFont.load_default()
    sub_lines = [
        "Free OCR. No Signup. No Card.",
        "Tamil + 19 Languages",
    ]
    y_pos = 500
    for line in sub_lines:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y_pos), line, fill=(255, 255, 255), font=font_sub)
        y_pos += 65

    # === BOTTOM: URL box ===
    try:
        font_url = ImageFont.truetype(FONT_BOLD, 36)
    except Exception:
        font_url = ImageFont.load_default()
    url_text = "www.meowocr.work.gd"
    bbox = draw.textbbox((0, 0), url_text, font=font_url)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    box_pad = 20
    box_x0 = (W - tw) // 2 - box_pad
    box_y0 = H - 140
    box_x1 = (W + tw) // 2 + box_pad
    box_y1 = box_y0 + th + box_pad * 2
    draw_rounded_rect(draw, (box_x0, box_y0, box_x1, box_y1), 16, (255, 140, 50))
    draw.text(((W - tw) // 2, box_y0 + box_pad), url_text, fill=(0, 0, 0), font=font_url)

    # === BOTTOM: cat paw / small tagline ===
    try:
        font_sm = ImageFont.truetype(FONT_REGULAR, 24)
    except Exception:
        font_sm = ImageFont.load_default()
    tagline = "PDF  |  Images  |  Documents  |  Scans"
    bbox = draw.textbbox((0, 0), tagline, font=font_sm)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 70), tagline, fill=(200, 200, 200), font=font_sm)

    bg.save(OUT_SQ, "JPEG", quality=92)
    print(f"Saved: {OUT_SQ}  ({os.path.getsize(OUT_SQ)//1024} KB)")


def make_story_post():
    W, H = 1080, 1920
    # Load hero cat
    cat = Image.open(os.path.join(ASSETS, "meow-hero.jpg")).convert("RGB")
    cat_ratio = cat.width / cat.height
    if cat_ratio > 1:
        new_h = H
        new_w = int(new_h * cat_ratio)
    else:
        new_w = W
        new_h = int(new_w / cat_ratio)
    cat = cat.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    cat = cat.crop((left, top, left + W, top + H))

    bg = cat.filter(ImageFilter.GaussianBlur(radius=3))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        if y < H * 0.4:
            alpha = int(190 * (1 - y / (H * 0.4)))
        elif y > H * 0.6:
            alpha = int(190 * ((y - H * 0.6) / (H * 0.4)))
        else:
            alpha = 80
        alpha = max(0, min(210, alpha))
        od.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    bg = bg.convert("RGBA")
    bg = Image.alpha_composite(bg, overlay)
    bg = bg.convert("RGB")

    draw = ImageDraw.Draw(bg)

    # Top brand
    try:
        font_brand = ImageFont.truetype(FONT_BOLD, 64)
    except Exception:
        font_brand = ImageFont.load_default()
    brand_text = "MEOW OCR"
    bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 120), brand_text, fill=(255, 255, 255), font=font_brand)

    # Big center block
    try:
        font_big = ImageFont.truetype(FONT_BOLD, 100)
    except Exception:
        font_big = ImageFont.load_default()

    # "SCAN > TEXT" in one line
    center_line = "SCAN  >  TEXT"
    bbox = draw.textbbox((0, 0), center_line, font=font_big)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 680), center_line, fill=(255, 210, 80), font=font_big)

    # Subtitle
    try:
        font_sub = ImageFont.truetype(FONT_BOLD, 48)
    except Exception:
        font_sub = ImageFont.load_default()
    sub_lines = [
        "Free OCR",
        "No Signup. No Card.",
        "Tamil + 19 Languages",
    ]
    y_pos = 850
    for line in sub_lines:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y_pos), line, fill=(255, 255, 255), font=font_sub)
        y_pos += 70

    # URL box
    try:
        font_url = ImageFont.truetype(FONT_BOLD, 44)
    except Exception:
        font_url = ImageFont.load_default()
    url_text = "www.meowocr.work.gd"
    bbox = draw.textbbox((0, 0), url_text, font=font_url)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    box_pad = 24
    box_x0 = (W - tw) // 2 - box_pad
    box_y0 = H - 220
    box_x1 = (W + tw) // 2 + box_pad
    box_y1 = box_y0 + th + box_pad * 2
    draw_rounded_rect(draw, (box_x0, box_y0, box_x1, box_y1), 18, (255, 140, 50))
    draw.text(((W - tw) // 2, box_y0 + box_pad), url_text, fill=(0, 0, 0), font=font_url)

    # Bottom tagline
    try:
        font_sm = ImageFont.truetype(FONT_REGULAR, 28)
    except Exception:
        font_sm = ImageFont.load_default()
    tagline = "PDF  |  Images  |  Documents  |  Scans"
    bbox = draw.textbbox((0, 0), tagline, font=font_sm)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 130), tagline, fill=(200, 200, 200), font=font_sm)

    # Swipe up
    try:
        font_sw = ImageFont.truetype(FONT_REGULAR, 30)
    except Exception:
        font_sw = ImageFont.load_default()
    swipe = "Swipe up to try"
    bbox = draw.textbbox((0, 0), swipe, font=font_sw)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 70), swipe, fill=(180, 180, 180), font=font_sw)

    bg.save(OUT_STORY, "JPEG", quality=92)
    print(f"Saved: {OUT_STORY}  ({os.path.getsize(OUT_STORY)//1024} KB)")


if __name__ == "__main__":
    make_square_post()
    make_story_post()
    print("Done!")
