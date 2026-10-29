import pytest

from solution import specialFilter


ODD_DIGITS = {1, 3, 5, 7, 9}
EVEN_TWO_REASON = (
    "specialFilter includes 2 in odd_digits, so it counts numbers with an "
    "even first or last digit of 2, contrary to its docstring."
)


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        pytest.param([15, -73, 14, -15], 1, id="first-docstring-example"),
        pytest.param(
            [33, -2, -3, 45, 21, 109],
            2,
            id="second-docstring-example",
            marks=pytest.mark.xfail(strict=True, reason=EVEN_TWO_REASON),
        ),
        pytest.param([], 0, id="empty"),
        pytest.param([0, 1, 3, 5, 7, 9, 10], 0, id="threshold-excludes-small"),
        pytest.param([-11, -33, -55, -77, -99, -109], 0, id="negative"),
        pytest.param([11], 1, id="first-number-above-threshold"),
        pytest.param([11, 13, 15, 17, 19, 31, 55, 77, 99], 9, id="odd-ends"),
        pytest.param([40, 46, 64, 68, 80, 88], 0, id="even-ends"),
        pytest.param([14, 16, 18, 34, 36, 38], 0, id="even-last-digit"),
        pytest.param([41, 43, 61, 65, 81, 89], 0, id="even-first-digit"),
        pytest.param([101, 109, 305, 507, 709, 901], 6, id="interior-zero"),
        pytest.param([121, 323, 545, 767, 989], 5, id="interior-parity-irrelevant"),
        pytest.param([15, 15, 15, 14, 14], 3, id="duplicates-count-individually"),
        pytest.param([10**100 + 1, 8 * 10**100 + 1, 10**100 + 8], 1, id="large-integers"),
    ],
)
def test_documented_counts(nums, expected):
    assert specialFilter(nums) == expected


def digit_cases():
    """Exercise every combination of first and last decimal digits."""
    for first in range(1, 10):
        for last in range(10):
            expected = int(first in ODD_DIGITS and last in ODD_DIGITS)
            marks = []
            if (first == 2 and last in ODD_DIGITS | {2}) or (
                last == 2 and first in ODD_DIGITS
            ):
                marks.append(pytest.mark.xfail(strict=True, reason=EVEN_TWO_REASON))
            yield pytest.param(
                first * 100 + 40 + last,
                expected,
                id=f"first-{first}-last-{last}",
                marks=marks,
            )


@pytest.mark.parametrize(("number", "expected"), list(digit_cases()))
def test_all_endpoint_digit_combinations(number, expected):
    assert specialFilter([number]) == expected


def test_input_is_not_modified():
    nums = [15, -73, 14, -15, 109, 15]
    original = nums.copy()

    assert specialFilter(nums) == 3
    assert nums == original


def test_result_is_an_integer():
    assert type(specialFilter([11, 33, 14])) is int
