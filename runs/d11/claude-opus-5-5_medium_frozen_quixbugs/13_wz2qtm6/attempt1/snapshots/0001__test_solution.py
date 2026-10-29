import itertools

import pytest

from solution import hanoi

PEGS = (1, 2, 3)
PEG_PAIRS = [(s, e) for s, e in itertools.product(PEGS, PEGS) if s != e]

BUG_REASON = (
    "Known bug in solution.py: the largest disk is moved to the helper peg "
    "(steps.append((start, helper))) instead of the target peg (start, end)."
)


def simulate(height, start, end, steps):
    """Apply steps to a peg state; raise AssertionError on any illegal move.

    Returns the final peg state as a dict peg -> list of disks (bottom..top).
    """
    pegs = {p: [] for p in PEGS}
    pegs[start] = list(range(height, 0, -1))
    for a, b in steps:
        assert a in PEGS and b in PEGS, f"invalid peg in step {(a, b)}"
        assert a != b, f"step moves a disk onto the same peg: {(a, b)}"
        assert pegs[a], f"step {(a, b)} moves from an empty peg"
        disk = pegs[a].pop()
        assert not pegs[b] or pegs[b][-1] > disk, (
            f"step {(a, b)} places disk {disk} on smaller disk {pegs[b][-1]}"
        )
        pegs[b].append(disk)
    return pegs


# ---------------------------------------------------------------------------
# Properties that hold for the current implementation
# ---------------------------------------------------------------------------

def test_height_zero_returns_empty_list():
    assert hanoi(0) == []


@pytest.mark.parametrize("start,end", PEG_PAIRS)
def test_height_zero_any_pegs_returns_empty_list(start, end):
    assert hanoi(0, start, end) == []


def test_returns_list_of_pairs():
    result = hanoi(3)
    assert isinstance(result, list)
    for step in result:
        assert isinstance(step, tuple)
        assert len(step) == 2


@pytest.mark.parametrize("height", range(0, 11))
def test_number_of_steps_is_minimal(height):
    assert len(hanoi(height)) == 2 ** height - 1


@pytest.mark.parametrize("height", range(1, 7))
@pytest.mark.parametrize("start,end", PEG_PAIRS)
def test_steps_use_valid_distinct_pegs(height, start, end):
    for a, b in hanoi(height, start, end):
        assert a in PEGS and b in PEGS
        assert a != b


@pytest.mark.parametrize("height", range(1, 6))
def test_default_arguments_match_explicit(height):
    assert hanoi(height) == hanoi(height, 1, 3)


def test_does_not_share_state_between_calls():
    first = hanoi(3)
    first.append(("junk", "junk"))
    assert ("junk", "junk") not in hanoi(3)


# ---------------------------------------------------------------------------
# Correctness per the docstring. These fail against the current solution.py.
# ---------------------------------------------------------------------------

@pytest.mark.xfail(reason=BUG_REASON, strict=True)
def test_single_disk_moves_directly():
    assert hanoi(1) == [(1, 3)]


@pytest.mark.xfail(reason=BUG_REASON, strict=True)
@pytest.mark.parametrize("start,end", PEG_PAIRS)
def test_single_disk_any_pegs(start, end):
    assert hanoi(1, start, end) == [(start, end)]


@pytest.mark.xfail(reason=BUG_REASON, strict=True)
def test_two_disks_known_solution():
    assert hanoi(2) == [(1, 2), (1, 3), (2, 3)]


@pytest.mark.xfail(reason=BUG_REASON, strict=True)
def test_three_disks_known_solution():
    assert hanoi(3) == [
        (1, 3), (1, 2), (3, 2), (1, 3), (2, 1), (2, 3), (1, 3),
    ]


@pytest.mark.xfail(reason=BUG_REASON, strict=True)
@pytest.mark.parametrize("height", range(1, 8))
@pytest.mark.parametrize("start,end", PEG_PAIRS)
def test_solution_is_legal_and_solves_puzzle(height, start, end):
    final = simulate(height, start, end, hanoi(height, start, end))
    assert final[end] == list(range(height, 0, -1))
    assert all(not final[p] for p in PEGS if p != end)
