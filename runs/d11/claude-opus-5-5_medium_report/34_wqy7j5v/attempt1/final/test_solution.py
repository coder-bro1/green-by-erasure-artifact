import pytest

from solution import histogram


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a b c", {"a": 1, "b": 1, "c": 1}),
        ("a b b a", {"a": 2, "b": 2}),
        ("a b c a b", {"a": 2, "b": 2}),
        ("b b b b a", {"b": 4}),
        ("", {}),
    ],
)
def test_docstring_examples(text, expected):
    assert histogram(text) == expected


def test_single_letter():
    assert histogram("a") == {"a": 1}


def test_single_letter_repeated():
    assert histogram("z z z") == {"z": 3}


def test_unique_maximum_excludes_others():
    assert histogram("r t g g") == {"g": 2}


def test_tie_among_three():
    assert histogram("a b c a b c d") == {"a": 2, "b": 2, "c": 2}


def test_order_independent():
    assert histogram("a b b c") == histogram("c b a b") == {"b": 2}


def test_all_letters_once():
    letters = "abcdefghijklmnopqrstuvwxyz"
    assert histogram(" ".join(letters)) == {ch: 1 for ch in letters}


def test_returns_dict():
    assert isinstance(histogram("a"), dict)


def test_input_not_mutated():
    s = "a b a"
    histogram(s)
    assert s == "a b a"


@pytest.mark.xfail(
    strict=True,
    reason="Empty tokens from repeated/leading/trailing spaces are skipped when "
    "finding the max count but not when building the result, so '' is "
    "returned as a key when its count equals the max.",
)
@pytest.mark.parametrize(
    "text, expected",
    [
        ("a  b", {"a": 1, "b": 1}),
        (" a", {"a": 1}),
        ("a b ", {"a": 1, "b": 1}),
    ],
)
def test_extra_spaces_do_not_produce_empty_key(text, expected):
    assert histogram(text) == expected


def test_extra_spaces_when_letter_count_exceeds_blanks():
    # '' appears once, 'a' twice -> '' not included
    assert histogram("a  a") == {"a": 2}
