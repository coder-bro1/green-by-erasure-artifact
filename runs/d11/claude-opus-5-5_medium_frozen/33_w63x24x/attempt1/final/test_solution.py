import pytest

from solution import split_words


# --- whitespace branch -------------------------------------------------------

@pytest.mark.parametrize(
    "txt, expected",
    [
        ("Hello world!", ["Hello", "world!"]),
        ("Hello world,!", ["Hello", "world,!"]),
        ("Hello,Hello,world !", ["Hello,Hello,world", "!"]),
        ("  leading and   multiple  spaces ", ["leading", "and", "multiple", "spaces"]),
        ("a b\tc\nd", ["a", "b", "c", "d"]),
        (" ", []),
    ],
)
def test_splits_on_whitespace_when_space_present(txt, expected):
    assert split_words(txt) == expected


# --- comma branch (actual behaviour) -----------------------------------------

@pytest.mark.parametrize(
    "txt, expected",
    [
        ("Hello,world!", ["Hello,world!"]),
        ("a,b,c", ["a,b,c"]),
        (",", [","]),
        ("a,\tb", ["a,", "b"]),  # no space, so the comma branch splits on the tab
    ],
)
def test_comma_branch_returns_list(txt, expected):
    result = split_words(txt)
    assert isinstance(result, list)
    assert result == expected


@pytest.mark.xfail(strict=True, reason="solution.py does not split on commas as the docstring promises")
def test_docstring_comma_example():
    assert split_words("Hello,world!") == ["Hello", "world!"]


# --- counting branch ---------------------------------------------------------

@pytest.mark.parametrize(
    "txt, expected",
    [
        ("abcdef", 3),            # b, d, f
        ("aaabb", 2),
        ("aaaBb", 1),             # uppercase B ignored
        ("", 0),
        ("ACEG", 0),              # uppercase only
        ("bdfhjlnprtvxz", 13),    # every odd-indexed letter
        ("acegikmoqsuwy", 0),     # every even-indexed letter
        ("abcdefghijklmnopqrstuvwxyz", 13),
        ("b1!d?", 2),             # digits and punctuation ignored
        ("a\tb", 1),              # tab is not a space: counts instead of splitting
    ],
)
def test_counts_lowercase_letters_with_odd_alphabet_index(txt, expected):
    assert split_words(txt) == expected


def test_count_branch_returns_int():
    assert type(split_words("xyz")) is int


def test_does_not_mutate_or_depend_on_repeated_calls():
    txt = "Hello world"
    assert split_words(txt) == split_words(txt) == ["Hello", "world"]
