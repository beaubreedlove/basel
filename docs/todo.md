# TODO List

This file outlines future directions and open questions for studying the Sylvester square stack and its simulation code.

1. **Identify the first point of divergence between strict and relaxed stacking.**
   - 1a. Determine if any square eventually settles on more than two squares of the same height, sliding across an extended plateau.
   - 1b. Investigate whether a single square can experience this phenomenon more than once as it moves and falls.
2. **Analyze the bottom boundary.**  Measure the total length of the intersection with the ground `y=0`.  Establish whether this length is finite or infinite and provide a decimal approximation if finite.
3. **Study the region near `(1, \alpha)`.**  With \(\alpha\) denoting the length of the intersection with `y=1`, describe the local shape just to the right and below this point.  Is the boundary differentiable there?  What slope, if any, does it approach?
4. **Review and refine the stacking algorithm.**  Confirm that the code matches the intended rules or update it accordingly.
5. **Design a more efficient data structure.**  Consider a tree-based approach to compute square placements more quickly.
6. **Define the function `f(a)`.**  For each `a` in `[0,1]`, let `f(a)` be the horizontal length of the stack's cross section at height `y=a`.  Explore properties of this function, including monotonicity, differentiability, and behavior near `a=1`.
7. **Create an interactive visualization.**  Develop a UI that allows zooming and panning.  The interface should request additional iterations as needed so users can explore fine details of the shape.
