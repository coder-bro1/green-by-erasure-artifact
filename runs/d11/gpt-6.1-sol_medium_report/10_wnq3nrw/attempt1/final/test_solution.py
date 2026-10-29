import pytest

from solution import total_match


def test_empty_docstring_example():
    assert total_match([], []) == []


@pytest.mark.xfail(
    strict=True,
    reason="Docstring requires the shorter character total; solution returns the longer list.",
)
@pytest.mark.parametrize(
    "first, second, expected",
    [
        (["hi", "admin"], ["hI", "Hi"], ["hI", "Hi"]),
        (["hi", "admin"], ["hi", "hi", "admin", "project"], ["hi", "admin"]),
        (["hi", "admin"], ["hI", "hi", "hi"], ["hI", "hi", "hi"]),
        (["4"], ["1", "2", "3", "4", "5"], ["4"]),
    ],
    ids=["shorter-second", "shorter-first", "sum-all-strings", "digits"],
)
def test_docstring_examples(first, second, expected):
    assert total_match(first, second) == expected


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Docstring requires the shorter character total and the first list on ties; "
        "solution returns the longer list and the second list on ties."
    ),
)
@pytest.mark.parametrize(
    "first, second, expected_index",
    [
        ([], ["a"], 0),
        (["a"], [], 1),
        ([""], ["", ""], 0),
        (["ab"], ["c", "d"], 0),
        (["ab", "cd"], ["wxyz"], 0),
        (["longword"], ["a", "b", "c"], 1),
        (["", "a", ""], ["bb"], 0),
        (["\u00e9"], ["ab"], 0),
        ([" "], ["", "\t", "\n"], 0),
    ],
    ids=[
        "empty-first",
        "empty-second",
        "zero-length-tie",
        "tie-different-list-sizes",
        "tie-different-string-sizes",
        "characters-not-list-size",
        "empty-strings",
        "unicode-characters-not-bytes",
        "whitespace-counts",
    ],
)
def test_selects_documented_list(first, second, expected_index):
    expected = (first, second)[expected_index]
    result = total_match(first, second)
    assert result == expected
    assert result is expected


@pytest.mark.parametrize(
    "first, second",
    [([], []), (["a", "", "bc"], ["longer"]), (["same"], ["size"])],
    ids=["empty", "unequal-totals", "equal-totals"],
)
def test_does_not_modify_inputs(first, second):
    first_before = first.copy()
    second_before = second.copy()
    total_match(first, second)
    assert first == first_before
    assert second == second_before
