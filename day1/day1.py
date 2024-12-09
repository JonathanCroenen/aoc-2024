import sys


def parse_input(input: str) -> tuple[list[int], list[int]]:
    data = input.splitlines()
    data = [[int(x) for x in line.split("   ")] for line in data]
    
    column1, column2 = zip(*data)
    column1 = sorted(column1)
    column2 = sorted(column2)

    return column1, column2

def distance(x1: int, x2: int) -> int:
    return abs(x1 - x2)



def main():
    column1, column2 = parse_input(sys.stdin.read())

    total = 0
    for x, y in zip(column1, column2):
        total += distance(x, y)
        
    print("part 1:", total)

    lookup = {}
    for x in column2:
        lookup[x] = lookup.get(x, 0) + 1

    total = 0
    for x in column1:
        total += lookup.get(x, 0) * x

    print("part 2:", total)

if __name__ == "__main__":
    main()

