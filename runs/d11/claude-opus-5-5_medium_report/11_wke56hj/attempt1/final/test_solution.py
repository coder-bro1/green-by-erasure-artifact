import pytest

from solution import fruit_distribution


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


@pytest.mark.parametrize(
    "s, n, expected",
    [
        ("0 apples and 0 oranges", 0, 0),
        ("0 apples and 0 oranges", 7, 7),
        ("1 apples and 0 oranges", 1, 0),
        ("3 apples and 4 oranges", 7, 0),
        ("1000 apples and 2000 oranges", 5000, 2000),
        ("10 apples and 15 oranges", 30, 5),
    ],
)
def test_additional_cases(s, n, expected):
    assert fruit_distribution(s, n) == expected


def test_multi_digit_numbers_parsed_whole():
    assert fruit_distribution("12 apples and 34 oranges", 100) == 54


def test_extra_spaces_ignored():
    assert fruit_distribution("5  apples  and  6  oranges", 19) == 8


def test_return_type_is_int():
    result = fruit_distribution("5 apples and 6 oranges", 19)
    assert isinstance(result, int)
    assert result == 8


def test_does_not_mutate_input():
    s = "5 apples and 6 oranges"
    fruit_distribution(s, 19)
    assert s == "5 apples and 6 oranges"
