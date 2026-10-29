import pytest

from solution import fruit_distribution


@pytest.mark.parametrize(
    ("description", "total", "expected_mangoes"),
    [
        pytest.param("5 apples and 6 oranges", 19, 8, id="example-1"),
        pytest.param("0 apples and 1 oranges", 3, 2, id="example-2"),
        pytest.param("2 apples and 3 oranges", 100, 95, id="example-3"),
        pytest.param("100 apples and 1 oranges", 120, 19, id="example-4"),
        pytest.param("0 apples and 0 oranges", 0, 0, id="empty-basket"),
        pytest.param("0 apples and 0 oranges", 12, 12, id="only-mangoes"),
        pytest.param("7 apples and 0 oranges", 10, 3, id="no-oranges"),
        pytest.param("0 apples and 8 oranges", 10, 2, id="no-apples"),
        pytest.param("7 apples and 8 oranges", 15, 0, id="no-mangoes"),
        pytest.param("12 apples and 34 oranges", 50, 4, id="multi-digit-counts"),
        pytest.param("6 oranges and 5 apples", 19, 8, id="reversed-order"),
        pytest.param(
            "1000000000000 apples and 2000000000000 oranges",
            3000000000007,
            7,
            id="large-counts",
        ),
    ],
)
def test_fruit_distribution(description, total, expected_mangoes):
    assert fruit_distribution(description, total) == expected_mangoes


@pytest.mark.parametrize("apples", [0, 1, 25])
@pytest.mark.parametrize("oranges", [0, 1, 30])
@pytest.mark.parametrize("mangoes", [0, 1, 40])
def test_fruit_distribution_recovers_mango_count(apples, oranges, mangoes):
    description = f"{apples} apples and {oranges} oranges"
    total = apples + oranges + mangoes

    assert fruit_distribution(description, total) == mangoes
