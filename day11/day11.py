import sys
import math


def parse_input(input: str) -> list[int]:
    return [int(x) for x in input.strip().split(" ")]


def blink(input: list[int], n: int) -> int:
    stones = {}
    for stone in input:
        stones[stone] = stones.get(stone, 0) + 1

    for _ in range(n):
        new_stones = {}
        for stone, count in stones.items():
            if stone == 0:
                new_stones[stone + 1] = new_stones.get(stone + 1, 0) + count
            elif (n := int(math.log10(stone))) % 2 == 1:
                n += 1
                stone1 = stone // (10 ** (n // 2))
                stone2 = stone - stone1 * (10 ** (n // 2))

                new_stones[stone1] = new_stones.get(stone1, 0) + count
                new_stones[stone2] = new_stones.get(stone2, 0) + count 
            else:
                new_stones[stone * 2024] = new_stones.get(stone * 2024, 0) + count

        stones = new_stones

    return sum(stones.values())


def part1(input: list[int]) -> int:
    return blink(input, 25)

def part2(input: list[int]) -> int:
    return blink(input, 75)


def main():
    input = parse_input(sys.stdin.read())

    result = part1(input)
    print("part 1:", result)

    result = part2(input)
    print("part 2:", result)


if __name__ == "__main__":
    main()
