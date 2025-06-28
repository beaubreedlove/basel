# Erdos Block Stacking

This document defines the *Erdos method* for placing axis aligned square blocks.
It mirrors the terminology used in the harmonic stack specification.

## Construction

1. Place the first square (the **1‑block**) with vertices `(0,0)`, `(1,0)`,
   `(1,1)` and `(0,1)`.
2. For each integer `n > 1` let `s = 1/n`.  Write `n` in binary and read the
   digits following the leading `1` from left to right.  Initialize
   `(x, y) = (0, 0)` and `p = 1`.
   For each digit `d`:
   - If `d` is `0`, set `x = x + 1/p`.
   - If `d` is `1`, set `y = y + 1/p`.
   - Update `p = 2*p + int(d)`.
   The **n‑block** is positioned with its lower left corner at `(x, y)` and has
   side length `s`.

This procedure deterministically assigns a location to every block.  The method
is unrelated to the physical falling and sliding rules of the harmonic stack but
produces a nested family of squares that can be rendered with the same
visualization script.
