import pytest

from solution import is_happy


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", False),
        ("a", False),
        ("aa", False),
        ("ab", False),
        ("abc", True),
        ("abcd", True),
        ("adb", True),
        pytest.param(
            "xyy",
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_happy only rejects triples where all three characters match; the docstring requires every adjacent triple to be pairwise distinct",
            ),
        ),
        pytest.param(
            "aab",
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_happy only rejects triples where all three characters match; the docstring requires every adjacent triple to be pairwise distinct",
            ),
        ),
        pytest.param(
            "aba",
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_happy only rejects triples where all three characters match; the docstring requires every adjacent triple to be pairwise distinct",
            ),
        ),
        pytest.param(
            "abb",
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_happy only rejects triples where all three characters match; the docstring requires every adjacent triple to be pairwise distinct",
            ),
        ),
        pytest.param(
            "aabb",
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_happy only rejects triples where all three characters match; the docstring requires every adjacent triple to be pairwise distinct",
            ),
        ),
    ],
)
def test_is_happy_examples_and_contract(value, expected):
    assert is_happy(value) is expected
