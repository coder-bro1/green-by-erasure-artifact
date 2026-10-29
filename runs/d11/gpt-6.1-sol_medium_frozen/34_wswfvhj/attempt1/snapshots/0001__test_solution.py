"""Tests for total_match's current behavior, which differs from its docstring."""

import pytest

from solution import total_match


@pytest.mark.parametrize(
    "first, second, expected_index",
    [
        pytest.param([], [], 1, id="both-empty"),
        pytest.param([], ["hello"], 1, id="first-empty"),
        pytest.param(["hello"], [], 0, id="second-empty"),
        pytest.param(["hi", "admin"], ["hI", "Hi"], 0, id="first-longer"),
        pytest.param(
            ["hi", "admin"], ["hi", "hi", "admin", "project"], 1,
            id="second-longer",
        ),
        pytest.param(["hi", "admin"], ["hI", "hi", "hi"], 0, id="sum-lengths"),
        pytest.param(["4"], ["1", "2", "3", "4", "5"], 1, id="numeric-strings"),
        pytest.param(["abcd"], ["a", "b", "c"], 0, id="length-not-item-count"),
        pytest.param(["a", "bc"], ["def"], 1, id="equal-nonzero-totals"),
        pytest.param([""], ["", ""], 1, id="equal-zero-totals"),
        pytest.param(["", "abc", ""], ["ab"], 0, id="empty-strings"),
        pytest.param([" \t\n"], ["ab"], 0, id="whitespace-counts"),
        pytest.param(["\u00e9\U0001f600"], ["abc"], 1, id="unicode-character-not-byte-length"),
        pytest.param(["e\u0301"], ["x"], 0, id="combining-code-points-count"),
        pytest.param(["x" * 10000], ["y" * 9999], 0, id="long-strings"),
    ],
)
def test_total_match_returns_original_list_with_larger_total(
    first, second, expected_index
):
    first_before = first.copy()
    second_before = second.copy()

    result = total_match(first, second)

    assert result is (first, second)[expected_index]
    assert first == first_before
    assert second == second_before


def test_total_match_accepts_same_list_as_both_arguments():
    values = ["hello", "", "world"]

    assert total_match(values, values) is values
    assert values == ["hello", "", "world"]
