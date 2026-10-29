import pytest

from solution import lcs_length


@pytest.mark.parametrize(
    "s,t,expected",
    [
        pytest.param("", "", 0, id="both-empty"),
        pytest.param("", "abc", 0, id="first-empty"),
        pytest.param("abc", "", 0, id="second-empty"),
        pytest.param("abc", "XYZ", 0, id="no-common-character"),
        pytest.param("a", "a", 1, id="single-character-match"),
        pytest.param("abc", "xby", 1, id="isolated-match"),
        pytest.param("ABC", "abc", 0, id="case-sensitive"),
        pytest.param("aaaa", "aaaa", 4, id="identical-repeated-characters"),
        pytest.param("abc", "aXbYc", 1, id="substring-must-be-contiguous"),
        pytest.param("abc", "cba", 1, id="character-order-matters"),
        pytest.param("a", "aaaa", 1, id="cannot-reuse-first-string-character"),
    ],
)
def test_lcs_length_documented_behavior(s, t, expected):
    assert lcs_length(s, t) == expected


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The recurrence uses dp[i - 1, j] instead of dp[i - 1, j - 1], "
        "missing mixed-character substrings and reusing characters in t."
    ),
)
@pytest.mark.parametrize(
    "s,t,expected",
    [
        pytest.param("witch", "sandwich", 2, id="docstring-witch"),
        pytest.param("meow", "homeowner", 4, id="docstring-meow"),
        pytest.param("abc", "abc", 3, id="identical-distinct-characters"),
        pytest.param("xxabczz", "yyabcww", 3, id="interior-substring"),
        pytest.param("aaaa", "a", 1, id="cannot-reuse-second-string-character"),
        pytest.param("baaaac", "zaaz", 2, id="unequal-repeated-runs"),
        pytest.param("ab12cdXYZ", "qqXYZrr12", 3, id="choose-longest-match"),
        pytest.param("x猫犬y", "z猫犬w", 2, id="unicode-substring"),
        pytest.param("x a!y", "z a!w", 3, id="spaces-and-punctuation"),
    ],
)
def test_lcs_length_known_docstring_mismatches(s, t, expected):
    assert lcs_length(s, t) == expected


@pytest.mark.parametrize(
    "s,t",
    [
        ("", "abc"),
        ("witch", "sandwich"),
    ],
)
def test_lcs_length_is_symmetric(s, t):
    assert lcs_length(s, t) == lcs_length(t, s)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The recurrence counts repeated runs only in s, so swapping strings "
        "changes the result even though common substring length is symmetric."
    ),
)
@pytest.mark.parametrize("s,t", [("aaaa", "a"), ("baaaac", "zaaz")])
def test_lcs_length_symmetry_for_unequal_repeated_runs(s, t):
    assert lcs_length(s, t) == lcs_length(t, s)
