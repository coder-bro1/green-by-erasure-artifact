import pytest

from solution import longest


@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        pytest.param([], None, id="empty-list"),
        pytest.param([""], "", id="single-empty-string"),
        pytest.param(["hello"], "hello", id="single-string"),
        pytest.param(["", "", ""], "", id="all-empty-strings"),
        pytest.param(["a", "b", "c"], "a", id="equal-length-first-wins"),
        pytest.param(["a", "bb", "ccc"], "ccc", id="longest-last"),
        pytest.param(["longest", "bb", "a"], "longest", id="longest-first"),
        pytest.param(["a", "longest", "bb"], "longest", id="longest-middle"),
        pytest.param(["a", "first", "last!"], "first", id="tied-longest"),
        pytest.param(["", "abc", ""], "abc", id="mixed-empty-strings"),
        pytest.param(["a", "   ", "bb"], "   ", id="whitespace-counts"),
        pytest.param(["é", "你好", "abc"], "abc", id="unicode-character-length"),
    ],
)
def test_longest(strings, expected):
    assert longest(strings) == expected


def test_longest_does_not_modify_input():
    strings = ["short", "the longest", "middle"]
    original = strings.copy()

    longest(strings)

    assert strings == original
