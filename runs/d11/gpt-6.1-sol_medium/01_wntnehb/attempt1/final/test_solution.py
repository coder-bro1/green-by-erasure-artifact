import pytest

from solution import circular_shift


@pytest.mark.parametrize(
    ("number", "shift", "expected"),
    [
        pytest.param(12, 1, "21", id="docstring-one-place"),
        pytest.param(12, 2, "12", id="docstring-full-rotation"),
        pytest.param(12345, 0, "12345", id="zero-shift"),
        pytest.param(12345, 1, "51234", id="right-one-place"),
        pytest.param(12345, 2, "45123", id="right-two-places"),
        pytest.param(12345, 4, "23451", id="all-but-one-place"),
        pytest.param(12345, 5, "12345", id="full-rotation"),
        pytest.param(12345, 6, "54321", id="oversized-shift-reverses"),
        pytest.param(12345, 10, "54321", id="oversized-multiple-reverses"),
        pytest.param(12345, 100, "54321", id="large-shift-reverses"),
        pytest.param(1200, 1, "0120", id="preserves-leading-zero"),
        pytest.param(1200, 2, "0012", id="preserves-multiple-leading-zeros"),
        pytest.param(1200, 5, "0021", id="reversal-preserves-zeros"),
        pytest.param(1111, 2, "1111", id="repeated-digits"),
        pytest.param(7, 0, "7", id="single-digit-zero-shift"),
        pytest.param(7, 1, "7", id="single-digit-full-rotation"),
        pytest.param(7, 2, "7", id="single-digit-reversal"),
        pytest.param(0, 0, "0", id="zero-zero-shift"),
        pytest.param(0, 1, "0", id="zero-full-rotation"),
        pytest.param(0, 2, "0", id="zero-reversal"),
        pytest.param(
            12345678901234567890,
            3,
            "89012345678901234567",
            id="large-integer",
        ),
    ],
)
def test_circular_shift(number, shift, expected):
    result = circular_shift(number, shift)

    assert isinstance(result, str)
    assert result == expected
