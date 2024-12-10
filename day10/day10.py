import sys

Map = list[list[int]]


def parse_input(input: str) -> Map:
    return [[int(x) for x in line] for line in input.splitlines()]


def is_in_bounds(map: Map, x: int, y: int) -> bool:
    return 0 <= y < len(map) and 0 <= x < len(map[y])


def step(map: Map, x: int, y: int, reached: set) -> int:
    current_height = map[y][x]
    if current_height == 9:
        if (x, y) in reached:
            return 0

        reached.add((x, y))
        return 1

    total = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if is_in_bounds(map, nx, ny) and map[ny][nx] == current_height + 1:
            total += step(map, nx, ny, reached)

    return total


def part1(map: Map) -> int:
    score = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 0:
                score += step(map, x, y, set())

    return score


def step2(map: Map, x: int, y: int) -> int:
    current_height = map[y][x]
    if current_height == 9:
        return 1

    total = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if is_in_bounds(map, nx, ny) and map[ny][nx] == current_height + 1:
            total += step2(map, nx, ny)

    return total


def part2(map: Map) -> int:
    score = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 0:
                score += step2(map, x, y)

    return score


def main():
    map = parse_input(sys.stdin.read())

    result = part1(map)
    print("part 1:", result)

    result = part2(map)
    print("part 2:", result)


if __name__ == "__main__":
    main()
