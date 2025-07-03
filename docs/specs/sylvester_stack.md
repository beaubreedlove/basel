# Sylvester Square Stack

This document formalizes the iterative stacking process described in the problem
statement. Each step adds an axis aligned square of side `1/n` for
`n = 1, 2, 3, ...`.

## Construction

1. Place the **1‑square** with vertices
   `(0,0)`, `(1,0)`, `(1,1)` and `(0,1)`.
2. For each integer `n > 1` let `s = 1/n` and position the **n‑square** of
   side `s` so that its
   bottom edge lies on the line `y = 1` and its left edge coincides with
   `x = 0`.  It then slides horizontally to the right along existing
   squares. Whenever it reaches a vertical drop, the square falls straight
  down until it touches the ground `y = 0` or rests on previously placed
  squares. It continues sliding and falling until the entire square lies
  no higher than the line `y = 1`.  If, once it has reached this height,
  either its bottom or left side is not completely supported, the square
  shifts right until it falls off the next cliff edge and the checks are
  repeated.
3. In its final position the square must have no gap beneath it and its
   entire left side must touch squares to its left (or the line `x = 0`).
   We consider two variants:
   
   - **Strict support** – both the bottom and left sides must touch a
     single square or the ground/left boundary.
   - **Relaxed support** – the bottom may rest on several squares as long
     as their top faces form a contiguous interval of equal height, and
     the left side may touch several squares whose right edges form a
     continuous vertical segment.

The distinction between these variants arises quite early in the
construction.  Immediately to the right of the 2‑square the stack contains
a 4‑square topped by a 5‑square, which in turn supports the 20‑square.
Both configurations reach exactly height `1/2`, leaving a plateau split
down the seam between the 2‑ and 20‑squares.  In the relaxed version the
21‑square can rest across that horizontal seam.  A vertical example occurs
later when the 9‑ and 72‑squares sit atop the 8‑square, extending just as
far to the right as the 8‑square itself, so the 80‑square rests on the
32‑square and covers the seam.  These cases confirm that both horizontal
and vertical seams appear at least once, though it remains unknown
whether they recur infinitely many times.

![Sylvester stack example](../images/sylvester.svg)
```
python -m tools.render_stack 2047 --algo sylvester --output sylvester.svg
```

The union of all placed squares forms a one unit tall shape of total area
`\sum_{n=1}^\infty 1/n^2 = \pi^2/6`.

The tree like structure formed by supports can be explored by examining
which square each new square eventually sits on.

## Questions of Interest

* What is the geometry of the right boundary of this shape?  Is the
  bottom edge of finite or infinite length?
* How do the strict and relaxed variants differ when a square lands on a
  ledge made up of multiple squares of the same height?

A small Python module (`algorithms/sylvester.py`) accompanies this document and
computes the first few square positions.  The script uses Python's `Fraction`
type so that every coordinate and interval length is represented exactly as a
rational number.

A companion script (`tools/render_stack.py`) renders the first N squares as an
image file. Run `python -m tools.render_stack` to generate `stack.svg` by
default. Pass `--binary` to obtain `stack.ppm` instead. Refer to the project
README for additional output options.
The renderer automatically scales its output to display all squares, even when
they extend above height 1. Squares can be colored using either a cycling
palette or a gradient from red to blue. Pass `--coloring gradient` for the
gradient style or adjust the number of cycling colors with `--colors N`. By
default the Sylvester algorithm leaves a small gap above each square. Use
`--fill` to pack squares flush against their supports or `--fill-cover-seams` to
cover seams in the packed version.

When squares are packed without gaps, the right edge develops a boundary with
infinitely many oscillations.  The boundary begins at $(S, 1)$ where

$$S = 1 + \tfrac16 + \tfrac1{42} + \tfrac1{1806} + \cdots,$$

and the denominators $1, 6, 42, 1806, \ldots$ are one less than each term of
[Sylvester's sequence](https://en.wikipedia.org/wiki/Sylvester%27s_sequence)
$2, 3, 7, 43, 1807, \ldots$ except the 2nd term. Each denominator after $6$ is
obtained by multiplying the previous one by the next integer (e.g.,
$1807 = 42 * 43$). The resulting shape resembles a fractal with endlessly finer
wiggles.

The fact that 2 is missing from this sequence that otherwise matches Sylvester's
sequence is that led me to include the rule that newly placed blocks must be
strictly smaller than the gap they fill. Below are two variations without that
requirement.

### Filled Sylvester stack

Notice the 6‑square sits on the 3‑square to completely fill the gap that the
default algorithm leaves for the 7‑square and every later square in Sylvester's
sequence.

![Filled Sylvester stack](../images/sylvester_fill.svg)
```
python -m tools.render_stack 2047 --algo sylvester --fill --output sylvester_fill.svg
```

### Covering seams

Notice the 4+5+20 squares stack to the same height as the 2‑square, letting the
21‑square rest on the seam they create.  Likewise the 9‑ and 72‑squares on top of
the 8‑square extend as far right as the 8‑square, so the 80‑square can sit on the
32‑square and cover the seam.

![Covering seams](../images/sylvester_fill_cover_seams.svg)
```
python -m tools.render_stack 2047 --algo sylvester --fill-cover-seams --output sylvester_fill_cover_seams.svg
```
