# Rational Square Stack

This document outlines a variant of the Erdos method for placing
axis aligned squares.  The procedure aims to avoid irrational
boundary points by repeatedly doubling squares whenever their placement
direction stays the same.

## Construction

1. Place the **1‑square** with vertices `(0,0)`,
   `(1,0)`, `(1,1)` and `(0,1)`.
2. Place the **2‑square** of side `1/2` immediately to the right of the
   1‑square and the **3‑square** of side `1/3` immediately above the
   1‑square.  These two squares establish the initial directions
   (*right* for the 2‑square and *up* for the 3‑square).
3. Afterwards proceed in rounds.  Suppose round `k` positioned a
   collection of squares labelled `n_1, n_2, ...`.  Round `k+1` consists
   of two stages:
   - **Doubling stage.**  For each square `n_i` placed in round `k`,
     position the square labelled `2 n_i` adjacent to `n_i` in the same
     direction (`right` or `up`) that `n_i` occupies relative to its
     own parent.
   - **Filling stage.**  Numerous corner gaps remain from round `k` that
     were not occupied by a doubled square.  Order these gaps from the
     bottom rightmost one to the top leftmost.  Into them place the
     smallest unused odd numbers in increasing order.  Each square fits
     snugly against the squares that form its corner.
A square's direction (*right* or *up*) is recorded when it is placed and
is inherited by its doubled successor in the following round.  If the
same direction repeats indefinitely along some path, the sequence of
square sizes on that path is `1/n, 1/(2n), 1/(4n), ...`, which sums to
`2/n`.  Consequently every jagged triangle on the boundary has
rationally located vertices.

An implementation of this algorithm lives in
`basel/algorithms/rational.py`.  See the module for a concise reference
version and the README for rendering instructions.
