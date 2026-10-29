import pytest

from solution import split_words


# --- Docstring examples -----------------------------------------------------

def test_docstring_space_example():
    assert split_words("Hello world!") == ["Hello", "world!"]


def test_docstring_comma_example():
    assert split_words("Hello,world!") == ["Hello", "world!"]


def test_docstring_count_example():
    assert split_words("abcdef") == 3


# --- Whitespace splitting ---------------------------------------------------

@pytest.mark.parametrize(
    "txt, expected",
    [
        ("Hello world", ["Hello", "world"]),
        ("Hello   world", ["Hello", "world"]),
        ("  leading and trailing  ", ["leading", "and", "trailing"]),
        ("one two three four", ["one", "two", "three", "four"]),
        ("Hello world,!", ["Hello", "world,!"]),
        ("a,b c,d", ["a,b", "c,d"]),
        ("Hello\tthere world", ["Hello", "there", "world"]),
    ],
)
def test_split_on_spaces(txt, expected):
    assert split_words(txt) == expected


def test_only_spaces_gives_empty_list():
    assert split_words("   ") == []


def test_whitespace_takes_priority_over_commas():
    # Whitespace present -> commas must be kept inside the words.
    assert split_words("x,y z") == ["x,y", "z"]


@pytest.mark.xfail(
    strict=True,
    reason="solution checks only for ' ' instead of any whitespace; a tab is "
    "whitespace so the text should be split on it",
)
def test_split_on_tab_only():
    assert split_words("Hello\tworld") == ["Hello", "world"]


@pytest.mark.xfail(
    strict=True,
    reason="solution checks only for ' ' instead of any whitespace; a newline "
    "is whitespace so the text should be split on it",
)
def test_split_on_newline_only():
    assert split_words("Hello\nworld") == ["Hello", "world"]


@pytest.mark.xfail(
    strict=True,
    reason="solution checks only for ' '; with a tab present it should split "
    "on whitespace and keep the comma, but it falls through to comma splitting",
)
def test_tab_whitespace_takes_priority_over_commas():
    assert split_words("a\tb,c") == ["a", "b,c"]


# --- Comma splitting --------------------------------------------------------

@pytest.mark.parametrize(
    "txt, expected",
    [
        ("Hello,world!", ["Hello", "world!"]),
        ("a,b,c", ["a", "b", "c"]),
        ("aaa,bbb", ["aaa", "bbb"]),
        ("trailing,", ["trailing"]),
        (",leading", ["leading"]),
    ],
)
def test_split_on_commas(txt, expected):
    assert split_words(txt) == expected


# --- Counting lower-case letters with odd alphabet order --------------------

@pytest.mark.parametrize(
    "txt, expected",
    [
        ("abcdef", 3),          # b, d, f
        ("aaabb", 2),           # b, b
        ("aaaBb", 1),           # only lower-case 'b'
        ("abcdefghijklmnopqrstuvwxyz", 13),
        ("bdfhjlnprtvxz", 13),  # all odd-order letters
        ("acegikmoqsuwy", 0),   # all even-order letters
        ("ABCDEF", 0),          # upper-case letters never count
        ("", 0),
        ("123!?", 0),
        ("b1d2", 2),
    ],
)
def test_count_odd_order_lowercase(txt, expected):
    assert split_words(txt) == expected


def test_count_returns_int():
    result = split_words("xyz")
    assert isinstance(result, int)
    assert result == 2  # x (23), z (25)
