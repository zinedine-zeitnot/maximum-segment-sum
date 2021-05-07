from typing import Callable, Tuple, TypeVar

from toolz.functoolz import pipe


X, Y = TypeVar('X'), TypeVar('Y')


#######################################
# Maximum segment sum implementations #
#######################################

def naive_maximum_segment_sum(xs: list[int]) -> int:
    '''
    Returns the maximum segment sum of an integer list.

    Example:
        In [1]: naive_maximum_segment_sum([-1, 2, -3, 5, -2, 1, 3, -2, -2, -3, 6])
        Out[1]: 7 (i.e. the sum of the maximal [5, -2, 1, 3] segment)

    Specification:
        naive_maximum_segment_sum = segments >> apply(sum) >> max
        
        where:
            - segments is the function yielding all contiguous subsequences of a list.

            - >> stands for left-to-right function composition. In our code, we use the 
              toolz.functoolz.pipe function as a substitute so that, in an ideal world where
              the >> operator would be defined between Python functions, we'd have:
              pipe(xs, f, g, h) = (f >> g >> h)(xs).

            - apply(f) is the function yielding the "f-transformed" version of a given list
              (or alternatively: apply(f) applies the function f to every element of a list).      

    Complexity: O(n**3).
    '''
    return pipe(xs,
        segments,
        apply(sum),
        max
    )


def efficient_maximum_segment_sum(xs: list[int]) -> int:
    '''
    Optimized version of the naive_maximum_segment_sum function.

    Complexity: O(n).
    '''
    return pipe(xs,
        accumulate_from_right(relu_sum, 0),
        max
    )


####################
# Helper functions #
####################

def segments(xs: list[X]) -> list[list[X]]:
    '''
    Returns all segments of a given list (i.e. all its contiguous subsequences). Warning: the empty
    list will appear several times due to the definition from tails and inits.

    Example:
        In [1]: segments([1, 2, 3])
        Out[1]: [[], [1], [1, 2], [1, 2, 3], [], [2], [2, 3], [], [3], []]

    Specification:
        segments = tails >> apply(inits) >> flatten

        where:
            - >> stands for left-to-right function composition.

            - tails is the function yielding all the tail segments of a given list.

            - inits is the function yielding all the initial segments of a given list.

            - apply(f) is the function yielding the "f-transformed" version of a given list
              (or said differently: apply(f) applies the function f to every element of a list).

            - flatten is the function yielding the 1-dimensional version of a given list.

        In other words: getting all segments of a list boils down to gathering all the initial segments
        of all the tail segments of the list.

    Complexity: O(n**2).
    '''
    return pipe(xs,
        tails,
        apply(inits),
        flatten
    )


def tails(l: list[X]) -> list[list[X]]:
    '''
    Returns all tail segments of a list.

    Example:
        In [1]: tails([1, 2, 3])
        Out[1]: [[1, 2, 3], [2, 3], [3], []]

    Complexity: O(n).
    '''
    match l:
        case []:
            return [[]]
        case [x, *xs]:
            return [l] + tails(xs)


def apply(f: Callable[[X], Y]) -> Callable[[list[X]], list[Y]]:
    '''
    Returns the function that applies f to every element of its input list.

    Definition:
        apply(f)([e1, e2, e3]) = [f(e1), f(e2), f(e3)]
    '''
    return lambda xs: [f(x) for x in xs]


def inits(l: list[X]) -> list[list[X]]:
    '''
    Returns all initial segments of a list.

    Example:
        In [1]: inits([1, 2, 3])
        Out[1]: [[], [1], [1, 2], [1, 2, 3]]
    
    Complexity: O(n).
    '''
    match l:
        case []:
            return [[]]
        case [x, *xs]:
            return [[]] + apply(lambda _: [x] + _)(inits(xs))


def flatten(xss: list[list[X]]) -> list[X]:
    '''
    Flattens a list of lists.

    Example:
        In [1]: flatten([[1], [2, 3], [4, 5, 6]])
        Out[1]: [1, 2, 3, 4, 5, 6]
    
    Complexity: O(n**2).
    ''' 
    return [x for xs in xss for x in xs]


def head(xs: list[X]) -> X:
    assert xs != [], "The head function only works on non-empty lists (so please provide one)."
    return xs[0]


def accumulate_from_right(f: Callable[[Tuple[X, Y]], Y], e: Y) -> Callable[[list[X]], list[Y]]:
    '''
    Returns the right-accumulation of a function f and starter element e.

    Definition:
        - [] list case: accumulate_from_right(f, e)([]) = [e]
        - General case: accumulate_from_right(f, e)([x, y]) = [f(x, f(y, e)), f(y, e), e]
    '''
    def uncurried_accumulate_from_right(
        f: Callable[[Tuple[X, Y]], Y],
        e: Y,
        xs: list[X]
    ) -> list[Y]:
        match xs:
            case []:
                return [e]
            case [x, *tail]:
                ys = uncurried_accumulate_from_right(f=f, e=e, xs=tail)
                return [f(x, head(ys))] + ys
    
    return lambda xs: uncurried_accumulate_from_right(f, e, xs)
            

def relu_sum(x: int, y: int) -> int:
    '''
    The ReLU (Rectified Linear Unit) function is the most-famous Deep Learning function and it is
    defined by ReLU(x) = max(0, x); so here is the ReLU_sum function.
    '''
    return max(0, x+y)


####################################################
# Bonus: Left- and right-folds + left-accumulation #
####################################################

def fold_from_left(f: Callable[[Tuple[Y, X]], Y], e: Y) -> Callable[[list[X]], Y]:
    '''
    Returns the left-fold of a function f and starter element e.

    Definition:
        - [] list case: fold_from_left(f, e)([]) = e
        - General case: fold_from_left(f, e)([x, y]) = f(f(e, x), y)
    '''
    def uncurried_fold_from_left(
        f: Callable[[Tuple[Y, X]], Y],
        e: Y,
        xs: list[X]
    ) -> Y:
        match xs:
            case []:
                return e
            case [x, *tail]:
                return uncurried_fold_from_left(f=f, e=f(e, x), xs=tail)

    return lambda xs: uncurried_fold_from_left(f, e, xs)


def fold_from_right(f: Callable[[Tuple[X, Y]], Y], e: Y) -> Callable[[list[X]], Y]:
    '''
    Returns the right-fold of a function f and starter element e.

    Definition:
        - [] list case: fold_from_right(f, e)([]) = e
        - General case: fold_from_right(f, e)([x, y]) = f(x, f(y, e))
    '''
    def uncurried_fold_from_right(
        f: Callable[[Tuple[X, Y]], Y],
        e: Y,
        xs: list[X]
    ) -> Y:
        match xs:
            case []:
                return e
            case [x, *tail]:
                return f(x, uncurried_fold_from_right(f=f, e=e, xs=tail))

    return lambda xs: uncurried_fold_from_right(f, e, xs)


def accumulate_from_left(f: Callable[[Tuple[Y, X]], Y], e: Y) -> Callable[[list[X]], list[Y]]:
    '''
    Returns the left-accumulation of a function f and starter element e.

        Definition:
        - [] list case: accumulate_from_left(f, e)([]) = [e]
        - General case: accumulate_from_left(f, e)([x, y]) = [e, f(e, x), f(f(e, x), y)]
    '''
    def uncurried_accumulate_from_left(
        f: Callable[[Tuple[Y, X]], Y],
        e: Y,
        xs: list[X]
    ) -> list[Y]:
        match xs:
            case []:
                return [e]
            case [x, *tail]:
                return [e] + uncurried_accumulate_from_left(f=f, e=f(e, x), xs=tail)
    
    return lambda xs: uncurried_accumulate_from_left(f, e, xs)
