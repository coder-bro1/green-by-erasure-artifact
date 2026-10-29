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
        (["a", "b"], ["ab"], ["a", "b"]),
        (["longer"], ["x", "y"], ["x", "y"]),
        ([""], [], [""]),
    ],
)
def test_total_match_returns_list_with_fewer_total_characters(lst1, lst2, expected):
    assert total_match(lst1, lst2) == expected


def test_total_match_returns_first_list_when_character_totals_tie():
    first = ["one", "two"]
    second = ["abcdef"]

    result = total_match(first, second)

    assert result == first
    assert result is first


def test_total_match_does_not_modify_inputs():
    first = ["hello", "world"]
    second = ["hi", "there"]
    original_first = first.copy()
    original_second = second.copy()

    total_match(first, second)

    assert first == original_first
    assert second == original_second
