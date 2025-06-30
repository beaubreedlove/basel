# Sylvester Square Stack

This document formalizes the iterative stacking process described in the problem
statement. Each step adds an axis aligned square of side `1/n` for
`n = 1, 2, 3, ...`.

## Construction

1. Place the first square (called the **1‑block**) with vertices
   `(0,0)`, `(1,0)`, `(1,1)` and `(0,1)`.
2. For each integer `n > 1` let `s = 1/n` and consider a new square of
   side `s` called the **n‑block**. Position the square so that its
   bottom edge lies on the line `y = 1` and its left edge coincides with
   `x = 0`.  It then slides horizontally to the right along existing
   blocks. Whenever it reaches a vertical drop, the square falls straight
  down until it touches the ground `y = 0` or rests on previously placed
  blocks. It continues sliding and falling until the entire square lies
  no higher than the line `y = 1`.  If, once it has reached this height,
  either its bottom or left side is not completely supported, the block
  shifts right until it falls off the next cliff edge and the checks are
  repeated.
3. In its final position the square must have no gap beneath it and its
   entire left side must touch blocks to its left (or the line `x = 0`).
   We consider two variants:
   
   - **Strict support** – both the bottom and left sides must touch a
     single block or the ground/left boundary.
   - **Relaxed support** – the bottom may rest on several blocks as long
     as their top faces form a contiguous interval of equal height, and
     the left side may touch several blocks whose right edges form a
     continuous vertical segment.

The union of all placed squares forms a one unit tall shape of total area
`\sum_{n=1}^\infty 1/n^2 = \pi^2/6`.

The tree like structure formed by supports can be explored by examining
which block each new block eventually sits on.

## Questions of Interest

* What is the geometry of the right boundary of this shape?  Is the
  bottom edge of finite or infinite length?
* How do the strict and relaxed variants differ when a block lands on a
  ledge made up of multiple blocks of the same height?

 A small Python module (`basel/algorithms/sylvester.py`) accompanies this document and
computes the first few block positions for both variants.  The script uses
Python's `Fraction` type so that every coordinate and interval length is
represented exactly as a rational number.

A companion script (`basel/tools/render_stack.py`) renders the first N blocks as a simple
PPM image. Run `python -m basel.tools.render_stack` to generate `stack.ppm`.
The renderer automatically scales its output to display all blocks, even when they
extend above height 1. Blocks can be colored using either a cycling palette or a
gradient from red to blue. Pass `--renderer gradient` for the gradient style or
adjust the number of cycling colors with `--colors N`. Pass `--relaxed` when using
the sylvester algorithm if you wish to enable the relaxed placement rules; otherwise
strict support is used.
