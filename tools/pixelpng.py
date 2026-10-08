#!/usr/bin/env python3
"""Black-and-white pixel art for the README. stdlib only, and the banner counts the real repo.

The figures in the image are read off disk at generation time, and build-readme.py runs this file,
so the art cannot drift from the library it describes. Pillow is not installed here; PNG is written
directly (colour type 2, filter 0) and decoded back before anyone trusts it.
"""
import os, re, struct, sys, zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import FONT, Grid, word

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

# exactly two colours: paper and ink. Anything that used grey is dithered instead.
BW = [(255, 255, 255), (0, 0, 0)]


def write_png(path, g, palette=BW):
    rows = []
    for y in range(g.h):
        row = bytearray()
        for x in range(g.w):
            r, gg, b = palette[g.p[y * g.w + x] % len(palette)]
            row += bytes((r, gg, b))
        rows.append(bytes(row))
    raw = b"".join(b"\x00" + r for r in rows)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", g.w, g.h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)
    return len(png)


def read_png(path):
    d = open(path, "rb").read()
    assert d[:8] == b"\x89PNG\r\n\x1a\n", "bad signature"
    w, h, depth, ctype = struct.unpack(">IIBB", d[16:26])
    assert (depth, ctype) == (8, 2), f"unexpected depth/colour {depth}/{ctype}"
    i, idat = 8, b""
    while i < len(d):
        ln = struct.unpack(">I", d[i:i + 4])[0]
        if d[i + 4:i + 8] == b"IDAT":
            idat += d[i + 8:i + 8 + ln]
        i += 12 + ln
    raw = zlib.decompress(idat)
    assert len(raw) == h * (1 + w * 3), "payload size does not match the header"
    return w, h, [raw[y * (1 + w * 3) + 1:y * (1 + w * 3) + 1 + w * 3] for y in range(h)]


def counts():
    """What the image says must be what the repo holds."""
    sk = os.path.join(ROOT, "skills")
    n = len([d for d in os.listdir(sk) if os.path.isdir(os.path.join(sk, d))])
    brief = open(os.path.join(ROOT, "BRIEF.md"), encoding="utf-8").read()
    areas = len(re.findall(r"^\s*\d+[.\s]+[a-z0-9-]+\s{2,}", brief, re.M))
    return n, areas


def require(text):
    """Every character must have a glyph. A missing one renders blank and looks like a typo."""
    missing = sorted({c for c in text.upper() if c not in FONT})
    assert not missing, f"no glyph for {missing} in {text!r} — it would render as a blank"


def tw(text, scale, gap=1):
    return len(text) * (5 + gap) * scale


def centre(g, y, text, colour, scale, gap=1):
    require(text)
    word(g, max(0, (g.w - tw(text, scale, gap)) // 2), y, text, colour, scale, gap)


def checker(g, x, y, w, h, colour=1):
    """50% dither. With only black and white available, this is what a lighter tone is."""
    for j in range(h):
        for i in range(w):
            if (i + j) % 2 == 0:
                g.px(x + i, y + j, colour)


def paper(w, h):
    """White sheet, faint graph-paper dots, black rule at the top."""
    g = Grid(w, h, 0)
    g.frame(2, 2, w - 4, h - 4, 1)
    return g


def banner():
    n, areas = counts()
    g = paper(500, 168)
    centre(g, 18, "MONEY", 1, 4)
    centre(g, 62, "MACHINE", 1, 4)
    g.rect(120, 112, 260, 3, 1)
    centre(g, 124, f"{n} SKILLS", 1, 2)
    checker(g, 150, 146, 200, 6)
    centre(g, 156, f"{areas} AREAS", 1, 2)
    return g


def machine():
    """A coin in the top, coins out the side. Ink on paper, nothing hidden in shadow."""
    g = paper(400, 180)
    g.rect(38, 52, 168, 106, 0)
    g.frame(38, 52, 168, 106, 1)
    g.frame(37, 51, 170, 108, 1)
    g.rect(76, 66, 92, 12, 1)                     # slot: solid ink
    g.rect(64, 122, 116, 22, 0)                   # tray: outlined
    g.frame(64, 122, 116, 22, 1)
    for y in (10, 20):                            # motion dashes, dithered
        checker(g, 116, y, 8, 8)
    g.rect(104, 32, 30, 22, 1)                    # the coin
    g.rect(110, 38, 18, 10, 0)
    g.rect(220, 94, 36, 10, 1)                    # arrow
    g.rect(250, 84, 10, 30, 1)
    g.rect(256, 88, 6, 22, 1)
    for i in range(6):                            # coins stacking up
        x = 282 + (i % 2) * 18
        y = 140 - i * 14
        if i % 2:
            checker(g, x, y, 58, 10)
            checker(g, x + 4, y + 3, 50, 2, 0)
        else:
            g.rect(x, y, 58, 10, 1)
            g.rect(x + 4, y + 3, 50, 2, 0)
    return g


def divider():
    g = Grid(480, 22, 0)
    for x in range(10, 470, 14):
        g.rect(x, 8, 8, 6, 1)
    for o in [(-14, 0), (0, -8), (0, 0), (0, 8), (14, 0)]:
        g.rect(232 + o[0], 8 + o[1], 8, 8, 1)
    return g


if __name__ == "__main__":
    n, areas = counts()
    print(f"  the repo says: {n} skills, {areas} areas")
    for name, fn in (("banner", banner), ("machine", machine), ("divider", divider)):
        g = fn()
        path = os.path.join(ASSETS, f"{name}.png")
        size = write_png(path, g)
        w, h, px = read_png(path)
        same = all(px[y][x * 3:x * 3 + 3] == bytes(BW[g.p[y * g.w + x] % len(BW)])
                   for y in range(0, h, 5) for x in range(0, w, 5))
        mono = all(px[y][x * 3] == px[y][x * 3 + 1] == px[y][x * 3 + 2]
                   for y in range(0, h, 3) for x in range(0, w, 3))
        print(f"  assets/{name}.png  {w}x{h}  {size} bytes  decodes identical: {same}  greyscale only: {mono}")
