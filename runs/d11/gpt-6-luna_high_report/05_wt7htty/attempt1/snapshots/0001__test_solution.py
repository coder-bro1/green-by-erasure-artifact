import pytest

from solution import add


def test_example_from_docstring():
    assert add([4, 2, 6, 7]) == 2


@pytest.mark.xfail(
    strict=True,
    reason="add checks every index after zero instead of only odd indices",
)
def test_sums_even_values_at_odd_indices_only():
    assert add([2, 4, 6, 8, 10, 12]) == 24


@pytest.mark.xfail(
    strict=True,
    reason="add incorrectly includes even values at even indices",
)
def test_excludes_even_values_at_even_indices():
    assert add([2, 3, 4, 5]) == 0


def test_sums_negative_even_values_at_odd_indices():
    assert add([1, -2, 3, -4, 5]) == -6


def test_returns_zero_when_no_even_values_qualify():
    assert add([1, 3, 5, 7]) == 0


def test_single_element_at_even_index_is_not_included():
    assert add([8]) == 0
