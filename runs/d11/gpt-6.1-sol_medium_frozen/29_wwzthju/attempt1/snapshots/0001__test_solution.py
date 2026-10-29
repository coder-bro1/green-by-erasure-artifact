"""Characterize the existing implementation and expose its documented bug."""

import pytest

from solution import largest_divisor


@pytest.mark.parametrize(
    "n",
    [2, 3, 4, 9, 15, 16, 25, 36, 97, 100],
    ids=[
        "smallest-prime", "odd-prime", "even-composite", "odd-square",
        "documented-input", "power-of-two", "prime-square",
        "multiple-divisors", "larger-prime", "larger-composite",
    ],
)
def test_positive_integers_currently_return_none(n):
    """Both prime and composite inputs currently fall through without a return."""
    assert largest_divisor(n) is None


@pytest.mark.parametrize("n", [-10, -1, 0, 1])
def test_boundary_inputs_return_none(n):
    assert largest_divisor(n) is None


@pytest.mark.parametrize("n", [2.5, "15", None, [15]])
def test_non_integer_inputs_raise_type_error(n):
    with pytest.raises(TypeError):
        largest_divisor(n)


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: largest_divisor(15) returns None instead of documented 5",
    raises=AssertionError,
)
def test_documented_example():
    assert largest_divisor(15) == 5
