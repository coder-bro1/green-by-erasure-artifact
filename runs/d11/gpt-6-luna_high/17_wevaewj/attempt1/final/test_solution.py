import pytest

from solution import fruit_distribution


@pytest.mark.parametrize(
    ("description", "total", "expected"),
    [
        ("5 apples and 6 oranges", 19, 8),
        ("0 apples and 1 oranges", 3, 2),
        ("2 apples and 3 oranges", 100, 95),
        ("100 apples and 1 oranges", 120, 19),
        ("0 apples and 0 oranges", 0, 0),
        ("12 apples and 34 oranges", 60, 14),
    ],
)
def test_fruit_distribution(description, total, expected):
    assert fruit_distribution(description, total) == expected
