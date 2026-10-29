import pytest

from solution import longest


@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        pytest.param([], None, id="empty-list"),
        pytest.param(["hello"], "hello", id="single-string"),
        pytest.param([""], "", id="single-empty-string"),
        pytest.param(["", "", ""], "", id="all-empty-strings"),
        pytest.param(["a", "bb", "ccc"], "ccc", id="longest-last"),
        pytest.param(["longest", "mid", "a"], "longest", id="longest-first"),
        pytest.param(["a", "longest", "bb"], "longest", id="longest-middle"),
        pytest.param(["a", "b", "c"], "a", id="all-lengths-tied"),
        pytest.param(["a", "first", "later"], "first", id="maximum-length-tie"),
        pytest.param(["", "text", ""], "text", id="mixed-empty-strings"),
        pytest.param(["abc", "    ", "xy"], "    ", id="whitespace-counts"),
        pytest.param(["abc", "\n\t\r\n"], "\n\t\r\n", id="control-characters-count"),
        pytest.param(["éé", "猫猫猫", "😀"], "猫猫猫", id="unicode-length"),
    ],
)
def test_longest(strings, expected):
    assert longest(strings) == expected


def test_longest_does_not_modify_input():
    strings = ["short", "the longest string", "", "medium"]
    original = strings.copy()

    longest(strings)

    assert strings == original
