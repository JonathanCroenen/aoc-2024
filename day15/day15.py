import sys
import time
from copy import deepcopy

Map = list[list[str]]
Moves = str
Pos = tuple[int, int]


def parse_input(input: str) -> tuple[Map, Moves, Pos]:
    map, moves = input.strip().split("\n\n")
    map = [list(row) for row in map.split("\n")]
    start = (0, 0)
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "@":
                start = (x, y)

    moves = moves.replace("\n", "")

    return map, moves, start


def print_map(map: Map):
    for row in map:
        print("".join(row))


def check_move(map: Map, pos: Pos, dp: Pos) -> bool:
    x, y = pos
    dx, dy = dp
    height, width = len(map), len(map[0])
    while True:
        x, y = x + dx, y + dy
        if 0 > x >= width and 0 > y >= height:
            return False

        if map[y][x] == "#":
            return False

        if map[y][x] == ".":
            return True


def move_and_push(map: Map, x: int, y: int, dx: int, dy: int):
    if map[y][x] == ".":
        map[y][x] = map[y - dy][x - dx]
        return

    move_and_push(map, x + dx, y + dy, dx, dy)
    map[y][x] = map[y - dy][x - dx]


def make_move(map: Map, pos: Pos, dp: Pos) -> Pos:
    if not check_move(map, pos, dp):
        return pos

    x, y = pos
    dx, dy = dp
    move_and_push(map, x + dx, y + dy, dx, dy)
    map[y][x] = "."
    return x + dx, y + dy


def part1(map: Map, moves: Moves, start: Pos, visualize=False) -> int:
    map = deepcopy(map)
    pos = start
    for move in moves:
        if visualize:
            print_map(map)
            print(move)
        match move:
            case "<":
                pos = make_move(map, pos, (-1, 0))
            case ">":
                pos = make_move(map, pos, (1, 0))
            case "^":
                pos = make_move(map, pos, (0, -1))
            case "v":
                pos = make_move(map, pos, (0, 1))

    if visualize:
        print_map(map)

    total = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "O":
                total += 100 * y + x

    return total


def widen_map(map: Map) -> Map:
    new_map = []
    for row in map:
        new_row = []
        new_map.append(new_row)
        for cell in row:
            if cell == "#":
                new_row.extend(("#", "#"))
            elif cell == "O":
                new_row.extend(("[", "]"))
            elif cell == ".":
                new_row.extend((".", "."))
            elif cell == "@":
                new_row.extend(("@", "."))

    return new_map


def check_move2(map: Map, pos: Pos, dp: Pos) -> bool:
    def check_vertical(x: int, y: int, dy: int) -> bool:
        if map[y][x] == ".":
            return True
        elif map[y][x] == "#":
            return False
        elif map[y][x] == "]":
            can_move = check_vertical(x, y + dy, dy)
            return can_move and check_vertical(x - 1, y + dy, dy)
        elif map[y][x] == "[":
            can_move = check_vertical(x, y + dy, dy)
            return can_move and check_vertical(x + 1, y + dy, dy)

        raise ValueError(f"invalid cell at {x}, {y}: '{map[y][x]}'")

    x, y = pos
    _, dy = dp
    if dy == 0:
        return check_move(map, pos, dp)
    else:
        return check_vertical(x, y + dy, dy)


def move_and_push2_vertical(map: Map, x: int, y: int, dy: int, handled: set):
    if (x, y) in handled:
        return

    handled.add((x, y))

    if map[y][x] == ".":
        map[y][x] = map[y - dy][x]
        map[y - dy][x] = "."
        return

    move_and_push2_vertical(map, x, y + dy, dy, handled)
    if map[y + dy][x] == "]":
        move_and_push2_vertical(map, x - 1, y + dy, dy, handled)
    if map[y + dy][x] == "[":
        move_and_push2_vertical(map, x + 1, y + dy, dy, handled)

    map[y][x] = map[y - dy][x]
    map[y - dy][x] = "."


def make_move2(map: Map, pos: Pos, dp: Pos) -> Pos:
    if not check_move2(map, pos, dp):
        return pos

    x, y = pos
    dx, dy = dp
    if dy == 0:
        move_and_push(map, x + dx, y + dy, dx, dy)
    else:
        move_and_push2_vertical(map, x, y + dy, dy, set())

    map[y][x] = "."
    return x + dx, y + dy


def part2(map: Map, moves: str, start: Pos, visualize=False) -> int:
    map = deepcopy(map)
    pos = start
    for move in moves:
        if visualize:
            print_map(map)
            print(move)

        match move:
            case "<":
                pos = make_move2(map, pos, (-1, 0))
            case ">":
                pos = make_move2(map, pos, (1, 0))
            case "^":
                pos = make_move2(map, pos, (0, -1))
            case "v":
                pos = make_move2(map, pos, (0, 1))

    if visualize:
        print_map(map)

    total = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "[":
                total += 100 * y + x

    return total


def main():
    map, moves, start = parse_input(sys.stdin.read())

    result = part1(map, moves, start, visualize=False)
    print("part 1:", result)

    result = part2(widen_map(map), moves, (start[0] * 2, start[1]), visualize=False)
    print("part 2:", result)


if __name__ == "__main__":
    main()
