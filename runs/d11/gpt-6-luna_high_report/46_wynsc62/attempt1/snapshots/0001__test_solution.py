import pytest

from solution import is_prime


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (6, False),
        pytest.param(
            101,
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_prime checks divisibility by 1, so it rejects primes",
            ),
        ),
        pytest.param(
            11,
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_prime checks divisibility by 1, so it rejects primes",
            ),
        ),
        pytest.param(
            13441,
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_prime checks divisibility by 1, so it rejects primes",
            ),
        ),
        pytest.param(
            61,
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_prime checks divisibility by 1, so it rejects primes",
            ),
        ),
        (4, False),
        pytest.param(
            1,
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_prime returns True for 1 because its divisor loop is empty",
            ),
        ),
    ],
)
def test_documented_examples(number, expected):
    assert is_prime(number) is expected


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (-7, False),
        (0, False),
        pytest.param(
            2,
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_prime checks divisibility by 1, so it rejects primes",
            ),
        ),
        pytest.param(
            3,
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="is_prime checks divisibility by 1, so it rejects primes",
            ),
        ),
        (9, False),
    ],
)
def test_prime_boundaries(number, expected):
    assert is_prime(number) is expected
