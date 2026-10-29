"""Tests for the documented contract, with known defects recorded explicitly."""

import pytest

from solution import fewer_letters


WRONG_SELECTION = pytest.mark.xfail(
    strict=True,
    reason="Implementation selects the larger character total instead of the smaller",
)
WRONG_TIE = pytest.mark.xfail(
    strict=True,
    reason="Implementation returns second on a tie instead of first",
)


@pytest.mark.parametrize(
    "first, second, expected",
    [
        pytest.param(["ab", "c"], ["xyz", "w"], ["ab", "c"],
                     marks=WRONG_SELECTION, id="docstring-first-smaller"),
        pytest.param(["long"], ["a", "b"], ["a", "b"],
                     marks=WRONG_SELECTION, id="docstring-second-smaller"),
        pytest.param([], [], [], id="docstring-both-empty"),
        pytest.param([], ["a"], [], marks=WRONG_SELECTION, id="first-empty"),
        pytest.param(["a"], [], [], marks=WRONG_SELECTION, id="second-empty"),
        pytest.param(["", ""], ["a"], ["", ""],
                     marks=WRONG_SELECTION, id="empty-strings-count-as-zero"),
        pytest.param(["abcdef"], ["a", "b", "c"], ["a", "b", "c"],
                     marks=WRONG_SELECTION, id="characters-not-list-length"),
        pytest.param(["a", "bc"], ["d", "ef"], ["a", "bc"],
                     marks=WRONG_TIE, id="equal-totals-different-strings"),
        pytest.param(["é", "猫"], ["abc"], ["é", "猫"],
                     marks=WRONG_SELECTION, id="unicode-character-count"),
        pytest.param(["a b"], ["xy"], ["xy"],
                     marks=WRONG_SELECTION, id="spaces-count-as-characters"),
        pytest.param(["same"], ["same"], ["same"], id="identical-values"),
    ],
)
def test_selects_list_with_fewer_characters(first, second, expected):
    assert fewer_letters(first, second) == expected


@WRONG_TIE
@pytest.mark.parametrize("values", [[], [""], ["same"]])
def test_tie_returns_first_list_object(values):
    first = list(values)
    second = list(values)

    assert fewer_letters(first, second) is first


@pytest.mark.parametrize(
    "first, second",
    [([], []), (["a"], ["long"]), (["long"], ["a"]), (["ab"], ["cd"])],
)
def test_does_not_mutate_inputs(first, second):
    original_first = first.copy()
    original_second = second.copy()

    fewer_letters(first, second)

    assert first == original_first
    assert second == original_second


def test_same_list_returns_original_object():
    values = ["ab", "", "猫"]

    assert fewer_letters(values, values) is values
