import pytest

from solution import add


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([4, 2, 6, 7], 2, id="docstring-example"),
        pytest.param([8], 0, id="single-even-element"),
        pytest.param([7], 0, id="single-odd-element"),
        pytest.param([3, 4], 4, id="even-at-index-one"),
        pytest.param([2, 5], 0, id="odd-at-index-one"),
        pytest.param([1, 2, 3, 4, 5, 6], 12, id="multiple-odd-indices"),
        pytest.param([1, 3, 5, 7], 0, id="all-odd-values"),
        pytest.param([1, -2, 3, -4], -6, id="negative-even-values"),
        pytest.param([1, -3, 5, -7], 0, id="negative-odd-values"),
        pytest.param([1, 0, 3, 0], 0, id="zero-is-even"),
        pytest.param([1, 2, 3, -2], 0, id="cancelling-values"),
        pytest.param([1, 10**100, 3, 2], 10**100 + 2, id="large-integers"),
    ],
)
def test_add_even_values_at_odd_indices(values, expected):
    assert add(values) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([1, 2, 4], 2, id="even-value-at-index-two"),
        pytest.param([2, 4, 6, 8, 10, 12], 24, id="all-even-values"),
        pytest.param([1, -2, -4, -6], -8, id="negative-at-even-index"),
        pytest.param([0, 0, 6, 0, 8], 0, id="only-even-indices-contribute"),
    ],
)
def test_add_ignores_even_indices(values, expected):
    assert add(values) == expected


def test_add_does_not_mutate_input():
    values = [1, 2, 3, 4]
    original = values.copy()

    add(values)

    assert values == original
