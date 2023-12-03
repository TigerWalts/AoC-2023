from io import TextIOWrapper
from os import path

FOLDER = path.dirname(__file__)
INPUT_EXAMPLE = path.join(FOLDER, "input_example.txt")
INPUT = path.join(FOLDER, "input.txt")


def iter_line(file_object: TextIOWrapper):
    for line in file_object.readlines():
        yield line.strip()


def part_1(input_file: TextIOWrapper) -> int:
    input_file.seek(0)
    return sum(1 for _ in iter_line(input_file))


def part_2(input_file: TextIOWrapper) -> int:
    input_file.seek(0)
    return sum(1 for _ in iter_line(input_file))


def main():
    with open(INPUT_EXAMPLE) as input_example_fd, open(INPUT) as input_fd:
        test_result = part_1(input_example_fd)
        assert test_result == 0, f"Test Failed! got {test_result}"
        print(part_1(input_fd))

        test_result = part_2(input_example_fd)
        assert test_result == 0, f"Test Failed! got {test_result}"
        print(part_2(input_fd))


if __name__ == "__main__":
    main()
