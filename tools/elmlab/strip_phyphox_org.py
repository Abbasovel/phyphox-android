#!/usr/bin/env python3
"""Elm Lab: remove references to the phyphox.org website and phyphox branding from the git submodules
(experiments, remote-access web interface). Run from the repository root; CI runs it before the build.
- experiments of the special "phyphox.org" category (support / sensor database) are deleted
- <link> elements pointing to phyphox.org are removed (root and translation blocks)
- the name phyphox in experiment texts (descriptions, labels, translations) becomes Elm Lab; the file
  format (<phyphox> root tag) and the phyphox:m sensor box name stay, as the app and the device need them
- the web interface gets the Elm Lab logo and colours"""
import re, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[2]
EXP = ROOT / "app/src/main/assets/experiments"
WEB = ROOT / "app/src/main/assets/remote"
#the word phyphox in text, but not the <phyphox> root tag, phyphox.org or the phyphox:m sensor box
NAME_RE = re.compile(r'(?<![</A-Za-z0-9_])phyphox(?![A-Za-z0-9_:]|\.org)', re.I)
deleted = links = names = 0
for p in EXP.rglob("*.phyphox"):
    s = p.read_text(encoding="utf-8")
    if "<category>phyphox.org</category>" in s:
        p.unlink(); deleted += 1; continue
    s2, n = re.subn(r'\s*<link\b[^>]*>[^<]*phyphox\.org[^<]*</link>', '', s)
    links += n
    s2 = s2.replace("phyphox-experiments", "Elm Lab experiments").replace("phyphoxem", "Elm Labem")
    s2, n = NAME_RE.subn("Elm Lab", s2)
    names += n
    if s2 != s: p.write_text(s2, encoding="utf-8")
left = [p.name for p in EXP.rglob("*.phyphox") if "phyphox.org" in p.read_text(encoding="utf-8")]
print(f"experiments: {deleted} deleted, {links} phyphox.org links removed, {names} names replaced, left: {left}")
if WEB.is_dir():
    shutil.copy(ROOT / "tools/elmlab/assets/webinterface_logo.png", WEB / "phyphox_orange.png")
    css = WEB / "style.css"; c = css.read_text(encoding="utf-8")
    css.write_text(re.sub(r'#ff7e22', '#2f6fd6', c, flags=re.I), encoding="utf-8")
    idx = WEB / "index.html"; h = idx.read_text(encoding="utf-8")
    idx.write_text(h.replace("The phyphox session has changed", "The Elm Lab session has changed"), encoding="utf-8")
    print("web interface: logo and colours replaced")
