#!/usr/bin/env python3
"""Regenerate og.png (1200x630) and apple-touch-icon.png (180x180) for tag.passqr.com.

    python3 -m pip install pillow
    python3 tools/make-images.py

Both outputs are quantised to a flat palette on the way out — the card is large areas
of one green, so 16 colours is visually identical and about a third of the bytes.

Fonts: uses Fraunces + Instrument Sans if they are installed (download them from Google
Fonts into ~/Library/Fonts on the Mac), otherwise falls back to DejaVu. The fallback is
legible but off-brand — install the real faces before regenerating for production.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent

PINE = (10, 79, 69)
PAPER = (239, 247, 244)
TEAL = (14, 124, 107)
MUTED = (150, 180, 172)

# In preference order. The first two are the real brand faces; install them into
# ~/Library/Fonts from Google Fonts and the card is drawn in the same type as the site.
# The rest are the same fallbacks the page's own font-family stack names, so the card
# degrades the way the page does rather than to a bitmap face.
DISPLAY = ["Fraunces-SemiBold.ttf", "Fraunces_9pt-SemiBold.ttf",
           "/Library/Fonts/Fraunces-SemiBold.ttf",
           "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
           "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
BODY = ["InstrumentSans-Medium.ttf", "/Library/Fonts/InstrumentSans-Medium.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def font(candidates, size):
    for c in candidates:
        for p in (Path(c), Path.home() / "Library/Fonts" / c, Path("/usr/share/fonts") / c):
            if p.exists():
                return ImageFont.truetype(str(p), size)
    print("  ! no candidate font found, falling back to a bitmap face:", candidates[0])
    return ImageFont.load_default()


def qr_mark(d, x, y, s, fg=PAPER):
    """The three-finder PassQR mark, drawn at size s."""
    u = s / 64
    for cx, cy in ((11, 11), (36, 11), (11, 36)):
        d.rounded_rectangle(
            [x + cx * u, y + cy * u, x + (cx + 17) * u, y + (cy + 17) * u],
            radius=3.5 * u, outline=fg, width=int(max(2, 5 * u)))
    d.ellipse([x + 35 * u, y + 35 * u, x + 54 * u, y + 54 * u], fill=TEAL)


def og():
    img = Image.new("RGB", (1200, 630), PINE)
    d = ImageDraw.Draw(img)

    # a single hairline rule under the wordmark, nothing else — no gradient wash
    d.line([(80, 176), (1120, 176)], fill=(24, 96, 85), width=2)

    qr_mark(d, 80, 78, 72)
    d.text((172, 92), "PassQR Tag", font=font(BODY, 34), fill=PAPER)

    h = font(DISPLAY, 72)
    d.text((80, 214), "Be reachable without", font=h, fill=PAPER)
    d.text((80, 300), "publishing your number.", font=h, fill=PAPER)

    b = font(BODY, 31)
    d.text((80, 426), "A contact sticker that carries a code, not a phone number.", font=b, fill=MUTED)
    d.text((80, 470), "The relay checks the sender is really there — then keeps trying", font=b, fill=MUTED)
    d.text((80, 514), "to reach you until you answer.", font=b, fill=MUTED)

    d.text((80, 574), "tag.passqr.com   ·   a DaSecure product", font=font(BODY, 24), fill=(120, 160, 150))

    img.quantize(colors=16, dither=Image.Dither.NONE).save(OUT / "og.png", optimize=True)
    print("wrote og.png")


def touch_icon():
    img = Image.new("RGB", (180, 180), PINE)
    qr_mark(ImageDraw.Draw(img), 14, 14, 152)
    img.quantize(colors=8, dither=Image.Dither.NONE).save(OUT / "apple-touch-icon.png", optimize=True)
    print("wrote apple-touch-icon.png")


if __name__ == "__main__":
    og()
    touch_icon()
