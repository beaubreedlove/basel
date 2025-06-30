from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Dict, Optional

@dataclass
class Block:
    n: int
    side: Fraction
    x: Fraction
    y: Fraction  # bottom coordinate
    direction: Optional[str] = None
    parent: Optional[int] = None

class Stack:
    """Construct blocks according to the rational stacking specification."""

    def __init__(self, strict: bool = True) -> None:
        # ``strict`` is accepted for API compatibility but ignored.
        self.blocks: List[Block] = []
        self._map: Dict[int, Block] = {}
        self._init_seed()

    def _init_seed(self) -> None:
        # create 1-block
        b1 = Block(1, Fraction(1), Fraction(0), Fraction(0))
        self.blocks.append(b1)
        self._map[1] = b1
        # place 2-block to the right and 3-block above
        b2 = Block(2, Fraction(1, 2), Fraction(1), Fraction(0), "right", 1)
        b3 = Block(3, Fraction(1, 3), Fraction(0), Fraction(1), "up", 1)
        self.blocks.extend([b2, b3])
        self._map[2] = b2
        self._map[3] = b3
        self._current_round: List[int] = [2, 3]
        self._next_odd = 5

    def _add_block(self, n: int, x: Fraction, y: Fraction, direction: str, parent: int) -> None:
        block = Block(n, Fraction(1, n), x, y, direction, parent)
        self.blocks.append(block)
        self._map[n] = block

    def build(self, count: int) -> None:
        if count <= 3:
            return
        while max(self._map) < count:
            next_round: List[int] = []
            # doubling stage
            for n in self._current_round:
                child = 2 * n
                b = self._map[n]
                if b.direction == "right":
                    x = b.x + b.side
                    y = b.y
                    orient = "right"
                else:
                    x = b.x
                    y = b.y + b.side
                    orient = "up"
                if child <= count:
                    self._add_block(child, x, y, orient, n)
                    next_round.append(child)
            # gather gaps for filling stage
            gaps = []
            for n in self._current_round:
                b = self._map[n]
                if b.direction == "right":
                    x = b.x
                    y = b.y + b.side
                    orient = "up"
                else:
                    x = b.x + b.side
                    y = b.y
                    orient = "right"
                gaps.append((y, -x, n, orient))
            gaps.sort()
            for y, negx, parent, orient in gaps:
                if self._next_odd > count:
                    break
                x = -negx
                n = self._next_odd
                self._next_odd += 2
                self._add_block(n, x, y, orient, parent)
                next_round.append(n)
            self._current_round = next_round

    def summary(self) -> str:
        lines = []
        for b in sorted(self.blocks, key=lambda b: b.n):
            lines.append(
                f"n={b.n}: left={b.x} bottom={b.y} side={b.side}"
            )
        return "\n".join(lines)
