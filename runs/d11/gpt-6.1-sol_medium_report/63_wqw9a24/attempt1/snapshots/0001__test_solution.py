import pytest

from solution import will_it_fly


@pytest.mark.parametrize(
    "q, w, expected",
    [
        pytest.param([1, 2], 5, False, id="example-unbalanced"),
        pytest.param([3, 2, 3], 1, False, id="example-overweight"),
        pytest.param([3, 2, 3], 9, True, id="example-balanced"),
        pytest.param([3], 5, True, id="example-single-element"),
        pytest.param([3, 2, 3], 8, True, id="weight-equals-limit"),
        pytest.param([3, 2, 3], 7, False, id="weight-exceeds-limit-by-one"),
        pytest.param([1, 2, 2, 1], 6, True, id="even-palindrome"),
        pytest.param([1, 2, 2, 1], 5, False, id="even-palindrome-overweight"),
        pytest.param([1, 2, 3, 1], 10, False, id="inner-pair-mismatch"),
        pytest.param([1, 2, 3], 6, False, id="unbalanced-at-weight-limit"),
        pytest.param([2, 1, 1, 1], 0, False, id="unbalanced-and-overweight"),
        pytest.param([4, 4], 8, True, id="equal-pair"),
        pytest.param([1, 2], 3, False, id="unequal-pair"),
        pytest.param([3], 3, True, id="single-element-at-limit"),
        pytest.param([3], 2, False, id="single-element-overweight"),
        pytest.param([], 0, True, id="empty-at-zero-limit"),
        pytest.param([], 5, True, id="empty-below-limit"),
        pytest.param([], -1, False, id="empty-above-negative-limit"),
        pytest.param([0, 0, 0], 0, True, id="all-zero-at-limit"),
        pytest.param([0, 0], -1, False, id="all-zero-overweight"),
        pytest.param([-2, 1, -2], -3, True, id="negative-sum-at-limit"),
        pytest.param([-2, 1, -2], -4, False, id="negative-sum-overweight"),
        pytest.param([-1, 0], 0, False, id="negative-unbalanced"),
        pytest.param([0.5, 1.0, 0.5], 2.0, True, id="fractional-at-limit"),
        pytest.param([0.5, 1.0, 0.5], 1.5, False, id="fractional-overweight"),
    ],
)
def test_will_it_fly_documented_conditions(q, w, expected):
    """Flying requires both a palindrome and a sum no greater than w."""
    assert will_it_fly(q, w) is expected
