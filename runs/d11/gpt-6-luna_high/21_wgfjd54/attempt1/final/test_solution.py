import pytest

from solution import longest


@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        ([], None),
        (["a", "bb", "ccc"], "ccc"),
        (["first", "other", "longest"], "longest"),
        (["same", "size", "last"], "same"),
        (["only"], "only"),
        (["", ""], ""),
        (["é", "漢字", "abc"], "abc"),
    ],
)
def test_longest(strings, expected):
    assert longest(strings) == expected
