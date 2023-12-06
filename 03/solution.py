from collections import deque
from io import TextIOWrapper
from itertools import chain, islice
from os import path
from typing import Callable, Iterator, Sequence, Tuple

FOLDER = path.dirname(__file__)
INPUT_EXAMPLE = path.join(FOLDER, "input_example.txt")
INPUT = path.join(FOLDER, "input.txt")


def iter_line(file_object: TextIOWrapper):
    for line in file_object.readlines():
        yield line.strip()


# https://docs.python.org/3/library/itertools.html#itertools-recipes
def sliding_window(iterable, n):
    it = iter(iterable)
    window = deque(islice(it, n - 1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)


def conv_3_3[T, U](
    seq: Sequence[Sequence[T]],
    fill: Sequence[T],
    func: Callable[[Tuple[Tuple[T, T, T], Tuple[T, T, T], Tuple[T, T, T]]], U],
) -> Iterator[Iterator[U]]:
    fill_ = fill[0:1]
    for first, second, third in sliding_window(chain([fill], seq, [fill]), 3):
        yield (
            func(x)
            for x in zip(
                sliding_window(chain(fill_, first, fill_), 3),
                sliding_window(chain(fill_, second, fill_), 3),
                sliding_window(chain(fill_, third, fill_), 3),
            )
        )


Lens = Tuple[Tuple[str, str, str], Tuple[str, str, str], Tuple[str, str, str]]


def part_1_conv(lens: Lens) -> Tuple[str, int]:
    """Takes a 3x3 tuple of characters and returns a tuple of the center character
    with a mask of:
        0   -   Not a digit
        1   -   Digit but no symbols
        2   -   Digit with a symbol"""
    char = lens[1][1]
    is_num = 1 if char.isnumeric() else 0
    return (
        char,
        is_num * 2
        if any(any((not x.isnumeric() and x != ".") for x in y) for y in lens)
        else is_num,
    )


def nums_from_line_mask(line_mask: Sequence[Tuple[str, int]]) -> Iterator[int]:
    acc = ""
    sym = False
    for char, mask in line_mask:
        if mask == 0:
            if acc and sym:
                yield int(acc)
            acc = ""
            sym = False
        else:
            acc += char
        sym |= mask > 1
    if acc and sym:
        yield int(acc)


def part_1(input_file: TextIOWrapper) -> int:
    input_file.seek(0)
    stride = len(input_file.readline().strip())
    input_file.seek(0)
    return sum(
        sum(nums_from_line_mask(line_mask))
        for line_mask in conv_3_3(iter_line(input_file), "." * stride, part_1_conv)
    )


def part_2(input_file: TextIOWrapper) -> int:
    input_file.seek(0)
    return sum(1 for _ in iter_line(input_file))


def main():
    with open(INPUT_EXAMPLE) as input_example_fd, open(INPUT) as input_fd:
        test_result = part_1(input_example_fd)
        assert test_result == 4361, f"Test Failed! got {test_result}"
        print(part_1(input_fd))

        # test_result = part_2(input_example_fd)
        # assert test_result == 0, f"Test Failed! got {test_result}"
        # print(part_2(input_fd))


if __name__ == "__main__":
    main()
