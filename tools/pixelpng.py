#!/usr/bin/env python3
"""Pixel-art PNG designs for the README. stdlib only: zlib, struct, and the shared Grid.

Pillow is not installed on this machine and adding a dependency to generate four images would be
absurd, so this writes PNG itself (colour type 2, filter 0) and decodes its own output back.
"""
import os, struct, sys, zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixelart import Grid, word, BG           # shared canvas, glyph font and palette

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def write_png(path, g, palette):
    rows = []
    for y in range(g.h):
        row = bytearray()
        for x in range(g.w):
            r, gg, b = palette[g.p[y * g.w + x] % len(palette)]
            row += bytes((r, gg, b))
        rows.append(bytes(row))
    raw = b"".join(b"\x00" + r for r in rows)          # filter byte 0 per scanline

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
    """Decode it back. An encoder that has only ever been written, never read, proves nothing."""
    d = open(path, "rb").read()
    assert d[:8] == b"\x89PNG\r\n\x1a\n", "bad signature"
    w, h, depth, ctype = struct.unpack(">IIBB", d[16:26])
    assert (depth, ctype) == (8, 2), f"unexpected depth/colour {depth}/{ctype}"
    i, idat = 8, b""
    while i < len(d):
        ln = struct.unpack(">I", d[i:i + 4])[0]
        tag = d[i + 4:i + 8]
        if tag == b"IDAT":
            idat += d[i + 8:i + 8 + ln]
        i += 12 + ln
    raw = zlib.decompress(idat)
    assert len(raw) == h * (1 + w * 3), f"payload {len(raw)} != {h * (1 + w * 3)}"
    px = []
    for y in range(h):
        off = y * (1 + w * 3)
        assert raw[off] == 0, "unexpected filter"
        px.append(raw[off + 1:off + 1 + w * 3])
    return w, h, px


def centre_word(g, y, text, colour, scale, gap=1):
    wpx = len(text) * (5 + gap) * scale
    word(g, max(0, (g.w - wpx) // 2), y, text, colour, scale, gap)


def panel(w, h, fill=1, border=3, accent=4):
    g = Grid(w, h, fill)
    for x in range(0, w, 10):
        for y in range(0, h, 10):
            g.px(x, y, fill + 1)                       # a faint dot grid, like graph paper
    g.frame(3, 3, w - 6, h - 6, border)
    g.rect(3, 3, w - 6, 2, accent)
    return g


def banner():
    g = panel(440, 130)
    centre_word(g, 26, "MONEY", 4, 4)
    centre_word(g, 74, "MACHINE", 8, 4)
    return g


def machine():
    """A coin goes in the top, coins come out the side. Every part outlined, because a dark shape
    on a dark panel is not a machine, it is a rectangle nobody can see."""
    g = panel(400, 176)
    # the machine: slate body, bright outline, green cap
    g.rect(40, 48, 172, 104, 2)
    g.frame(40, 48, 172, 104, 3)
    g.rect(40, 48, 172, 3, 4)
    g.rect(80, 62, 92, 12, 0)                    # the slot: a dark hole in a lit body
    g.frame(80, 62, 92, 12, 4)
    g.rect(66, 118, 120, 22, 0)                  # the tray
    g.frame(66, 118, 120, 22, 3)
    # the coin, mid-fall, with two motion dashes above it
    g.rect(114, 12, 6, 6, 12)
    g.rect(114, 22, 6, 6, 12)
    g.rect(102, 32, 30, 22, 8)
    g.rect(106, 36, 22, 14, 12)
    # a clean arrow: shaft plus head, pointing out of the machine
    g.rect(222, 92, 34, 10, 4)
    g.rect(250, 82, 10, 30, 4)
    g.rect(256, 86, 6, 22, 4)
    # coins coming out and stacking higher
    for i in range(6):
        x = 282 + (i % 2) * 18
        y = 138 - i * 14
        g.rect(x, y, 58, 10, 8)
        g.rect(x, y, 58, 3, 12)
    return g


def divider():
    """A pixel rule: black squares on white, evenly spaced, with a diamond at the centre."""
    g = Grid(480, 24, 12)                          # white
    for x in range(8, 472, 14):
        g.rect(x, 9, 8, 6, 0)                      # near-black squares
    for o in [(-14, 0), (0, -8), (0, 0), (0, 8), (14, 0)]:
        g.rect(232 + o[0], 12 + o[1] - 4, 8, 8, 0)
    return g


if __name__ == "__main__":
    made = {}
    for name, fn in (("banner", banner), ("machine", machine), ("divider", divider)):
        g = fn()
        path = os.path.join(ASSETS, f"{name}.png")
        size = write_png(path, g, BG)
        w, h, px = read_png(path)
        same = all(px[y][x * 3:x * 3 + 3] == bytes(BG[g.p[y * g.w + x] % len(BG)])
                   for y in range(0, h, 7) for x in range(0, w, 7))
        made[name] = (w, h, size, same)
    for k, (w, h, sz, same) in made.items():
        print(f"  assets/{k}.png  {w}x{h}  {sz // 1024} KB  decoded back identical: {'yes' if same else 'NO'}")
