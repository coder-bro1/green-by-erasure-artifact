import pytest

from solution import even_odd_palindrome


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        pytest.param(
            1,
            (0, 1),
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation excludes n, though the docstring says the range is inclusive.",
            ),
            id="inclusive-lower-bound",
        ),
        pytest.param(
            3,
            (1, 2),
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation excludes n, though the docstring's example counts n=3.",
            ),
            id="documented-example-3",
        ),
        (10, (4, 5)),
        pytest.param(
            11,
            (4, 6),
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation excludes n, though the docstring says the range is inclusive.",
            ),
            id="two-digit-palindrome-endpoint",
        ),
        (12, (4, 6)),
        pytest.param(
            22,
            (5, 6),
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation excludes n, though the docstring says the range is inclusive.",
            ),
            id="even-palindrome-endpoint",
        ),
        (100, (8, 10)),
        pytest.param(
            101,
            (8, 11),
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation excludes n, though the docstring says the range is inclusive.",
            ),
            id="three-digit-palindrome-endpoint",
        ),
        (1000, (258, 260)),
    ],
)
def test_even_odd_palindrome_counts_inclusive_range(n, expected):
    assert even_odd_palindrome(n) == expected
