import pytest

from solution import total_match


@pytest.mark.parametrize(
    ("lst1", "lst2", "expected"),
    [
        ([], [], []),
        (["hi", "admin"], ["hI", "Hi"], ["hI", "Hi"]),
        (
            ["hi", "admin"],
            ["hi", "hi", "admin", "project"],
            ["hi", "admin"],
        ),
        (["hi", "admin"], ["hI", "hi", "hi"], ["hI", "hi", "hi"]),
        (["4"], ["1", "2", "3", "4", "5"], ["4"]),
    ],
)
def test_docstring_examples(lst1, lst2, expected):
    assert total_match(lst1, lst2) == expected


def test_equal_character_totals_return_first_list():
    first = ["a", "bc"]
    second = ["ab", "c"]

    assert total_match(first, second) is first


def test_empty_list_has_smaller_total_than_nonempty_list():
    empty = []

    assert total_match(empty, [""]) is empty


def test_more_strings_can_have_smaller_total_character_count():
    shorter_total = ["", "x", ""]
    longer_total = ["ab"]

    assert total_match(shorter_total, longer_total) is shorter_total


def test_unicode_strings_are_counted_by_python_string_length():
    one_character = ["é"]
    two_characters = ["e\u0301"]

    assert total_match(one_character, two_characters) is one_character
