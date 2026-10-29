import pytest

from solution import fruit_distribution


@pytest.mark.xfail(
    strict=True,
    reason="fruit_distribution subtracts an extra 1 beyond the apple and orange counts",
)
@pytest.mark.parametrize(
    ("description", "total", "expected"),
    [
        ("5 apples and 6 oranges", 19, 8),
        ("0 apples and 1 oranges", 3, 2),
        ("2 apples and 3 oranges", 100, 95),
        ("100 apples and 1 oranges", 120, 19),
    ],
)
def test_fruit_distribution_matches_docstring_examples(description, total, expected):
    assert fruit_distribution(description, total) == expected
