"""Tests for the documented sum/product contract and its known product bug."""

import pytest

from solution import total_and_multiple


@pytest.mark.parametrize(
    "values, expected",
    [
        ([0], (0, 0)),
        ([0, 0, 0], (0, 0)),
        ([0, 2, 5], (7, 0)),
        ([2, 0, 5], (7, 0)),
        ([2, 5, 0], (7, 0)),
        ([-3, 0, 4, 1], (2, 0)),
        ([-5, -2, 0], (-7, 0)),
        ([10**100, 0, 10**100], (2 * 10**100, 0)),
    ],
)
def test_sum_and_product_with_zero(values, expected):
    assert total_and_multiple(values) == expected


@pytest.mark.parametrize(
    "values, expected_sum",
    [([], 0), ([7], 7), ([2, 5], 7), ([-3, 4, 1], 2), ([-5, -2], -7)],
)
def test_sum(values, expected_sum):
    assert total_and_multiple(values)[0] == expected_sum


def test_returns_pair_of_integers_without_mutating_input():
    values = [-3, 0, 4, 1]
    original = values.copy()

    result = total_and_multiple(values)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(value, int) for value in result)
    assert values == original


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: the product accumulator starts at 0 instead of 1",
)
@pytest.mark.parametrize(
    "values, expected",
    [
        ([], (0, 1)),
        ([7], (7, 7)),
        ([2, 5], (7, 10)),
        ([-3, 4, 1], (2, -12)),
        ([-5, -2], (-7, 10)),
        ([1, 1, 1], (3, 1)),
        ([10**100, 10**100], (2 * 10**100, 10**200)),
    ],
)
def test_product_without_zero_matches_documented_contract(values, expected):
    assert total_and_multiple(values) == expected
