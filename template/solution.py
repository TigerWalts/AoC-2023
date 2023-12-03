from io import TextIOWrapper
from os import path

FOLDER = path.dirname(__file__)
INPUT_EXAMPLE = path.join(FOLDER, 'input_example.txt')
INPUT = path.join(FOLDER, 'input.txt')

def iter_line(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()

def main(filename: str):
    with open(filename, 'r') as input_file:
        ...

if __name__ == '__main__':
    test_result = main(INPUT_EXAMPLE)
    assert test_result == 0, f"Test Failed! got {test_result}"
    print(main(INPUT))