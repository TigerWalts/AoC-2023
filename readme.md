# Advent of Code 2023

https://adventofcode.com/2023

## Insights & Learnings

### Day 2

#### Bitwise operators with Counters

Counters can be combined with a key-wise max using `|` .

```python
from collections import Counter

a = Counter({ "a": 1, "b": 2, "c": 4})
b = Counter({ "b": 9, "c": 3, "d": 1})

print(a | b)
print(a & b)
```

```console
Counter({'b': 9, 'c': 4, 'a': 1, 'd': 1})
Counter({'c': 3, 'b': 2})
```

The and operation only gives the intersecting keys. Which may not be desired, I couldn't find a way to do this without creating other data structures.

These operations can also be done in place with `|=` and `&=`

You can use these operations in `functools.reduce` by passing `operator.or_` or `Counter.__or__` as the first argument.

e.g. What characters do we need so that we can display any one of these film titles on our Cinema hording?

```python
from collections import Counter
from functools import reduce
from operator import or_

FILMS = [
    "Back to the future",
    "A View to a Kill",
    "Beverly Hills Cop",
    "Witness",
    "Amadeus",
    "The Terminator",
    "Cocoon",
    "Legend",
    "A Nightmare on Elm Street",
    "The Goonies"
]

print(
    "".join(
        sorted(
            reduce(
                or_,
                ( Counter(film) for film in FILMS )
            ).elements()
        )
    ).strip()
)
```

```console
ABCEGHKLNSTTVWacdeeefghiiklllmmnoooprrsstttuuvwy
```

In Python 3.12 the only difference between using `operator.or_` or `Counter.__or__` was that `or_` is loaded directly wheras `__or__` requires loading `Counter` and then loading the `__or__` attribute. A function passed to reduce is loaded only once, this will be the same for any itertools or functools function that accept another function, so use either.

#### No need to do any grouping by each handful of dice

When testing to see if there were too many dice or getting the most dice seen for a colour we didn't need to group by handful.

It would have been nice to split strings on multiple substrings `", "` and `"; `. The simplest workaround was to pre-process the string with a replace so they were all the same.

#### No need to parse and keep the Game number

This was a nice pattern to sum the game numbers that were legitimate:

```python
sum(mul(*pair) for pair in enumerate(<bool_sequence>, 1))
```
