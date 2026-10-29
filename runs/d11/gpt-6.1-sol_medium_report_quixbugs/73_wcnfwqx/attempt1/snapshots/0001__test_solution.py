"""Tests for the documented Towers of Hanoi contract."""

import itertools

import pytest

from solution import hanoi


PEG_PAIRS = list(itertools.permutations((1, 2, 3), 2))


@pytest.mark.parametrize("start,end", itertools.product((1, 2, 3), repeat=2))
def test_empty_stack_requires_no_moves(start, end):
    assert hanoi(0, start, end) == []


@pytest.mark.parametrize("start,end", PEG_PAIRS)
def test_single_disk_moves_directly_to_destination(start, end):
    assert hanoi(1, start, end) == [(start, end)]


@pytest.mark.parametrize(
    "height,expected",
    [
        (0, []),
        (1, [(1, 3)]),
        (2, [(1, 2), (1, 3), (2, 3)]),
        (3, [(1, 3), (1, 2), (3, 2), (1, 3), (2, 1), (2, 3), (1, 3)]),
    ],
)
def test_default_pegs_produce_expected_order(height, expected):
    assert hanoi(height) == expected


@pytest.mark.parametrize("height", range(1, 8))
@pytest.mark.parametrize("start,end", PEG_PAIRS)
def test_moves_are_legal_and_solve_puzzle_in_minimum_steps(height, start, end):
    moves = hanoi(height, start, end)
    assert isinstance(moves, list)
    assert len(moves) == 2**height - 1

    pegs = {peg: [] for peg in (1, 2, 3)}
    pegs[start] = list(range(height, 0, -1))
    for move in moves:
        assert isinstance(move, tuple)
        assert len(move) == 2
        source, destination = move
        assert source in pegs
        assert destination in pegs
        assert source != destination
        assert pegs[source], "Cannot move a disk from an empty peg"
        disk = pegs[source].pop()
        assert not pegs[destination] or pegs[destination][-1] > disk
        pegs[destination].append(disk)

    assert pegs[end] == list(range(height, 0, -1))
    assert all(not disks for peg, disks in pegs.items() if peg != end)


@pytest.mark.parametrize("peg", (1, 2, 3))
@pytest.mark.parametrize("height", (1, 2, 3, 5))
def test_stack_already_on_destination_requires_no_moves(height, peg):
    assert hanoi(height, peg, peg) == []
