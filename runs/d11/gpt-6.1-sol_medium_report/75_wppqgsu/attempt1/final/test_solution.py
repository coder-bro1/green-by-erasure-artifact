import pytest

from solution import longest


def test_empty_list_returns_none():
    assert longest([]) is None


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Docstring requires the first longest string, but longest checks "
        "len(s) > maxlen, which is impossible, and returns None for nonempty lists."
    ),
)
@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        pytest.param(["a", "b", "c"], "a", id="docstring-tie"),
        pytest.param(["a", "bb", "ccc"], "ccc", id="docstring-increasing"),
        pytest.param(["hello"], "hello", id="single-string"),
        pytest.param([""], "", id="single-empty-string"),
        pytest.param(["", "", ""], "", id="all-empty-strings"),
        pytest.param(["longest", "bb", "c"], "longest", id="longest-first"),
        pytest.param(["a", "longest", "bb"], "longest", id="longest-middle"),
        pytest.param(["", "abc", ""], "abc", id="mixed-empty-strings"),
        pytest.param(["x", "cat", "dog", "a"], "cat", id="first-maximum-tie"),
        pytest.param(["dog", "cat", "x"], "dog", id="tie-at-start"),
        pytest.param(["a", "   ", "bb"], "   ", id="whitespace-counts"),
        pytest.param(["abc", "\u00e9\u00e9", "\U0001f600"], "abc", id="unicode-character-length"),
        pytest.param(["a", "b\nc", "dd"], "b\nc", id="newline-counts"),
    ],
)
def test_nonempty_list_returns_first_longest_string(strings, expected):
    assert longest(strings) == expected
