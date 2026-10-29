import pytest

from solution import total_match


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ([], [], []),
        (["hi", "admin"], ["hI", "Hi"], ["hI", "Hi"]),
        (["hi", "admin"], ["hi", "hi", "admin", "project"], ["hi", "admin"]),
        (["hi", "admin"], ["hI", "hi", "hi"], ["hI", "hi", "hi"]),
        (["4"], ["1", "2", "3", "4", "5"], ["4"]),
    ],
)
def test_total_match_examples(first, second, expected):
    assert total_match(first, second) == expected


def test_compares_total_characters_instead_of_number_of_items():
    first = ["a", "b", "c", "d", "e", "f"]
    second = ["longer"]

    assert total_match(first, second) is second


def test_handles_empty_strings():
    first = ["", "x"]
    second = ["y"]

    assert total_match(first, second) == second


def test_equal_totals_with_equal_values():
    first = ["same", "length"]
    second = ["same", "length"]

    assert total_match(first, second) == first
