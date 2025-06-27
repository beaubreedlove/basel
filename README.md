# Basel

This directory contains code and notes for experimenting with the harmonic square stacking problem. The scripts simulate how axis-aligned squares of side `1/n` are stacked according to simple falling and sliding rules. Supporting documentation lives in `docs/`.

**Note:** The current implementation has a bug that allows gaps to form between vertical towers. As a result, the top boundary of the stack sometimes rises after falling instead of decreasing monotonically.
