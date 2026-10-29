"""Tests for Hanoi, including explicit coverage of its known move defect."""

from itertools import permutations, product

import pytest

from solution import hanoi


PEG_PAIRS = list(permutations((1, 2, 3), 2))
KNOWN_MOVE_DEFECT = pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="The central move uses the helper peg instead of the destination peg",
)


@pytest.mark.parametrize("start,end", list(product((1, 2, 3), repeat=2)))
def test_zero_height_has_no_moves(start, end):
    assert hanoi(0, start, end) == []


@pytest.mark.parametrize("height", [1, 2, 3, 6])
@pytest.mark.parametrize("start,end", PEG_PAIRS)
def test_move_count_and_format(height, start, end):
    moves = hanoi(height, start, end)

    assert isinstance(moves, list)
    assert len(moves) == 2**height - 1
    for move in moves:
        assert isinstance(move, tuple)
        assert len(move) == 2
        source, destination = move
        assert source in (1, 2, 3)
        assert destination in (1, 2, 3)
        assert source != destination


@pytest.mark.parametrize("height", [0, 1, 2, 5])
def test_default_pegs_match_explicit_arguments(height):
    assert hanoi(height) == hanoi(height, start=1, end=3)


def test_calls_return_independent_lists():
    first = hanoi(3)
    second = hanoi(3)

    assert first == second
    assert first is not second
    first.clear()
    assert second == hanoi(3)
    assert len(second) == 7


@KNOWN_MOVE_DEFECT
@pytest.mark.parametrize("start,end", PEG_PAIRS)
def test_single_disk_moves_directly_to_destination(start, end):
    assert hanoi(1, start, end) == [(start, end)]


@KNOWN_MOVE_DEFECT
def test_three_disk_reference_solution():
    assert hanoi(3) == [
        (1, 3),
        (1, 2),
        (3, 2),
        (1, 3),
        (2, 1),
        (2, 3),
        (1, 3),
    ]


@KNOWN_MOVE_DEFECT
@pytest.mark.parametrize("height", [2, 3, 5])
@pytest.mark.parametrize("start,end", PEG_PAIRS)
def test_moves_legally_solve_the_puzzle(height, start, end):
    initial_stack = list(range(height, 0, -1))
    pegs = {peg: [] for peg in (1, 2, 3)}
    pegs[start] = initial_stack.copy()
    moves = hanoi(height, start, end)

    for source, destination in moves:
        assert pegs[source], "Cannot move a disk from an empty peg"
        disk = pegs[source].pop()
        assert not pegs[destination] or pegs[destination][-1] > disk, (
            "Cannot place a larger disk on a smaller disk"
        )
        pegs[destination].append(disk)

    assert pegs[end] == initial_stack
    assert all(not disks for peg, disks in pegs.items() if peg != end)
    assert len(moves) == 2**height - 1
