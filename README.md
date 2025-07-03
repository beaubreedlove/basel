# Basel

This project collects code and notes from my attempt to construct a geometric
proof for the **Basel problem**.  The problem asks for the exact value of the
infinite sum

$$\sum_{n=1}^{\infty} \frac{1}{n^2} = 1 + \frac{1}{2^2} + \frac{1}{3^2} + \cdots = \frac{\pi^2}{6}.$$

To study this series visually, I developed algorithms that place a sequence of
axis aligned squares with side lengths $1/n$ for $n = 1, 2, 3, \ldots$.  We call
such a square the **$n$‑square**.  Each algorithm positions the $n$‑squares
according to different rules and the accompanying tools render the resulting
shapes for further exploration.  Individual implementations live in
`algorithms/` with corresponding specifications under `docs/specs/`.

The helper script `tools/render_stack.py` visualizes any of the algorithms. It
produces a PPM image of the first *N* squares by default and automatically scales
the output so all squares remain visible.  Pass `--vector` to generate an SVG instead for unlimited zooming
precision.

```
python -m tools.render_stack [N] --algo NAME [--output FILE] \
    [--renderer {cycle,gradient}] [--colors NUM] [--fill] [--fill-with-seams]
```

Arguments:

* `N` – number of squares to render (default: `100`)
* `--algo` – algorithm to use (default: `rational`)
* `--output` – name of the generated image file (default: `stack.ppm` or
  `stack.svg` when `--vector` is used)
* `--renderer` – coloring method: `cycle` or `gradient` (default: `cycle`)
* `--colors` – number of colors for the cycle renderer (default: `2`)
* `--vector` – output an SVG vector image instead of PPM
* `--fill` – use the packed variant of the Sylvester algorithm
* `--fill-with-seams` – allow seams in the packed variant

Some algorithms accept extra flags that extend or modify their behavior.
Consult the relevant specification for details.

### Available algorithms

- [`sylvester`](docs/specs/sylvester_stack.md) – falling and sliding rules
- [`erdos`](docs/specs/erdos_stack.md) – binary expansion placement
- [`rational`](docs/specs/rational_stack.md) – doubles squares when direction repeats

The **Sylvester** algorithm was my starting point.  It drops each $n$‑square
into a unit‑tall horizontal cavity using the simplest possible sliding rule.
This process creates a boundary with infinitely many oscillations.  The boundary
begins at $(S, 1)$ where

$$S = 1 + \tfrac16 + \tfrac1{42} + \tfrac1{1806} + \cdots,$$

and the denominators $1, 6, 42, 1806, \ldots$ are one less than each term of
[Sylvester's sequence](https://en.wikipedia.org/wiki/Sylvester%27s_sequence)
$2, 3, 7, 43, 1807, \ldots$ except the 2nd term.  Each denominator after $6$ is obtained by
multiplying the previous one by the next integer (e.g., $1807 = 42 * 43$). The resulting shape
resembles a fractal with endlessly finer wiggles.

Seeking a configuration with clearer structure, I next tried the **Erdos**
algorithm.  Rest the $1$‑square against the ground and a wall to create two
corners.  Place the $2$‑square in the lower corner and the $3$‑square above it.
These squares in turn create four new corners for squares $4$ through $7$,
and in general the $n$th stage provides positions for $2^{n-1}$ additional
squares numbered $2^{n-1}$ through $2^n-1$.  The bottom edge of the stack has
length $1 + \tfrac12 + \tfrac14 + \tfrac18 + \cdots = 2$, while the left edge
equals the [Erdos–Borwein constant](https://mathworld.wolfram.com/Erdos-BorweinConstant.html)
$1 + \tfrac13 + \tfrac17 + \tfrac1{15} + \tfrac1{2^n-1} + \cdots$.  This
irrational value and related series appear throughout the boundary, making the
geometry difficult to analyze.

Finally the **Rational** algorithm reorganizes the placements to produce edges
whose nontrivial vertices have rational coordinates.  Whenever an $n$‑square is
placed, the next even‑numbered square $2n$ is positioned adjacent to it in the
same direction.  Remaining odd squares fill the unused corners in order from bottom right
to top left.  Infinite paths that repeat the same direction generate series of
the form $\tfrac1n + \tfrac1{2n} + \tfrac1{4n} + \cdots = \tfrac2n$, ensuring every such vertex is
rational.  This result is still under investigation.

### Examples

Render 50 squares using the gradient coloring:

```
python -m tools.render_stack 50 --renderer gradient
```

Render 20 squares cycling through 5 colors:

```
python -m tools.render_stack 20 --colors 5
```

Generate a vector image instead of a PPM:

```
python -m tools.render_stack 20 --vector
```
