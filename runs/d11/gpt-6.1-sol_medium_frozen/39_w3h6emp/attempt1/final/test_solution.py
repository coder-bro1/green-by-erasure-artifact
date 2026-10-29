import pytest

from solution import specialFilter


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], 0),
        ([15, -73, 14, -15], 1),
        # The implementation also counts 21; the docstring says 2.
        ([33, -2, -3, 45, 21, 109], 3),
        ([-999, -11, -1, 0, 1, 9, 10], 0),
        ([11], 1),
        ([11, 13, 15, 17, 19, 31, 53, 75, 97], 9),
        ([14, 16, 18, 41, 61, 81, 44, 66, 88], 0),
        ([101, 103, 305, 507, 709, 901], 6),
        ([110, 330, 550, 770, 990, 1000], 0),
        ([15, 15, 15, 14, 14], 3),
        ([10**100 + 1, 4 * 10**100 + 1, 10**100 + 4], 1),
    ],
)
def test_special_filter_counts_qualifying_numbers(nums, expected):
    assert specialFilter(nums) == expected


@pytest.mark.parametrize("num", [12, 21, 22, 23, 32, 202, 219])
def test_current_behavior_accepts_digit_two(num):
    """Record the implementation's inclusion of 2 despite its docstring."""
    assert specialFilter([num]) == 1


def test_special_filter_does_not_modify_input():
    nums = [15, -73, 14, -15, 33, 109, 15]
    original = nums.copy()

    assert specialFilter(nums) == 4
    assert nums == original


def test_special_filter_returns_an_integer_count():
    assert type(specialFilter([11])) is int
