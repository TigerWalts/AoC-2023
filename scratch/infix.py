from functools import reduce
from itertools import cycle, tee
from math import sqrt
from statistics import mean
from typing import Any, Callable, Iterable, Iterator, Optional, Self, Sequence, Tuple


class Enchain:
    def __init__(self, seq: Optional[Iterable] = None):
        self.input = seq
        self.genfuncs = []

    def __ror__(self, left: Any) -> Self:
        self.input = left
        return self

    def __or__(self, right: Callable) -> Self:
        self.genfuncs.append(right)
        return self
    
    def clone(self) -> Self:
        clone = Enchain()
        clone.genfuncs = list(self.genfuncs)
        return clone

    def __truediv__(self, right: Callable) -> Self:
        return right(reduce(lambda a, f: f(a), self.genfuncs, self.input))


def apply_each(func: Callable) -> Callable[[Sequence], Iterator]:
    return lambda seq: (func(it) for it in seq)


def filter_each(func: Callable) -> Callable[[Sequence], Iterator]:
    return lambda seq: filter(func, seq)


def zip_with(seq: Sequence, last=False) -> Callable[[Sequence], Iterator]:
    if last:
        return lambda other_seq: zip(other_seq, seq)
    return lambda other_seq: zip(seq, other_seq)


def str_join(glue=""):
    return lambda seq: glue.join(seq)


def debug(name, first=False, last=False, max_elements=None) -> Iterable:
    end = "\n" if last else " -> "
    print(name, end=end)
    prefix = "---\n" if first else ""
    w = len(name)

    def func(seq: Iterable):
        for i, it in enumerate(seq):
            if max_elements is None or i < max_elements:
                print(f"{prefix}{repr(it):<{w}}", end=end)
            yield it

    return func


def even_each(rev=False) -> Callable[[Sequence], Iterator]:
    return filter_each(lambda x: (x % 2 == 0) is not rev)


def pow_each(val: int | float) -> Callable[[Sequence], Iterator]:
    return apply_each(lambda x: x**val)


sum_of_squares_of_evens = (
    Enchain(range(1, 10000))
    # | debug("input", first=True, last=True)
    | even_each()
    # | debug("filtered")
    | pow_each(2)
    # | debug("squared", last=True)
) / sum

print(sum_of_squares_of_evens)
print()


def apply_on_each_tuple() -> Callable[[Sequence[Tuple]], Iterator]:
    """Applies the first value in a tuple as a function on the remaining values"""
    return apply_each(lambda it: it[0](*(it[1:])))


def apply_args_kwargs_each() -> Callable[[Sequence[Tuple]], Iterator]:
    return apply_each(lambda f, a, k: f(*a, **k))


alt_capped = (
    "If it compiles, it works!"
    | (
        Enchain()
        # | debug("input")
        | zip_with(cycle((str.upper, str.lower)))
        # | debug("zip")
        | apply_on_each_tuple()
        # | debug("case", last=True)
    )
) / str_join()

print(alt_capped)
print()


def sub_each(val: int | float) -> Callable[[Sequence], Iterator]:
    return apply_each(lambda x: x - val)


def std_dev(seq: Sequence) -> float:
    seq, seq_ = tee(seq)
    average = mean(seq_)
    return sqrt((Enchain(seq) | sub_each(average) | pow_each(2)) / mean)


print(std_dev(range(1, 200)))
