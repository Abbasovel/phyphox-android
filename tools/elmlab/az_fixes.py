#!/usr/bin/env python3
"""Elm Lab: Azerbaijani terminology agreed during the phyphox translation (Weblate), applied to the
experiment files (git submodule) and the app strings until upstream syncs them.
- no "xam" (raw): "Raw Sensors" -> "Sensorlar", "raw data" -> "verilənlər"
- gyroscope "rotation rate" -> "bucaq sürəti"
Only <translation locale="az"> blocks are touched. Run from the repository root (CI does it before the build)."""
import re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
RULES = [
    ("Xam sensorlar", "Sensorlar"),
    ("Xam verilənlər", "Verilənlər"),
    ("xam mövqe verilənlərini", "mövqe verilənlərini"),
    ("xam verilənlər", "verilənlər"),
    ("Xam spektr", "İlkin spektr"),
    ("Giroskop (dönmə sürəti)", "Giroskop (bucaq sürəti)"),
    ("dönmə sürəti", "bucaq sürəti"),
    ("Dönmə sürəti", "Bucaq sürəti"),
    ("aAlətlər", "Alətlər"),
]
def fix(text):
    for a, b in RULES: text = text.replace(a, b)
    return text
changed = 0
for p in (ROOT / "app/src/main/assets/experiments").rglob("*.phyphox"):
    s = p.read_text(encoding="utf-8")
    s2 = re.sub(r'(<translation locale="az">)(.*?)(</translation>)', lambda m: m.group(1) + fix(m.group(2)) + m.group(3), s, flags=re.S)
    if s2 != s: p.write_text(s2, encoding="utf-8"); changed += 1
p = ROOT / "app/src/main/res/values-az/strings.xml"
s = p.read_text(encoding="utf-8"); s2 = fix(s)
if s2 != s: p.write_text(s2, encoding="utf-8"); changed += 1
left = []
for q in list((ROOT / "app/src/main/assets/experiments").rglob("*.phyphox")) + [p]:
    for m in re.finditer(r'<translation locale="az">(.*?)</translation>', q.read_text(encoding="utf-8"), re.S) if q.suffix == ".phyphox" else [re.match(r'(.*)', q.read_text(encoding="utf-8"), re.S)]:
        for w in re.findall(r'\b[Xx]am\b\s+\w+', m.group(1)): left.append(f"{q.name}: {w}")
print(f"az_fixes: {changed} files changed")
if left: print("still contains 'xam':", *left, sep="\n  ")
