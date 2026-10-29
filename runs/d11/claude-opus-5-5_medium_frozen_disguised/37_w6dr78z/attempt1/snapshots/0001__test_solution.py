import pytest

from solution import break_text

COMMA_BUG = pytest.mark.xfail(
    strict=True,
    reason="Bug in solution.py: comma branch calls text.replace(' ', ',').split(), "
    "which splits on whitespace instead of commas, so the text is never split.",
)


# --- space branch -----------------------------------------------------------

@pytest.mark.parametrize(
    "text, expected",
    [
        ("one two", ["one", "two"]),
        ("a b c", ["a", "b", "c"]),
        ("  leading and trailing  ", ["leading", "and", "trailing"]),
        ("multiple   spaces", ["multiple", "spaces"]),
        ("tab\tand space", ["tab", "and", "space"]),
        (" ", []),
    ],
)
def test_space_splits_on_whitespace(text, expected):
    assert break_text(text) == expected


def test_space_takes_priority_over_comma():
    assert break_text("red,green blue") == ["red,green", "blue"]


# --- comma branch -----------------------------------------------------------

@COMMA_BUG
def test_docstring_comma_example():
    assert break_text("red,green") == ["red", "green"]


@COMMA_BUG
@pytest.mark.parametrize(
    "text, expected",
    [
        ("a,b,c", ["a", "b", "c"]),
        ("x,", ["x", ""]),
        (",", ["", ""]),
    ],
)
def test_comma_splits_on_commas(text, expected):
    assert break_text(text) == expected


def test_comma_result_is_a_list():
    assert isinstance(break_text("red,green"), list)


# --- counting branch --------------------------------------------------------

def test_docstring_count_example():
    assert break_text("bdx") == 3


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", 0),
        ("a", 0),          # position 0 (even)
        ("b", 1),          # position 1 (odd)
        ("abcdefghijklmnopqrstuvwxyz", 13),
        ("bdfhjlnprtvxz", 13),
        ("acegikmoqsuwy", 0),
        ("BDF", 0),        # uppercase is not counted
        ("bB", 1),
        ("b1d2!f", 3),     # digits/punctuation ignored
        ("zzz", 3),        # z is position 25 (odd)
        ("\tb\nd", 2),     # whitespace other than space does not trigger splitting
    ],
)
def test_counts_lowercase_letters_at_odd_positions(text, expected):
    assert break_text(text) == expected


def test_count_returns_int():
    assert isinstance(break_text("hello"), int)
