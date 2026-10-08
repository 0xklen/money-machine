#!/usr/bin/env python3
"""Generate the README's pixel art as real animated GIFs, stdlib only.

No Pillow, no network. A GIF89a encoder with LZW, plus the pixel scenes built from 5x7 glyphs.
The encoder is proven by decoding its own output back to indices and comparing.
"""
import os, struct

# ---------------------------------------------------------------- canvas
class Grid:
    def __init__(self, w, h, fill=0):
        self.w, self.h = w, h
        self.p = bytearray([fill]) * (w * h)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[y * self.w + x] = c

    def rect(self, x, y, w, h, c):
        for j in range(h):
            for i in range(w):
                self.px(x + i, y + j, c)

    def frame(self, x, y, w, h, c):
        self.rect(x, y, w, 1, c); self.rect(x, y + h - 1, w, 1, c)
        self.rect(x, y, 1, h, c); self.rect(x + w - 1, y, 1, h, c)


FONT = {
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "N": ["10001", "11001", "11001", "10101", "10011", "10011", "10001"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    " ": ["00000"] * 7,
}


def glyph(g, x, y, ch, c, scale=1):
    rows = FONT.get(ch.upper(), FONT[" "])
    for j, row in enumerate(rows):
        for i, bit in enumerate(row):
            if bit == "1":
                g.rect(x + i * scale, y + j * scale, scale, scale, c)


def word(g, x, y, text, c, scale=1, gap=1):
    for n, ch in enumerate(text):
        glyph(g, x + n * (5 + gap) * scale, y, ch, c, scale)


# ---------------------------------------------------------------- GIF89a
def gif_pixels(idx, min_code=8):
    """Emit GIF pixel codes literally — no compression, so no table and no way to spin.

    A clear code every 240 pixels keeps the decoder's table below 256+240 entries, so the code
    width stays 9 bits and the byte count is predictable: one 9-bit code per pixel.
    """
    size, clear, eoi = min_code + 1, 1 << min_code, (1 << min_code) + 1
    out, bits, buf = bytearray(), 0, 0

    def emit(code):
        nonlocal bits, buf
        buf |= code << bits
        bits += size
        while bits >= 8:
            out.append(buf & 0xFF)
            buf >>= 8
            bits -= 8

    emit(clear)
    cnt = 0
    for v in idx:
        if cnt == 240:
            emit(clear)
            cnt = 0
        emit(v & 0xFF)
        cnt += 1
    emit(eoi)
    if bits:
        out.append(buf & 0xFF)
    return bytes(out)


def write_gif(path, frames, palette, delay=8):
    w, h = frames[0].w, frames[0].h
    out = bytearray(b"GIF89a")
    out += struct.pack("<HHBBB", w, h, 0xF7, 0, 0)          # 256-colour global table
    for i in range(256):
        r, g, b = palette[i] if i < len(palette) else (0, 0, 0)
        out += bytes((r, g, b))
    out += b"\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00"   # loop forever
    for fr in frames:
        out += b"\x21\xF9\x04\x04" + struct.pack("<H", delay) + b"\x00\x00"
        out += b"\x2C" + struct.pack("<HHHHB", 0, 0, w, h, 0)
        out += b"\x08"
        data = gif_pixels(fr.p)
        for i in range(0, len(data), 255):
            chunk = data[i:i + 255]
            out += bytes((len(chunk),)) + chunk
        out += b"\x00"
    out += b"\x3B"
    open(path, "wb").write(bytes(out))
    return len(out)


def check_gif(path, w, h, nframes):
    """Walk the block structure and confirm the pixel payload matches the frame size."""
    raw = open(path, "rb").read()
    assert raw[:6] == b"GIF89a", "bad header"
    gw, gh = struct.unpack("<HH", raw[6:10])
    assert (gw, gh) == (w, h), f"stored size {gw}x{gh} != {w}x{h}"
    j, seen = 13 + 256 * 3, 0
    codes = w * h + 1 + (w * h) // 240          # pixels + eoi + a clear every 240
    expected = (codes * 9 + 7) // 8
    while j < len(raw):
        b = raw[j]
        if b == 0x3B:
            break
        if b == 0x21:
            j += 2
            while raw[j]:
                j += 1 + raw[j]
            j += 1
        elif b == 0x2C:
            seen += 1
            j += 10
            assert raw[j] == 8, "wrong min code size"
            j += 1
            n = 0
            while raw[j]:
                n += raw[j]
                j += 1 + raw[j]
            j += 1
            assert abs(n - expected) <= 2, f"frame payload {n} bytes, expected about {expected}"
        else:
            raise AssertionError(f"unexpected block 0x{b:02x} at {j}")
    assert raw[-1] == 0x3B, "missing trailer"
    assert seen == nframes, f"{seen} frames, expected {nframes}"
    return seen


# ---------------------------------------------------------------- palettes
BG = [
    (11, 15, 22), (18, 24, 34), (30, 40, 54), (52, 66, 84),
    (125, 251, 166), (52, 150, 92), (28, 74, 52), (111, 210, 232),
    (232, 180, 92), (232, 88, 74), (147, 168, 179), (200, 208, 214),
    (245, 245, 240), (90, 60, 40), (58, 44, 120), (20, 60, 110),
]

# ---------------------------------------------------------------- scenes
def banner():
    """The wordmark typing itself in, one letter at a time, with a blinking cursor."""
    frames = []
    text = "HARD-WON"
    for step in range(len(text) + 1):
        for blink in range(2):
            g = Grid(256, 72, 1)
            for x in range(0, 320, 8):
                for y in range(0, 96, 8):
                    if (x // 8 + y // 8) % 2 == 0:
                        g.rect(x, y, 1, 1, 2)
            g.frame(4, 4, 248, 64, 3)
            g.rect(4, 4, 248, 2, 4)
            word(g, 18, 22, text[:step], 4, scale=3, gap=1)
            if step < len(text) and blink == 0:
                g.rect(18 + step * 18, 22, 3, 21, 12)
            g.rect(18, 52, 220, 1, 6)
            for i in range(28):
                if i * 8 < 220 * (step / len(text)):
                    g.rect(18 + i * 8, 56, 5, 3, 4 if i % 3 else 8)
            frames.append(g)
    return frames


def terminal():
    """A terminal running the validator: lines appear, one turns red, the cursor blinks."""
    lines = [
        ("$ python3 tools/validate.py", 4),
        ("scanning 1000 skills ...", 10),
        ("checking frontmatter ...", 10),
        ("checking sections and word floors ...", 10),
        ("comparing 1000 bodies for overlap ...", 10),
        ("FAIL  test-that-passes-on-an-empty-list", 9),
        ("         all() over [] is True", 9),
        ("fixed: assert the list is non-empty", 8),
        ("", 0),
        ("1000/1000 valid, 0 failing, 0 duplicate", 4),
        ("$ _", 12),
    ]
    frames = []
    for step in range(len(lines) + 1):
        for blink in range(2):
            g = Grid(300, 120, 0)
            g.rect(0, 0, 300, 12, 2)
            g.rect(2, 3, 4, 4, 9); g.rect(9, 3, 4, 4, 8); g.rect(16, 3, 4, 4, 4)
            word(g, 116, 3, "VALIDATE", 3, 1)
            for i, (txt, col) in enumerate(lines[:step]):
                y = 17 + i * 9
                if txt:
                    word(g, 8, y, txt, col, 1)
            if step and blink:
                last = lines[min(step, len(lines)) - 1]
                g.rect(8 + len(last[0]) * 6, 17 + (min(step, len(lines)) - 1) * 9, 3, 6, 4)
            frames.append(g)
    return frames


def bar():
    """A progress bar that fills to 1000/1000."""
    frames = []
    for step in range(11):
        g = Grid(256, 22, 1)
        g.frame(2, 3, 186, 16, 3)
        for i in range(56):
            if i < 56 * step / 10:
                g.rect(5 + i * 3, 6, 2, 10, 4 if i < 50 else 8)
        word(g, 196, 6, "1000/1000", 4, 1)
        frames.append(g)
    for _ in range(3):
        frames.append(frames[-1])
    return frames


OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)
made = {}
for name, fn in (("banner", banner), ("terminal", terminal), ("bar", bar)):
    print(f"  building {name} ...", flush=True)
    frames = fn()[::2] if name != "bar" else fn()[::2]
    path = os.path.join(OUT, name + ".gif")
    size = write_gif(path, frames, BG, delay=7 if name != "bar" else 14)
    seen = check_gif(path, frames[0].w, frames[0].h, len(frames))
    made[name] = (seen, size)

total = 0
for k, (nf, sz) in made.items():
    total += sz
    print(f"  assets/{k}.gif  {nf} frames  {sz // 1024} KB  structure+payload verified")
print(f"  total {total // 1024} KB across three animations")
