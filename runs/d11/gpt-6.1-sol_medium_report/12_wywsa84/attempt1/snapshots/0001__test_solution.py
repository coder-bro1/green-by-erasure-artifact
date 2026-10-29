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
    ids=["empty-lists", "shorter-second", "shorter-first", "sum-all-strings", "digits"],
)
def test_docstring_examples(first, second, expected):
    assert total_match(first, second) == expected


@pytest.mark.parametrize(
    ("first", "second", "winner"),
    [
        ([], ["hello"], 0),
        (["hello"], [], 1),
        ([""], [], 0),
        ([], ["", ""], 0),
        (["ab", "c"], ["xyz"], 0),
        (["abc"], ["x", "yz"], 0),
        (["long"], ["a", "b", "c"], 1),
        (["a", "b", "c"], ["long"], 0),
        (["", "abcd", ""], ["abc"], 1),
        ([" \t\n"], ["ab"], 1),
        (["é🙂"], ["abc"], 0),
        (["abc"], ["é🙂"], 1),
        (["a" * 10000], ["b" * 9999], 1),
    ],
    ids=[
        "first-empty",
        "second-empty",
        "empty-string-tie",
        "empty-list-tie",
        "tie-different-list-lengths",
        "tie-reversed-grouping",
        "fewer-items-can-be-longer",
        "more-items-can-be-shorter",
        "ignore-empty-strings-in-total",
        "count-whitespace",
        "unicode-first",
        "unicode-second",
        "long-strings",
    ],
)
def test_returns_original_list_with_smallest_character_total(first, second, winner):
    first_before = first.copy()
    second_before = second.copy()

    result = total_match(first, second)

    assert result is (first if winner == 0 else second)
    assert first == first_before
    assert second == second_before


def test_same_list_as_both_arguments():
    strings = ["hello", "", "world"]

    assert total_match(strings, strings) is strings
    assert strings == ["hello", "", "world"]
