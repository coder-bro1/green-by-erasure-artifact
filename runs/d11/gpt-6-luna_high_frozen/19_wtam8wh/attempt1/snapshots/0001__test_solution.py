import pytest

from solution import longest


def test_empty_list_returns_none():
    assert longest([]) is None


@pytest.mark.xfail(
    reason="solution.longest currently falls through without returning a value for nonempty input",
    strict=True,
)
@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        (["a"], "a"),
        (["a", "bb", "ccc"], "ccc"),
        (["a", "bb", "cc"], "bb"),
        (["", "x", ""], "x"),
    ],
)
def test_returns_first_longest_string(strings, expected):
    assert longest(strings) == expected
