import pytest

from solution import remaining_mangoes


@pytest.mark.parametrize(
    "note, total, expected",
    [
        ("4 apples and 9 oranges", 30, 17),   # docstring example
        ("0 apples and 0 oranges", 7, 7),     # docstring example
        ("5 apples and 6 oranges", 19, 8),
        ("1 apples and 0 oranges", 1, 0),     # no mangoes left
        ("0 apples and 1 oranges", 5, 4),
        ("100 apples and 200 oranges", 1000, 700),
        ("2 apples and 3 oranges", 5, 0),
    ],
)
def test_remaining_mangoes(note, total, expected):
    assert remaining_mangoes(note, total) == expected


def test_only_apples_and_oranges_counted_with_no_fruit_and_empty_basket():
    assert remaining_mangoes("0 apples and 0 oranges", 0) == 0


def test_returns_int():
    assert isinstance(remaining_mangoes("4 apples and 9 oranges", 30), int)
