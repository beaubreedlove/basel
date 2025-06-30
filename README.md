# Basel

This directory contains code and notes for experimenting with various block
stacking problems. Individual algorithms live in `algorithms/` and each has a
corresponding specification under `docs/specs/`.

The helper script `tools/render_stack.py` visualizes any of the algorithms. It
produces a PPM image of the first *N* blocks by default and automatically scales
the output so all blocks remain visible even if the stack extends above
height 1.  Pass `--vector` to generate an SVG instead for unlimited zooming
precision.

```
python -m basel.tools.render_stack [N] --algo NAME [--output FILE] \
    [--renderer {cycle,gradient}] [--colors NUM]
```

Arguments:

* `N` – number of blocks to render (default: `40`)
* `--algo` – algorithm to use (default: `sylvester`)
* `--output` – name of the generated image file (default: `stack.ppm` or
  `stack.svg` when `--vector` is used)
* `--renderer` – coloring method: `cycle` or `gradient` (default: `cycle`)
* `--colors` – number of colors for the cycle renderer (default: `2`)
* `--vector` – output an SVG vector image instead of PPM

Some algorithms accept extra flags that extend or modify their behavior.
Consult the relevant specification for details.

### Available algorithms

- [`sylvester`](docs/specs/sylvester_stack.md) – falling and sliding rules
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

Generate a vector image instead of a PPM:

```
python -m basel.tools.render_stack 20 --vector
```
