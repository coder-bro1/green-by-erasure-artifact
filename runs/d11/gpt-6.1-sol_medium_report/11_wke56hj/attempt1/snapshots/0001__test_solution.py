"""Tests for the documented mango-count calculation."""

import pytest

from solution import fruit_distribution


@pytest.mark.parametrize(
    "description,total,expected",
    [
        pytest.param("5 apples and 6 oranges", 19, 8, id="example-1"),
        pytest.param("0 apples and 1 oranges", 3, 2, id="example-2"),
        pytest.param("2 apples and 3 oranges", 100, 95, id="example-3"),
        pytest.param("100 apples and 1 oranges", 120, 19, id="example-4"),
    ],
)
def test_docstring_examples(description, total, expected):
    assert fruit_distribution(description, total) == expected


@pytest.mark.parametrize(
    "description,total,expected",
    [
        pytest.param("0 apples and 0 oranges", 0, 0, id="empty-basket"),
        pytest.param("0 apples and 0 oranges", 17, 17, id="only-mangoes"),
        pytest.param("7 apples and 0 oranges", 12, 5, id="no-oranges"),
        pytest.param("0 apples and 9 oranges", 13, 4, id="no-apples"),
        pytest.param("7 apples and 9 oranges", 16, 0, id="no-mangoes"),
        pytest.param("1 apples and 1 oranges", 3, 1, id="one-of-each"),
        pytest.param("12 apples and 34 oranges", 60, 14, id="multi-digit-counts"),
        pytest.param(
            "12345678901234567890 apples and 98765432109876543210 oranges",
            111111111011111111107,
            7,
            id="large-integers",
        ),
    ],
)
def test_valid_basket_counts(description, total, expected):
    assert fruit_distribution(description, total) == expected


@pytest.mark.parametrize(
    "description",
    [
        pytest.param("5 apples and 6 oranges", id="apples-first"),
        pytest.param("6 oranges and 5 apples", id="oranges-first"),
    ],
)
def test_fruit_order_does_not_change_count(description):
    assert fruit_distribution(description, 19) == 8


@pytest.mark.parametrize("total,expected", [(11, 0), (12, 1), (19, 8), (100, 89)])
def test_total_controls_remaining_mangoes(total, expected):
    assert fruit_distribution("5 apples and 6 oranges", total) == expected
