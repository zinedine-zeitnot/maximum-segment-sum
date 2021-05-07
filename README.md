## A functional-style Python implementation of the maximum segment sum problem

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zinedine-zeitnot/maximum-segment-sum/HEAD?filepath=playground.ipynb)

The *maximum segment sum* problem is the task of computing the largest sum amongst the sums of all contiguous subsequences (or "segments") of a given list of integers.

So, for instance, the maximum segment sum of the list `[-1, 2, -3, 5, -2, 1, 3, -2, -2, -3, 6]` is 7 and it is achieved for the maximal segment `[5, -2, 1, 3]`.

The specification of the problem naturally leads to the following simple (but inefficient) brute-force solution:

```py
maximum_segment_sum = segments >> apply(sum) >> max
```

where

- `segments` is the function returning all contiguous subsequences of a given list of integers
- `apply(f)` is the function yielding the "`f`-transformed" version of a given list (i.e. `apply(f)` applies the function `f` to every list element)
- `max` is the function returning the maximum element of a given list
- `>>` designates the left-to-right function composition, i.e. `(f >> g >> h)(x) = h(g(f(x)))`

In words: obtaining the maximum segment sum of an integer list amounts (quite naturally in fact) to generating all list segments, taking their sums and finally returning the maximum of them all.

However, the complexity of the resulting solution is `O(n**3)` (because the `O(n**2)` complexity of the `segments` function is compounded with the `O(n)` linear complexity of each  segment-wise summation).

Surprisingly though, an `O(n)` solution exists and it is known in the literature as *Kadane's algorithm*.

In 1989, Richard Bird rederived Kadane's solution from a purely functional setting and showed that it could in fact be *calculated* from the very problem specification by employing *equational reasoning*, i.e. using the properties of the specification terms (and those of their byproducts) to algebraically refine the solution and progressively turn it into a more efficient one (a process formalized into the so called [Bird-Meertens formalism](https://en.wikipedia.org/wiki/Bird–Meertens_formalism)).

We present Bird's proof from a slightly-adapted Pythonic setting in `fromO(n**3)ToO(n).md`.

Finally, we offer you to get your hands on the Python implementation (cf. `maximum_segment_sum.py`) through a corresponding Jupyter notebook playground (available by clicking on the Binder badge above :point_up:)

N.B.: The implementation makes use of Python 3.10 through the new pattern matching mechanism (cf. [PEP 622](https://www.python.org/dev/peps/pep-0622/)). However, this requires (to this date) a custom build of Python 3.10 to be used onto the Binder-hosted notebook. Consequently, your notebook environment may take a bit long to setup the first time (~7-8mn) before you can finally play with it. So please go on about your other businesses in the meantime (but also please don't go too far at the risk of not coming back :wink:). Then, if you were to experience a "Kernel Not Found" pop-up message at the notebook's opening, clicking on "Set Kernel" should be fine to finally get you your notebook up and running.

And on those last words: happy wandering :slightly_smiling_face: