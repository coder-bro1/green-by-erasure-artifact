import pytest

from solution import mergesort


def test_mergesort_empty_list():
    assert mergesort([]) == []


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([7], [7], id="single-element"),
        pytest.param([2, 1], [1, 2], id="two-reversed-elements"),
        pytest.param([1, 2], [1, 2], id="two-sorted-elements"),
        pytest.param([4, 1, 3, 2], [1, 2, 3, 4], id="even-length"),
        pytest.param([5, 2, 4, 1, 3], [1, 2, 3, 4, 5], id="odd-length"),
        pytest.param([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], id="already-sorted"),
        pytest.param([5, 4, 3, 2, 1], [1, 2, 3, 4, 5], id="reverse-sorted"),
        pytest.param([3, 1, 3, 2, 1], [1, 1, 2, 3, 3], id="duplicates"),
        pytest.param([2, 2, 2], [2, 2, 2], id="all-equal"),
        pytest.param([-1, -5, -3], [-5, -3, -1], id="negative-integers"),
        pytest.param([0, -2, 5, 0, -1], [-2, -1, 0, 0, 5], id="mixed-signs"),
        pytest.param(
            [10**100, 0, -(10**100)],
            [-(10**100), 0, 10**100],
            id="large-integers",
        ),
    ],
)
def test_mergesort_returns_elements_in_sorted_order(values, expected):
    assert mergesort(values) == expected
