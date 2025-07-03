from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional

@dataclass
class Block:
    n: int
    side: Fraction
    x: Fraction
    y: Fraction

@dataclass
class Corner:
    x: Fraction
    bottom: Fraction
    vspan: Fraction
    hspan: Optional[Fraction]
    left_is_wall: bool
    bottom_is_ground: bool

class Stack:
    """Faster Sylvester stack using a list of inside corners."""

    def __init__(self, strict: bool = True, open_bounds: bool = False) -> None:
        if not strict:
            raise NotImplementedError("Relaxed support not implemented")
        self.strict = True
        self.open_bounds = open_bounds
        self.blocks: List[Block] = [Block(1, Fraction(1), Fraction(0), Fraction(0))]
        self.segments: List[tuple[Fraction, Fraction, Fraction]] = [
            (Fraction(0), Fraction(1), Fraction(1))
        ]
        self.corners: List[Corner] = [
            Corner(
                Fraction(1),
                Fraction(0),
                Fraction(1),
                None,
                False,
                True,
            )
        ]

    def _merge(self) -> None:
        self.segments.sort()

    def _insert_segment(self, left: Fraction, right: Fraction, height: Fraction) -> None:
        new_segments: List[tuple[Fraction, Fraction, Fraction]] = []
        for l, r, h in self.segments:
            if r <= left or l >= right:
                new_segments.append((l, r, h))
            else:
                if l < left:
                    new_segments.append((l, left, h))
                if r > right:
                    new_segments.append((right, r, h))
        new_segments.append((left, right, height))
        self.segments = new_segments

    def add_block(self, n: int) -> None:
        side = Fraction(1, n)
        for i, c in enumerate(self.corners):
            if c.hspan is not None and side > c.hspan:
                continue
            if side > c.vspan:
                continue
            top = c.bottom + side
            if top > 1 or (self.open_bounds and top == 1):
                continue
            if self.open_bounds:
                if not c.bottom_is_ground and c.hspan is not None and side == c.hspan:
                    continue
                if not c.left_is_wall and side == c.vspan:
                    continue
            break
        else:
            raise RuntimeError("no position found")
        x = c.x
        bottom = c.bottom
        self.blocks.append(Block(n, side, x, bottom))
        self._insert_segment(x, x + side, bottom + side)
        self._merge()
        self.corners.pop(i)
        idx = i
        if c.vspan > side:
            self.corners.insert(
                idx,
                Corner(
                    x,
                    bottom + side,
                    c.vspan - side,
                    side,
                    c.left_is_wall,
                    False,
                ),
            )
            idx += 1
        if c.hspan is None:
            new_hspan = None
        else:
            new_hspan = c.hspan - side
        if new_hspan is None or new_hspan > 0:
            self.corners.insert(
                idx,
                Corner(
                    x + side,
                    bottom,
                    side,
                    new_hspan,
                    False,
                    c.bottom_is_ground,
                ),
            )

    def build(self, count: int) -> None:
        for n in range(2, count + 1):
            self.add_block(n)

    def summary(self) -> str:
        lines = []
        for b in self.blocks:
            lines.append(f"n={b.n}: left={b.x} bottom={b.y} side={b.side}")
        return "\n".join(lines)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simulate Sylvester block stacking (corner version)")
    parser.add_argument("N", type=int, nargs="?", default=10, help="number of blocks to simulate")
    parser.add_argument("--open", action="store_true", help="use open placement rules")
    args = parser.parse_args()

    stack = Stack(strict=True, open_bounds=args.open)
    stack.build(args.N)
    print(stack.summary())
