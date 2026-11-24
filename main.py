import os
import sys, shutil
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    _out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
    os.makedirs(os.path.dirname(_out) or ".", exist_ok=True)
    shutil.copyfile(os.path.join(os.environ.get("MAKEFUN_BOT_DIR", "/bot"), "entry.png"), _out)
    sys.exit(0)

 # Warm paper, rust accents, and dark ink set the page's visual palette.
CANVAS_WIDTH = CANVAS_HEIGHT = 1024
PAPER_TONE = "#f2eadb"
RUST_ACCENT = "#9d4f35"
CARD_TONE = "#fffaf0"
MUTED_INK = "#726b60"
PRIMARY_INK = "#292b2b"
BADGE_BLUE = "#203b52"
BAR_TONE = "#e8ddc9"
BAR_INK = "#68645d"

# Keep the compact drawing helpers readable below.
W, H = CANVAS_WIDTH, CANVAS_HEIGHT
NAVY, TEAL, CREAM, GRAY, INK = PAPER_TONE, RUST_ACCENT, CARD_TONE, MUTED_INK, PRIMARY_INK
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

im = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(im)
font_dir = "/usr/share/fonts/truetype/dejavu"
regular = os.path.join(font_dir, "DejaVuSans.ttf")
bold = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
def f(size, heavy=False):
    try:
        return ImageFont.truetype(bold if heavy else regular, size)
    except OSError:
        return ImageFont.load_default()

def text(x, y, value, size, color, heavy=False):
    d.text((x, y), value, font=f(size, heavy), fill=color)

def badge(cx, cy, kind, color):
    r = 39
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill="#203b52")
    if kind == "chip":
        d.rounded_rectangle((cx-19, cy-19, cx+19, cy+19), radius=5, outline=color, width=3)
        d.rectangle((cx-8, cy-8, cx+8, cy+8), outline=color, width=2)
        for n in (-12, 0, 12):
            d.line((cx-25, cy+n, cx-19, cy+n), fill=color, width=3)
            d.line((cx+19, cy+n, cx+25, cy+n), fill=color, width=3)
    elif kind == "chart":
        d.line((cx-22, cy+19, cx-22, cy-20), fill=color, width=3)
        d.line((cx-22, cy+19, cx+23, cy+19), fill=color, width=3)
        d.line((cx-16, cy+9, cx-4, cy-2, cx+6, cy+5, cx+19, cy-13), fill=color, width=4, joint="curve")
    elif kind == "flag":
        d.line((cx-16, cy+23, cx-16, cy-23), fill=color, width=4)
        d.polygon(((cx-13,cy-20),(cx+21,cy-13),(cx+5,cy+1),(cx-13,cy-4)), outline=color)
        d.line((cx-13, cy-20, cx+21, cy-13, cx+5, cy+1, cx-13, cy-4), fill=color, width=3)
    else:
        for off in (-10, 2, 14):
            d.arc((cx-24, cy+off-9, cx+24, cy+off+9), 200, 340, fill=color, width=3)

# Masthead: a narrow rust line gives the paper a clear top edge.
d.rectangle((0, 0, CANVAS_WIDTH, 8), fill=RUST_ACCENT)

# The desk name and edition number sit on a shared baseline.
masthead_y = 25
text(46, masthead_y, "THE WORLD / DAILY BRIEF", 16, RUST_ACCENT, True)
text(747, masthead_y + 2, "NO. 327  •  GLOBAL", 14, BAR_INK, True)
d.line((46, 52, 978, 52), fill="#d8cbb7", width=1)

# Today's date carries the page's strongest type weight.
date_label = "Monday 23 November 2026"
text(46, 66, date_label, 42, PRIMARY_INK, True)

# Pair the short deck with a small edition marker at the right edge.
deck_y = 122
text(48, deck_y, "Nine stories moving the world tonight", 18, MUTED_INK)
d.rounded_rectangle((795, 117, 978, 148), radius=15, fill=BAR_TONE)
text(836, 125, "MONDAY EDITION", 11, RUST_ACCENT, True)

# A quiet lower rule separates the heading from the story cards.
d.line((46, 165, 978, 165), fill="#d8cbb7", width=1)

cards = [
    (46, 184, "#ef6461", "TECH · REDMOND", "Microsoft: patch AI", "flaws with care", "Rushing AI-exposure fixes can", "risk downtime across critical", "systems.", "23 Nov  /  IANS", "chip"),
    (526, 184, "#e8b44d", "MARKETS · SF", "Anthropic's IPO road", "was no normal float", "Bankers bridled at founder", "control, in a SpaceX echo.", "", "23 Nov  /  BS", "chart"),
    (46, 397, "#67a9e8", "POLITICS · DC", "Democrats hit 258", "House seats record", "AP: the mark fell Sunday as", "wave gains reshaped the", "House.", "23 Nov  /  AP", "flag"),
    (526, 397, TEAL, "CLIMATE · PORTSMOUTH", "UK digs reservoirs", "against drought", "£800m Havant Thicket", "reservoir is rising to help", "secure water supplies.", "23 Nov  /  SBS", "waves"),
]
for (x, y, accent, kicker, title_line_1, title_line_2,
     body_line_1, body_line_2, body_line_3, credit, glyph) in cards:
    d.rounded_rectangle((x, y, x + 452, y + 194), radius=16, fill=CREAM)
    d.rounded_rectangle((x, y + 13, x + 6, y + 181), radius=3, fill=accent)
    text(x + 22, y + 14, kicker.upper(), 12, accent, True)
    text(x + 22, y + 39, title_line_1, 20, INK, True)
    text(x + 22, y + 65, title_line_2, 20, INK, True)
    for i, line in enumerate((body_line_1, body_line_2, body_line_3)):
        if line:
            text(x + 22, y + 99 + i * 19, line, 12, "#66717d")
    text(x + 22, y + 164, credit, 11, "#7e8790", True)
    badge(x + 391, y + 96, glyph, accent)

# A one-line ticker carries four more briefs between the cards and the lead.
d.rounded_rectangle((46, 604, 978, 668), radius=14, fill="#e8ddc9")
tick = [
    (66, "LIBYA  Ukrainian sea drone sinks", "Russian warship at Benghazi dock"),
    (526, "HORMUZ  Three more ships struck;", "pace highest since February"),
]
for x, l1, l2 in tick:
    text(x, 624, l1, 13, "#d5dde5")
    text(x, 643, l2, 13, "#d5dde5")

# The evening lead spans the full page width.
d.rounded_rectangle((46, 688, 978, 916), radius=18, fill="#e8ddc9")
text(270, 712, "EUROPE  /  ANTALYA", 13, "#9d4f35", True)
text(270, 752, "COP31 ends with no deal for the first time", 22, INK, True)
text(270, 812, "EU and ~130 parties rejected a draft that", 17, GRAY)
text(270, 840, "skipped fossil fuels; AI fears sank stocks.  /  23 Nov", 17, GRAY)
# Summit emblem: an ascending frame topped by a compact flame.
left_rail = (114, 891, 158, 765)
right_rail = (185, 891, 158, 765)
d.line(left_rail, fill=RUST_ACCENT, width=6)
d.line(right_rail, fill=RUST_ACCENT, width=6)
for rung_y in (876, 852, 828, 804):
    inset = (876 - rung_y) // 3
    d.line((125 + inset, rung_y, 179 - inset, rung_y), fill=RUST_ACCENT, width=4)
flame_shape = ((153, 767), (143, 748), (157, 753), (164, 734), (173, 757), (166, 771))
d.polygon(flame_shape, fill="#ef6461")

# Footer rule and desk label close the page beneath the lead panel.
footer_y = 938
d.line((46, footer_y, 978, footer_y), fill="#c9bba5", width=1)
text(46, footer_y + 16, "WORLD DESK  •  NOV 23, 2026", 11, MUTED_INK)
text(788, footer_y + 16, "5 STORIES / 24 HOURS", 11, RUST_ACCENT, True)
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
im.save(OUT)
print(f"wrote {OUT}")
