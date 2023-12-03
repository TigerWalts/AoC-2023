from collections import Counter
from functools import reduce
from io import TextIOWrapper
from operator import mul, or_
from os import path

FOLDER = path.dirname(__file__)
INPUT_EXAMPLE = path.join(FOLDER, "input_example.txt")
INPUT = path.join(FOLDER, "input.txt")


def iter_line(file_object: TextIOWrapper):
    for line in file_object.readlines():
        yield line.strip()


def part_1(input_file: TextIOWrapper) -> int:
    input_file.seek(0)
    legal_cubes = {"red": 12, "green": 13, "blue": 14}
    return sum(
        mul(*pair)
        for pair in enumerate(
            (
                all(
                    int(count) <= legal_cubes[colour]
                    for count, _, colour in (
                        cr.partition(" ")
                        for cr in (
                            line.partition(": ")[-1].replace("; ", ", ").split(", ")
                        )
                    )
                )
                for line in iter_line(input_file)
            ),
            1,
        )
    )


def part_2(input_file: TextIOWrapper) -> int:
    input_file.seek(0)
    return sum(
        reduce(
            mul,
            reduce(
                or_,
                (
                    Counter({colour: int(count)})
                    for count, _, colour in (
                        cr.partition(" ")
                        for cr in (
                            line.partition(": ")[-1].replace("; ", ", ").split(", ")
                        )
                    )
                ),
            ).values(),
        )
        for line in iter_line(input_file)
    )


def main():
    with open(INPUT_EXAMPLE) as input_example_fd, open(INPUT) as input_fd:
        test_result = part_1(input_example_fd)
        assert test_result == 8, f"Test Failed! got {test_result}"
        print(part_1(input_fd))

        test_result = part_2(input_example_fd)
        assert test_result == 2286, f"Test Failed! got {test_result}"
        print(part_2(input_fd))


if __name__ == "__main__":
    main()
