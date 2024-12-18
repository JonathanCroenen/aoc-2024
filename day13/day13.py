import sys
from dataclasses import dataclass, replace


@dataclass
class Machine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]

    goal: tuple[int, int]


def parse_input(input: str) -> list[Machine]:
    machines = []
    for block in input.split("\n\n"):
        lines = block.splitlines()

        buttons = []
        for line in lines[:2]:
            x_str, y_str = line.split(": ")[1].split(", ")
            x = int(x_str.split("+")[1])
            y = int(y_str.split("+")[1])
            buttons.append((x, y))

        x_str, y_str = lines[-1].split(": ")[1].split(", ")
        x = int(x_str.split("=")[1])
        y = int(y_str.split("=")[1])

        machines.append(Machine(buttons[0], buttons[1], (x, y)))

    return machines


def solve(machine: Machine) -> tuple[bool, int, int]:
    x1 = machine.button_a[0]
    x2 = machine.button_b[0]
    y1 = machine.button_a[1]
    y2 = machine.button_b[1]
    xg = machine.goal[0]
    yg = machine.goal[1]

    b = (yg * x1 - xg * y1) / (y2 * x1 - y1 * x2)
    a = (xg - b * x2) / x1
    return int(a) == a and int(b) == b, int(a), int(b)


def part1(machines: list[Machine]) -> int:
    total = 0
    for machine in machines:
        success, a, b = solve(machine)
        cost = 3 * a + b
        if success:
            total += cost

    return total


def part2(machines: list[Machine]) -> int:
    total = 0
    for machine in machines:
        machine = replace(
            machine,
            goal=(
                10000000000000 + machine.goal[0],
                10000000000000 + machine.goal[1],
            ),
        )
        success, a, b = solve(machine)
        cost = 3 * a + b
        if success:
            total += cost

    return total


def main():
    input = parse_input(sys.stdin.read())

    result = part1(input)
    print("part 1:", result)

    result = part2(input)
    print("part 2:", result)


if __name__ == "__main__":
    main()
