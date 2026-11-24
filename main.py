import os
import sys, shutil
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    _out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
    os.makedirs(os.path.dirname(_out) or ".", exist_ok=True)
    shutil.copyfile(os.path.join(os.environ.get("MAKEFUN_BOT_DIR", "/bot"), "entry.png"), _out)
    sys.exit(0)

W = H = 1024
NAVY = "#f2eadb"
TEAL = "#9d4f35"
CREAM = "#fffaf0"
GRAY = "#726b60"
INK = "#292b2b"
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

# A restrained vermilion edge anchors the paper-like page.
d.rectangle((0, 0, W, 7), fill=TEAL)
text(46, 26, "THE WORLD / DAILY BRIEF", 16, TEAL, True)
text(747, 28, "NO. 327  •  GLOBAL", 14, "#68645d", True)
text(46, 63, "Monday 23 November 2026", 43, INK, True)
text(48, 122, "Nine stories moving the world tonight", 18, GRAY)

cards = [
    (46, 184, "#ef6461", "TECH · REDMOND", ["Microsoft: patch AI", "flaws with care"], ["Rushing AI-exposure fixes can", "risk downtime across critical", "systems."], "23 Nov  /  IANS", "chip"),
    (526, 184, "#e8b44d", "MARKETS · SF", ["Anthropic's IPO road", "was no normal float"], ["Bankers bridled at founder", "control, in a SpaceX echo.", ""], "23 Nov  /  BS", "chart"),
    (46, 397, "#67a9e8", "POLITICS · DC", ["Democrats hit 258", "House seats record"], ["AP: the mark fell Sunday as", "wave gains reshaped the", "House."], "23 Nov  /  AP", "flag"),
    (526, 397, TEAL, "CLIMATE · PORTSMOUTH", ["UK digs reservoirs", "against drought"], ["£800m Havant Thicket", "reservoir is rising to help", "secure water supplies."], "23 Nov  /  SBS", "waves"),
]
for x, y, accent, kicker, title, body, credit, glyph in cards:
    d.rounded_rectangle((x, y, x+452, y+194), radius=16, fill=CREAM)
    d.rounded_rectangle((x, y+13, x+6, y+181), radius=3, fill=accent)
    text(x+22, y+14, kicker, 12, accent, True)
    text(x+22, y+39, title[0], 20, INK, True)
    text(x+22, y+65, title[1], 20, INK, True)
    for i, line in enumerate(body):
        if line:
            text(x+22, y+99+i*19, line, 12, "#66717d")
    text(x+22, y+164, credit, 11, "#7e8790", True)
    badge(x+391, y+96, glyph, accent)

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
d.rounded_rectangle((823, 707, 948, 737), radius=15, fill="#d7c5a9")
text(851, 714, "CLIMATE", 12, TEAL, True)
text(270, 752, "COP31 collapses: no deal, first time in 17 years", 22, INK, True)
text(270, 812, "EU and ~130 parties threw out a text that", 17, GRAY)
text(270, 840, "skipped fossil fuels; markets slid on AI fears.  /  23 Nov", 17, GRAY)
# A ladder beside a small flame marks the summit story.
d.line((114, 891, 158, 765), fill=TEAL, width=6)
d.line((185, 891, 158, 765), fill=TEAL, width=6)
for yy in (876, 852, 828, 804):
    d.line((125+(876-yy)//3, yy, 179-(876-yy)//3, yy), fill=TEAL, width=4)
d.polygon(((153,767),(143,748),(157,753),(164,734),(173,757),(166,771)), fill="#ef6461")

d.line((46, 938, 978, 938), fill="#c9bba5", width=1)
text(46, 954, "WORLD DESK  •  NOV 23, 2026", 11, GRAY)
text(788, 954, "9 STORIES  /  1 DAY", 11, TEAL, True)
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
im.save(OUT)
print(f"wrote {OUT}")
