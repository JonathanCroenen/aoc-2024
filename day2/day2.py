
Input = list[list[int]]


def parse_input(path: str) -> Input:
    with open(path, "r") as f:
        data = f.readlines()
        data = [[int(x) for x in line.split()] for line in data]

    return data

def is_safe(a: int, b: int, is_ascending: bool) -> bool:
    if is_ascending and a > b:
        return False

    if not is_ascending and a < b:
        return False

    diff = abs(a - b)
    if diff > 3 or diff < 1:
        return False

    return True


def check_report(report: list[int], is_ascending: bool) -> tuple[bool, int]:
    for i, (a, b) in enumerate(zip(report[:-1], report[1:])):
        if not is_safe(a, b, is_ascending):
            return False, i
    
    return True, -1

def part1(data: Input) -> int:
    total = 0
    for report in data:
        is_ascending = report[0] < report[1]
        if check_report(report, is_ascending)[0]:
            total += 1

    return total

    


def part2(data: Input) -> int:
    total = 0
    for report in data:
        is_ascending = report[0] < report[1]
        _is_safe, fail_index = check_report(report, is_ascending)
        if _is_safe or fail_index == len(report) - 2:
            total += 1
            continue

        if fail_index == 0 or fail_index == 1:
            is_ascending = report[1] < report[2]
            if check_report(report[1:], is_ascending)[0]:
                total += 1
                continue

            is_ascending = report[0] < report[2]
            if check_report([report[0]] + report[:2], is_ascending)[0]:
                total += 1
                continue

        if check_report(report[:fail_index] + report[fail_index+1:], is_ascending)[0]:
            total += 1
            continue

        if check_report(report[:fail_index+1] + report[fail_index+2:], is_ascending)[0]:
            total += 1
            continue

    return total

def main():
    data = parse_input("input.txt")

    total = part1(data)
    print("part 1:", total)

    total = part2(data)
    print("part 2:", total)


if __name__ == "__main__":
    main()
