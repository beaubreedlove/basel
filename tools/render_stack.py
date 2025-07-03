from __future__ import annotations
from fractions import Fraction
from typing import Tuple, List
from decimal import Decimal, localcontext
import importlib

# ``python -m`` executed from the repository root already puts the project on
# ``sys.path``.  Additional path manipulation is unnecessary and has been
# removed so this script only works when run from the project root.

def load_stack(algo: str, strict: bool, open_bounds: bool) -> "Stack":
    """Import the requested stack implementation."""
    module = importlib.import_module(f"algorithms.{algo}")
    stack_class = getattr(module, "Stack")
    try:
        return stack_class(strict=strict, open_bounds=open_bounds)
    except TypeError:
        try:
            return stack_class(strict=strict)
        except TypeError:
            return stack_class()


COLOR_PALETTE = [
    (51, 102, 204),  # blue
    (220, 57, 18),   # red
    (255, 153, 0),   # orange
    (16, 150, 24),   # green
    (153, 0, 153),   # purple
    (0, 153, 198),   # cyan
    (221, 68, 119),
    (102, 170, 0),
    (184, 46, 46),
    (49, 99, 149),
    (153, 68, 153),
    (34, 170, 153),
    (170, 170, 17),
    (102, 51, 204),
    (230, 115, 0),
    (139, 7, 7),
    (50, 146, 98),
    (85, 116, 166),
    (59, 62, 172),
    (183, 115, 34),
    (22, 214, 32),
    (185, 19, 131),
    (244, 53, 158),
    (156, 89, 53),
]


def _fmt(fr: Fraction) -> str:
    """Format a Fraction as a high precision decimal string."""
    with localcontext() as ctx:
        ctx.prec = 50
        return str(Decimal(fr.numerator) / Decimal(fr.denominator))


def _gradient_color(index: int, total: int) -> Tuple[int, int, int]:
    if total <= 1:
        ratio = 0.0
    else:
        ratio = (index - 1) / (total - 1)
    r = int(round(255 * (1 - ratio)))
    b = int(round(255 * ratio))
    return r, 0, b


def _cycle_color(index: int, count: int) -> Tuple[int, int, int]:
    return COLOR_PALETTE[(index - 1) % count]


def _text_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """Return black or white text color depending on square brightness."""
    brightness = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
    return (0, 0, 0) if brightness > 128 else (255, 255, 255)


_DIGITS = {
    "0": [
        "#####",
        "#   #",
        "#   #",
        "#   #",
        "#####",
    ],
    "1": [
        "  #  ",
        " ##  ",
        "  #  ",
        "  #  ",
        "#####",
    ],
    "2": [
        "#####",
        "    #",
        "#####",
        "#    ",
        "#####",
    ],
    "3": [
        "#####",
        "    #",
        "#####",
        "    #",
        "#####",
    ],
    "4": [
        "#   #",
        "#   #",
        "#####",
        "    #",
        "    #",
    ],
    "5": [
        "#####",
        "#    ",
        "#####",
        "    #",
        "#####",
    ],
    "6": [
        "#####",
        "#    ",
        "#####",
        "#   #",
        "#####",
    ],
    "7": [
        "#####",
        "    #",
        "    #",
        "    #",
        "    #",
    ],
    "8": [
        "#####",
        "#   #",
        "#####",
        "#   #",
        "#####",
    ],
    "9": [
        "#####",
        "#   #",
        "#####",
        "    #",
        "#####",
    ],
}


def _draw_number(
    pixels: List[List[Tuple[int, int, int]]],
    text: str,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: Tuple[int, int, int],
) -> None:
    """Draw ``text`` centered inside the box (x0, y0, x1, y1)."""
    char_w = 5
    char_h = 5
    spacing = 1
    box_w = x1 - x0
    box_h = y1 - y0
    total_w = len(text) * char_w + (len(text) - 1) * spacing
    scale = min(box_w // total_w, box_h // char_h)
    if scale <= 0:
        return
    text_w = total_w * scale
    text_h = char_h * scale
    start_x = x0 + (box_w - text_w) // 2
    start_y = y0 + (box_h - text_h) // 2
    for index, ch in enumerate(text):
        pattern = _DIGITS.get(ch)
        if not pattern:
            continue
        offset_x = start_x + index * (char_w * scale + spacing * scale)
        for row, line in enumerate(pattern):
            for col, c in enumerate(line):
                if c != "#":
                    continue
                for dy in range(scale):
                    for dx in range(scale):
                        px = offset_x + col * scale + dx
                        py = start_y + row * scale + dy
                        if 0 <= py < len(pixels) and 0 <= px < len(pixels[0]):
                            pixels[py][px] = color

def render_ppm(
    stack: Stack,
    filename: str = "stack.ppm",
    scale: int = 400,
    renderer: str = "cycle",
    colors: int = 2,
    numbers: bool = False,
) -> None:
    """Render the stack to a simple PPM image file."""
    xmax = max(b.x + b.side for b in stack.squares)
    ymax = max(b.y + b.side for b in stack.squares)
    width = int(scale * xmax) + 1
    height = int(scale * ymax) + 1
    # initialize black background
    pixels: List[List[Tuple[int, int, int]]] = [
        [(0, 0, 0) for _ in range(width)] for _ in range(height)
    ]
    total_squares = len(stack.squares)
    color_count = max(1, min(colors, len(COLOR_PALETTE)))
    for square in stack.squares:
        if renderer == "gradient":
            color = _gradient_color(square.n, total_squares)
        else:
            color = _cycle_color(square.n, color_count)
        x0 = int(scale * square.x)
        x1 = int(scale * (square.x + square.side))
        y0 = int(scale * (ymax - (square.y + square.side)))
        y1 = int(scale * (ymax - square.y))
        for y in range(max(y0, 0), min(y1, height)):
            for x in range(max(x0, 0), min(x1, width)):
                pixels[y][x] = color
        if numbers:
            _draw_number(pixels, str(square.n), x0, y0, x1, y1, _text_color(color))
    with open(filename, "w") as fh:
        fh.write(f"P3\n{width} {height}\n255\n")
        for row in pixels:
            fh.write(" ".join(f"{r} {g} {b}" for r, g, b in row))
            fh.write("\n")


def render_svg(
    stack: Stack,
    filename: str = "stack.svg",
    renderer: str = "cycle",
    colors: int = 2,
    numbers: bool = False,
) -> None:
    """Render the stack to a simple SVG vector image."""
    xmax = max(b.x + b.side for b in stack.squares)
    ymax = max(b.y + b.side for b in stack.squares)
    total_squares = len(stack.squares)
    color_count = max(1, min(colors, len(COLOR_PALETTE)))
    with open(filename, "w") as fh:
        fh.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_fmt(xmax)} {_fmt(ymax)}">\n'
        )
        fh.write('<rect width="100%" height="100%" fill="black" />\n')
        for square in stack.squares:
            if renderer == "gradient":
                color = _gradient_color(square.n, total_squares)
            else:
                color = _cycle_color(square.n, color_count)
            fh.write(
                f'<rect x="{_fmt(square.x)}" y="{_fmt(ymax - (square.y + square.side))}" '
                f'width="{_fmt(square.side)}" height="{_fmt(square.side)}" '
                f'fill="rgb({color[0]},{color[1]},{color[2]})" />\n'
            )
            if numbers:
                text_color = _text_color(color)
                digits = len(str(square.n))
                max_size = square.side * Fraction(8, 10)
                width_based = square.side * Fraction(8, 10) / (Fraction(6, 10) * digits)
                font_size = min(max_size, width_based)
                fh.write(
                    f'<text x="{_fmt(square.x + square.side / 2)}" '
                    f'y="{_fmt(ymax - (square.y + square.side / 2))}" '
                    f'font-size="{_fmt(font_size)}" '
                    f'text-anchor="middle" dominant-baseline="central" '
                    f'fill="rgb({text_color[0]},{text_color[1]},{text_color[2]})">'
                    f'{square.n}</text>\n'
                )
        fh.write("</svg>\n")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Render square stacks")
    parser.add_argument(
        "N", type=int, nargs="?", default=100, help="number of squares to render"
    )
    parser.add_argument(
        "--algo",
        default="rational",
        help="stacking algorithm (module name in algorithms)",
    )
    parser.add_argument(
        "--fill",
        action="store_true",
        help="pack squares flush when using the sylvester algorithm",
    )
    parser.add_argument(
        "--fill-with-seams",
        action="store_true",
        help="allow seams in the packed sylvester variant",
    )
    parser.add_argument(
        "--coloring",
        choices=["cycle", "gradient"],
        default="cycle",
        help="coloring method",
    )
    parser.add_argument(
        "--colors",
        type=int,
        default=2,
        help="number of colors to cycle through (for cycle renderer)",
    )
    parser.add_argument(
        "--no-numbers",
        action="store_true",
        help="omit square numbers on the squares",
    )
    parser.add_argument(
        "--binary",
        action="store_true",
        help="write a PPM bitmap image instead of an SVG file",
    )
    parser.add_argument("--output", help="output file name")
    args = parser.parse_args()

    if args.algo == "sylvester":
        if args.fill_with_seams:
            stack = load_stack(
                "sylvester_with_seams", strict=False, open_bounds=False
            )
        else:
            stack = load_stack(
                "sylvester", strict=True, open_bounds=not args.fill
            )
    else:
        stack = load_stack(args.algo, strict=True, open_bounds=False)
    stack.build(args.N)
    if args.output is None:
        args.output = "stack.ppm" if args.binary else "stack.svg"
    if args.binary:
        render_ppm(
            stack,
            filename=args.output,
            renderer=args.coloring,
            colors=args.colors,
            numbers=not args.no_numbers,
        )
    else:
        render_svg(
            stack,
            filename=args.output,
            renderer=args.coloring,
            colors=args.colors,
            numbers=not args.no_numbers,
        )


if __name__ == "__main__":
    main()
