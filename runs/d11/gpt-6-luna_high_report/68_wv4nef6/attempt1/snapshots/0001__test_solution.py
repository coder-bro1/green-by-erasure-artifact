import pytest

from solution import fibfib


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, 0),
        pytest.param(
            1,
            0,
            marks=pytest.mark.xfail(
                strict=True,
                reason="fibfib uses 1 for n=1, but its docstring specifies 0",
            ),
        ),
        pytest.param(
            2,
            1,
            marks=pytest.mark.xfail(
                strict=True,
                reason="fibfib uses 2 for n=2, but its docstring specifies 1",
            ),
        ),
        pytest.param(
            3,
            1,
            marks=pytest.mark.xfail(
                strict=True,
                reason="incorrect base cases make fibfib(3) differ from the documented sequence",
            ),
        ),
        pytest.param(
            4,
            2,
            marks=pytest.mark.xfail(
                strict=True,
                reason="incorrect base cases make fibfib(4) differ from the documented sequence",
            ),
        ),
        pytest.param(
            5,
            4,
            marks=pytest.mark.xfail(
                strict=True,
                reason="fibfib(5) should be 4 according to its docstring",
            ),
        ),
        pytest.param(
            6,
            7,
            marks=pytest.mark.xfail(
                strict=True,
                reason="incorrect base cases make fibfib(6) differ from the documented sequence",
            ),
        ),
        pytest.param(
            7,
            13,
            marks=pytest.mark.xfail(
                strict=True,
                reason="incorrect base cases make fibfib(7) differ from the documented sequence",
            ),
        ),
        pytest.param(
            8,
            24,
            marks=pytest.mark.xfail(
                strict=True,
                reason="fibfib(8) should be 24 according to its docstring",
            ),
        ),
    ],
)
def test_fibfib_matches_documented_sequence(n, expected):
    assert fibfib(n) == expected
