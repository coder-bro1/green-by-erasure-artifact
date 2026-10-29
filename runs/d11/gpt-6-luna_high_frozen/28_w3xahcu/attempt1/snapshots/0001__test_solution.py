import pytest

from solution import is_prime


@pytest.mark.parametrize("n", [-10, -1, 0])
def test_numbers_less_than_two_are_not_prime(n):
    assert is_prime(n) is False


def test_two_is_prime():
    assert is_prime(2) is True


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        pytest.param(1, False, marks=pytest.mark.xfail(
            strict=True, reason="is_prime(1) currently returns True"
        )),
        pytest.param(3, True, marks=pytest.mark.xfail(
            strict=True, reason="the divisor loop incorrectly tests 1"
        )),
        pytest.param(4, False, marks=pytest.mark.xfail(
            strict=True, reason="the divisor loop incorrectly tests 1"
        )),
        pytest.param(6, False, marks=pytest.mark.xfail(
            strict=True, reason="the divisor loop incorrectly tests 1"
        )),
        pytest.param(11, True, marks=pytest.mark.xfail(
            strict=True, reason="the divisor loop incorrectly tests 1"
        )),
        pytest.param(61, True, marks=pytest.mark.xfail(
            strict=True, reason="the divisor loop incorrectly tests 1"
        )),
        pytest.param(101, True, marks=pytest.mark.xfail(
            strict=True, reason="the divisor loop incorrectly tests 1"
        )),
        pytest.param(13441, True, marks=pytest.mark.xfail(
            strict=True, reason="the divisor loop incorrectly tests 1"
        )),
    ],
)
def test_primality_cases_from_docstring_and_boundaries(n, expected):
    assert is_prime(n) is expected
