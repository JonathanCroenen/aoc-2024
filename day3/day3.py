import re


def load_input(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def part1(mem: str) -> int:
    regex = re.compile(r"mul\((\d+),(\d+)\)")
    matches = regex.findall(mem)

    total = 0
    for a, b in matches:
        total += int(a) * int(b)

    return total



def part2(mem: str) -> int:
    regex = re.compile(r"mul\((\d+),(\d+)\)|(do)\(\)|(don)'t\(\)")
    matches = regex.findall(mem)

    total = 0
    enabled = True
    for a, b, do, dont in matches:
        if do:
            enabled = True
        elif dont:
            enabled = False
        elif a and b and enabled:
            total += int(a) * int(b)

    return total


def main():
    mem = load_input("input.txt")

    result = part1(mem)
    print("part 1:", result)

    result = part2(mem)
    print("part 2:", result)


if __name__ == "__main__":
    main()

