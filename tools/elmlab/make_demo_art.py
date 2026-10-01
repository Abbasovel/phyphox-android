#!/usr/bin/env python3
"""Illustrations for the Elm Lab demo home screen (4 experiments). Output: app/src/main/res/drawable-nodpi/elmlab_demo_*.png"""
import math, pathlib
from PIL import Image, ImageDraw, ImageFont
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT/"app/src/main/res/drawable-nodpi"; OUT.mkdir(exist_ok=True)
F = pathlib.Path(__file__).parent/"fonts"
S = 1200  # draw at 2x, save 600
BG, BG2, BLUE, BLUE2, RED, YEL, WHITE, MUTED = (20,34,51), (28,46,68), (122,170,255), (47,111,214), (255,123,111), (255,209,102), (255,255,255), (154,170,189)
def font(sz, bold=True): return ImageFont.truetype(str(F/("IBMPlexSansCondensed-Bold.ttf" if bold else "IBMPlexSans-SemiBold.ttf")), sz)
def canvas():
    im = Image.new("RGB",(S,S),BG); d = ImageDraw.Draw(im)
    for i in range(0,S,60):  # faint graph-paper grid
        d.line([(i,0),(i,S)], fill=BG2, width=2); d.line([(0,i),(S,i)], fill=BG2, width=2)
    return im, d
def arrow(d, p0, p1, col, w=18, head=48):
    d.line([p0,p1], fill=col, width=w)
    a = math.atan2(p1[1]-p0[1], p1[0]-p0[0])
    l = (p1[0]-head*math.cos(a-0.45), p1[1]-head*math.sin(a-0.45)); r = (p1[0]-head*math.cos(a+0.45), p1[1]-head*math.sin(a+0.45))
    d.polygon([p1,l,r], fill=col)
def save(im, n): im.resize((600,600), Image.LANCZOS).save(OUT/f"elmlab_demo_{n}.png", optimize=True)

# 1. pressure: person, air denser at the feet, arrows
im, d = canvas()
import random; random.seed(3)
for _ in range(900):
    y = random.random()**0.55*S; x = random.random()*S
    r = 5; d.ellipse([x-r,y-r,x+r,y+r], fill=(60,90,130))
cx = 680
d.ellipse([cx-85,170,cx+85,340], fill=WHITE)                      # head
d.rounded_rectangle([cx-150,370,cx+150,760], radius=90, fill=WHITE) # body
d.rounded_rectangle([cx-130,700,cx-30,1050], radius=45, fill=WHITE) # legs
d.rounded_rectangle([cx+30,700,cx+130,1050], radius=45, fill=WHITE)
d.line([(120,1080),(1080,1080)], fill=MUTED, width=8)
arrow(d,(1000,250),(860,250),BLUE,w=12,head=36); arrow(d,(1000,1000),(800,1000),RED,w=26,head=64)
d.text((1010,250),"p₂", font=font(80), fill=BLUE, anchor="lm"); d.text((990,900),"p₁", font=font(90), fill=RED, anchor="lm")
arrow(d,(220,1000),(220,260),YEL,w=10,head=36); arrow(d,(220,260),(220,1000),YEL,w=10,head=36)
d.text((260,620),"1,7 m", font=font(78), fill=YEL, anchor="lm")
d.rounded_rectangle([60,50,560,150], radius=30, fill=BLUE2); d.text((310,100),"Δp ≈ 20 Pa", font=font(78), fill=WHITE, anchor="mm")
save(im,"pressure")

# 2. weightlessness: parabola with phone, |a| = 0
im, d = canvas()
pts = [(150+i*9, 1040 - (1-((i-50)/50)**2)*600) for i in range(101)]
for i in range(0,100,4): d.line([pts[i],pts[i+2]], fill=BLUE, width=16)
arrow(d, pts[8], pts[14], BLUE, w=16, head=50); arrow(d, pts[86], pts[93], BLUE, w=16, head=50)
def phone(cx, cy, ang, sc=1.0):
    w,h = 150*sc, 270*sc
    ph = Image.new("RGBA",(int(w)+20,int(h)+20),(0,0,0,0)); pd = ImageDraw.Draw(ph)
    pd.rounded_rectangle([10,10,10+w,10+h], radius=30*sc, fill=WHITE); pd.rounded_rectangle([24,40*sc,w-4,h-30*sc], radius=10, fill=BLUE2)
    ph = ph.rotate(ang, expand=True, resample=Image.BICUBIC); im.paste(ph,(int(cx-ph.width/2),int(cy-ph.height/2)),ph)
phone(*pts[50], 25)
for (x,y),a in [(pts[22],-30),(pts[78],60)]: phone(x,y,a,0.6)
d.ellipse([60,1000,250,1080], fill=MUTED); d.text((155,1040),"", font=font(40))
d.line([(80,1090),(1120,1090)], fill=MUTED, width=8)
d.rounded_rectangle([390,60,810,170], radius=30, fill=RED); d.text((600,115),"|a| = 0", font=font(90), fill=WHITE, anchor="mm")
arrow(d,(600,640),(600,820),YEL,w=14,head=44); d.text((630,760),"g", font=font(90), fill=YEL, anchor="lm")
save(im,"weightless")

# 3. car acceleration
im, d = canvas()
for y,l in [(520,260),(620,340),(720,220)]: d.line([(40,y),(40+l,y)], fill=MUTED, width=14)
body = [(300,760),(300,600),(420,590),(540,450),(830,450),(960,590),(1110,620),(1130,760)]
d.polygon(body, fill=BLUE2); d.line(body+[body[0]], fill=BLUE, width=10)
d.polygon([(560,480),(680,480),(680,585),(470,585)], fill=(150,190,240)); d.polygon([(710,480),(815,480),(920,585),(710,585)], fill=(150,190,240))
for x in (450,980):
    d.ellipse([x-100,680,x+100,880], fill=(10,16,26)); d.ellipse([x-55,725,x+55,835], fill=MUTED)
d.line([(80,890),(1160,890)], fill=MUTED, width=8)
arrow(d,(560,300),(1000,300),RED,w=30,head=80); d.text((480,300),"a", font=font(140), fill=RED, anchor="mm")
d.rounded_rectangle([200,960,1000,1100], radius=36, fill=BLUE2); d.text((600,1030),"0–100 km/s", font=font(96), fill=WHITE, anchor="mm")
save(im,"car")

# 4. speed of sound: two phones, waves, distance d
im, d = canvas()
def phone_up(cx, cy):
    d.rounded_rectangle([cx-80,cy-150,cx+80,cy+150], radius=26, fill=WHITE); d.rounded_rectangle([cx-62,cy-120,cx+62,cy+118], radius=8, fill=BLUE2)
phone_up(200,640); phone_up(1000,640)
d.text((200,430),"A", font=font(110), fill=WHITE, anchor="mm"); d.text((1000,430),"B", font=font(110), fill=WHITE, anchor="mm")
for r in range(120,700,95):
    d.arc([200-r,640-r,200+r,640+r], start=-30, end=30, fill=BLUE, width=16)
arrow(d,(220,1030),(980,1030),YEL,w=12,head=40); arrow(d,(980,1030),(220,1030),YEL,w=12,head=40)
d.text((600,1110),"d", font=font(110), fill=YEL, anchor="mm")
d.rounded_rectangle([250,90,950,230], radius=36, fill=RED); d.text((600,160),"v = 2d / Δt", font=font(100), fill=WHITE, anchor="mm")
save(im,"sound")
print("art ok")
