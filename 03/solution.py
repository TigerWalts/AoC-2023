from io import TextIOWrapper
from operator import and_, or_
from os import path
from typing import Callable, Sequence

FOLDER = path.dirname(__file__)
INPUT_EXAMPLE = path.join(FOLDER, "input_example.txt")
INPUT = path.join(FOLDER, "input.txt")


def iter_line(file_object: TextIOWrapper):
    for line in file_object.readlines():
        yield line.strip()


def conv_3[T, U](seq: Sequence[T], fill: T, func: Callable[[T, T], U]) -> Sequence[U]:
    gen = (x for x in seq)
    first = fill
    try:
        second = next(gen)
    except StopIteration:
        second = fill
    try:
        third = next(gen)
    except StopIteration:
        third = fill
    yield func(second, third)
    for incoming in gen:
        first = second
        second = third
        third = incoming
        yield func(func(first, second), third)
    yield func(func(fill, second), third)


def linear_or[T](a: Sequence[T], b: Sequence[T]) -> Sequence[T]:
    return (or_(*pair) for pair in zip(a, b))


def sum_line_nums(line, num_row, comb_row) -> int:
    acc = 0
    num = ""
    in_sym = False
    for char, n, c in zip(line, num_row, comb_row):
        if not n and num:
            if in_sym:
                acc += int(num)
            num = ""
            in_sym = False
        if n:
            num += char
        if c:
            in_sym = True
    if num and in_sym:
        acc += int(num)
    return acc


def part_1(input_file: TextIOWrapper) -> int:
    input_file.seek(0)
    stride = len(input_file.readline().strip())

    input_file.seek(0)
    number_mask = [[c.isnumeric() for c in line] for line in iter_line(input_file)]

    input_file.seek(0)
    symbol_mask = list(
        conv_3(
            (
                list(conv_3((not c.isnumeric() and c != "." for c in line), False, or_))
                for line in iter_line(input_file)
            ),
            [False for _ in range(stride)],
            linear_or,
        )
    )

    combined_mask = [
        [and_(*pair) for pair in zip(*row_pair)]
        for row_pair in zip(number_mask, symbol_mask)
    ]

    input_file.seek(0)
    return sum(
        sum_line_nums(line, num_row, comb_row)
        for line, num_row, comb_row in zip(
            iter_line(input_file), number_mask, combined_mask
        )
        if any(comb_row)
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
