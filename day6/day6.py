from __future__ import annotations
import sys
from enum import Enum
import time


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




def parse_input(input: str) -> tuple[Map, Pos, Dir]:
    data = input.splitlines()
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


def simulate(map: Map, p0: Pos, d0: Dir, animate: bool) -> set:
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

    return visited


def part1(map: Map, p0: Pos, d0: Dir, animate: bool) -> int:
    return len(simulate(map, p0, d0, animate))


def part2(map: Map, p0: Pos, d0: Dir) -> int:
    orig_ps = simulate(map, p0, d0, False)
    orig_ps.remove(p0)

    result = 0
    prev_obst = None
    for obst_x, obst_y in orig_ps:
        if prev_obst is not None:
            prev_x, prev_y = prev_obst
            map[prev_y][prev_x] = "."

        map[obst_y][obst_x] = "#"
        prev_obst = (obst_x, obst_y)

        p, d = p0, d0
        visited = set()
        while True:
            visited.add((p, d))
            p, d, cont = step(map, p, d)
            if not cont:
                break

            if (p, d) in visited:
                result += 1
                break

    return result



def main():
    map, p0, d0 = parse_input(sys.stdin.read())

    total = part1(map, p0, d0, animate=False)
    print("part 1:", total)

    total = part2(map, p0, d0)
    print("part 2:", total)



if __name__ == "__main__":
    main()

