import pytest

from solution import derivative

# NOTE: solution.derivative has a known bug: it returns [i * x for i, x in enumerate(xs)]
# without dropping the leading term, so the result always starts with an extra 0 and has
# the same length as the input (e.g. [3, 1, 2, 4, 5] -> [0, 1, 4, 12, 20] instead of
# [1, 4, 12, 20]). Tests of the documented behavior that this bug breaks are marked
# xfail(strict=True): they will start failing (XPASS -> error) once the bug is fixed,
# signalling that the marker should be removed.
KNOWN_BUG = pytest.mark.xfail(
    strict=True,
    reason="derivative() does not drop the constant term (missing [1:])",
)


# --- Documented (correct) behavior -------------------------------------------------

@KNOWN_BUG
@pytest.mark.parametrize(
    "xs, expected",
    [
        ([3, 1, 2, 4, 5], [1, 4, 12, 20]),  # docstring example
        ([1, 2, 3], [2, 6]),                # docstring example
        ([3, 2, 1], [2, 2]),
        ([3, 2, 1, 0, 4], [2, 2, 0, 16]),
        ([0, 0, 5], [0, 10]),
        ([-1, -2, -3], [-2, -6]),
        ([1.5, 2.5, 0.5], [2.5, 1.0]),
    ],
)
def test_documented_derivative(xs, expected):
    assert derivative(xs) == expected


@KNOWN_BUG
def test_constant_polynomial_has_empty_derivative():
    assert derivative([7]) == []


@KNOWN_BUG
def test_result_length_is_one_less_than_input():
    xs = [4, 3, 2, 1]
    assert len(derivative(xs)) == len(xs) - 1


# --- Properties that hold regardless of the bug ------------------------------------

def test_empty_input_returns_empty_list():
    assert derivative([]) == []


def test_returns_list():
    assert isinstance(derivative([1, 2, 3]), list)


def test_does_not_mutate_input():
    xs = [3, 1, 2, 4, 5]
    original = list(xs)
    derivative(xs)
    assert xs == original


@pytest.mark.parametrize(
    "xs",
    [[3, 1, 2, 4, 5], [1, 2, 3], [0, 0, 5], [-1, -2, -3], [1.5, 2.5, 0.5], [9, 8, 7, 6, 5, 4]],
)
def test_nonconstant_coefficients_are_power_times_coefficient(xs):
    # For k >= 1, the derivative coefficient of x^(k-1) is k * xs[k]; these values
    # appear in order at the tail of the output in both the buggy and correct versions.
    expected_tail = [k * xs[k] for k in range(1, len(xs))]
    result = derivative(xs)
    assert result[len(result) - len(expected_tail):] == expected_tail


def test_large_degree_polynomial():
    xs = list(range(100))
    expected_tail = [k * k for k in range(1, 100)]
    result = derivative(xs)
    assert result[-99:] == expected_tail
