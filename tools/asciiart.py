#!/usr/bin/env python3
"""ASCII art for the README, generated rather than typed, so columns cannot drift.

Every glyph is exactly 5 columns wide and 5 rows tall. Blocks are padded to a single width:
a rectangle of monospace text, which the README then centres with <div align="center">.
Hand-typed banner art is the usual reason a README's letters shear by one column.
"""

F = {
    "M": ["█   █", "██ ██", "█ █ █", "█   █", "█   █"],
    "O": [" ███ ", "█   █", "█   █", "█   █", " ███ "],
    "N": ["█   █", "██  █", "█ █ █", "█  ██", "█   █"],
    "E": ["█████", "█    ", "████ ", "█    ", "█████"],
    "Y": ["█   █", "█   █", " ███ ", "  █  ", "  █  "],
    "A": [" ███ ", "█   █", "█████", "█   █", "█   █"],
    "C": [" ████", "█    ", "█    ", "█    ", " ████"],
    "H": ["█   █", "█   █", "█████", "█   █", "█   █"],
    "I": ["█████", "  █  ", "  █  ", "  █  ", "█████"],
    "S": [" ████", "█    ", " ███ ", "    █", "████ "],
    "T": ["█████", "  █  ", "  █  ", "  █  ", "  █  "],
    "P": ["████ ", "█   █", "████ ", "█    ", "█    "],
    " ": ["     ", "     ", "     ", "     ", "     "],
}


def word(text):
    rows = [""] * 5
    for i, ch in enumerate(text):
        g = F.get(ch.upper(), F[" "])
        for r in range(5):
            rows[r] += g[r] + ("" if i == len(text) - 1 else " ")
    return rows


def block(rows, width=None):
    """Pad every row to one width — a rectangle, the only shape that survives centring."""
    w = width or max(len(r) for r in rows)
    out = [r.ljust(w) for r in rows]
    assert len({len(r) for r in out}) == 1, "rows are not a rectangle"
    return out


def centre(lines, width=None):
    w = width or max(len(l) for l in lines)
    out = []
    for l in lines:
        gap = w - len(l)
        left = gap // 2
        out.append(" " * left + l + " " * (gap - left))
    assert len({len(l) for l in out}) == 1, "rows are not a rectangle"
    return out


def wordmark():
    money, machine = block(word("MONEY")), block(word("MACHINE"))
    w = max(len(money[0]), len(machine[0]))
    money = block(money, w)
    machine = block(machine, w)
    divider = centre(["─" * 9 + " ◆ " + "─" * 9], w)
    return "\n".join(centre(money, w) + [""] + centre(machine, w) + ["", divider[0]])


def machine_art():
    raw = [
        "  .-----------.",
        " /      $      \\",
        "|       $       |",
        " \\      $      /",
        "  '-----------'",
        "       |",
        "       v",
        "",
        "+---------------------+",
        "|   [   C O I N   ]   |",
        "|                     |",
        "|   $  $  $  $  $  $  |",
        "|   $  $  $  $  $  $  |",
        "+---------------------+",
    ]
    return "\n".join(centre(raw))


if __name__ == "__main__":
    w, m = wordmark(), machine_art()
    for name, art in (("wordmark", w), ("machine", m)):
        widths = {len(l) for l in art.split("\n")}
        print(f"  {name}: {len(art.splitlines())} lines, widths {sorted(widths)} -> "
              f"{'aligned rectangle' if len(widths) == 1 else 'RAGGED'}")
    print()
    print(w)
    print()
    print(m)
