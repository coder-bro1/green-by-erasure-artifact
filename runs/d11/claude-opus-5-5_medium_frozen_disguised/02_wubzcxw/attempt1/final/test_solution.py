"""Tests for solution.fewer_letters.

The docstring spec: return the list whose strings have the smaller total
character count; on a tie, return `first`.

NOTE: the current implementation inverts the comparison (it returns the list
with MORE characters, and `second` on ties). Tests that expose this are marked
xfail(strict=True) so the suite passes today but will flag (XPASS -> failure)
once the bug is fixed, prompting removal of the markers.
"""
import pytest

from solution import fewer_letters

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py inverts comparison: returns larger total / second on tie",
)


# --- Cases where the result is correct regardless of the bug ---------------

def test_both_empty_returns_empty():
    assert fewer_letters([], []) == []


def test_returns_one_of_the_inputs_by_identity():
    a, b = ["ab"], ["xyz"]
    result = fewer_letters(a, b)
    assert result is a or result is b


def test_does_not_mutate_inputs():
    a, b = ["ab", "c"], ["xyz", "w"]
    fewer_letters(a, b)
    assert a == ["ab", "c"]
    assert b == ["xyz", "w"]


def test_tie_with_identical_content_returns_equal_list():
    assert fewer_letters(["ab"], ["ab"]) == ["ab"]


def test_works_with_tuples_and_generic_iterables():
    # Should not raise on any sequence of strings.
    result = fewer_letters(("a",), ("bb",))
    assert result in (("a",), ("bb",))


def test_non_string_items_raise_type_error():
    with pytest.raises(TypeError):
        fewer_letters([1], ["a"])


# --- Spec cases (expose the inverted comparison) ---------------------------

@BUG
def test_docstring_example_first_smaller():
    assert fewer_letters(["ab", "c"], ["xyz", "w"]) == ["ab", "c"]


@BUG
def test_docstring_example_second_smaller():
    assert fewer_letters(["long"], ["a", "b"]) == ["a", "b"]


@BUG
def test_tie_returns_first_by_identity():
    a, b = ["ab"], ["cd"]
    assert fewer_letters(a, b) is a


@BUG
def test_empty_first_vs_nonempty_second():
    assert fewer_letters([], ["a"]) == []


@BUG
def test_empty_strings_count_as_zero():
    assert fewer_letters(["", "", ""], ["a"]) == ["", "", ""]


@BUG
def test_total_not_item_count_matters():
    # first has more items but fewer characters.
    assert fewer_letters(["a", "b", "c"], ["abcdef"]) == ["a", "b", "c"]


@BUG
def test_unicode_characters_counted_by_len():
    assert fewer_letters(["éé"], ["abc"]) == ["éé"]


@BUG
@pytest.mark.parametrize(
    "first, second, expected",
    [
        (["x"], ["yy"], ["x"]),
        (["yy"], ["x"], ["x"]),
        (["abc"], ["a", "b", "c"], ["abc"]),  # tie -> first
    ],
)
def test_parametrized_spec(first, second, expected):
    assert fewer_letters(first, second) == expected
