#!/usr/bin/env python3
"""Reusable news-image generator (news-image-20261123, based on proven news22d/repo3 engine).

NEXT-RUN USAGE:
  1. Edit DATE_LINE and STORIES below with 23 Nov 2026 news (5-6 stories, cross-region/field).
  2. Test: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   (check out/entry.png < 1 MiB, 1024x1024)
  3. Copy out/entry.png to repo root as entry.png, commit, submit.
"""
import os, shutil, sys
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile("/bot/entry.png", "/output/entry.png")
    sys.exit(0)

OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output") + "/entry.png"
W = H = 1024
BG = "#101C2C"
PAPER = "#F4F1E8"
INK = "#172638"
MUTED = "#A8B5C2"
TEAL = "#63D5C0"
CORAL = "#FF776D"
GOLD = "#F5C968"
BLUE = "#79AFFF"

# ---------------- EDIT ONLY THIS BLOCK NEXT RUN ----------------
DATE_LINE = "Monday 23 November 2026"
SUBHEAD = "Five stories moving the world"
STORIES = [
    # (accent, kicker, [title lines], [body lines], icon kind, source line)
    (CORAL, "Cyber · Washington", ["Microsoft warns AI-fix", "race risks outages"],
     ["IANS: patching AI-exposed flaws", "fast may cause more downtime.", "23 Nov  /  IANS"], "ai"),
    (GOLD,  "Markets · SF", ["Anthropic ran odd", "path to its IPO"],
     ["Bankers chafed over tight control,", "echoing the SpaceX listing.", "23 Nov  /  BS"], "market"),
    (BLUE,  "Politics · US", ["Democrats take 258", "House seats: record"],
     ["AP: marker reached Sunday; big", "gains from general election.", "23 Nov  /  AP"], "diplomacy"),
    (TEAL,  "Climate · Portsmouth", ["UK digs reservoirs", "for droughts"],
     ["£800m Havant Thicket near", "Portsmouth under construction.", "23 Nov  /  SBS"], "climate"),
]
# Wide bottom story (diplomatic dispatch style)
WIDE = {
    "region": "EUROPE  /  ANTALYA", "accent": CORAL, "kind": "fire",
    "title": "COP31 collapses: no deal for first time in 17 years",
    "l1": "EU and ~130 parties rejected a text omitting",
    "l2": "fossil fuels; markets slid on AI fears.  /  23 Nov",
    "badge": "CLIMATE",
}
FOOTER_LEFT = "WORLD DESK  •  Reported 23 November 2026"
# ----------------------------------------------------------------

def font(size, bold=False):
    candidates = (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else
                  ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)

def rr(box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def text(x, y, s, size, fill=INK, bold=False, anchor=None):
    d.text((x, y), s, font=font(size, bold), fill=fill, anchor=anchor)

def line(points, fill, width=4):
    d.line(points, fill=fill, width=width, joint="curve")

def icon(kind, cx, cy, color):
    d.ellipse((cx-49, cy-49, cx+49, cy+49), fill="#20364A")
    if kind == "climate":
        d.ellipse((cx-17, cy-24, cx+17, cy+10), outline=color, width=5)
        for a,b in [(-34,-24),(-31,2),(34,-24),(31,2),(0,-39)]:
            line([(cx+a,cy+b),(cx+a*1.18,cy+b*1.18)], color, 3)
        line([(cx-31,cy+20),(cx-12,cy+13),(cx+5,cy+22),(cx+30,cy+14)], color, 5)
        line([(cx-31,cy+32),(cx-12,cy+25),(cx+5,cy+34),(cx+30,cy+26)], color, 5)
    elif kind == "ai":
        rr((cx-27,cy-27,cx+27,cy+27),8,None,color,4)
        for dx,dy in [(-37,-16),(-37,0),(-37,16),(37,-16),(37,0),(37,16),(-16,-37),(0,-37),(16,-37),(-16,37),(0,37),(16,37)]:
            line([(cx+dx,cy+dy),(cx+dx*0.78,cy+dy*0.78)],color,3)
        d.ellipse((cx-7,cy-7,cx+7,cy+7),fill=color)
    elif kind == "ship":
        line([(cx-37,cy+12),(cx+37,cy+12),(cx+23,cy+29),(cx-23,cy+29),(cx-37,cy+12)],color,4)
        rr((cx-19,cy-12,cx+15,cy+9),3,None,color,4)
        line([(cx-26,cy+38),(cx-9,cy+33),(cx+8,cy+38),(cx+25,cy+33)],color,3)
        line([(cx+30,cy-31),(cx+19,cy-18),(cx+31,cy-15),(cx+20,cy-1)],GOLD,4)
    elif kind == "fire":
        line([(cx-23,cy+34),(cx,cy-32),(cx+23,cy+34)],color,4)
        line([(cx-16,cy+10),(cx+16,cy+10)],color,3)
        line([(cx-20,cy+23),(cx+20,cy+23)],color,3)
        line([(cx-31,cy-12),(cx+31,cy-12)],color,4)
        line([(cx+16,cy-27),(cx+28,cy-37),(cx+27,cy-21),(cx+39,cy-28),(cx+32,cy-8)],CORAL,4)
    elif kind == "diplomacy":
        line([(cx,cy-34),(cx,cy+35)],color,4)
        d.polygon([(cx+2,cy-31),(cx+29,cy-22),(cx+2,cy-12)],fill=CORAL)
        line([(cx-2,cy-5),(cx-30,cy-14),(cx-2,cy-23)],color,4)
        line([(cx-28,cy+35),(cx+28,cy+35)],color,4)
    elif kind == "health":
        line([(cx,cy-28),(cx,cy+28)],color,6)
        line([(cx-28,cy),(cx+28,cy)],color,6)
        d.ellipse((cx-34,cy-16,cx-18,cy),outline=color,width=3)
    elif kind == "market":
        line([(cx-32,cy+22),(cx-14,cy+4),(cx, cy+14),(cx+16,cy-10),(cx+32,cy-22)],color,4)

def card(x, y, w, h, accent, kicker, title_lines, body_lines, kind):
    rr((x,y,x+w,y+h),20,PAPER)
    d.rounded_rectangle((x,y,x+8,y+h),radius=4,fill=accent)
    icon(kind,x+w-83,y+83,accent)
    text(x+24,y+20,kicker.upper(),16,accent,True)
    for i, s in enumerate(title_lines):
        text(x+24,y+53+i*30,s,24,INK,True)
    for i, s in enumerate(body_lines):
        text(x+24,y+123+i*27,s,18,"#3F5060")

# Masthead
d.rectangle((0,0,W,8),fill=TEAL)
text(44,31,"THE WORLD / DAILY BRIEF",17,TEAL,True)
text(980,31,"NO. 327   •   GLOBAL",15,MUTED,True,anchor="ra")
text(44,66,DATE_LINE,48,PAPER,True)
text(46,127,SUBHEAD,22,MUTED)
line([(44,170),(980,170)],"#304254",2)

# Four compact cards
cw, ch = 454, 264
positions = [(44,190),(526,190),(44,472),(526,472)]
for (x,y),(accent,kicker,tl,bl,kind) in zip(positions,STORIES):
    card(x,y,cw,ch,accent,kicker,tl,bl,kind)

# Wide bottom story
wd = WIDE
rr((44,754,980,944),20,"#20364A")
d.rounded_rectangle((44,754,52,944),radius=4,fill=wd["accent"])
icon(wd["kind"],126,849,wd["accent"])
text(202,775,wd["region"],16,wd["accent"],True)
text(202,808,wd["title"],25,PAPER,True)
text(202,850,wd["l1"],19,"#D2DCE5")
text(202,878,wd["l2"],19,"#D2DCE5")
rr((841,774,954,814),18,"#314D63")
text(897,794,wd["badge"],13,PAPER,True,anchor="mm")

line([(44,966),(980,966)],"#304254",2)
text(44,978,FOOTER_LEFT,14,MUTED)
text(980,978,"5 STORIES / ONE DAY",14,TEAL,True,anchor="ra")

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
im.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")