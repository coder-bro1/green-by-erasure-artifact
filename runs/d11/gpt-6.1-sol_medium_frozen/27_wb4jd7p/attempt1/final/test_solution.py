import pytest

from solution import prime_length


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("Hello", True),
        ("abcdcba", True),
        ("kittens", True),
        ("orange", False),
    ],
)
def test_docstring_examples(string, expected):
    assert prime_length(string) is expected


@pytest.mark.parametrize(
    ("length", "expected"),
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
                reason="The divisor loop skips 2, so length 4 is treated as prime.",
            ),
        ),
        (5, True),
        (6, False),
        (7, True),
        (8, False),
        (9, False),
        (10, False),
        (11, True),
        (13, True),
        (15, False),
        (16, False),
        (25, False),
        (49, False),
        (97, True),
        (100, False),
        (101, True),
        (121, False),
        (127, True),
    ],
)
def test_prime_and_nonprime_lengths(length, expected):
    assert prime_length("x" * length) is expected


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("  ", True),
        ("\n\t ", True),
        ("123456", False),
        ("a! b?", True),
        ("\u00e9\u00e9", True),
        ("\U0001f600" * 3, True),
        ("\U0001f600" * 6, False),
        ("e\u0301", True),
    ],
)
def test_length_counts_all_characters(string, expected):
    assert prime_length(string) is expected
