### Abstract/disclaimer:
 Here we employ program calculation to derive a more efficient `O(n)` implementation of the maximum segment sum algorithm from its original `O(n**3)` specification. However, our contribution in the following presentation was only to port Richard Bird's Haskell proof (cf. R. Bird's [Thinking Functionally with Haskell](https://www.cs.ox.ac.uk/publications/books/functional/), section 6.6) into a more Pythonic setting. In doing so, we took the liberty to lighten certain parts of the original exposition to make ours a little more digestible (and, let's hope so, a little more accessible to non-Haskellers). All in all, our secret motive behind this rewriting has only been to revive the truly beautiful wedding between program construction and equational reasoning (so may our lack of rigor be forgiven).

---

Let us begin with the specification of the `maximum_segment_sum` function (`naive_maximum_segment_sum` in our code):

```py
maximum_segment_sum =
    segments
    >> apply(sum)
    >> max
```

And inject the definition of the `segments` function:

```py
segments =
    tails
    >> apply(inits)
    >> flatten
```

We thus have:

```py
maximum_segment_sum = 
    tails 
    >> apply(inits)
    >> flatten
    >> apply(sum)
    >> max
```

Now using the following law (always valid for list of lists): 

```py
flatten >> apply(f) = apply(apply(f)) >> flatten
```

and applying it for the subterm `flatten >> apply(sum)`, we get:

```py
maximum_segment_sum =
    tails
    >> apply(inits)
    >> apply(apply(sum))
    >> flatten
    >> max
```

Using the following fusion property of `apply`:

```py
apply(f) >> apply(g) = apply(f >> g)
```

the `maximum_segment_sum` function is thus refined even further into:

```py
maximum_segment_sum = 
    tails
    >> apply(inits >> apply(sum))
    >> flatten
    >> max
```

Now, provided the argument to `flatten` is a non-empty list of non-empty lists, we can also use the following law:

```py
flatten >> max = apply(max) >> max
```

N.B.: Since the `max` function is undefined on empty lists, the above law wouldn't be applicable for a list containing empty sub-lists. However, the `sum` function evaluating to zero on empty lists, the `apply(inits >> apply(sum))` term of the `maximum_segment_sum` function guarantees that the input to the `flatten` function will always be safe for us to apply the `flatten >> max` law.

Using this last law, we arrive at:

```py
maximum_segment_sum =
    tails
    >> apply(inits >> apply(sum))
    >> apply(max)
    >> max
```

And using the fusion property of `apply` once again:

```py
maximum_segment_sum =
    tails
    >> apply(inits >> apply(sum) >> max)
    >> max
```

What a journey yet! So let's breathe for a moment and ask if we've gained something thus far.

The `inits` function being `O(n**2)` in complexity, the whole term inside the `apply` function is `O(n**2)` as well, and applying this `apply` on top of it all remains `O(n**3)` (unfortunately). So in case you wondered: yes, all we did up to this point was only cosmetic. But don't huff and puff too fast: that wasn't wasted time, I promise!

And without further ado, let's introduce another useful function that will reduce the `maximum_segment_sum` complexity to `O(n**2)`, straightaway. So ladies and gentlemen, please welcome the left-accumulation function: `accumulate_from_left`.

On non-empty lists, it is defined by:

```py
accumulate_from_left(f, 0)([x, y]) = [0, f(0, x), f(f(0, x), y)]
```

(you get the pattern for longer lists)

And for empty lists:

```py
accumulate_from_left(f, 0)([]) = [0]
```

One property of this function that will be useful for our purposes is the following one:

```py
accumulate_from_left(add, 0) = inits >> apply(sum)
```

Moreover, we see from the definition that the actual complexity of this function is `O(n)` (and not `O(n**2)` as the above property suggests) because it only requires `n` evaluations of the `f` function.

So using this, we get that:

```py
maximum_segment_sum =
    tails
    >> apply(accumulate_from_left(add, 0) >> max)
    >> max
```

and the `maximum_segment_sum` complexity is thus reduced to `O(n**2)`.

But all this was without mentioning the dual companion of `accumulate_from_left`, i.e. `accumulate_from_right`.

In a similar fashion, the `accumulate_from_right` function is defined on non-empty lists by:

```py
accumulate_from_right(f, 0)([x, y]) = [f(y, f(x, 0)), f(x, 0), 0]
```

and on empty lists by:

```py
accumulate_from_right(f, 0)([]) = [0]
```

Now the interesting property that would reduce the `maximum_segment_sum` complexity even further is:

```py
accumulate_from_right(f, 0) = tails >> apply(fold_from_right(f, 0))
```

where the `fold_from_right` function is defined by:

```py
fold_from_right(f, 0)([]) = 0

fold_from_right(f, 0)([x, y]) = f(x, f(y, 0))
```

This is because substituting into `maximum_segment_sum`, we would finally have:

```py
maximum_segment_sum =
    accumulate_from_right(h, 0)
    >> max
```

for a certain function `h`.

And since `accumulate_from_right` is `O(n)`, `maximum_segment_sum` would be too!

Okay, but turning `tails >> apply(accumulate_from_left(add, 0) >> max)` into `accumulate_from_right(h, 0)` supposes beforehand that we can write `accumulate_from_left(add, 0) >> max` as a `fold_from_right(h, 0)`, right?

But can we?

Well, the beauty of it all is that **yes**, we can. However, this requires a bit of additional work. So you can stop there if you've seen enough to be satisfied, but in case you're hungry for the finish: let's get started! :point_right:

## The last mile :checkered_flag:

Since the beginning, we understood the `max` function as a *list* function returning the maximal element of a given list. And though the `max` function provided by Python doesn't care if you give it elements as is or elements as a list (i.e. you can equivalently write `max(1, 2, 3)` or `max([1, 2, 3])`), we'll differentiate between the two modus operandi to avoid confusion later.

Thus, let us introduce a `binary_max` function defined as:

```py
binary_max(x, y) = max([x, y])
```

With this definition, we claim that the `max` function itself can be written as a right-fold (though a *strict* one that operates on non-empty lists since the `max` of an empty list is undefined): 

```py
max = strict_fold_from_right(binary_max)
```

where the `strict_fold_from_right(g)` function is defined for any function `g` as:

```py
strict_fold_from_right(g)([x]) = x

strict_fold_from_right(g)([x, y, z]) = g(x, g(y, z))
```

Substituting `g` with the `binary_max` function we have:

```py
strict_fold_from_right(binary_max)([x, y, z]) = binary_max(x, binary_max(y, z)) = max([x, y, z])
```

thus validating our claim.

"Okay but what's that for? If we use your `max` rewriting into `accumulate_from_left(add, 0) >> max`, we get `accumulate_from_left(add, 0) >> strict_fold_from_right(binary_max)` but that still ain't no `fold_from_right(h, 0)`, right?"

Right. But we're getting close!

"Yeah? How's that?"


Well, **spoiler alert** but we can actually write `accumulate_from_left(add, 0)` itself as a right-fold and use some kind of fusion law again to finally get our long-awaited `fold_from_right(h, 0)`!

":boom: :boom:"


Actually, we have:

```py
accumulate_from_left(add, 0)([x, y, z])
    = [0, add(0, x), add(add(0, x), y), add(add(add(0, x), y), z)]
    = [0, 0+x, (0+x)+y, ((0+x)+y)+z]
    = [0, x, x+y, x+y+z]
    = [0] + apply(lambda _: add(x, _))([0, y, y+z])
    = [0] + apply(lambda _: add(x, _))(accumulate_from_left(add, 0)([y, z]))
```

So this suggests that:

```py
accumulate_from_left(add, 0) = fold_from_right(f, [0])
```

for a certain function `f` defined by:

```py
def f(x: int, xs: list[int]) -> list[int]:
    return [0] + apply(lambda _: add(x, _))(xs)
```

Indeed, we have:

```py
f(z, [0]) = [0] + apply(lambda _: add(z, _))([0])
          = [0] + [add(z, 0)]
          = [0] + [z]
          = [0, z]
```

So,

```py
f(y, f(z, [0])) = f(y, [0, z])
                = [0] + apply(lambda _: add(y, _))([0, z])
                = [0] + [add(y, 0), add(y, z)]
                = [0] + [y, y+z]
                = [0, y, y+z]
```

Hence:

```py
fold_from_right(f, [0])([x, y, z]) = f(x, f(y, f(z, [0])))
                                   = [0] + apply(lambda _: add(x, _))(f(y, f(z, [0])))
                                   = [0] + apply(lambda _: add(x, _))([0, y, y+z])
                                   = [0] + [x, x+y, x+y+z]
                                   = [0, x, x+y, x+y+z]
                                   = [0, 0+x, (0+x)+y, ((0+x)+y)+z]
                                   = [0, add(0, x), add(add(0, x), y), add(add(add(0, x), y), z)]
                                   = accumulate_from_left(add, 0)([x, y, z])
```

And voilà: `fold_from_right(f, [0]) = accumulate_from_left(add, 0)`.

"Really cool yeah. But, how about the fusion law now?"

Well, we'd like to have:
```py
fold_from_right(f, [0]) >> strict_fold_from_right(binary_max) = fold_from_right(h, 0)       (*)
```

for a certain function `h`.

So first, let's make sure we've got no discrepancy on empty lists.

We have:

```py
fold_from_right(f, [0])([]) = [0] 
```

(by definition of `fold_from_right`)

and

```py
strict_fold_from_right(binary_max)([0]) = 0
```

(because, by definition again, `strict_fold_from_right(g)([x]) = x` for any `g`)

So, the function composition `fold_from_right(f, [0]) >> strict_fold_from_right(binary_max)` returns `0` when evaluated on an empty list and this coincides with the fact that `fold_from_right(h, 0)([]) = 0` (by definition of `fold_from_right`).


"So that's all good on empty lists, okay thanks. But what about the function `h` itself? What's it like?"

Well, let's evaluate both sides of the above equation `(*)` on a non-empty `[x, y]` list to try infering the anatomy of `h`:

```py
fold_from_right(f, [0])([x, y]) = f(x, f(y, [0])) = [0, x, x+y]
```

and because we showed earlier that

```py
strict_fold_from_right(binary_max)([x, y, z]) = binary_max(x, binary_max(y, z))
```

we thus have:

```py
strict_fold_from_right(binary_max)([0, x, x+y]) = binary_max(0, binary_max(x, x+y))
```

So, the `fold_from_right(f, [0]) >> strict_fold_from_right(binary_max)` right-hand side of the `(*)` equation yields `binary_max(0, binary_max(x, x+y))` when fed with `[x, y]`.

"That doesn't quite look like it but, is that a hidden right-fold of some kind?"

Yes it is! The trick to achieve it is to remark that:
    
```py
binary_max(x, x+y) = x if y <= 0 else x + y
                   = x + binary_max(0, y)
```

and so:

```py
binary_max(0, binary_max(x, x+y)) = binary_max(0, x + binary_max(0, y+0))
                                  = h(x, h(y, 0)) with h(x, y) = binary_max(0, x+y)
```

And, ladies and gentlemen, we have `fold_from_right(h, 0)([x, y]) = h(x, h(y, 0))` by definition, so indeed:

```py
fold_from_right(f, [0]) >> strict_fold_from_right(binary_max) = fold_from_right(h, 0)
```

with `h(x, y) = binary_max(0, x+y)`.

And QED.
