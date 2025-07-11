from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import List

@dataclass
class Square:
    n: int
    side: Fraction
    x: Fraction
    y: Fraction  # bottom coordinate

class Stack:
    """Construct the square stack using the Erdos method."""

    def __init__(self, strict: bool = True) -> None:
        # ``strict`` is accepted for API compatibility but ignored.
        self.squares: List[Square] = [
            Square(1, Fraction(1), Fraction(0), Fraction(0))
        ]

    def _position(self, n: int) -> tuple[Fraction, Fraction]:
        if n == 1:
            return Fraction(0), Fraction(0)
        x = Fraction(0)
        y = Fraction(0)
        prefix = 1
        bits = bin(n)[3:]  # drop '0b1'
        for b in bits:
            if b == '0':
                x += Fraction(1, prefix)
            else:
                y += Fraction(1, prefix)
            prefix = prefix * 2 + int(b)
        return x, y

    def add_square(self, n: int) -> None:
        x, y = self._position(n)
        self.squares.append(Square(n, Fraction(1, n), x, y))

    def build(self, count: int) -> None:
        for n in range(2, count + 1):
            self.add_square(n)

    def summary(self) -> str:
        lines = []
        for b in self.squares:
            lines.append(
                f"n={b.n}: left={b.x} bottom={b.y} side={b.side}"
            )
        return "\n".join(lines)
