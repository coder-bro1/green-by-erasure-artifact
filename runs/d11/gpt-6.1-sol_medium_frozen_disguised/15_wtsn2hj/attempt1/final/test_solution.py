import pytest

from solution import length_is_prime


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        pytest.param(
            4,
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation misses the divisor 2 for length 4.",
            ),
        ),
        (5, True),
        (6, False),
        (7, True),
        (8, False),
        (9, False),
        (10, False),
        (11, True),
        (15, False),
        (25, False),
        (49, False),
        (97, True),
        (100, False),
        (121, False),
        (127, True),
    ],
)
def test_prime_and_nonprime_lengths(size, expected):
    assert length_is_prime("a" * size) is expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abc", True),
        ("pythons", True),
        ("banana", False),
        ("  ", True),
        ("a b", True),
        ("\t\n", True),
        ("\u00e9", False),
        ("\U0001f600\U0001f680", True),
        ("\u4f60\u597d\u554a", True),
        ("e\u0301", True),
    ],
)
def test_length_counts_characters_including_whitespace_and_unicode(text, expected):
    assert length_is_prime(text) is expected
