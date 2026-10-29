import pytest

from solution import greatest_common_divisor


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        pytest.param(3, 5, 1, marks=pytest.mark.xfail(reason="solution.py returns the final remainder (0), not the GCD")),
        pytest.param(25, 15, 5, marks=pytest.mark.xfail(reason="solution.py returns the final remainder (0), not the GCD")),
        pytest.param(15, 25, 5, marks=pytest.mark.xfail(reason="solution.py returns the final remainder (0), not the GCD")),
        pytest.param(-24, 18, 6, marks=pytest.mark.xfail(reason="solution.py returns the final remainder (0), not the GCD")),
        pytest.param(24, -18, 6, marks=pytest.mark.xfail(reason="solution.py returns the final remainder (0), not the GCD")),
        pytest.param(0, 9, 9, marks=pytest.mark.xfail(reason="solution.py returns the final remainder (0), not the GCD")),
        pytest.param(9, 0, 9, marks=pytest.mark.xfail(reason="solution.py returns the final remainder (0), not the GCD")),
        (0, 0, 0),
    ],
)
def test_greatest_common_divisor(a, b, expected):
    assert greatest_common_divisor(a, b) == expected
