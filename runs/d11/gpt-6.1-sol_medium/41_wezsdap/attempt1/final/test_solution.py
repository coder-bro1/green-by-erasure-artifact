import pytest

from solution import total_match


@pytest.mark.parametrize(
    "first, second, expected_index",
    [
        pytest.param([], [], 0, id="both-empty"),
        pytest.param(["hi", "admin"], ["hI", "Hi"], 1, id="example-second-shorter"),
        pytest.param(
            ["hi", "admin"], ["hi", "hi", "admin", "project"], 0,
            id="example-first-shorter",
        ),
        pytest.param(["hi", "admin"], ["hI", "hi", "hi"], 1, id="example-summed-lengths"),
        pytest.param(["4"], ["1", "2", "3", "4", "5"], 0, id="example-digit-strings"),
        pytest.param([], ["abc"], 0, id="first-empty"),
        pytest.param(["abc"], [], 1, id="second-empty"),
        pytest.param(["ab", "c"], ["xyz"], 0, id="tie-different-list-lengths"),
        pytest.param(["abc"], ["xyz"], 0, id="tie-different-contents"),
        pytest.param(["", ""], [], 0, id="tie-empty-strings"),
        pytest.param(["", "a", ""], ["ab"], 0, id="empty-strings-add-no-length"),
        pytest.param(["abcdef"], ["a", "b", "c"], 1, id="fewer-items-can-be-longer"),
        pytest.param(["a", "b", "c"], ["abcdef"], 0, id="more-items-can-be-shorter"),
        pytest.param([" ", "\t", "\n"], ["ab"], 1, id="whitespace-counts"),
        pytest.param(["\u00e9", "\U0001f600"], ["abc"], 0, id="unicode-characters-not-bytes"),
        pytest.param(["e\u0301"], ["x"], 1, id="combining-mark-counts-separately"),
        pytest.param(["a", "a", "a"], ["bb"], 1, id="duplicate-strings-count"),
        pytest.param(["z"], ["aa"], 0, id="length-not-lexicographic-order"),
    ],
)
def test_total_match(first, second, expected_index):
    first_before = first.copy()
    second_before = second.copy()

    result = total_match(first, second)

    assert result is (first, second)[expected_index]
    assert first == first_before
    assert second == second_before


def test_total_match_with_same_list_for_both_arguments():
    strings = ["hello", "", "world"]

    assert total_match(strings, strings) is strings
    assert strings == ["hello", "", "world"]
