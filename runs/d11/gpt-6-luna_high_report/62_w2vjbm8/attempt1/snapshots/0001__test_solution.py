import pytest

from solution import cycpattern_check


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("abcd", "abd", False),
        ("hello", "ell", True),
        ("whassup", "psus", False),
        pytest.param(
            "abab",
            "baa",
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="Only the unrotated pattern is checked; the docstring requires checking every rotation.",
            ),
        ),
        ("efef", "eeff", False),
        pytest.param(
            "himenss",
            "simen",
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="Only the unrotated pattern is checked; the docstring requires checking every rotation.",
            ),
        ),
    ],
)
def test_docstring_examples(a, b, expected):
    assert cycpattern_check(a, b) is expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("xxcdeyy", "cde", True),  # Match at a nonzero position.
        ("cabxx", "abc", False),  # A rotation is not enough unless it occurs contiguously.
        ("zzabxx", "abc", False),
        ("xabcx", "abcd", False),  # The pattern is longer than the searched word.
        ("aaaaa", "aaa", True),
        ("Abc", "abc", False),  # Matching is case-sensitive.
    ],
)
def test_substring_and_boundary_cases(a, b, expected):
    assert cycpattern_check(a, b) is expected


@pytest.mark.xfail(
    strict=True,
    reason="The docstring requires checking rotations, but the implementation tests only the original pattern.",
)
def test_rotation_that_is_a_substring():
    assert cycpattern_check("xxbcayy", "abc") is True
