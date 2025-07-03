from __future__ import annotations
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Block:
    n: int
    side: Fraction
    x: Fraction
    y: Fraction  # bottom coordinate

class Stack:
    def __init__(self, strict: bool = True, open_bounds: bool = False):
        self.strict = strict
        self.open_bounds = open_bounds
        self.blocks: List[Block] = [Block(1, Fraction(1), Fraction(0), Fraction(0))]
        self.segments: List[Tuple[Fraction, Fraction, Fraction]] = [
            (Fraction(0), Fraction(1), Fraction(1))
        ]

    # merge overlapping segments; adjacent segments of the same height are
    # merged only in the relaxed variant so that the strict version keeps
    # track of individual supports.
    def _merge(self):
        # Only sort segments.  We deliberately keep adjacent segments
        # separate so that strict support can detect them.
        self.segments.sort()

    # top surface height at position x
    def _top(self, x: Fraction) -> Fraction:
        for l, r, h in self.segments:
            if l <= x < r:
                return h
        return Fraction(0)

    # segments covering [start, end)
    def _segments_between(
        self, start: Fraction, end: Fraction, clip: bool = True
    ) -> List[Tuple[Fraction, Fraction, Fraction]]:
        segs: List[Tuple[Fraction, Fraction, Fraction]] = []
        for l, r, h in self.segments:
            if r <= start or l >= end:
                continue
            if clip:
                segs.append((max(l, start), min(r, end), h))
            else:
                segs.append((l, r, h))
        segs.sort()
        if not clip:
            return segs
        # fill gaps with ground
        result: List[Tuple[Fraction, Fraction, Fraction]] = []
        coverage = start
        for l, r, h in segs:
            if l > coverage:
                result.append((coverage, l, Fraction(0)))
            result.append((l, r, h))
            coverage = r
        if coverage < end:
            result.append((coverage, end, Fraction(0)))
        return result

    def _support_height(self, start: Fraction, side: Fraction) -> Fraction:
        segs = self._segments_between(start, start + side)
        return max(h for _, _, h in segs)

    def _is_supported(self, start: Fraction, side: Fraction, bottom: Fraction) -> bool:
        end = start + side
        segs = []
        coverage = start
        right_extent = None
        for l, r, h in self.segments:
            if r <= coverage:
                continue
            if l >= end:
                break
            seg_left = max(l, start)
            seg_right = min(r, end)
            if seg_left > coverage:
                return False
            if h != bottom:
                return False
            segs.append((seg_left, seg_right, h))
            coverage = seg_right
            if seg_right == end:
                right_extent = r
        if coverage < end:
            return False
        if self.open_bounds and bottom != Fraction(0):
            if right_extent is None or right_extent <= end:
                return False
        if self.strict:
            return len(segs) == 1
        return True

    def _is_left_supported(self, x: Fraction, side: Fraction, bottom: Fraction) -> bool:
        """Check that the entire left edge at position x is covered."""
        intervals: List[Tuple[Fraction, Fraction]] = []
        if x == 0:
            intervals.append((Fraction(0), Fraction(1)))
        for b in self.blocks:
            if b.x + b.side == x:
                intervals.append((b.y, b.y + b.side))
        intervals.sort()
        target_top = bottom + side
        coverage = bottom
        top_extent = None
        for l, r in intervals:
            if r <= coverage:
                continue
            if l > coverage:
                return False
            if r >= target_top:
                top_extent = r
                coverage = target_top
                break
            coverage = r
        if coverage < target_top:
            return False
        if self.open_bounds and x != Fraction(0):
            if top_extent is None or top_extent <= target_top:
                return False
        if self.strict:
            count = 0
            for l, r in intervals:
                if l <= bottom and r >= target_top:
                    count += 1
            return count == 1
        return True

    def _next_boundary(self, x: Fraction) -> Fraction:
        boundaries = sorted({l for l, _, _ in self.segments} | {r for _, r, _ in self.segments})
        for b in boundaries:
            if b > x:
                return b
        return x

    def _insert_segment(self, left: Fraction, right: Fraction, height: Fraction) -> None:
        new_segments: List[Tuple[Fraction, Fraction, Fraction]] = []
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

    def add_block(self, n: int):
        side = Fraction(1, n)
        x = Fraction(0)
        bottom = Fraction(1)
        while True:
            support = self._support_height(x, side)
            if bottom > support:
                bottom = support
            top = bottom + side
            if (top > 1) or (self.open_bounds and top == 1):
                next_x = self._next_boundary(x)
                if next_x == x:
                    bottom = support
                    break
                x = next_x
                continue
            if self._is_supported(x, side, bottom) and self._is_left_supported(x, side, bottom):
                break
            next_x = self._next_boundary(x)
            if next_x == x:
                bottom = support
                break
            x = next_x
        self.blocks.append(Block(n, side, x, bottom))
        # insert new segment and remove covered pieces of older segments
        self._insert_segment(x, x + side, bottom + side)
        self._merge()

    def build(self, count: int):
        for n in range(2, count + 1):
            self.add_block(n)

    def summary(self) -> str:
        lines = []
        for b in self.blocks:
            lines.append(
                f"n={b.n}: left={b.x} bottom={b.y} side={b.side}"
            )
        return "\n".join(lines)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simulate Sylvester block stacking")
    parser.add_argument("N", type=int, nargs="?", default=10, help="number of blocks to simulate")
    parser.add_argument("--relaxed", action="store_true", help="use relaxed support rule")
    parser.add_argument("--open", action="store_true", help="use open placement rules")
    args = parser.parse_args()

    stack = Stack(strict=not args.relaxed, open_bounds=args.open)
    stack.build(args.N)
    print(stack.summary())
