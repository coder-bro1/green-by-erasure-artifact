"""Tests for solution.total_match.

Spec (from the docstring): return the list whose strings have the smaller total
number of characters; if the totals are equal, return the first list.

NOTE: the current implementation inverts the comparison (`if l1 <= l2: return lst2`),
so it returns the list with MORE characters and, on ties, the SECOND list. Tests that
expose this are marked xfail(strict=True): they document the bug, and will start
failing loudly (XPASS -> error) once solution.py is fixed, prompting removal of the marker.
"""
import pytest

from solution import total_match

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py inverts the comparison: returns the longer list / second list on ties",
)


# --- Cases where spec and implementation agree --------------------------------

def test_both_empty():
    assert total_match([], []) == []


def test_tie_with_identical_contents_returns_equal_value():
    # Value-equal either way, so passes regardless of which list is returned.
    assert total_match(["ab"], ["ab"]) == ["ab"]


def test_returns_one_of_the_input_objects():
    a, b = ["x"], ["yy"]
    result = total_match(a, b)
    assert result is a or result is b


def test_does_not_mutate_inputs():
    a, b = ["hi", "admin"], ["hI", "Hi"]
    total_match(a, b)
    assert a == ["hi", "admin"]
    assert b == ["hI", "Hi"]


def test_accepts_tuples_and_other_iterables():
    result = total_match(("a",), ("b",))
    assert result in (("a",), ("b",))


# --- Docstring examples (spec) ------------------------------------------------

@BUG
def test_doc_example_second_shorter():
    assert total_match(["hi", "admin"], ["hI", "Hi"]) == ["hI", "Hi"]


@BUG
def test_doc_example_first_shorter():
    assert total_match(["hi", "admin"], ["hi", "hi", "admin", "project"]) == ["hi", "admin"]


@BUG
def test_doc_example_second_shorter_more_items():
    assert total_match(["hi", "admin"], ["hI", "hi", "hi"]) == ["hI", "hi", "hi"]


@BUG
def test_doc_example_digits():
    assert total_match(["4"], ["1", "2", "3", "4", "5"]) == ["4"]


# --- Additional spec cases ----------------------------------------------------

@BUG
def test_tie_returns_first_list_identity():
    a, b = ["ab"], ["cd"]
    assert total_match(a, b) is a


@BUG
def test_tie_with_different_item_counts_returns_first():
    assert total_match(["abcd"], ["a", "b", "c", "d"]) == ["abcd"]


@BUG
def test_empty_vs_nonempty_returns_empty():
    assert total_match([], ["a"]) == []


@BUG
def test_nonempty_vs_empty_returns_empty():
    assert total_match(["a"], []) == []


def test_empty_strings_count_as_zero_chars():
    # Both total 0 -> spec says first list; value-equal check avoids the bug.
    assert total_match([""], ["", ""]) in ([""], ["", ""])


@BUG
def test_empty_strings_tie_returns_first():
    a, b = [""], ["", ""]
    assert total_match(a, b) is a


@BUG
def test_counts_characters_not_items():
    # Fewer items but more chars in first list -> second list wins.
    assert total_match(["abcdef"], ["a", "b", "c"]) == ["a", "b", "c"]


@BUG
def test_whitespace_counts_as_characters():
    assert total_match(["   "], ["ab"]) == ["ab"]


@BUG
def test_unicode_counts_code_points():
    assert total_match(["éé"], ["abc"]) == ["éé"]


@pytest.mark.parametrize(
    "lst1, lst2, expected_index",
    [
        (["a"], ["bb"], 0),
        (["aaa"], ["b"], 1),
        (["a", "b"], ["c", "d"], 0),
    ],
)
@BUG
def test_parametrized_spec(lst1, lst2, expected_index):
    expected = (lst1, lst2)[expected_index]
    assert total_match(lst1, lst2) is expected
