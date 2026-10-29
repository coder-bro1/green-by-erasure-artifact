import pytest

from solution import is_happy


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", False),
        ("a", False),
        ("ab", False),
        ("abc", True),
        ("abcd", True),
        ("adb", True),
        ("aab", False),
        ("abb", False),
        ("aba", False),
        ("aaa", False),
        ("aabb", False),
        ("xyy", False),
        ("abca", True),
        ("abcb", False),
        ("a!b", True),
    ],
)
def test_is_happy(value, expected):
    assert is_happy(value) is expected
