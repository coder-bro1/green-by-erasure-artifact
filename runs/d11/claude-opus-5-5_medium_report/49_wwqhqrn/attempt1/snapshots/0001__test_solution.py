import pytest

from solution import cycpattern_check


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("abcd", "abd", False),
        ("hello", "ell", True),
        ("whassup", "psus", False),
        ("abab", "baa", True),
        ("efef", "eeff", False),
        ("himenss", "simen", True),
    ],
)
def test_docstring_examples(a, b, expected):
    assert cycpattern_check(a, b) is expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("abcdef", "cde", True),      # plain substring (rotation 0)
        ("abcdef", "dec", True),      # rotation "cde"
        ("abcdef", "ecd", True),      # rotation "cde"
        ("abcdef", "edc", False),     # reversal, not a rotation
        ("xyzabc", "bca", True),      # rotation "abc" at end of a
        ("abcxyz", "cab", True),      # rotation "abc" at start of a
        ("abc", "abc", True),         # whole word
        ("abc", "cab", True),         # whole word, rotated
        ("abc", "abcd", False),       # b longer than a
        ("aaaa", "a", True),
        ("aaaa", "b", False),
        ("ab", "ba", True),
        ("AbC", "abc", False),        # case-sensitive
    ],
)
def test_rotations(a, b, expected):
    assert cycpattern_check(a, b) is expected


def test_empty_pattern_is_substring():
    # The empty string (and its only rotation) is a substring of any word.
    assert cycpattern_check("abc", "") is True
    assert cycpattern_check("", "") is True


def test_empty_word_nonempty_pattern():
    assert cycpattern_check("", "a") is False


def test_matches_brute_force_reference():
    import itertools

    def reference(a, b):
        return any(b[k:] + b[:k] in a for k in range(max(len(b), 1)))

    alphabet = "ab"
    words = [
        "".join(p)
        for n in range(0, 5)
        for p in itertools.product(alphabet, repeat=n)
    ]
    for a in words:
        for b in words:
            assert cycpattern_check(a, b) == reference(a, b), (a, b)
