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
        ("aabb", False),
        ("xyy", False),
        ("aab", False),
        ("aba", False),
        ("baa", False),
        ("abca", True),
        ("abac", True),
        ("abcb", False),
        ("abcdef", True),
        ("abcdaef", True),
    ],
)
def test_is_happy(value, expected):
    assert is_happy(value) is expected
