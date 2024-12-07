from enum import Enum

Input = list[list[str]]


def load_input(path: str) -> Input:
    with open(path, 'r') as f:
        data = f.read().splitlines()
        data = [[x for x in line] for line in data]

    return data

class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_LEFT = (-1, 1)
    DOWN_RIGHT = (1, 1)


def search_word(input: Input, word: str, x0: int, y0: int, direction: Direction) -> bool:
    x, y = x0, y0

    for char in word:
        if y < 0 or y >= len(input) or x < 0 or x >= len(input[y]):
            return False

        if input[y][x] != char:
            return False

        x += direction.value[0]
        y += direction.value[1]

    return True



def part1(input: Input) -> int:
    total = 0
    for y in range(len(input)):
        for x in range(len(input[y])):
            for direction in Direction:
                if search_word(input, "XMAS", x, y, direction):
                    total += 1

    return total


def extract_pattern(input: Input, mask: list[list[bool]], x0: int, y0: int) -> list[str]:
    result = []
    for j, row in enumerate(mask):
        for i, value in enumerate(row):
            x, y = x0 + i, y0 + j

            if y < 0 or y >= len(input) or x < 0 or x >= len(input[y]):
                break

            if value:
                result.append(input[y][x])

    return result



def part2(input: Input) -> int:
    mask = [[True, False, True], [False, True, False], [True, False, True]]

    total = 0
    for y in range(len(input)):
        for x in range(len(input[y])):
            values = extract_pattern(input, mask, x, y)
            if len(values) != 5:
                continue
            
            diag1 = values[0] + values[2] + values[4]
            diag2 = values[1] + values[2] + values[3]

            if (diag1 == "MAS" or diag1 == "SAM") and (diag2 == "MAS" or diag2 == "SAM"):
                total += 1

    return total



def main():
    input = load_input("input.txt")

    total = part1(input)
    print("part 1:", total)

    total = part2(input)
    print("part 2:", total)

if __name__ == "__main__":
    main()


