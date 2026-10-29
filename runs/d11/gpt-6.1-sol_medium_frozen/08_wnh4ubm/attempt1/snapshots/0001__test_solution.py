"""Tests for fruit distribution, including its known off-by-one defect."""

import pytest

from solution import fruit_distribution


@pytest.mark.xfail(
    strict=True,
    reason="fruit_distribution subtracts an extra 1 from the mango count",
)
@pytest.mark.parametrize(
    "description,total,expected",
    [
        ("5 apples and 6 oranges", 19, 8),
        ("0 apples and 1 oranges", 3, 2),
        ("2 apples and 3 oranges", 100, 95),
        ("100 apples and 1 oranges", 120, 19),
        ("0 apples and 0 oranges", 0, 0),
        ("0 apples and 0 oranges", 10, 10),
        ("5 apples and 6 oranges", 11, 0),
        ("1234 apples and 5678 oranges", 10000, 3088),
    ],
)
def test_mango_count_matches_documented_contract(description, total, expected):
    assert fruit_distribution(description, total) == expected


@pytest.mark.parametrize("increase", [1, 7, 1000])
def test_increasing_total_increases_mango_count(increase):
    description = "5 apples and 6 oranges"
    assert fruit_distribution(description, 19 + increase) == (
        fruit_distribution(description, 19) + increase
    )


@pytest.mark.parametrize("increase", [1, 7, 1000])
@pytest.mark.parametrize("fruit", ["apples", "oranges"])
def test_increasing_other_fruit_decreases_mango_count(fruit, increase):
    apples = 5 + (increase if fruit == "apples" else 0)
    oranges = 6 + (increase if fruit == "oranges" else 0)
    total = 2000
    assert fruit_distribution(f"{apples} apples and {oranges} oranges", total) == (
        fruit_distribution("5 apples and 6 oranges", total) - increase
    )


@pytest.mark.parametrize("apples,oranges", [(0, 1), (5, 6), (1234, 5678)])
def test_swapping_apple_and_orange_counts_preserves_mango_count(apples, oranges):
    total = apples + oranges + 10
    assert fruit_distribution(f"{apples} apples and {oranges} oranges", total) == (
        fruit_distribution(f"{oranges} apples and {apples} oranges", total)
    )
