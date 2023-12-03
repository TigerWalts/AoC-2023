from collections import Counter
from functools import reduce
from io import TextIOWrapper
from operator import mul
from os import path
from typing import Dict, Tuple

FOLDER = path.dirname(__file__)
INPUT_EXAMPLE = path.join(FOLDER, "input_example.txt")
INPUT = path.join(FOLDER, "input.txt")


def iter_line(file_object: TextIOWrapper):
    for line in file_object:
        yield line.strip()


def is_legal(game_result: str, dice_counts: Dict[str, int]) -> bool:
    return all(
        dice_counts[colour] >= int(count)
        for count, _, colour in (
            dice_result.partition(" ") for dice_result in game_result.split(", ")
        )
    )


def product_of_min_dice(game_results: str):
    no_dice = {colour: 0 for colour in ("red", "green", "blue")}
    return reduce(
        mul,
        reduce(
            lambda a, x: {k: max(v, x[k]) for k, v in a.items()},
            (
                Counter(no_dice)
                + Counter(
                    {
                        colour: int(count)
                        for count, _, colour in (
                            dice_result.partition(" ")
                            for dice_result in game_result.split(", ")
                        )
                    }
                )
                for game_result in game_results.split("; ")
            ),
            Counter(no_dice),
        ).values(),
    )


def main(filename: str, legal_cubes_rgb: Tuple[int, int, int]):
    dice_counts = {k: v for k, v in zip(("red", "green", "blue"), legal_cubes_rgb)}
    with open(filename, "r") as input_file:
        return sum(
            int(game.split(" ")[-1])
            for game, _, game_results in (
                line.partition(": ") for line in iter_line(input_file)
            )
            if all(
                is_legal(game_result, dice_counts)
                for game_result in game_results.split("; ")
            )
        )


def main2(filename: str):
    with open(filename, "r") as input_file:
        return sum(
            product_of_min_dice(game_results)
            for game_results in (line.split(": ")[-1] for line in iter_line(input_file))
        )


if __name__ == "__main__":
    legal_cubes_rgb = (12, 13, 14)
    test_result = main(INPUT_EXAMPLE, legal_cubes_rgb)
    assert test_result == 8, f"Test Failed! got {test_result}"
    print(main(INPUT, legal_cubes_rgb))

    test_result = main2(INPUT_EXAMPLE)
    assert test_result == 2286, f"Test Failed! got {test_result}"
    print(main2(INPUT))
