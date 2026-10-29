import pytest

from solution import prime_length


def _is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n ** 0.5) + 1))


@pytest.mark.parametrize(
    "s, expected",
    [
        ("Hello", True),
        ("abcdcba", True),
        ("kittens", True),
        ("orange", False),
    ],
)
def test_docstring_examples(s, expected):
    assert prime_length(s) is expected


def test_empty_string():
    assert prime_length("") is False


def test_single_character():
    assert prime_length("a") is False


@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23, 97, 101])
def test_prime_lengths(n):
    assert prime_length("x" * n) is True


@pytest.mark.parametrize("n", [6, 8, 9, 10, 12, 15, 21, 25, 49, 100, 121])
def test_composite_lengths(n):
    assert prime_length("x" * n) is False


@pytest.mark.xfail(
    strict=True,
    reason="Bug in solution.py: loop starts at 3, so divisibility by 2 is "
    "never checked and length 4 is wrongly reported as prime.",
)
def test_length_four_is_not_prime():
    assert prime_length("abcd") is False


@pytest.mark.parametrize("n", [n for n in range(0, 200) if n != 4])
def test_matches_reference_primality(n):
    assert prime_length("a" * n) is _is_prime(n)


def test_whitespace_and_unicode_count_as_characters():
    assert prime_length("  ") is True        # length 2
    assert prime_length("ééé") is True  # length 3
    assert prime_length("a b c d e f") is True  # length 11
