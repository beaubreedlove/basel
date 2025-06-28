# Basel

This directory contains code and notes for experimenting with various block
stacking problems.  Individual algorithms live in `algorithms/` and each has a
corresponding specification under `docs/specs/`.  The provided rendering tool in
`tools/render_stack.py` can visualize any of the algorithms.

**Note:** The current implementation has a bug that allows gaps to form between vertical towers. As a result, the top boundary of the stack sometimes rises after falling instead of decreasing monotonically.
