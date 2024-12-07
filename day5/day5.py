from copy import copy


RuleSet = dict[int, set[int]]
Update = list[int]
Input = tuple[RuleSet, list[Update]]


def parse_input(path: str) -> Input:
    with open(path, "r") as f:
        data = f.read().splitlines()

        section = data.index("")
        rules = [line.split("|", maxsplit=1) for line in data[:section]]

        lookup = {}
        for a, b in rules:
            lookup.setdefault(int(a), set()).add(int(b))

        updates = [[int(x) for x in line.split(",")] for line in data[section + 1:]]
    
    return lookup, updates


def check_update(rules: RuleSet, update: Update) -> bool:
    seen = {update[0]}
    for page in update[1:]:
        if page in rules and rules[page].intersection(seen):
            return False

        seen.add(page)

    return True


def part1(rules: RuleSet, updates: list[Update]) -> int:
    result = 0

    for update in updates:
        if check_update(rules, update):
            result += update[len(update)//2]

    return result


def sort_update(rules: RuleSet, update: Update) -> Update:
    sorted = copy(update)

    while not check_update(rules, sorted):
        for i in range(len(sorted)):
            if sorted[i] not in rules:
                continue

            violating_pages = rules[sorted[i]].intersection(sorted[:i])
            if not violating_pages:
                continue

            index = 0
            for page in violating_pages:
                index = min(index, sorted[:i].index(page))

            sorted.insert(index, sorted.pop(i))

    return sorted


def part2(rules: RuleSet, updates: list[Update]) -> int:
    result = 0

    for update in updates:
        if not check_update(rules, update):
            sorted_update = sort_update(rules, update)
            result += sorted_update[len(sorted_update)//2]

    return result


def main():
    rules, updates = parse_input("input.txt")

    result = part1(rules, updates)
    print("part 1:", result)

    result = part2(rules, updates)
    print("part 2:", result)


if __name__ == "__main__":
    main()
