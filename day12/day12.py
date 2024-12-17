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


def perimiter(map: Map, crop: str, region: set) -> int:
    total = 0
    for x, y in region:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if not is_in_bounds(map, nx, ny):
                total += 1
            elif map[ny][nx] != crop:
                total += 1

    return total


def find_regions(map: Map) -> list[set]:
    regions = []
    consumed = set()
    for y in range(len(map)):
        for x in range(len(map[0])):
            if (x, y) not in consumed:
                consumed.add((x, y))
                regions.append((map[y][x], make_region(map, x, y, consumed)))

    return regions


def part1(map: Map) -> int:
    regions = find_regions(map)

    result = 0
    for crop, region in regions:
        result += area(region) * perimiter(map, crop, region)

    return result


def perimiter2(map: Map, crop: str, region: set) -> int:
    total = 0

    py = -1
    is_fence = False
    for x, y in sorted(region):
        if py == -1:
            py = y

        if y != py and is_fence:
            total += 1
        py = y

        if not is_in_bounds(map, x, y - 1) or map[y - 1][x] != crop:
            if not is_fence:
                total += 1
            is_fence = True
        else:
            is_fence = False

    py = -1
    is_fence = False
    for x, y in sorted(region):
        if py == -1:
            py = y

        if y != py and is_fence:
            total += 1
        py = y

        if not is_in_bounds(map, x, y + 1) or map[y + 1][x] != crop:
            if not is_fence:
                total += 1
            is_fence = True
        else:
            is_fence = False

    px = -1
    is_fence = False
    for x, y in sorted(region, key=lambda x: (x[1], x[0])):
        if px == -1:
            px = x

        if x != px and is_fence:
            total += 1
        px = x

        if not is_in_bounds(map, x - 1, y) or map[y][x - 1] != crop:
            if not is_fence:
                total += 1
            is_fence = True
        else:
            is_fence = False

    px = -1
    is_fence = False
    for x, y in sorted(region, key=lambda x: (x[1], x[0])):
        if px == -1:
            px = x

        if x != px and is_fence:
            total += 1
        px = x

        if not is_in_bounds(map, x + 1, y) or map[y][x + 1] != crop:
            if not is_fence:
                total += 1
            is_fence = True
        else:
            is_fence = False

    return total


def part2(map: Map) -> int:
    regions = find_regions(map)

    result = 0
    for crop, region in regions:
        print(area(region), perimiter2(map, crop, region))
        result += area(region) * perimiter2(map, crop, region)

    return result


def main():
    map = parse_input(sys.stdin.read())

    result = part1(map)
    print("part 1:", result)

    result = part2(map)
    print("part 2:", result)


if __name__ == "__main__":
    main()
