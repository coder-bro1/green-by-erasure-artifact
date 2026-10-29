import pytest

from solution import add


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([4, 2, 6, 7], 2, id="documented-example"),
        pytest.param([2], 0, id="single-element"),
        pytest.param([1, 2], 2, id="two-elements"),
        pytest.param([2, 1, 4, 3, 6], 0, id="even-values-at-even-indices"),
        pytest.param([1, 2, 3, 4, 5, 6], 12, id="multiple-matches"),
        pytest.param([1, 2, 3, 4, 100], 6, id="odd-length-list"),
        pytest.param([1, 3, 5, 7], 0, id="only-odd-values"),
        pytest.param([9, -2, 8, -4, 7, -3], -6, id="negative-values"),
        pytest.param([8, -4, 6, 4], 0, id="cancelling-values"),
        pytest.param([5, 0, 7, 2], 2, id="zero-is-even"),
        pytest.param([2, 2, 2, 2, 2, 2], 6, id="repeated-values"),
        pytest.param([0, 10**100, 0, 2], 10**100 + 2, id="large-integers"),
    ],
)
def test_add_sums_even_values_at_zero_based_odd_indices(values, expected):
    assert add(values) == expected


def test_add_does_not_modify_input():
    values = [4, 2, 6, -8, 0, 7]
    original = values.copy()

    assert add(values) == -6
    assert values == original
