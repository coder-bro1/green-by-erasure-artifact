import pytest

from solution import break_text


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("one two", ["one", "two"]),
        ("  one   two  ", ["one", "two"]),
        (" ", []),
        ("\t one\n two\r\n", ["one", "two"]),
        ("red,green blue", ["red,green", "blue"]),
        ("red, green", ["red,", "green"]),
        ("a , b", ["a", ",", "b"]),
    ],
)
def test_literal_space_triggers_whitespace_split(text, expected):
    assert break_text(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("red,green", ["red,green"]),
        (",", [","]),
        ("red,,green,", ["red,,green,"]),
        ("red,\tgreen", ["red,", "green"]),
        ("\nred,green\t", ["red,green"]),
    ],
)
def test_comma_branch_currently_splits_whitespace_not_commas(text, expected):
    """Characterize the implementation's known difference from its docstring."""
    assert break_text(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("bdx", 3),
        ("bdfhjlnprtvxz", 13),
        ("acegikmoqsuwy", 0),
        ("abcdefghijklmnopqrstuvwxyz", 13),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0),
        ("bBdDfF", 3),
        ("bbbb", 4),
        ("0123456789!?_-", 0),
        ("b1d!f", 3),
        ("\t\n\r", 0),
        ("b\td\nf", 3),
        ("éê", 1),
    ],
)
def test_counts_lowercase_characters_with_even_codepoints(text, expected):
    assert break_text(text) == expected


@pytest.mark.parametrize("text", [None, 42])
def test_non_iterable_inputs_raise_type_error(text):
    with pytest.raises(TypeError):
        break_text(text)
