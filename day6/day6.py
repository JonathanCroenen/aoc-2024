from __future__ import annotations
from enum import Enum
import time
from copy import deepcopy


Map = list[list[str]]
Pos = tuple[int, int]


class Dir(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

    @staticmethod
    def from_char(char: str) -> Dir | None:
        match char:
            case "<":
                return Dir.LEFT
            case ">":
                return Dir.RIGHT
            case "^":
                return Dir.UP
            case "v":
                return Dir.DOWN

        return None

    def to_char(self) -> str:
        match self:
            case Dir.LEFT:
                return "<"
            case Dir.RIGHT:
                return ">"
            case Dir.UP:
                return "^"
            case Dir.DOWN:
                return "v"

    def next(self) -> Dir:
        match self:
            case Dir.LEFT:
                return Dir.UP
            case Dir.UP:
                return Dir.RIGHT
            case Dir.RIGHT:
                return Dir.DOWN
            case Dir.DOWN:
                return Dir.LEFT




def parse_input(path: str) -> tuple[Map, Pos, Dir]:
    with open(path, "r") as f:
        data = f.read().splitlines()
        data = [[char for char in line] for line in data]

        for y in range(len(data)):
            for x in range(len(data[y])):
                dir = Dir.from_char(data[y][x])
                if dir is not None:
                    data[y][x] = "."
                    return data, (x, y), dir

        raise RuntimeError("No starting position found")


def print_map(map: Map, p: Pos, d: Dir):
    print("\033[H\033[J")
 
    for y in range(len(map)):
        for x in range(len(map[y])):
            if (x, y) == p:
                print(d.to_char(), end="")
            else:
                print(map[y][x], end="")

        print()


def is_out_of_bounds(x: int, y: int, width: int, height: int) -> bool:
    return y < 0 or y >= height or x < 0 or x >= width


def step(map: Map, p: Pos, d: Dir) -> tuple[Pos, Dir, bool]:
    width, height = len(map[0]), len(map)

    x, y = p
    dx, dy = d.value

    if is_out_of_bounds(x + dx, y + dy, width, height):
        return p, d, False

    if map[y + dy][x + dx] == "#":
        # d = d.next()
        # dx, dy = d.value
        return p, d.next(), True
    else:
        return (x + dx, y + dy), d, True
    
    # return (x + dx, y + dy), d, True


def part1(map: Map, p0: Pos, d0: Dir, animate: bool) -> int:
    p = p0
    d = d0

    visited = set()
    while True:
        if animate:
            print_map(map, p, d)
            time.sleep(0.2)

        visited.add(p)
        p, d, cont = step(map, p, d)
        if not cont:
            break

    return len(visited)

def can_place_obstacle_in_front(map: Map, p0: Pos, p: Pos, d: Dir) -> bool:
    width, height = len(map[0]), len(map)
    x, y = p
    dx, dy = d.value

    if is_out_of_bounds(x + dx, y + dy, width, height):
        return False

    if map[y + dy][x + dx] == "#":
        return False

    if (x + dx, y + dy) == p0:
        return False

    return True


def part2(map: Map, p0: Pos, d0: Dir, animate: bool) -> int:
    p = p0
    d = d0

    visited = {}
    total = 0
    while True:
        if animate:
            print_map(map, p, d)
            time.sleep(0.2)

        if can_place_obstacle_in_front(map, p0, p, d):
            visited2 = deepcopy(visited)
            visited2.setdefault(p, set()).add(d)
            map2 = deepcopy(map)

            x, y = p
            dx, dy = d.value
            map2[y + dy][x + dx] = "#"
            q, e = p, d.next()

            while True:
                if q in visited2 and e in visited2[q]:
                    if animate:
                        input(f"option found: ({p[0] + d.value[0]}, {p[1] + d.value[1]})")

                    total += 1
                    break


                _q, _e, cont = step(map2, q, e)
                if _e != e:
                    visited2.setdefault(q, set()).update((e, _e))
                q, e = _q, _e

                if not cont:
                    break

        _p, _d, cont = step(map, p, d)
        if _d != d:
            visited.setdefault(p, set()).update((d, _d))
        p, d = _p, _d

        if not cont:
            break

    return total


def main():
    map, p0, d0 = parse_input("input.txt")

    total = part1(map, p0, d0, animate=False)
    print("part 1:", total)

    total = part2(map, p0, d0, animate=False)
    print("part 2:", total)



if __name__ == "__main__":
    main()

