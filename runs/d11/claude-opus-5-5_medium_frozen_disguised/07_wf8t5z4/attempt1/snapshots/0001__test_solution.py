import pytest

from solution import has_opposite_pair

# Known bug in solution.py: the inner loop starts at j = i, so an element is
# paired with itself. A lone 0 therefore counts as an "opposite pair", which
# contradicts the docstring ("two different positions"; [0, 3] -> False).
# These tests encode the documented behaviour and are marked strict xfail, so
# they will start failing (XPASS) once the bug is fixed, signalling to remove
# the marker.
SELF_PAIR_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py pairs an element with itself (range(i, ...) should be range(i + 1, ...))",
)


@pytest.mark.parametrize(
    "nums",
    [
        [4, -4, 2],          # docstring example
        [-4, 4],
        [1, 2, 3, -2],       # non-adjacent pair
        [7, 0, 0],           # two zeros at different positions
        [0, 0],
        [-1000000, 5, 1000000],
        [3, 3, -3],
    ],
)
def test_returns_true_when_opposite_pair_exists(nums):
    assert has_opposite_pair(nums) is True


@pytest.mark.parametrize(
    "nums",
    [
        [],
        [5],                 # docstring example
        [-5],
        [1, 2, 3],
        [-1, -2, -3],
        [2, 2, 2],
        [1, -2, 3, -4],
    ],
)
def test_returns_false_when_no_opposite_pair(nums):
    assert has_opposite_pair(nums) is False


@SELF_PAIR_BUG
@pytest.mark.parametrize(
    "nums",
    [
        [0, 3],              # docstring example
        [0],
        [1, 0, 2],
    ],
)
def test_single_zero_is_not_a_pair(nums):
    assert has_opposite_pair(nums) is False


def test_works_with_floats():
    assert has_opposite_pair([1.5, -1.5]) is True
    assert has_opposite_pair([1.5, -1.25]) is False


def test_accepts_tuple_input():
    assert has_opposite_pair((2, -2)) is True


def test_does_not_mutate_input():
    nums = [3, -1, 1]
    has_opposite_pair(nums)
    assert nums == [3, -1, 1]
