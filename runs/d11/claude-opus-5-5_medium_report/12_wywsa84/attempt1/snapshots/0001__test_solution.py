import pytest

from solution import total_match


@pytest.mark.parametrize(
    "lst1, lst2, expected",
    [
        ([], [], []),
        (["hi", "admin"], ["hI", "Hi"], ["hI", "Hi"]),
        (["hi", "admin"], ["hi", "hi", "admin", "project"], ["hi", "admin"]),
        (["hi", "admin"], ["hI", "hi", "hi"], ["hI", "hi", "hi"]),
        (["4"], ["1", "2", "3", "4", "5"], ["4"]),
    ],
)
def test_docstring_examples(lst1, lst2, expected):
    assert total_match(lst1, lst2) == expected


def test_first_list_smaller():
    assert total_match(["a"], ["bb"]) == ["a"]


def test_second_list_smaller():
    assert total_match(["abc"], ["ab"]) == ["ab"]


def test_equal_counts_returns_first_list_identity():
    a, b = ["ab", "c"], ["abc"]
    assert total_match(a, b) is a


def test_returns_original_object_not_copy():
    a, b = ["xyz"], ["x"]
    assert total_match(a, b) is b


def test_empty_vs_nonempty():
    assert total_match([], ["a"]) == []
    assert total_match(["a"], []) == []


def test_empty_strings_count_as_zero():
    a = ["", "", ""]
    b = ["a"]
    assert total_match(a, b) is a
    assert total_match(b, a) is a


def test_counts_chars_not_number_of_elements():
    # lst1 has more elements but fewer total chars
    assert total_match(["a", "b", "c"], ["abcd"]) == ["a", "b", "c"]


def test_whitespace_and_unicode_counted_as_chars():
    assert total_match([" ", "é"], ["abc"]) == [" ", "é"]
    assert total_match(["日本語"], ["ab"]) == ["ab"]


def test_inputs_not_mutated():
    a, b = ["hi", "admin"], ["hI", "Hi"]
    total_match(a, b)
    assert a == ["hi", "admin"]
    assert b == ["hI", "Hi"]
