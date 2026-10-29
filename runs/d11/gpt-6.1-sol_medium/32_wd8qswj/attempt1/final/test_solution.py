import pytest

from solution import specialFilter


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        pytest.param([15, -73, 14, -15], 1, id="first-docstring-example"),
        pytest.param([33, -2, -3, 45, 21, 109], 2, id="second-docstring-example"),
        pytest.param([], 0, id="empty-input"),
        pytest.param([-999, -33, -11, 0, 1, 3, 5, 7, 9, 10], 0, id="at-or-below-ten"),
        pytest.param([10, 11, 12, 13], 2, id="threshold"),
        pytest.param([11, 33, 55, 77, 99], 5, id="all-odd-endpoint-digits"),
        pytest.param([21, 43, 65, 87, 89], 0, id="even-first-digit"),
        pytest.param([12, 34, 56, 78, 90], 0, id="even-last-digit"),
        pytest.param([22, 44, 66, 88, 200], 0, id="both-endpoint-digits-even"),
        pytest.param([101, 305, 507, 709, 901, 123456789], 6, id="middle-digits-do-not-matter"),
        pytest.param([11, 11, 33, 22, 33], 4, id="duplicates-count-separately"),
        pytest.param([10**100 + 1, 2 * 10**100 + 1, 9 * 10**100 + 8], 1, id="large-integers"),
    ],
)
def test_special_filter_examples_and_edge_cases(nums, expected):
    assert specialFilter(nums) == expected


@pytest.mark.parametrize("first_digit", range(1, 10))
@pytest.mark.parametrize("last_digit", range(10))
def test_special_filter_all_endpoint_digit_combinations(first_digit, last_digit):
    # Use a zero middle digit to isolate the two digits in the specification.
    number = first_digit * 100 + last_digit
    expected = int(first_digit % 2 == 1 and last_digit % 2 == 1)

    assert specialFilter([number]) == expected


def test_special_filter_does_not_modify_input():
    nums = [15, -73, 14, -15, 109, 15]
    original = nums.copy()

    assert specialFilter(nums) == 3
    assert nums == original
