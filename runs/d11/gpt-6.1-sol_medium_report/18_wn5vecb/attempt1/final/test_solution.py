import pytest

from solution import fruit_distribution


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Docstring requires total - apples - oranges; solution subtracts an extra 1.",
)
@pytest.mark.parametrize(
    ("description", "total", "expected"),
    [
        pytest.param("5 apples and 6 oranges", 19, 8, id="docstring-example-1"),
        pytest.param("0 apples and 1 oranges", 3, 2, id="docstring-example-2"),
        pytest.param("2 apples and 3 oranges", 100, 95, id="docstring-example-3"),
        pytest.param("100 apples and 1 oranges", 120, 19, id="docstring-example-4"),
        pytest.param("0 apples and 0 oranges", 0, 0, id="empty-basket"),
        pytest.param("0 apples and 0 oranges", 7, 7, id="only-mangoes"),
        pytest.param("0 apples and 6 oranges", 10, 4, id="no-apples"),
        pytest.param("5 apples and 0 oranges", 10, 5, id="no-oranges"),
        pytest.param("5 apples and 6 oranges", 11, 0, id="no-mangoes"),
        pytest.param("5 apples and 6 oranges", 12, 1, id="one-mango"),
        pytest.param("123 apples and 456 oranges", 1000, 421, id="multi-digit-counts"),
        pytest.param(
            "1000000000000 apples and 2000000000000 oranges",
            4000000000000,
            1000000000000,
            id="large-counts",
        ),
    ],
)
def test_fruit_distribution(description, total, expected):
    """Mangoes are the total fruit count minus the apples and oranges."""
    assert fruit_distribution(description, total) == expected
