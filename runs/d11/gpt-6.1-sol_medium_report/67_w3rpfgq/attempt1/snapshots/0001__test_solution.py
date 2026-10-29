import pytest

from solution import will_it_fly


@pytest.mark.parametrize(
    ("q", "w", "expected"),
    [
        pytest.param([1, 2], 5, False, id="example-unbalanced"),
        pytest.param([3, 2, 3], 1, False, id="example-overweight"),
        pytest.param([3, 2, 3], 9, True, id="example-balanced"),
        pytest.param([3], 5, True, id="example-singleton"),
        pytest.param([2, 4, 2], 8, True, id="odd-palindrome-at-limit"),
        pytest.param([2, 4, 2], 7, False, id="odd-palindrome-over-limit"),
        pytest.param([1, 2, 2, 1], 6, True, id="even-palindrome-at-limit"),
        pytest.param([1, 2, 2, 1], 5, False, id="even-palindrome-over-limit"),
        pytest.param([2, 2], 4, True, id="equal-pair-at-limit"),
        pytest.param([1, 2], 3, False, id="unequal-pair-at-limit"),
        pytest.param([1, 2, 3], 6, False, id="odd-unbalanced-at-limit"),
        pytest.param([1, 2, 3, 4], 10, False, id="even-unbalanced-at-limit"),
        pytest.param([1, 2, 3, 1], 7, False, id="matching-ends-unbalanced-middle"),
        pytest.param([1, 2, 2, 3], 8, False, id="matching-middle-unbalanced-ends"),
        pytest.param([1, 2], 2, False, id="unbalanced-overweight"),
        pytest.param([5], 5, True, id="singleton-at-limit"),
        pytest.param([5], 4, False, id="singleton-over-limit"),
        pytest.param([], 0, True, id="empty-at-limit"),
        pytest.param([], 1, True, id="empty-below-limit"),
        pytest.param([], -1, False, id="empty-over-limit"),
        pytest.param([0, 0, 0], 0, True, id="zero-palindrome-at-limit"),
        pytest.param([-2, 1, -2], -3, True, id="negative-sum-at-limit"),
        pytest.param([-2, 1, -2], -4, False, id="negative-sum-over-limit"),
        pytest.param([1.5, 2.0, 1.5], 5.0, True, id="fractional-palindrome-at-limit"),
    ],
)
def test_will_it_fly_matches_documented_balance_and_weight(q, w, expected):
    assert will_it_fly(q, w) is expected
