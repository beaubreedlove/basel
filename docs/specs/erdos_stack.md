# Erdos Square Stacking

This document defines the *Erdos method* for placing axis aligned squares.
It mirrors the terminology used in the Sylvester stack specification.

## Construction

1. Place the **1‑square** with vertices `(0,0)`, `(1,0)`, `(1,1)` and `(0,1)`.
2. For each integer `n > 1` let `s = 1/n`.  Write `n` in binary and read the
   digits following the leading `1` from left to right.  Initialize
   `(x, y) = (0, 0)` and `p = 1`.
   For each digit `d`:
   - If `d` is `0`, set `x = x + 1/p`.
   - If `d` is `1`, set `y = y + 1/p`.
   - Update `p = 2*p + int(d)`.
   The **n‑square** is positioned with its lower left corner at `(x, y)` and has
   side length `s`.

This procedure deterministically assigns a location to every square.  The method
is unrelated to the physical falling and sliding rules of the Sylvester stack but
produces a nested family of squares that can be rendered with the same
visualization script.

A reference implementation lives in `basel/algorithms/erdos.py`.  Use
`basel/tools/render_stack.py` with `--algo erdos` to visualize the first N
squares.  The renderer scales automatically to include all squares.
