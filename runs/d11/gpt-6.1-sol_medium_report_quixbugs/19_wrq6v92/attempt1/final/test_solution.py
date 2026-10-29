"""Tests for the Towers of Hanoi contract documented in solution.py."""

from itertools import permutations, product

import pytest

from solution import hanoi


PEG_PAIRS = list(permutations((1, 2, 3), 2))


@pytest.mark.parametrize("start,end", product((1, 2, 3), repeat=2))
def test_empty_stack_needs_no_moves(start, end):
    assert hanoi(0, start, end) == []


@pytest.mark.xfail(
    strict=True,
    reason="hanoi appends (start, helper) instead of (start, end), producing incorrect moves",
)
@pytest.mark.parametrize(
    "height,expected",
    [
        (1, [(1, 3)]),
        (2, [(1, 2), (1, 3), (2, 3)]),
        (3, [(1, 3), (1, 2), (3, 2), (1, 3), (2, 1), (2, 3), (1, 3)]),
    ],
)
def test_default_pegs_have_expected_moves(height, expected):
    assert hanoi(height) == expected


@pytest.mark.parametrize("start,end", PEG_PAIRS)
@pytest.mark.parametrize("height", (1, 2, 3, 5))
def test_distinct_pegs_have_minimum_number_of_moves(height, start, end):
    assert len(hanoi(height, start, end)) == 2**height - 1


@pytest.mark.xfail(
    strict=True,
    reason="Moving to helper instead of end leaves disks on the wrong peg or creates illegal moves",
)
@pytest.mark.parametrize("start,end", PEG_PAIRS)
@pytest.mark.parametrize("height", (1, 2, 3, 5))
def test_moves_are_legal_and_reach_destination(height, start, end):
    steps = hanoi(height, start, end)
    assert isinstance(steps, list)
    pegs = {peg: [] for peg in (1, 2, 3)}
    pegs[start] = list(range(height, 0, -1))

    for step in steps:
        assert isinstance(step, tuple)
        assert len(step) == 2
        source, destination = step
        assert source in pegs and destination in pegs
        assert source != destination
        assert pegs[source], "Cannot move a disk from an empty peg"
        disk = pegs[source][-1]
        assert not pegs[destination] or pegs[destination][-1] > disk, (
            "Cannot place a larger disk on a smaller disk"
        )
        pegs[source].pop()
        pegs[destination].append(disk)

    assert pegs[end] == list(range(height, 0, -1))
    assert all(not stack for peg, stack in pegs.items() if peg != end)


@pytest.mark.xfail(
    strict=True,
    reason="Equal start and end satisfy the preconditions but hanoi returns moves instead of []",
)
@pytest.mark.parametrize("peg", (1, 2, 3))
@pytest.mark.parametrize("height", (1, 2, 3, 5))
def test_stack_already_at_destination_needs_no_moves(height, peg):
    assert hanoi(height, peg, peg) == []
