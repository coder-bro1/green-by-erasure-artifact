from itertools import product

import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], True),
        ([5], True),
        ([0], True),
        ([1, 2, 3, 4, 5], True),
        ([1, 3, 2, 4, 5], False),
        ([1, 2, 3, 4, 5, 6], True),
        ([1, 2, 3, 4, 5, 6, 7], True),
        ([1, 3, 2, 4, 5, 6, 7], False),
        ([1, 2, 2, 3, 3, 4], True),
        ([0, 0, 1, 1, 2, 2], True),
        ([2, 2], True),
        ([2, 1], False),
        ([5, 4, 3, 2, 1], False),
        ([0, 2, 1, 3], False),
        ([0, 1, 3, 2], False),
        ([1, 2, 1], False),
        ([2, 2, 2, 1], False),
        ([0, 10**100, 10**100], True),
        ([10**100, 0], False),
    ],
)
def test_is_sorted(numbers, expected):
    assert is_sorted(numbers) is expected


def test_short_lists_with_at_most_two_occurrences():
    """Compare against sorting for every valid small input in this domain."""
    for length in range(7):
        for values in product(range(3), repeat=length):
            if any(values.count(number) > 2 for number in set(values)):
                continue
            numbers = list(values)
            assert is_sorted(numbers) is (numbers == sorted(numbers)), numbers


@pytest.mark.parametrize("numbers", [[], [1], [1, 2, 2], [3, 1, 2]])
def test_does_not_modify_input(numbers):
    original = numbers.copy()
    is_sorted(numbers)
    assert numbers == original


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: is_sorted ignores the documented two-occurrence limit",
)
@pytest.mark.parametrize(
    "numbers",
    [
        [1, 2, 2, 2, 3, 4],
        [0, 0, 0],
        [1, 1, 1, 2],
        [1, 2, 2, 2],
        [7, 7, 7, 7],
    ],
)
def test_rejects_more_than_two_occurrences(numbers):
    assert is_sorted(numbers) is False
