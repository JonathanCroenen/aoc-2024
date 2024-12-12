from __future__ import annotations
import sys
from dataclasses import dataclass
from copy import copy


EMPTY_SPACE = -1


def parse_input(input: str) -> list[int]:
    is_file = True
    file_id = 0

    result = []
    for char in input.strip():
        length = int(char)

        if is_file:
            result.extend([file_id] * length)
            file_id += 1
        else:
            result.extend([EMPTY_SPACE] * length)

        is_file = not is_file

    return result


def print_input(input: list[int]) -> None:
    for x in input:
        if x == EMPTY_SPACE:
            print(".", end="")
        else:
            print(x, end="")

    print()


def is_compacted(data: list[int]) -> bool:
    num_empty = data.count(EMPTY_SPACE)
    slice_index = len(data) - num_empty
    return len([x for x in data[slice_index:] if x != EMPTY_SPACE]) == 0


def checksum(data: list[int]) -> int:
    return sum([i * x for i, x in enumerate(data) if x != EMPTY_SPACE])


def part1(input: list[int]) -> int:
    data = copy(input)
    free_index = data.index(EMPTY_SPACE)
    if data[-1] != EMPTY_SPACE:
        rear_index = len(data) - 1
    else:
        rear_index = len(data) - data[::-1].index(EMPTY_SPACE) - 2

    while not is_compacted(data):
        data[free_index], data[rear_index] = data[rear_index], data[free_index]

        while data[free_index] != EMPTY_SPACE:
            free_index += 1
            if free_index >= len(data):
                return checksum(data)

        while data[rear_index] == EMPTY_SPACE:
            rear_index -= 1
            if rear_index < 0:
                return checksum(data)

    return checksum(data)


@dataclass
class EmptyBlock:
    loc: int
    size: int
    next: EmptyBlock | None


def parse_input2(input: str) -> tuple[EmptyBlock, list[tuple[int, int, int]]]:
    is_file = True
    file_id = 0
    loc = 0

    files = []
    root_block = None
    current_block = None
    for char in input.strip():
        length = int(char)

        if is_file:
            files.append((file_id, loc, length))
            file_id += 1
        else:
            if current_block is None:
                root_block = EmptyBlock(loc, length, None)
                current_block = root_block
            else:
                current_block.next = EmptyBlock(loc, length, None)
                current_block = current_block.next

        loc += length
        is_file = not is_file

    assert root_block is not None
    return root_block, files


def print_files(files: list[tuple[int, int, int]]) -> None:
    current_loc = 0
    for file_id, loc, length in files:
        for _ in range(max(loc - current_loc, 0)):
            print(".", end="")

        for _ in range(length):
            print(file_id, end="")

        current_loc = loc + length

    print()


def checksum2(files: list[tuple[int, int, int]]) -> int:
    result = 0
    for file_id, loc, length in files:
        result += file_id * sum(range(loc, loc + length))

    return result


def part2(root_block: EmptyBlock, files: list[tuple[int, int, int]]) -> int:
    new_files = []
    for file_id, orig_loc, length in files[::-1]:
        previous = None
        current = root_block
        while True:
            if current.size >= length and current.loc < orig_loc:
                new_files.append((file_id, current.loc, length))

                if current.size == length:
                    if previous is None and current.next is not None:
                        root_block = current.next
                    elif previous is not None:
                        previous.next = current.next
                else:
                    current.loc += length
                    current.size -= length

                break

            if current.next is None or current.loc >= orig_loc:
                new_files.append((file_id, orig_loc, length))
                break
            previous = current
            current = current.next

    # print_files(sorted(new_files, key=lambda x: x[1]))
    new_files = sorted(new_files, key=lambda x: x[1])
    return checksum2(new_files)


def main():
    raw_input = sys.stdin.read()
    input = parse_input(raw_input)

    result = part1(input)
    print("part 1:", result)

    root_block, files = parse_input2(raw_input)
    result = part2(root_block, files)
    print("part 2:", result)


if __name__ == "__main__":
    main()
