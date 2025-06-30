# Basel

This directory contains code and notes for experimenting with various block
stacking problems. Individual algorithms live in `algorithms/` and each has a
corresponding specification under `docs/specs/`.

The helper script `tools/render_stack.py` visualizes any of the algorithms. It
produces a PPM image of the first *N* blocks and automatically scales the output
so all blocks remain visible even if the stack extends above height 1.

```
python -m basel.tools.render_stack [N] --algo NAME [--output FILE] \
    [--renderer {cycle,gradient}] [--colors NUM]
```

Arguments:

* `N` – number of blocks to render (default: `40`)
* `--algo` – algorithm to use (default: `harmonic`)
* `--output` – name of the generated PPM file (default: `stack.ppm`)
* `--renderer` – coloring method: `cycle` or `gradient` (default: `cycle`)
* `--colors` – number of colors for the cycle renderer (default: `2`)

Some algorithms accept extra flags that extend or modify their behavior.
Consult the relevant specification for details.

### Available algorithms

- [`harmonic`](docs/specs/harmonic_stack.md) – falling and sliding rules
- [`erdos`](docs/specs/erdos_stack.md) – binary expansion placement
- [`rational`](docs/specs/rational_stack.md) – doubles blocks when direction repeats

### Examples

Render 50 blocks using the gradient coloring:

```
python -m basel.tools.render_stack 50 --renderer gradient
```

Render 20 blocks cycling through 5 colors:

```
python -m basel.tools.render_stack 20 --colors 5
```
