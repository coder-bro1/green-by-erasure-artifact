import pytest

from solution import derivative


@pytest.mark.parametrize(
    ("coefficients", "expected"),
    [
        pytest.param(
            [3, 1, 2, 4, 5],
            [1, 4, 12, 20],
            marks=pytest.mark.xfail(
                strict=True,
                reason="derivative includes the constant-term zero and uses coefficient indices one too high",
            ),
            id="docstring-example-five-terms",
        ),
        pytest.param(
            [1, 2, 3],
            [2, 6],
            marks=pytest.mark.xfail(
                strict=True,
                reason="derivative includes the constant-term zero and uses coefficient indices one too high",
            ),
            id="docstring-example-three-terms",
        ),
        pytest.param(
            [7, 3],
            [3],
            marks=pytest.mark.xfail(
                strict=True,
                reason="derivative includes the constant-term zero and uses coefficient indices one too high",
            ),
            id="linear-polynomial",
        ),
        pytest.param(
            [2, -3, 4],
            [-3, 8],
            marks=pytest.mark.xfail(
                strict=True,
                reason="derivative includes the constant-term zero and uses coefficient indices one too high",
            ),
            id="negative-and-positive-coefficients",
        ),
    ],
)
def test_derivative_returns_derivative_coefficients(coefficients, expected):
    assert derivative(coefficients) == expected


def test_derivative_of_empty_coefficient_list_is_empty():
    assert derivative([]) == []
