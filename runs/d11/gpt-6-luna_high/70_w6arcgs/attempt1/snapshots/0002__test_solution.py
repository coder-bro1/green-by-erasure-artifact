import pytest

from solution import fruit_distribution


@pytest.mark.parametrize(
    ("description", "total", "expected"),
    [
        ("5 apples and 6 oranges", 19, 8),
        ("0 apples and 1 oranges", 3, 2),
        ("2 apples and 3 oranges", 100, 95),
        ("100 apples and 1 oranges", 120, 19),
    ],
)
def test_fruit_distribution(description, total, expected):
    assert fruit_distribution(description, total) == expected


def test_fruit_distribution_with_zero_apples_and_oranges():
    assert fruit_distribution("0 apples and 0 oranges", 7) == 7


def test_fruit_distribution_when_no_mangoes_remain():
    assert fruit_distribution("4 apples and 6 oranges", 10) == 0
