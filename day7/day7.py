import sys
from enum import Enum

Input = list[tuple[int, list[int]]]


class Op(Enum):
    ADD = 0
    MULT = 1
    CONCAT = 2


def parse_input(input: str) -> Input:
    data = input.splitlines()

    eqs = []
    for line in data:
        lhs, rhs = line.split(":")
        lhs = int(lhs)
        values = [int(v) for v in rhs.strip().split(" ")]

        eqs.append((lhs, values))

    return eqs
        
def solve(total: int, values: list[int], operators: list[Op]) -> tuple[list[Op], bool]:
    if len(operators) == len(values) - 1:
        result = values[0]
        for value, op in zip(values[1:], operators):
            match op:
                case Op.ADD:
                    result += value
                case Op.MULT:
                    result *= value

        return operators, result == total

    for op in [Op.ADD, Op.MULT]:
        ops = operators + [op]
        if solve(total, values, ops)[1]:
            return operators, True
    
    return [], False
            

def part1(input: Input) -> int:
    result = 0
    for total, values in input:
        _, solved = solve(total, values, [])
        if solved:
            result += total

    return result

def solve2(total: int, values: list[int], operators: list[Op]) -> tuple[list[Op], bool]:
    if len(operators) == len(values) - 1:
        result = values[0]
        for value, op in zip(values[1:], operators):
            match op:
                case Op.ADD:
                    result += value
                case Op.MULT:
                    result *= value
                case Op.CONCAT:
                    result = int(str(result) + str(value))

        return operators, result == total

    for op in Op:
        ops = operators + [op]
        if solve2(total, values, ops)[1]:
            return operators, True
    
    return [], False

def part2(input: Input) -> int:
    result = 0
    for total, values in input:
        _, solved = solve2(total, values, [])
        if solved:
            result += total

    return result


def main():
    input = parse_input(sys.stdin.read())

    result = part1(input)
    print("part 1:", result)
    
    result = part2(input)
    print("part 2:", result)


if __name__ == "__main__":
    main()
