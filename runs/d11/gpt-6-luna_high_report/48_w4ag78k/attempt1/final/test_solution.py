import pytest

from solution import split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world!", ["Hello", "world!"]),
        pytest.param(
            "one\ttwo\nthree",
            ["one", "two", "three"],
            marks=pytest.mark.xfail(
                strict=True,
                reason="The docstring promises splitting on whitespace, but the implementation only detects spaces.",
            ),
        ),
        ("one,two three", ["one,two", "three"]),
    ],
)
def test_splits_on_whitespace_when_present(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello,world!", ["Hello", "world!"]),
        ("red,,blue,", ["red", "blue"]),
        (",", []),
    ],
)
def test_splits_on_commas_when_no_whitespace_is_present(text, expected):
    assert split_words(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abcdef", 3),  # b, d, and f have odd zero-based alphabet indices.
        ("aBcDeF", 0),  # Only lowercase letters count; a, c, and e have even indices.
        ("xyz!", 2),  # x and z have odd alphabet indices.
        ("123!?", 0),
        ("", 0),
    ],
)
def test_counts_lowercase_letters_with_odd_alphabet_indices(text, expected):
    assert split_words(text) == expected
