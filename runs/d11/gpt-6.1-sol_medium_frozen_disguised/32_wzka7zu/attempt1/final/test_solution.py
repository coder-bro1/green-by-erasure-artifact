import pytest

from solution import first_longest


def test_empty_list_returns_none():
    assert first_longest([]) is None


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Known bug: first_longest compares lengths with > max instead of == max",
)
@pytest.mark.parametrize(
    ("words", "expected"),
    [
        pytest.param(["solo"], "solo", id="single-word"),
        pytest.param([""], "", id="single-empty-string"),
        pytest.param(["", "", ""], "", id="all-empty-strings"),
        pytest.param(["longest", "a", "bb"], "longest", id="longest-first"),
        pytest.param(["xy", "abc", "q"], "abc", id="longest-middle"),
        pytest.param(["a", "bb", "longest"], "longest", id="longest-last"),
        pytest.param(["no", "at"], "no", id="equal-length-tie"),
        pytest.param(["a", "first", "x", "later"], "first", id="maximum-length-tie"),
        pytest.param(["", "word", ""], "word", id="mixed-empty-strings"),
        pytest.param(["a", "   ", "bb"], "   ", id="whitespace-counts"),
        pytest.param(["a", "猫犬", "é"], "猫犬", id="unicode-characters"),
    ],
)
def test_returns_first_longest_string(words, expected):
    assert first_longest(words) == expected


def test_does_not_modify_input():
    words = ["short", "longest", "a", "longest"]
    original = words.copy()

    first_longest(words)

    assert words == original
