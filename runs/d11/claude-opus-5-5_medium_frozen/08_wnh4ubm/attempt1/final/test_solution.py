import pytest

from solution import fruit_distribution


@pytest.mark.parametrize(
    "s, n, expected",
    [
        # Examples from the docstring
        ("5 apples and 6 oranges", 19, 8),
        ("0 apples and 1 oranges", 3, 2),
        ("2 apples and 3 oranges", 100, 95),
        ("100 apples and 1 oranges", 120, 19),
        # Additional cases
        ("1 apples and 0 oranges", 3, 2),
        ("0 apples and 0 oranges", 0, 0),
        ("0 apples and 0 oranges", 10, 10),
        ("10 apples and 20 oranges", 30, 0),
        ("1 apples and 100 oranges", 120, 19),
    ],
)
def test_spec_values(s, n, expected):
    assert fruit_distribution(s, n) == expected


def test_result_increases_by_one_with_n():
    s = "5 apples and 6 oranges"
    assert fruit_distribution(s, 20) - fruit_distribution(s, 19) == 1


def test_order_of_counts_does_not_matter():
    assert fruit_distribution("3 apples and 7 oranges", 50) == fruit_distribution(
        "7 apples and 3 oranges", 50
    )


def test_returns_int():
    assert isinstance(fruit_distribution("1 apples and 2 oranges", 10), int)
