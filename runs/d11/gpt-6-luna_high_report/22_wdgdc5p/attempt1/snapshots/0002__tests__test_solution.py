from pathlib import Path
import sys

import pytest

# Some pytest launchers add only the tests directory to sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solution import count_nums


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], 0),
        ([0], 0),
        ([1, 1, 2], 3),
        ([0, 1, 10, 101, 1000, 222], 5),
        ([-1, 11, -11], 1),
        ([-1, -10, -11, -12, -100, -101], 0),
        ([-102, -113, -123], 2),
        ([-19, 19, -91, 91], 2),
        ([123, -123, 222, -222], 2),
    ],
)
def test_count_nums_counts_positive_signed_digit_sums(numbers, expected):
    assert count_nums(numbers) == expected


def test_count_nums_uses_only_the_first_digit_as_signed_for_negative_numbers():
    # -102 has digit sum -1 + 0 + 2 = 1; -101 has digit sum 0.
    assert count_nums([-102, -101]) == 1
