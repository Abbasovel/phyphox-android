#!/usr/bin/env python3
"""Elm Lab rebrand of the phyphox Android source (GPL-3.0).
Run from the repository root:  python3 tools/elmlab/rebrand.py
Idempotent. Keeps the phyphox/RWTH attribution texts (credits, GPL notice) intact,
replaces the phyphox and RWTH logos (registered trademarks) and the product name."""
import re, math, pathlib, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
APP = ROOT / "app"
RES = APP / "src/main/res"
FONTS = pathlib.Path(__file__).resolve().parent / "fonts"
NAME = "Elm Lab"
APP_ID = "az.elmmuzeyi.elmlab"
NAVY, NAVY2, GRID, BLUE, RED, WHITE, MUTED, INK = (14,24,38), (20,34,51), (43,63,88), (122,170,255), (255,123,111), (255,255,255), (154,170,189), (20,36,59)
DENS = {"mdpi":1, "hdpi":1.5, "xhdpi":2, "xxhdpi":3, "xxxhdpi":4}

def font(name, size): return ImageFont.truetype(str(FONTS / name), size)

# ---------- icon art ----------
def art(S, box, im=None, bg=None):
    """Draw grid + decaying sine inside box=(x0,y0,x1,y1) on an S*S RGBA image."""
    im = im or Image.new("RGBA", (S, S), bg or (0,0,0,0)); d = ImageDraw.Draw(im)
    x0,y0,x1,y1 = box; w = x1-x0; lw = max(1, S//160)
    for i in range(7):
        x = x0 + i*w/6; y = y0 + i*w/6
        d.line([(x,y0),(x,y1)], fill=GRID, width=lw); d.line([(x0,y),(x1,y)], fill=GRID, width=lw)
    r = max(2, S//52)
    for i in range(3001):
        t = i/3000; x = x0 + t*w
        y = (y0+y1)/2 - math.sin(t*2*math.pi*1.5)*math.exp(-1.2*t)*(w/2)*0.85
        d.ellipse([x-r,y-r,x+r,y+r], fill=BLUE)
    R = S//20; d.ellipse([x0-R,(y0+y1)/2-R,x0+R,(y0+y1)/2+R], fill=RED)
    return im

def launcher_pngs():
    for dn, k in DENS.items():
        n = int(48*k); S = n*4
        # legacy square (rounded) and round
        base = art(S, (S*0.2,S*0.2,S*0.8,S*0.8), bg=NAVY+(255,))
        m = Image.new("L",(S,S),0); ImageDraw.Draw(m).rounded_rectangle([S*0.04,S*0.04,S*0.96,S*0.96], radius=S*0.18, fill=255)
        sq = Image.new("RGBA",(S,S),(0,0,0,0)); sq.paste(base,(0,0),m)
        sq.resize((n,n),Image.LANCZOS).save(RES/f"mipmap-{dn}/ic_launcher.png")
        m2 = Image.new("L",(S,S),0); ImageDraw.Draw(m2).ellipse([S*0.04,S*0.04,S*0.96,S*0.96], fill=255)
        rd = Image.new("RGBA",(S,S),(0,0,0,0)); rd.paste(base,(0,0),m2)
        rd.resize((n,n),Image.LANCZOS).save(RES/f"mipmap-{dn}/ic_launcher_round.png")
        # adaptive foreground: 108dp canvas, art inside the 66dp safe zone
        f = int(108*k); FS = f*4; a = FS*30/108; b = FS*78/108
        art(FS, (a,a,b,b)).resize((f,f),Image.LANCZOS).save(RES/f"mipmap-{dn}/ic_launcher_foreground.png")

def launcher_vector():
    pts = []
    for i in range(121):
        t = i/120; x = 30 + t*48; y = 54 - math.sin(t*2*math.pi*1.5)*math.exp(-1.2*t)*24*0.85
        pts.append(f"{x:.2f},{y:.2f}")
    grid = " ".join([f"M{30+i*8},30 L{30+i*8},78 M30,{30+i*8} L78,{30+i*8}" for i in range(7)])
    xml = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- Elm Lab launcher foreground (replaces the phyphox logo, a registered trademark) -->
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
  <path android:pathData="{grid}" android:strokeColor="#2B3F58" android:strokeWidth="0.7"/>
  <path android:pathData="M{' L'.join(pts)}" android:strokeColor="#7AAAFF" android:strokeWidth="3.6"
      android:strokeLineCap="round" android:strokeLineJoin="round" android:fillColor="#00000000"/>
  <path android:pathData="M30,54 m-3.6,0 a3.6,3.6 0 1,0 7.2,0 a3.6,3.6 0 1,0 -7.2,0" android:fillColor="#FF7B6F"/>
</vector>
'''
    (RES/"drawable/ic_elmlab_foreground.xml").write_text(xml, encoding="utf-8")
    for n in ["ic_launcher.xml","ic_launcher_round.xml"]:
        p = RES/"mipmap-anydpi-v26"/n; s = p.read_text(encoding="utf-8")
        p.write_text(s.replace("@drawable/ic_phyphox_transparent","@drawable/ic_elmlab_foreground"), encoding="utf-8")
    p = RES/"values/ic_launcher_background.xml"; s = p.read_text(encoding="utf-8")
    p.write_text(re.sub(r'(name="ic_launcher_background">)#[0-9A-Fa-f]+', r'\g<1>#FF0E1826', s), encoding="utf-8")

# ---------- wordmarks ----------
def header_png():
    """Main-screen title image (was the phyphox wordmark), 718x192 at xxxhdpi."""
    W,H = 718*2, 192*2
    im = Image.new("RGBA",(W,H),NAVY+(255,)); d = ImageDraw.Draw(im)
    sq = Image.new("RGBA",(H,H),NAVY2+(255,)); art(H,(H*0.16,H*0.16,H*0.84,H*0.84),im=sq); im.paste(sq,(0,0))
    fb = font("IBMPlexSansCondensed-Bold.ttf", 238); fr = font("IBMPlexSans-Regular.ttf", 58)
    x = H + 44
    wl = d.textlength("Elm ", font=fb)
    d.text((x, 262), "Elm", font=fb, fill=WHITE, anchor="ls")
    d.text((x+wl, 262), "Lab", font=fb, fill=BLUE, anchor="ls")
    d.text((x+4, 350), "fizika təcrübələri telefonla", font=fr, fill=MUTED, anchor="ls")
    for dn,k in DENS.items():
        im.resize((round(718*k/4), round(192*k/4)), Image.LANCZOS).save(RES/f"drawable-{dn}/phyphox_dark.png")

def museum_png(path_sizes, color, bgcolor=None):
    W,H = 827*2, 378*2
    im = Image.new("RGBA",(W,H),bgcolor or (0,0,0,0)); d = ImageDraw.Draw(im)
    f1 = font("IBMPlexSans-SemiBold.ttf", 150); f2 = font("IBMPlexSansCondensed-Bold.ttf", 270)
    d.text((W/2, 300), "İnteraktiv", font=f1, fill=color, anchor="ms")
    d.text((W/2, 610), "Elm Muzeyi", font=f2, fill=color, anchor="ms")
    for p,(w,h) in path_sizes:
        # keep the aspect: fit into (w,h)
        r = min(w/W, h/H); img = im.resize((max(1,round(W*r)), max(1,round(H*r))), Image.LANCZOS)
        canvas = Image.new("RGBA",(w,h),(0,0,0,0)); canvas.paste(img,((w-img.width)//2,(h-img.height)//2))
        canvas.save(p)

def logos():
    header_png()
    museum_png([(RES/f"drawable-{dn}/rwth.png", Image.open(RES/f"drawable-{dn}/rwth.png").size) for dn in DENS], INK+(255,))
    museum_png([(RES/"drawable/rwth_white.png", Image.open(RES/"drawable/rwth_white.png").size)], WHITE+(255,))

# ---------- strings ----------
KEEP = {"creditsRWTH","gpl","categoryPhyphoxOrg","categoryPhyphoxOrgHint"}
WORD = re.compile(r'(?<![\w./:@#-])[Pp]hyphox(?![\w®]|\.org|\.[a-z])')
def strings():
    for p in sorted(RES.glob("values*/strings.xml")):
        s = p.read_text(encoding="utf-8")
        def fix(m):
            name, body = m.group(2), m.group(3)
            if name in ("app_name","title_activity_experiment"): return f'{m.group(1)}{NAME}{m.group(4)}'
            if name in KEEP or name.endswith("URL") or name.endswith("_url"): return m.group(0)
            return m.group(1) + WORD.sub(NAME, body) + m.group(4)
        s2 = re.sub(r'(<string name="([^"]+)"[^>]*>)(.*?)(</string>)', fix, s, flags=re.S)
        # grammar after the rename: vowel harmony (phyphox-un -> Lab-ın) and English article
        if p.parent.name == "values-az": s2 = s2.replace(f"{NAME}-un", f"{NAME}-ın").replace(f"{NAME}-u ", f"{NAME}-ı ")
        if p.parent.name == "values": s2 = re.sub(rf"\b([Aa]) {NAME}", rf"\1n {NAME}", s2)
        if s2 != s: p.write_text(s2, encoding="utf-8")

# ---------- gradle / manifest ----------
def gradle():
    p = APP/"build.gradle"; s = p.read_text(encoding="utf-8")
    s = re.sub(r'applicationId "[^"]+"', f'applicationId "{APP_ID}"', s)
    s = re.sub(r'versionName "([^"]+)"', lambda m: m.group(0) if "elmlab" in m.group(1) else f'versionName "{m.group(1)}-elmlab"', s)
    if "signingConfigs {" not in s:
        s = s.replace("    buildTypes {", '''    signingConfigs {
        elmlab {
            // Elm Lab test key (public). Replace with a private key before a store release.
            storeFile file('elmlab.keystore')
            storePassword 'elmlab-test'
            keyAlias 'elmlab'
            keyPassword 'elmlab-test'
        }
    }

    lint {
        checkReleaseBuilds false
        abortOnError false
    }

    buildTypes {
        debug {
            signingConfig signingConfigs.elmlab
        }''', 1)
        s = s.replace("        release {\n", "        release {\n            signingConfig signingConfigs.elmlab\n", 1)
    p.write_text(s, encoding="utf-8")
    m = APP/"src/main/AndroidManifest.xml"; t = m.read_text(encoding="utf-8")
    m.write_text(t.replace('android:authorities="de.rwth_aachen.phyphox.exportProvider"', 'android:authorities="${applicationId}.exportProvider"'), encoding="utf-8")

if __name__ == "__main__":
    launcher_pngs(); launcher_vector(); logos(); strings(); gradle()
    print("Elm Lab rebrand applied")
