#!/usr/bin/env python3
"""Subset Noto Sans SC to the characters the Chinese pages use (Google Fonts text=)."""
import os, re, glob, urllib.parse, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
text = ""
for f in glob.glob(os.path.join(ROOT, "sc", "*.html")) + [os.path.join(ROOT, "assets", "app.js")]:
    text += open(f, encoding="utf-8").read()
chars = "".join(sorted(set(c for c in text if ord(c) > 0x2E7F)))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
for fam, spec, out in [("Noto Sans SC", "wght@400..700", "notosanssc.woff2")]:
    url = "https://fonts.googleapis.com/css2?family=" + fam.replace(" ", "+") + ":" + spec + "&text=" + urllib.parse.quote(chars)
    css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read().decode()
    src = re.findall(r"url\((.*?)\)", css)
    assert len(src) == 1, (fam, len(src))
    data = urllib.request.urlopen(urllib.request.Request(src[0], headers={"User-Agent": UA})).read()
    open(os.path.join(ROOT, "assets", "fonts", out), "wb").write(data)
    print(out, len(data), "bytes,", len(chars), "chars")
