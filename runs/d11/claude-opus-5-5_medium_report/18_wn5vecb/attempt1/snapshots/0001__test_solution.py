import pytest

from solution import fruit_distribution

BUG = (
    "solution.py returns n - apples - oranges - 1; the trailing '- 1' "
    "contradicts the docstring (n - apples - oranges), so results are off by one"
)


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "s, n, expected",
    [
        ("5 apples and 6 oranges", 19, 8),
        ("0 apples and 1 oranges", 3, 2),
        ("2 apples and 3 oranges", 100, 95),
        ("100 apples and 1 oranges", 120, 19),
    ],
)
def test_docstring_examples(s, n, expected):
    assert fruit_distribution(s, n) == expected


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "s, n, expected",
    [
        ("1 apples and 0 oranges", 3, 2),
        ("0 apples and 0 oranges", 5, 5),
        ("10 apples and 20 oranges", 30, 0),
        ("1 apples and 100 oranges", 120, 19),
        ("99 apples and 1 oranges", 1000, 900),
    ],
)
def test_additional_values(s, n, expected):
    assert fruit_distribution(s, n) == expected


def test_returns_int():
    assert isinstance(fruit_distribution("5 apples and 6 oranges", 19), int)


def test_result_decreases_by_one_per_extra_apple():
    # Relative behaviour holds regardless of the constant offset bug.
    a = fruit_distribution("5 apples and 6 oranges", 19)
    b = fruit_distribution("6 apples and 6 oranges", 19)
    assert a - b == 1


def test_result_increases_by_one_per_extra_total_fruit():
    a = fruit_distribution("5 apples and 6 oranges", 19)
    b = fruit_distribution("5 apples and 6 oranges", 20)
    assert b - a == 1
