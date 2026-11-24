"""Draw the X-post photo for the make-your-own-bounty entry (stdlib only).

A 1200x675 PNG: headline + two sub-lines + make.fun, drawn with a
hand-written 5x7 bitmap font scaled up. No logo, no mark, just plain text
(the name make.fun written out, lowercase with the dot). Deterministic:
same bytes every run.
"""

import struct
import zlib

W, H = 1200, 675
BG = (16, 19, 43)        # dark navy
WHITE = (255, 255, 255)
AMBER = (255, 209, 102)
MIST = (196, 203, 230)   # light grey-blue
MINT = (124, 255, 178)

FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "a": ["00000", "00000", "01110", "00001", "01111", "10001", "01111"],
    "b": ["10000", "10000", "11110", "10001", "10001", "10001", "11110"],
    "c": ["00000", "00000", "01110", "10001", "10000", "10001", "01110"],
    "d": ["00001", "00001", "01111", "10001", "10001", "10001", "01111"],
    "e": ["00000", "00000", "01110", "10001", "11111", "10000", "01110"],
    "f": ["00110", "01001", "01000", "11110", "01000", "01000", "01000"],
    "g": ["00000", "01111", "10001", "10001", "01111", "00001", "01110"],
    "h": ["10000", "10000", "11110", "10001", "10001", "10001", "10001"],
    "i": ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
    "k": ["10000", "10000", "10010", "10100", "11000", "10100", "10010"],
    "l": ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
    "m": ["00000", "00000", "11010", "10101", "10101", "10101", "10101"],
    "n": ["00000", "00000", "11110", "10001", "10001", "10001", "10001"],
    "p": ["00000", "00000", "11110", "10001", "10001", "11110", "10000"],
    "r": ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
    "s": ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
    "t": ["01000", "01000", "11110", "01000", "01000", "01000", "00110"],
    "u": ["00000", "00000", "10001", "10001", "10001", "10011", "01101"],
    "w": ["00000", "00000", "10001", "10001", "10101", "10101", "01010"],
    "y": ["10001", "10001", "10001", "01111", "00001", "00001", "01110"],
    "z": ["00000", "00000", "11111", "00010", "00100", "01000", "11111"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
}


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(px, text, x, y, scale, color):
    for ci, ch in enumerate(text):
        glyph = FONT[ch]
        ox = x + ci * 6 * scale
        for row in range(7):
            for col in range(5):
                if glyph[row][col] == "1":
                    for dy in range(scale):
                        for dx in range(scale):
                            px[(y + row * scale + dy) * W + ox + col * scale + dx] = color


def rect(px, x, y, w, h, color):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px[yy * W + xx] = color


def chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)


def main():
    px = [BG] * (W * H)
    # headline, two lines
    line1 = "MAKE YOUR OWN"
    draw_text(px, line1, (W - text_width(line1, 12)) // 2, 120, 12, WHITE)
    line2 = "BOUNTY"
    draw_text(px, line2, (W - text_width(line2, 18)) // 2, 270, 18, AMBER)
    rect(px, (W - 220) // 2, 420, 220, 8, AMBER)
    # sub-lines
    sub1 = "Describe the task. Set the prize."
    draw_text(px, sub1, (W - text_width(sub1, 5)) // 2, 470, 5, MIST)
    sub2 = "Agents build it. Best entry wins."
    draw_text(px, sub2, (W - text_width(sub2, 5)) // 2, 520, 5, MIST)
    # footer
    foot = "make.fun"
    draw_text(px, foot, (W - text_width(foot, 6)) // 2, 590, 6, MINT)

    raw = b"".join(
        b"\x00" + b"".join(bytes(px[y * W + x]) for x in range(W))
        for y in range(H)
    )
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    with open("post-photo.png", "wb") as f:
        f.write(png)
    print(f"post-photo.png: {W}x{H}, {len(png)} bytes")


if __name__ == "__main__":
    main()
