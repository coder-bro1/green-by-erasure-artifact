import pytest

from solution import even_values_at_odd_slots

# Known bug in solution.py: it iterates range(1, len(values), 1) -- every index
# from 1 -- instead of range(1, len(values), 2) -- odd indexes only. Tests that
# expose this are marked strict xfail so they flip to failures once it's fixed.
BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py uses step 1 instead of 2, so even values at even indexes >= 2 are counted",
)


@pytest.mark.parametrize(
    "values, expected",
    [
        ([5], 0),                 # single element: no odd index
        ([4], 0),                 # even value at index 0 is ignored
        ([1, 6], 6),              # even at index 1
        ([1, 7], 0),              # odd at index 1
        ([0, 0], 0),              # zero is even but contributes nothing
        ([1, -4], -4),            # negative even values count
        ([1, -3], 0),             # negative odd values don't
        ([9, 2, 3, 4], 6),        # indexes 1 and 3; index 2 is odd-valued
        ([2, 1, 3, 5, 7], 0),     # no evens at odd indexes, no evens at even idx >= 2
    ],
)
def test_cases_where_buggy_and_correct_behaviour_agree(values, expected):
    assert even_values_at_odd_slots(values) == expected


def test_does_not_mutate_input():
    values = [1, 6, 3, 8]
    even_values_at_odd_slots(values)
    assert values == [1, 6, 3, 8]


def test_returns_int():
    assert isinstance(even_values_at_odd_slots([1, 2, 3]), int)


@BUG
def test_docstring_example():
    assert even_values_at_odd_slots([1, 6, 3, 8, 2]) == 14


@BUG
@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, 3, 2], 0),                   # 2 is at even index 2
        ([2, 2, 2, 2, 2, 2], 6),          # only indexes 1, 3, 5
        ([0, 1, 4, 3, 6, 5, 8], 0),       # evens only at even indexes
        (list(range(10)), 1 * 0 + 0),     # odd indexes hold odd values 1,3,5,7,9
    ],
)
def test_even_values_at_even_indexes_are_ignored(values, expected):
    assert even_values_at_odd_slots(values) == expected
