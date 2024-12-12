import sys
from copy import deepcopy


Map = list[list[str]]


def parse_input(input: str) -> Map:
    return [[char for char in line] for line in input.splitlines()]


def print_map(map: Map):
    for line in map:
        print("".join(line))


def in_bounds(map: Map, x: int, y: int) -> bool:
    return 0 <= x < len(map[0]) and 0 <= y < len(map)


def is_free(map: Map, x: int, y: int) -> bool:
    return map[y][x] != "#"


def part1(map: Map) -> int:
    map = deepcopy(map)

    symbols = {}
    for y in range(len(map)):
        for x in range(len(map[y])):
            symbol = map[y][x]
            if symbol == ".":
                continue

            symbols.setdefault(symbol, []).append((x, y))

    total = 0
    for symbol, occurances in symbols.items():
        for i, (x1, y1) in enumerate(occurances):
            for x2, y2 in occurances[i + 1 :]:
                dx, dy = x2 - x1, y2 - y1

                antinode1 = (x2 + dx, y2 + dy)
                antinode2 = (x1 - dx, y1 - dy)

                if in_bounds(map, *antinode1) and is_free(map, *antinode1):
                    total += 1
                    map[antinode1[1]][antinode1[0]] = "#"

                if in_bounds(map, *antinode2) and is_free(map, *antinode2):
                    total += 1
                    map[antinode2[1]][antinode2[0]] = "#"

    return total


def part2(map: Map) -> int:
    map = deepcopy(map)

    symbols = {}
    for y in range(len(map)):
        for x in range(len(map[y])):
            symbol = map[y][x]
            if symbol == ".":
                continue

            symbols.setdefault(symbol, []).append((x, y))

    total = 0
    for symbol, occurances in symbols.items():
        for i, (x1, y1) in enumerate(occurances):
            for x2, y2 in occurances[i + 1 :]:
                dx, dy = x2 - x1, y2 - y1

                limit = max(len(map), len(map[0]))
                for d in [-1, 1]:
                    for i in range(limit):
                        antinode = (x2 + d * i * dx, y2 + d * i * dy)

                        if not in_bounds(map, *antinode):
                            break

                        if is_free(map, *antinode):
                            total += 1
                            map[antinode[1]][antinode[0]] = "#"

    return total


def main():
    map = parse_input(sys.stdin.read())

    result = part1(map)
    print("part 1:", result)

    result = part2(map)
    print("part 2:", result)


if __name__ == "__main__":
    main()
