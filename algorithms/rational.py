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

    def _add_block(self, n: int, x: Fraction, y: Fraction, direction: str, parent: int) -> None:
        block = Block(n, Fraction(1, n), x, y, direction, parent)
        self.blocks.append(block)
        self._map[n] = block

    def build(self, count: int) -> None:
        if count <= 3:
            return
        while max(self._map) < count:
            next_round: List[int] = []
            for n in self._current_round:
                b = self._map[n]
                even = 2 * n
                odd = even + 1
                if b.direction == "right":
                    x_even = b.x + b.side
                    y_even = b.y
                    orient_even = "right"
                    x_odd = b.x
                    y_odd = b.y + b.side
                    orient_odd = "up"
                else:
                    x_even = b.x
                    y_even = b.y + b.side
                    orient_even = "up"
                    x_odd = b.x + b.side
                    y_odd = b.y
                    orient_odd = "right"
                if even <= count:
                    self._add_block(even, x_even, y_even, orient_even, n)
                    next_round.append(even)
                if odd <= count:
                    self._add_block(odd, x_odd, y_odd, orient_odd, n)
                    next_round.append(odd)
            self._current_round = next_round

    def summary(self) -> str:
        lines = []
        for b in sorted(self.blocks, key=lambda b: b.n):
            lines.append(
                f"n={b.n}: left={b.x} bottom={b.y} side={b.side}"
            )
        return "\n".join(lines)
