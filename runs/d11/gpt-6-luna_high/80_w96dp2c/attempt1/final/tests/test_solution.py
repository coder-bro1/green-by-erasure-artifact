import pytest

from solution import total_match


@pytest.mark.parametrize(
    ("lst1", "lst2", "expected"),
    [
        (["hi", "admin"], ["hi", "hi", "admin", "project"], 0),
        (["hi", "admin"], ["hI", "hi", "hi"], 1),
        (["4"], ["1", "2", "3", "4", "5"], 0),
    ],
)
def test_returns_list_with_fewer_total_characters(lst1, lst2, expected):
    result = total_match(lst1, lst2)

    assert result is (lst1, lst2)[expected]


def test_equal_character_totals_return_first_list():
    lst1 = ["ab", "c"]
    lst2 = ["a", "bc"]

    assert total_match(lst1, lst2) is lst1


def test_two_empty_lists_return_first_list():
    lst1 = []
    lst2 = []

    assert total_match(lst1, lst2) is lst1

