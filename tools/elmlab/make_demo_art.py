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

# ---------- tools (full Elm Lab app) ----------
def save_tool(im, n): im.resize((600,600), Image.LANCZOS).save(OUT/f"elmlab_tool_{n}.png", optimize=True)

# tone generator: speaker + waves + frequency
im, d = canvas()
d.rectangle([180,470,330,730], fill=WHITE); d.polygon([(330,470),(560,280),(560,920),(330,730)], fill=WHITE)
for i,r in enumerate(range(140,560,105)):
    d.arc([560-r,600-r,560+r,600+r], start=-38, end=38, fill=BLUE if i%2==0 else YEL, width=22)
pts=[(250+i*7, 1050+70*math.sin(i/9)) for i in range(101)]
d.line(pts, fill=RED, width=16, joint="curve")
d.rounded_rectangle([700,90,1120,220], radius=36, fill=BLUE2); d.text((910,155),"440 Hz", font=font(96), fill=WHITE, anchor="mm")
save_tool(im,"tone")

# flashlight stroboscope: torch + pulsed beam + rotating fan
im, d = canvas()
d.rounded_rectangle([90,520,420,680], radius=30, fill=WHITE); d.polygon([(420,500),(520,450),(520,750),(420,700)], fill=WHITE)
d.rounded_rectangle([200,560,260,640], radius=10, fill=BLUE2)
for k in range(4):
    x0=560+k*150; d.polygon([(x0,600-60-k*45),(x0+90,600-90-k*55),(x0+90,600+90+k*55),(x0,600+60+k*45)], fill=YEL if k%2==0 else (120,110,60))
cx,cy=960,950
for a in range(0,360,90):
    ang=math.radians(a+20); d.polygon([(cx,cy),(cx+170*math.cos(ang-0.25),cy+170*math.sin(ang-0.25)),(cx+170*math.cos(ang+0.25),cy+170*math.sin(ang+0.25))], fill=BLUE)
d.ellipse([cx-28,cy-28,cx+28,cy+28], fill=WHITE)
for i in range(6):  # square pulse train
    x=90+i*110; d.line([(x,1060),(x,980),(x+55,980),(x+55,1060),(x+110,1060)], fill=RED, width=14)
d.rounded_rectangle([90,90,520,220], radius=36, fill=BLUE2); d.text((305,155),"f = 25 Hz", font=font(92), fill=WHITE, anchor="mm")
save_tool(im,"strobe")

# pendulum: pivot, string, bob, arc, period
im, d = canvas()
px,py,L=600,170,700
d.rectangle([380,130,820,170], fill=MUTED)
for a,col,w in [(-28,(70,90,120),10),(0,(70,90,120),10)]:
    x=px+L*math.sin(math.radians(a)); y=py+L*math.cos(math.radians(a)); d.line([(px,py),(x,y)], fill=col, width=w); d.ellipse([x-70,y-70,x+70,y+70], outline=col, width=10)
a=24; x=px+L*math.sin(math.radians(a)); y=py+L*math.cos(math.radians(a))
d.line([(px,py),(x,y)], fill=WHITE, width=12); d.ellipse([x-80,y-80,x+80,y+80], fill=RED)
d.arc([px-L-90,py-L-90,px+L+90,py+L+90], start=90-34, end=90+34, fill=YEL, width=12)
arrow(d,(px+(L+90)*math.sin(math.radians(30)),py+(L+90)*math.cos(math.radians(30))),(px+(L+90)*math.sin(math.radians(34)),py+(L+90)*math.cos(math.radians(34))),YEL,w=12,head=44)
d.rounded_rectangle([140,960,1060,1100], radius=36, fill=BLUE2); d.text((600,1030),"T = 2π√(L/g)", font=font(96), fill=WHITE, anchor="mm")
save_tool(im,"pendulum")

# acoustic stopwatch: stopwatch + two claps
im, d = canvas()
cx,cy,R=600,640,330
d.rectangle([555,230,645,300], fill=WHITE); d.rounded_rectangle([510,190,690,240], radius=16, fill=WHITE)
d.ellipse([cx-R,cy-R,cx+R,cy+R], fill=WHITE); d.ellipse([cx-R+40,cy-R+40,cx+R-40,cy+R-40], fill=BG2)
for k in range(12):
    ang=math.radians(k*30); d.line([(cx+(R-80)*math.sin(ang),cy-(R-80)*math.cos(ang)),(cx+(R-50)*math.sin(ang),cy-(R-50)*math.cos(ang))], fill=MUTED, width=12)
d.pieslice([cx-R+60,cy-R+60,cx+R-60,cy+R-60], start=-90, end=20, fill=(47,111,214))
d.line([(cx,cy),(cx+(R-90)*math.cos(math.radians(20)),cy+(R-90)*math.sin(math.radians(20)))], fill=RED, width=18); d.ellipse([cx-26,cy-26,cx+26,cy+26], fill=RED)
for sx in (130,1070):
    for r in (60,120,180):
        d.arc([sx-r,330-r,sx+r,330+r], start=(200 if sx<600 else -20), end=(340 if sx<600 else 160), fill=YEL, width=12)
d.rounded_rectangle([320,1020,880,1130], radius=36, fill=BLUE2); d.text((600,1075),"Δt = 0,347 s", font=font(84), fill=WHITE, anchor="mm")
save_tool(im,"stopwatch")
print("tools art ok")

# ---------- sensors (full Elm Lab app) ----------
def save_sensor(im, n): im.resize((600,600), Image.LANCZOS).save(OUT/f"elmlab_sensor_{n}.png", optimize=True)
def phone_at(d, cx, cy, w=300, h=520):
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2], radius=50, fill=WHITE)
    d.rounded_rectangle([cx-w/2+24,cy-h/2+60,cx+w/2-24,cy+h/2-60], radius=14, fill=BLUE2)
def badge(d, text, col=BLUE2, y=150):
    w = font(92).getlength(text)+120
    d.rounded_rectangle([600-w/2,y-65,600+w/2,y+65], radius=36, fill=col); d.text((600,y),text, font=font(92), fill=WHITE, anchor="mm")

# accelerometer with g: phone + x/y/z axes + g
im, d = canvas(); phone_at(d,600,660)
arrow(d,(600,660),(900,660),RED,w=16,head=46); d.text((930,660),"x", font=font(90), fill=RED, anchor="lm")
arrow(d,(600,660),(600,330),(92,224,160),w=16,head=46); d.text((640,330),"y", font=font(90), fill=(92,224,160), anchor="lm")
arrow(d,(600,660),(420,840),BLUE,w=16,head=46); d.text((380,880),"z", font=font(90), fill=BLUE, anchor="mm")
arrow(d,(1000,850),(1000,1120),YEL,w=22,head=60); d.text((1050,990),"g", font=font(110), fill=YEL, anchor="lm")
badge(d,"9,81 m/s²"); save_sensor(im,"accelerometer")

# linear acceleration: phone moving with speed lines
im, d = canvas()
for y,l in [(520,260),(660,340),(800,220)]: d.line([(80,y),(80+l,y)], fill=MUTED, width=16)
phone_at(d,620,660)
arrow(d,(820,660),(1110,660),RED,w=30,head=80); d.text((960,560),"a", font=font(120), fill=RED, anchor="mm")
badge(d,"g olmadan"); save_sensor(im,"linear")

# gyroscope: phone + rotation arc ω
im, d = canvas(); phone_at(d,600,660,260,450)
d.arc([260,320,940,1000], start=200, end=340, fill=YEL, width=24)
arrow(d,(870,420),(905,470),YEL,w=24,head=70)
d.arc([260,320,940,1000], start=20, end=160, fill=(120,110,60), width=14)
badge(d,"ω, rad/s"); save_sensor(im,"gyroscope")

# magnetometer: horseshoe magnet + field lines
im, d = canvas()
for k,r in enumerate([150,230,310,390]):
    d.arc([600-r,560-r,600+r,560+r], start=180, end=360, fill=(60,90,130) if k%2 else BLUE, width=10)
d.rounded_rectangle([330,560,480,1000], radius=20, fill=RED); d.rounded_rectangle([720,560,870,1000], radius=20, fill=BLUE2)
d.rectangle([330,940,870,1060], fill=MUTED)
d.rectangle([330,560,480,650], fill=WHITE); d.rectangle([720,560,870,650], fill=WHITE)
d.text((405,605),"N", font=font(80), fill=RED, anchor="mm"); d.text((795,605),"S", font=font(80), fill=BLUE2, anchor="mm")
badge(d,"B, µT"); save_sensor(im,"magnetometer")

# pressure: barometer gauge
im, d = canvas(); cx,cy,R = 600,680,380
d.ellipse([cx-R,cy-R,cx+R,cy+R], fill=WHITE); d.ellipse([cx-R+36,cy-R+36,cx+R-36,cy+R-36], fill=BG2)
for k in range(11):
    a=math.radians(225-k*27); d.line([(cx+(R-70)*math.cos(a),cy-(R-70)*math.sin(a)),(cx+(R-110)*math.cos(a),cy-(R-110)*math.sin(a))], fill=MUTED, width=12)
a=math.radians(80); d.line([(cx,cy),(cx+(R-120)*math.cos(a),cy-(R-120)*math.sin(a))], fill=RED, width=22); d.ellipse([cx-34,cy-34,cx+34,cy+34], fill=RED)
d.text((cx,cy+190),"1013", font=font(110), fill=WHITE, anchor="mm")
badge(d,"p, hPa"); save_sensor(im,"pressure")

# light: bulb with rays
im, d = canvas(); cx,cy = 600,600
for k in range(12):
    a=math.radians(k*30); d.line([(cx+230*math.cos(a),cy+230*math.sin(a)),(cx+330*math.cos(a),cy+330*math.sin(a))], fill=YEL, width=24)
d.ellipse([cx-170,cy-200,cx+170,cy+140], fill=YEL); d.rectangle([cx-80,cy+120,cx+80,cy+240], fill=WHITE)
for y in (155,195): d.line([(cx-80,cy+y),(cx+80,cy+y)], fill=MUTED, width=10)
d.rounded_rectangle([cx-60,cy+240,cx+60,cy+290], radius=20, fill=MUTED)
badge(d,"E, lx", y=1080); save_sensor(im,"light")

# GPS: globe + pin + satellite
im, d = canvas(); cx,cy,R = 560,720,330
d.ellipse([cx-R,cy-R,cx+R,cy+R], fill=BLUE2)
for k in (-2,-1,0,1,2):
    r = R*math.cos(math.radians(k*28)); y = cy + R*math.sin(math.radians(k*28)); d.line([(cx-r,y),(cx+r,y)], fill=BLUE, width=8)
for w in (R*0.35, R*0.75): d.ellipse([cx-w,cy-R,cx+w,cy+R], outline=BLUE, width=8)
px,py = cx+60, cy-150
d.ellipse([px-110,py-260,px+110,py-40], fill=RED); d.polygon([(px-95,py-120),(px+95,py-120),(px,py+40)], fill=RED); d.ellipse([px-45,py-195,px+45,py-105], fill=WHITE)
sx,sy = 960,260
d.rectangle([sx-50,sy-50,sx+50,sy+50], fill=WHITE); d.rectangle([sx-200,sy-30,sx-70,sy+30], fill=BLUE); d.rectangle([sx+70,sy-30,sx+200,sy+30], fill=BLUE)
for r in (90,150): d.arc([sx-r-60,sy+60-r,sx+r-60,sy+60+r], start=100, end=170, fill=YEL, width=10)
save_sensor(im,"gps")
print("sensor art ok")
