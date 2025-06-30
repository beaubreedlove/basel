# Basel

This directory contains code and notes for experimenting with various block
stacking problems. Individual algorithms live in `algorithms/` and each has a
corresponding specification under `docs/specs/`.

The helper script `tools/render_stack.py` visualizes any of the algorithms. It
produces a PPM image of the first *N* blocks and automatically scales the output
so all blocks remain visible even if the stack extends above height 1.

```
python -m basel.tools.render_stack [N] --algo NAME [--relaxed] [--output FILE]
```

Arguments:

* `N` – number of blocks to render (default: `40`)
* `--algo` – algorithm to use (default: `harmonic`)
* `--relaxed` – use any relaxed placement rules supported by the algorithm
* `--output` – name of the generated PPM file (default: `stack.ppm`)

**Note:** The current implementation has a bug that allows gaps to form between
vertical towers. As a result, the top boundary of the stack sometimes rises after
falling instead of decreasing monotonically.

### Available algorithms

- `harmonic` – falling and sliding rules
- `erdos` – binary expansion placement
- `rational` – doubles blocks when direction repeats
