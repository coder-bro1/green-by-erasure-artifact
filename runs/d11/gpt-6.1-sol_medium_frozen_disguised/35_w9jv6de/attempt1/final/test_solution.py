import pytest

from solution import poly_slope_coeffs


@pytest.mark.parametrize(
    ("coeffs", "expected"),
    [
        pytest.param([], [], id="empty"),
        pytest.param([5], [0], id="constant"),
        pytest.param([0], [0], id="zero-constant"),
        pytest.param([2, 4], [0, 4], id="linear"),
        pytest.param([5, 0, 3], [0, 0, 6], id="quadratic"),
        pytest.param([1, 2, 3, 4, 5], [0, 2, 6, 12, 20], id="higher-degree"),
        pytest.param([-5, -2, -3], [0, -2, -6], id="negative"),
        pytest.param([0, 0, 0, 0], [0, 0, 0, 0], id="all-zero"),
        pytest.param([7, 3, 0, 0], [0, 3, 0, 0], id="trailing-zeros"),
        pytest.param([1.5, -0.5, 2.25], [0.0, -0.5, 4.5], id="fractional"),
        pytest.param([10**100, 10**100, -(10**100)],
                     [0, 10**100, -2 * 10**100], id="large-integers"),
    ],
)
def test_current_index_weighted_coefficients(coeffs, expected):
    """Characterize the implementation, including its leading zero."""
    result = poly_slope_coeffs(coeffs)

    assert isinstance(result, list)
    assert result == expected


@pytest.mark.parametrize("coeffs", [[], [5], [5, 0, 3]])
def test_returns_new_list_without_mutating_input(coeffs):
    original = coeffs.copy()

    result = poly_slope_coeffs(coeffs)

    assert coeffs == original
    assert result is not coeffs
    result.append(99)
    assert coeffs == original


@pytest.mark.xfail(
    strict=True,
    reason="Implementation retains the constant term's zero instead of dropping it.",
)
@pytest.mark.parametrize(
    ("coeffs", "expected"),
    [
        pytest.param([5, 0, 3], [0, 6], id="documented-quadratic"),
        pytest.param([2, 4], [4], id="documented-linear"),
        pytest.param([5], [], id="constant-derivative"),
    ],
)
def test_documented_derivative_contract(coeffs, expected):
    assert poly_slope_coeffs(coeffs) == expected
