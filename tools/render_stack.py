from __future__ import annotations
from fractions import Fraction
from typing import Tuple, List
import importlib

def load_stack(algo: str, strict: bool) -> "Stack":
    module = importlib.import_module(f"basel.algorithms.{algo}")
    stack_class = getattr(module, "Stack")
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


def render_ppm(
    stack: Stack,
    filename: str = "stack.ppm",
    scale: int = 400,
    renderer: str = "cycle",
    colors: int = 2,
) -> None:
    """Render the stack to a simple PPM image file."""
    xmax = max(b.x + b.side for b in stack.blocks)
    ymax = max(b.y + b.side for b in stack.blocks)
    width = int(scale * xmax) + 1
    height = int(scale * ymax) + 1
    # initialize black background
    pixels: List[List[Tuple[int, int, int]]] = [
        [(0, 0, 0) for _ in range(width)] for _ in range(height)
    ]
    total_blocks = len(stack.blocks)
    color_count = max(1, min(colors, len(COLOR_PALETTE)))
    for block in stack.blocks:
        if renderer == "gradient":
            color = _gradient_color(block.n, total_blocks)
        else:
            color = _cycle_color(block.n, color_count)
        x0 = int(scale * block.x)
        x1 = int(scale * (block.x + block.side))
        y0 = int(scale * (ymax - (block.y + block.side)))
        y1 = int(scale * (ymax - block.y))
        for y in range(max(y0, 0), min(y1, height)):
            for x in range(max(x0, 0), min(x1, width)):
                pixels[y][x] = color
    with open(filename, "w") as fh:
        fh.write(f"P3\n{width} {height}\n255\n")
        for row in pixels:
            fh.write(" ".join(f"{r} {g} {b}" for r, g, b in row))
            fh.write("\n")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Render block stacks")
    parser.add_argument(
        "N", type=int, nargs="?", default=40, help="number of blocks to render"
    )
    parser.add_argument(
        "--algo",
        default="sylvester",
        help="stacking algorithm (module name in basel.algorithms)",
    )
    parser.add_argument(
        "--relaxed",
        action="store_true",
        help="use relaxed rules where supported",
    )
    parser.add_argument(
        "--renderer",
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
    parser.add_argument("--output", default="stack.ppm", help="output PPM file")
    args = parser.parse_args()

    stack = load_stack(args.algo, strict=not args.relaxed)
    stack.build(args.N)
    render_ppm(
        stack,
        filename=args.output,
        renderer=args.renderer,
        colors=args.colors,
    )


if __name__ == "__main__":
    main()
