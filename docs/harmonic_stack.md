# Harmonic Square Stack

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
  no higher than the line `y = 1`.
3. The square must never have a gap beneath it in its final position.
   We consider two variants:
   
   - **Strict support** – the whole bottom side must sit on a single
     block or the ground.
   - **Relaxed support** – the bottom may rest on several blocks as long
     as their top faces form a contiguous interval of equal height.

The union of all placed squares forms a one unit tall shape of total area
`\sum_{n=1}^\infty 1/n^2 = \pi^2/6`.

The tree like structure formed by supports can be explored by examining
which block each new block eventually sits on.

## Questions of Interest

* What is the geometry of the right boundary of this shape?  Is the
  bottom edge of finite or infinite length?
* How do the strict and relaxed variants differ when a block lands on a
  ledge made up of multiple blocks of the same height?

 A small Python script (`basel/stack_blocks.py`) accompanies this document and
computes the first few block positions for both variants.  The script uses
Python's `Fraction` type so that every coordinate and interval length is
represented exactly as a rational number.

 A companion script (`basel/render_stack.py`) renders the first N blocks as a simple
 PPM image. Run `python basel/render_stack.py` to generate `stack.ppm`. Odd-numbered
blocks appear in red and even-numbered blocks in blue on a black background.
