# Basel

This directory contains code and notes for experimenting with various block
stacking problems.  Individual algorithms live in `algorithms/` and each has a
corresponding specification under `docs/specs/`.  The provided rendering tool in
`tools/render_stack.py` can visualize any of the algorithms.  It automatically
adjusts the vertical scale so blocks that extend above height 1 remain visible.

**Note:** The current implementation has a bug that allows gaps to form between vertical towers. As a result, the top boundary of the stack sometimes rises after falling instead of decreasing monotonically.

Available algorithms:
- `harmonic` -- falling and sliding rules
- `erdos` -- binary expansion placement
- `rational` -- doubles blocks when direction repeats
