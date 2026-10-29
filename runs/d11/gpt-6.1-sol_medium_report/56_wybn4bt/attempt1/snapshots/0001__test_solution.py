import pytest

from solution import add


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([4, 2, 6, 7], 2, id="docstring-example"),
        pytest.param([8], 0, id="single-even-element"),
        pytest.param([3], 0, id="single-odd-element"),
        pytest.param([1, 2], 2, id="even-at-first-odd-index"),
        pytest.param([2, 3], 0, id="even-at-even-index-is-excluded"),
        pytest.param([2, 4, 6, 8, 10, 12], 24, id="all-even-values"),
        pytest.param([1, 3, 5, 7, 9], 0, id="all-odd-values"),
        pytest.param([2, 1, 4, 3, 6], 0, id="evens-only-at-even-indices"),
        pytest.param([1, 2, 3, 4, 5], 6, id="evens-only-at-odd-indices"),
        pytest.param([100, 2, 200, 3, 300, 4], 6, id="mixed-parities"),
        pytest.param([1, -2, 3, -4, 5, -5], -6, id="negative-values"),
        pytest.param([9, -4, 8, 4, 6, 2], 2, id="positive-negative-cancellation"),
        pytest.param([8, 0, 6, 2], 2, id="zero-at-odd-index"),
        pytest.param([2, 3, 4, 6], 6, id="last-odd-index-included"),
        pytest.param([2, 3, 4, 5, 100], 0, id="last-even-index-excluded"),
        pytest.param(
            [10**100, 10**100, 2, -(10**100) + 2],
            2,
            id="arbitrary-precision-integers",
        ),
    ],
)
def test_add_sums_even_values_at_odd_indices(values, expected):
    assert add(values) == expected


def test_add_does_not_modify_input():
    values = [4, -2, 6, 8, 0, 3]
    original = values.copy()

    assert add(values) == 6
    assert values == original
