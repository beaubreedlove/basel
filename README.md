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
produces an SVG vector image of the first *N* squares by default and
automatically scales the output so all squares remain visible. Pass `--binary`
to generate a PPM bitmap instead for simple pixel graphics.

```
python -m tools.render_stack [N] --algo NAME [--output FILE] \
    [--coloring {cycle,gradient}] [--colors NUM] [--no-numbers] [--binary]
```

Arguments:

* `N` – number of squares to render (default: `100`)
* `--algo` – algorithm to use (default: `rational`)
* `--output` – name of the generated image file (default: `stack.svg` or
  `stack.ppm` when `--binary` is used)
* `--coloring` – coloring method: `cycle` or `gradient` (default: `cycle`)
* `--colors` – number of colors for the cycle renderer (default: `2`)
* `--binary` – output a PPM image instead of SVG
* `--no-numbers` – omit square numbers on the squares

Some algorithms accept extra flags that extend or modify their behavior.
Consult the relevant specification for details.

### Available algorithms

- [`sylvester`](docs/specs/sylvester_stack.md) – falling and sliding rules
- [`erdos`](docs/specs/erdos_stack.md) – binary expansion placement
- [`rational`](docs/specs/rational_stack.md) – doubles squares when direction repeats

The **Sylvester** algorithm was my starting point.  It drops each $n$‑square
into a unit‑tall horizontal cavity using the simplest possible sliding rule
while never allowing a square to completely fill the remining space. As a result,
the squares immediately to the right of the 1 follow [Sylvester's sequence](https://en.wikipedia.org/wiki/Sylvester%27s_sequence),
whose first few terms are $2, 3, 7, 43,$ and $1807$.

The variant appears to trace a boundary stretching from $(1,1)$ to
$(0,S)$, where $S$ may diverge to infinity though this has not been proven. The
boundary wiggles like a snake with progressively smaller fractal-like
sub-wiggles as tall or wide stacks of similar sized squares fill narrow gaps
between similarly sized larger squares.

![Sylvester stack example](docs/images/sylvester.svg)
```
python -m tools.render_stack 2047 --algo sylvester --output sylvester.svg --colors 12
```

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

![Erdos stack example](docs/images/erdos.svg)
```
python -m tools.render_stack 2047 --algo erdos --output erdos.svg
```

Finally the **Rational** algorithm reorganizes the placements to produce edges
whose nontrivial vertices have rational coordinates.  Whenever an $n$‑square is
placed, the next even‑numbered square $2n$ is positioned adjacent to it in the
same direction, while the square $2n+1$ is positioned in the opposite
direction.  Each round therefore expands every square into two children.  Infinite paths that
repeat the same direction generate series of the form $\tfrac1n + \tfrac1{2n} + \tfrac1{4n} + \cdots = \tfrac2n$, ensuring every such vertex is
rational.

![Rational stack example](docs/images/rational.svg)
```
python -m tools.render_stack 2047 --algo rational --output rational.svg
```

### Examples

Render 50 squares using the gradient coloring:

```
python -m tools.render_stack 50 --coloring gradient
```

Render 20 squares cycling through 5 colors:

```
python -m tools.render_stack 20 --colors 5
```

Render squares without numbers:

```
python -m basel.tools.render_stack 10 --no-numbers
```

Generate a PPM image instead of a vector SVG:

```
python -m tools.render_stack 20 --binary
```
