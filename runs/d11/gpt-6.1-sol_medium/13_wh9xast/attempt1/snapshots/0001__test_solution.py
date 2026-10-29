from collections import Counter
from itertools import product

import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([5], True, id="example-singleton"),
        pytest.param([1, 2, 3, 4, 5], True, id="example-ascending-five"),
        pytest.param([1, 3, 2, 4, 5], False, id="example-inversion-five"),
        pytest.param([1, 2, 3, 4, 5, 6], True, id="example-ascending-six"),
        pytest.param([1, 2, 3, 4, 5, 6, 7], True, id="example-ascending-seven"),
        pytest.param([1, 3, 2, 4, 5, 6, 7], False, id="example-inversion-seven"),
        pytest.param([1, 2, 2, 3, 3, 4], True, id="example-allowed-duplicates"),
        pytest.param([1, 2, 2, 2, 3, 4], False, id="example-excess-duplicates"),
        pytest.param([], True, id="empty"),
        pytest.param([0], True, id="zero"),
        pytest.param([0, 0], True, id="two-zeros"),
        pytest.param([0, 0, 0], False, id="three-zeros"),
        pytest.param([1, 1], True, id="two-equal-values"),
        pytest.param([1, 1, 1], False, id="three-equal-values"),
        pytest.param([0, 0, 1, 1, 2, 2], True, id="every-value-twice"),
        pytest.param([0, 0, 0, 1, 2], False, id="excess-duplicates-at-start"),
        pytest.param([0, 1, 2, 2, 2], False, id="excess-duplicates-at-end"),
        pytest.param([2, 1], False, id="descending-pair"),
        pytest.param([4, 3, 2, 1, 0], False, id="descending-list"),
        pytest.param([1, 0, 2, 3], False, id="inversion-at-start"),
        pytest.param([0, 1, 3, 2], False, id="inversion-at-end"),
        pytest.param([0, 1, 0], False, id="nonadjacent-duplicates-unsorted"),
        pytest.param([0, 2, 1, 2, 3], False, id="allowed-counts-but-unsorted"),
        pytest.param([0, 10**100, 10**100], True, id="large-integers"),
    ],
)
def test_is_sorted_examples_and_boundaries(numbers, expected):
    original = numbers.copy()

    assert is_sorted(numbers) is expected
    assert numbers == original, "is_sorted must not modify its input"


@pytest.mark.parametrize("length", range(7))
def test_is_sorted_matches_specification_for_small_lists(length):
    """Check every list of length 0 through 6 over four distinct values."""
    for values in product(range(4), repeat=length):
        numbers = list(values)
        expected = numbers == sorted(numbers) and all(
            count <= 2 for count in Counter(numbers).values()
        )

        assert is_sorted(numbers) is expected, f"Incorrect result for {numbers!r}"
