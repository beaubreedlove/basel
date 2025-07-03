# Open Problems

This document collects questions and answers that arise while studying the Sylvester square stack described in `specs/sylvester_stack.md`.

## Length of the segment along `y = 1`

**Problem.**  As squares are stacked, what is the length of the portion of the top boundary that lies exactly on the horizontal line `y = 1`?

**Answer.**  Several squares ultimately come to rest with their top sides on the line `y = 1`.  The pattern begins with the 1-square occupying `[0,1]`.  Later, the 6-square sits atop the stack of the 2- and 3-squares and contributes an additional segment of length `1/6`.  The 42-square rests on a stack involving the 7-square and contributes `1/42`, and so on.  These special square sizes are one less than the Sylvester numbers `2, 3, 7, 43, 1807, ...`.

The total length of the intersection is therefore

\[
\alpha = \sum_{k \ge 0} \frac{1}{S_k - 1} \approx 1.19659,
\]
where `S_k` denotes the `k`‑th Sylvester number.  Determining the exact value of `\alpha` remains an open question, but the series converges quickly.

## Does the 20-square align with the 4-square?

Some hand calculations suggested the 20-square might come to rest with its top at the same height as the 4-square.  A simulation using exact rational arithmetic shows this is not the case.  The 4-square has top height `1/4`, while the 20-square ends with bottom height `35873/58140` and top height `1939/2907`.  Thus there is no matching height at square 20 in either the strict or relaxed variants.
