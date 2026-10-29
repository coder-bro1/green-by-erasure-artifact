import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    ("source", "deleted", "expected"),
    [
        ("abcdef", "b", "acdef"),
        ("abcdedcba", "ab", "cdedc"),
        ("banana", "an", "b"),
        ("hello", "", "hello"),
        ("", "abc", ""),
    ],
)
def test_removes_all_matching_characters_and_preserves_order(source, deleted, expected):
    result, _ = reverse_delete(source, deleted)

    assert result == expected
    assert not any(char in deleted for char in result)


def test_flag_is_true_for_a_non_palindrome():
    assert reverse_delete("abcdef", "b") == ("acdef", True)


def test_flag_is_false_for_a_palindrome():
    assert reverse_delete("abcdedcba", "ab") == ("cdedc", False)


def test_flag_is_false_when_everything_is_deleted():
    assert reverse_delete("abc", "abc") == ("", False)
