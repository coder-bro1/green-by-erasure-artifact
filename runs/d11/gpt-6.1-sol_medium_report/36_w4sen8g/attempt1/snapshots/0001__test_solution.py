import pytest

from solution import derivative


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        pytest.param([3, 1, 2, 4, 5], [1, 4, 12, 20], id="docstring-quartic"),
        pytest.param([1, 2, 3], [2, 6], id="docstring-quadratic"),
        pytest.param([], [], id="empty-polynomial"),
        pytest.param([7], [], id="constant"),
        pytest.param([0], [], id="zero-constant"),
        pytest.param([9, 5], [5], id="linear"),
        pytest.param([-3, -2, -4, -5], [-2, -8, -15], id="negative-coefficients"),
        pytest.param([2, 0, 0, 4], [0, 0, 12], id="missing-powers"),
        pytest.param([3, 2, 0, 0], [2, 0, 0], id="trailing-zero-coefficients"),
        pytest.param([0, 0, 0, 0], [0, 0, 0], id="all-zero-coefficients"),
        pytest.param([1.5, -0.5, 2.25, 0.125], [-0.5, 4.5, 0.375], id="floats"),
        pytest.param([10**100, 10**100, -(10**100)], [10**100, -2 * 10**100], id="large-integers"),
        pytest.param([0] * 20 + [3], [0] * 19 + [60], id="high-degree"),
    ],
)
def test_derivative(coefficients, expected):
    """Return coefficients in ascending power order, dropping the constant."""
    original = coefficients.copy()

    result = derivative(coefficients)

    assert isinstance(result, list)
    assert result == expected
    assert coefficients == original
    assert result is not coefficients
