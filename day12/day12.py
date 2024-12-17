import sys

Map = list[list[str]]


def parse_input(input: str) -> Map:
    return [[char for char in line] for line in input.splitlines()]


def is_in_bounds(map: Map, x: int, y: int) -> bool:
    return 0 <= x < len(map[0]) and 0 <= y < len(map)


def make_region(map: Map, x0: int, y0: int, consumed: set) -> set:
    region = {(x0, y0)}

    current_crop = map[y0][x0]
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x = x0 + dx
        y = y0 + dy

        if (
            is_in_bounds(map, x, y)
            and map[y][x] == current_crop
            and (x, y) not in consumed
        ):
            consumed.add((x, y))
            region.update(make_region(map, x, y, consumed))

    return region


def area(region: set) -> int:
    return len(region)


def is_edge(region: set, x: int, y: int) -> bool:
    return (x, y) not in region


def perimiter(map: Map, region: set) -> int:
    total = 0
    for x, y in region:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if is_edge(region, nx, ny):
                total += 1

    return total


def find_regions(map: Map) -> list[set]:
    regions = []
    consumed = set()
    for y in range(len(map)):
        for x in range(len(map[0])):
            if (x, y) not in consumed:
                consumed.add((x, y))
                regions.append(make_region(map, x, y, consumed))

    return regions


def part1(map: Map) -> int:
    regions = find_regions(map)

    result = 0
    for region in regions:
        result += area(region) * perimiter(map, region)

    return result


def perimiter2(map: Map, region: set) -> int:
    # n sides == n corners
    total = 0
    handled = set()
    directions = [
        ((-1, 0), (-1, -1), (0, -1)),
        ((0, -1), (1, -1), (1, 0)),
        ((1, 0), (1, 1), (0, 1)),
        ((0, 1), (-1, 1), (-1, 0)),
    ]
    for x, y in sorted(region):
        for (dx1, dy1), (dx2, dy2), (dx3, dy3) in directions:
            to_check = tuple(
                sorted(
                    (
                        (x, y),
                        (x + dx1, y + dy1),
                        (x + dx2, y + dy2),
                        (x + dx3, y + dy3),
                    )
                )
            )

            if to_check in handled:
                continue

            handled.add(to_check)

            this = is_edge(region, *to_check[0])
            neighbor1 = is_edge(region, *to_check[1])
            neighbor2 = is_edge(region, *to_check[2])
            neighbor3 = is_edge(region, *to_check[3])
            count = [this, neighbor1, neighbor2, neighbor3].count(True)

            if count % 2 == 1:
                total += 1
                continue

            diagonal = count == 2 and (
                (neighbor1 and neighbor2) or (this and neighbor3)
            )
            if diagonal:
                total += 2

    return total


def part2(map: Map) -> int:
    regions = find_regions(map)

    result = 0
    for region in regions:
        result += area(region) * perimiter2(map, region)

    return result


def main():
    map = parse_input(sys.stdin.read())

    result = part1(map)
    print("part 1:", result)

    result = part2(map)
    print("part 2:", result)


if __name__ == "__main__":
    main()
