from io import TextIOWrapper
from itertools import chain
from os import path
from functools import cmp_to_key

FOLDER = path.dirname(__file__)
INPUT_EXAMPLE = path.join(FOLDER, "input_example.txt")
INPUT_EXAMPLE_2 = path.join(FOLDER, "input_example_2.txt")
INPUT = path.join(FOLDER, "input.txt")

NUM_WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)

NUM_WORDS_REVERSED = tuple("".join(reversed(x)) for x in NUM_WORDS)

NUMS = tuple(str(n) for n in range(10))


def iter_line(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()


def first_num(input: str, rev=False) -> int:
    return sorted(
        (
            (i, value)
            for i, value in (
                (("".join(reversed(input)) if rev else input).find(search), val)
                for val, search in chain(
                    enumerate(NUM_WORDS_REVERSED if rev else NUM_WORDS), enumerate(NUMS)
                )
            )
            if i > -1
        ),
        key=cmp_to_key(lambda a, b: a[0] - b[0]),
    )[0][1]


def main(filename: str):
    with open(filename, "r") as input_file:
        return sum(
            (
                10 * int(next(c for c in line if c.isnumeric()))
                + int(next(c for c in reversed(line) if c.isnumeric()))
            )
            for line in iter_line(input_file)
        )


def main2(filename: str):
    with open(filename, "r") as input_file:
        return sum(
            10 * first_num(line) + first_num(line, rev=True)
            for line in iter_line(input_file)
        )


if __name__ == "__main__":
    test_result = main(INPUT_EXAMPLE)
    assert test_result == 142, f"Test Failed! got {test_result}"
    print(main(INPUT))

    test_result = main2(INPUT_EXAMPLE_2)
    assert test_result == 281, f"Test Failed! got {test_result}"
    print(main2(INPUT))
