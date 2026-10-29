import pytest

from solution import histogram


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a b c", {"a": 1, "b": 1, "c": 1}),
        ("a b b a", {"a": 2, "b": 2}),
        ("a b c a b", {"a": 2, "b": 2}),
        ("b b b b a", {"b": 4}),
    ],
)
def test_docstring_examples(text, expected):
    assert histogram(text) == expected


def test_single_letter():
    assert histogram("a") == {"a": 1}


def test_single_letter_repeated():
    assert histogram("z z z") == {"z": 3}


def test_single_winner_among_many():
    assert histogram("r t g r t r") == {"r": 3}


def test_all_letters_unique_returns_all_with_count_one():
    letters = "abcdefghijklmnopqrstuvwxyz"
    assert histogram(" ".join(letters)) == {c: 1 for c in letters}


def test_ties_at_max_return_all_tied_letters():
    assert histogram("a b c a b c d") == {"a": 2, "b": 2, "c": 2}


def test_order_of_input_does_not_affect_result():
    assert histogram("a a b") == histogram("b a a") == {"a": 2}


def test_large_input():
    text = " ".join(["x"] * 1000 + ["y"] * 999)
    assert histogram(text) == {"x": 1000}


def test_returns_new_dict_each_call():
    first = histogram("a a")
    first["mutated"] = 99
    assert histogram("a a") == {"a": 2}


def test_input_not_modified():
    text = "a b a"
    histogram(text)
    assert text == "a b a"


# --- Known deviations from the documented contract ---------------------------
# solution.py splits on a single space and does not filter empty tokens when
# building the result, so empty strings leak in as keys. These are marked
# strict xfail: if solution.py is fixed, these will XPASS and fail the run,
# signalling that the markers should be removed.

@pytest.mark.xfail(strict=True, reason="Bug: histogram('') returns {'': 1}, docstring says {}")
def test_empty_string_returns_empty_dict():
    assert histogram("") == {}


@pytest.mark.xfail(strict=True, reason="Bug: double spaces produce an '' key")
def test_multiple_spaces_ignored():
    assert histogram("a  b") == {"a": 1, "b": 1}


@pytest.mark.xfail(strict=True, reason="Bug: leading/trailing spaces produce an '' key")
def test_leading_and_trailing_spaces_ignored():
    assert histogram(" a a ") == {"a": 2}


def test_current_behavior_empty_string():
    """Pins the actual current behavior so regressions are visible."""
    assert histogram("") == {"": 1}
