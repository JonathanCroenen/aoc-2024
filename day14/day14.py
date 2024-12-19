import sys
from copy import deepcopy
from dataclasses import dataclass
import time

WIDTH = 101
HEIGHT = 103
# WIDTH = 11
# HEIGHT = 7


@dataclass
class Robot:
    x: int
    y: int

    vx: int
    vy: int


def parse_input(input: str) -> list[Robot]:
    robots = []
    lines = input.splitlines()
    for line in lines:
        pos, vel = line.split(" ")
        x, y = pos[2:].split(",")
        vx, vy = vel[2:].split(",")

        robots.append(Robot(int(x), int(y), int(vx), int(vy)))

    return robots


def print_grid(robots: list[Robot]):
    grid = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            count = sum(1 for robot in robots if robot.x == x and robot.y == y)
            row.append(str(count) if count > 0 else ".")

        grid.append(row)

    for row in grid:
        print("".join(row))


def step(robots: list[Robot]):
    for robot in robots:
        robot.x += robot.vx
        robot.y += robot.vy

        if robot.x >= WIDTH:
            robot.x -= WIDTH

        if robot.y >= HEIGHT:
            robot.y -= HEIGHT

        if robot.x < 0:
            robot.x += WIDTH

        if robot.y < 0:
            robot.y += HEIGHT


def part1(robots: list[Robot]) -> int:
    robots = deepcopy(robots)
    for _ in range(100):
        step(robots)

    quadrants = [[], [], [], []]
    for robot in robots:
        if robot.x < WIDTH // 2 and robot.y < HEIGHT // 2:
            quadrants[0].append(robot)
        elif robot.x > WIDTH // 2 and robot.y < HEIGHT // 2:
            quadrants[1].append(robot)
        elif robot.x < WIDTH // 2 and robot.y > HEIGHT // 2:
            quadrants[2].append(robot)
        elif robot.x > WIDTH // 2 and robot.y > HEIGHT // 2:
            quadrants[3].append(robot)

    counts = [len(q) for q in quadrants]
    return counts[0] * counts[1] * counts[2] * counts[3]


def part2(robots: list[Robot]) -> int:
    robots = deepcopy(robots)
    i = 0

    grid = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            row.append(0)
        grid.append(row)

    while True:
        i += 1
        # for _ in range(10):
        step(robots)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                grid[y][x] = 0

        for robot in robots:
            grid[robot.y][robot.x] = 1

        for y in range(HEIGHT):
            do_break = False
            for x in range(WIDTH):
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and grid[ny][nx] != 0:
                            count += 1

                if count >= 9:
                    do_break = True
                    print_grid(robots)
                    break
            if do_break:
                break

        print("step:", i)


def main():
    input = parse_input(sys.stdin.read())

    result = part1(input)
    print("part 1:", result)

    result = part2(input)
    print("part 2:", result)


if __name__ == "__main__":
    main()
