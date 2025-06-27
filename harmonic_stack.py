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
    """Construct the harmonic square stack."""

    def __init__(self, strict: bool = True) -> None:
        self.strict = strict
        self.blocks: List[Block] = [Block(1, Fraction(1), Fraction(0), Fraction(0))]
        # each segment is (left, right, height)
        self.segments: List[Tuple[Fraction, Fraction, Fraction]] = [
            (Fraction(0), Fraction(1), Fraction(1))
        ]

    # return all segments overlapping [start, end)
    def _segments_between(self, start: Fraction, end: Fraction) -> List[Tuple[Fraction, Fraction, Fraction]]:
        segs: List[Tuple[Fraction, Fraction, Fraction]] = []
        for l, r, h in self.segments:
            if r <= start or l >= end:
                continue
            segs.append((max(l, start), min(r, end), h))
        segs.sort()
        # fill uncovered gaps with ground (height 0)
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
        segs = self._segments_between(start, end)
        coverage = start
        for l, r, h in segs:
            if l > coverage:
                return False
            if h != bottom:
                return False
            coverage = r
        if coverage < end:
            return False
        if self.strict:
            return len(segs) == 1
        return True

    def _is_left_supported(self, x: Fraction, side: Fraction, bottom: Fraction) -> bool:
        """Check that the full left side contacts earlier blocks."""
        intervals: List[Tuple[Fraction, Fraction]] = []
        if x == 0:
            intervals.append((Fraction(0), Fraction(1)))
        for b in self.blocks:
            if b.x + b.side == x:
                intervals.append((b.y, b.y + b.side))
        intervals.sort()
        target_top = bottom + side
        coverage = bottom
        for l, r in intervals:
            if r <= coverage:
                continue
            if l > coverage:
                return False
            coverage = min(target_top, r)
            if coverage >= target_top:
                break
        if coverage < target_top:
            return False
        if self.strict:
            count = 0
            for l, r in intervals:
                if l <= bottom and r >= target_top:
                    count += 1
            return count == 1
        return True

    def _prev_boundary(self, x: Fraction) -> Fraction:
        boundaries = sorted({l for l, _, _ in self.segments} | {r for _, r, _ in self.segments})
        prev = x
        for b in boundaries:
            if b >= x:
                break
            prev = b
        return prev

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

    def _merge(self) -> None:
        self.segments.sort()
        if not self.strict:
            merged: List[Tuple[Fraction, Fraction, Fraction]] = []
            for l, r, h in self.segments:
                if merged and merged[-1][2] == h and merged[-1][1] == l:
                    merged[-1] = (merged[-1][0], r, h)
                else:
                    merged.append((l, r, h))
            self.segments = merged

    def add_block(self, n: int) -> None:
        side = Fraction(1, n)
        x = Fraction(0)
        bottom = Fraction(1)
        while True:
            support = self._support_height(x, side)
            if bottom > support:
                bottom = support
            top = bottom + side
            if top > 1:
                next_x = self._next_boundary(x)
                if next_x == x:
                    bottom = support
                    break
                x = next_x
                continue
            if self._is_supported(x, side, bottom) and self._is_left_supported(x, side, bottom):
                break
            prev_x = self._prev_boundary(x)
            if prev_x == x:
                bottom = support
                break
            x = prev_x
        self.blocks.append(Block(n, side, x, bottom))
        self._insert_segment(x, x + side, bottom + side)
        self._merge()

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

    parser = argparse.ArgumentParser(description="Simulate harmonic square stack")
    parser.add_argument("N", type=int, nargs="?", default=10, help="number of blocks to simulate")
    parser.add_argument("--relaxed", action="store_true", help="use relaxed support rule")
    args = parser.parse_args()

    stack = Stack(strict=not args.relaxed)
    stack.build(args.N)
    print(stack.summary())
