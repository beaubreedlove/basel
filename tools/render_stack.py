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


def render_ppm(stack: Stack, filename: str = "stack.ppm", scale: int = 400) -> None:
    """Render the stack to a simple PPM image file."""
    xmax = max(b.x + b.side for b in stack.blocks)
    width = int(scale * xmax) + 1
    height = scale
    # initialize black background
    pixels: List[List[Tuple[int, int, int]]] = [
        [(0, 0, 0) for _ in range(width)] for _ in range(height)
    ]
    for block in stack.blocks:
        color = (255, 0, 0) if block.n % 2 else (0, 0, 255)
        x0 = int(scale * block.x)
        x1 = int(scale * (block.x + block.side))
        y0 = int(scale * (1 - (block.y + block.side)))
        y1 = int(scale * (1 - block.y))
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
        default="harmonic",
        help="stacking algorithm (module name in basel.algorithms)",
    )
    parser.add_argument(
        "--relaxed",
        action="store_true",
        help="use relaxed rules where supported",
    )
    parser.add_argument("--output", default="stack.ppm", help="output PPM file")
    args = parser.parse_args()

    stack = load_stack(args.algo, strict=not args.relaxed)
    stack.build(args.N)
    render_ppm(stack, args.output)


if __name__ == "__main__":
    main()
