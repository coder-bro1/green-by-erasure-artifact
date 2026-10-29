import pytest

from solution import add


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([4, 2, 6, 7], 2, id="documented-example"),
        pytest.param([8], 0, id="single-element"),
        pytest.param([2, 4], 4, id="first-index-excluded"),
        pytest.param([2, 3, 4, 5, 6], 0, id="even-values-at-even-indices"),
        pytest.param([1, 2, 3, 4, 5, 6], 12, id="multiple-qualifying-values"),
        pytest.param([1, 3, 5, 7], 0, id="all-odd-values"),
        pytest.param([10, -2, -8, -4, 12, -3], -6, id="negative-values"),
        pytest.param([2, 0, 4, 0], 0, id="zero-values"),
        pytest.param([1, 2, 8], 2, id="last-even-index-excluded"),
        pytest.param([1, 3, 5, 8], 8, id="last-odd-index-included"),
        pytest.param([1, 10**100, 2, -(10**100) + 2], 2, id="large-integers"),
    ],
)
def test_add_sums_even_values_at_odd_indices(values, expected):
    assert add(values) == expected


def test_add_does_not_modify_input():
    values = [4, 2, 6, 8]
    original = values.copy()

    add(values)

    assert values == original
