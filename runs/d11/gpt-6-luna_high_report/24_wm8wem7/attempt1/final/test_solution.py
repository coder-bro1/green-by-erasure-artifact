import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], True),
        ([5], True),
        ([1, 2, 3, 4, 5], True),
        ([1, 2, 3, 4, 5, 6, 7], True),
        ([1, 2, 2, 3, 3, 4], True),
        ([1, 3, 2, 4, 5], False),
        ([1, 3, 2, 4, 5, 6, 7], False),
        ([1, 2, 2, 2, 3, 4], False),
        ([2, 1, 1, 1], False),
    ],
)
def test_is_sorted_docstring_examples_and_boundaries(numbers, expected):
    assert is_sorted(numbers) is expected


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([0, 0], True),
        ([0, 0, 1, 1, 2], True),
        ([0, 0, 0], False),
        ([1, 1, 2, 2, 2], False),
        ([1, 2, 2, 1], False),
        ([3, 2, 2, 1], False),
    ],
)
def test_is_sorted_allows_at_most_two_of_each_value(numbers, expected):
    assert is_sorted(numbers) is expected
