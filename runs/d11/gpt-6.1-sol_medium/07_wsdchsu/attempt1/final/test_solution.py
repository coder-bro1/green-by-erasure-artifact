import pytest

from solution import will_it_fly


@pytest.mark.parametrize(
    ("q", "w", "expected"),
    [
        pytest.param([1, 2], 5, False, id="example-unbalanced"),
        pytest.param([3, 2, 3], 1, False, id="example-overweight"),
        pytest.param([3, 2, 3], 9, True, id="example-balanced"),
        pytest.param([3], 5, True, id="example-single-element"),
        pytest.param([], 0, True, id="empty-at-capacity"),
        pytest.param([], -1, False, id="empty-overweight"),
        pytest.param([3], 3, True, id="single-at-capacity"),
        pytest.param([3], 2, False, id="single-overweight"),
        pytest.param([2, 2], 4, True, id="even-at-capacity"),
        pytest.param([2, 2], 3, False, id="even-overweight"),
        pytest.param([3, 2, 3], 8, True, id="odd-at-capacity"),
        pytest.param([3, 2, 3], 7, False, id="odd-just-overweight"),
        pytest.param([1, 2, 2, 1], 6, True, id="even-palindrome"),
        pytest.param([1, 2, 3, 2, 1], 9, True, id="odd-palindrome"),
        pytest.param([1, 2, 3, 1], 7, False, id="inner-mismatch"),
        pytest.param([1, 2, 2, 3], 8, False, id="outer-mismatch"),
        pytest.param([1, 2, 3, 4], 10, False, id="all-pairs-mismatch"),
        pytest.param([0, 0, 0], 0, True, id="zero-weights"),
        pytest.param([-2, 1, -2], -3, True, id="negative-at-capacity"),
        pytest.param([-2, 1, -2], -4, False, id="negative-overweight"),
    ],
)
def test_will_it_fly(q, w, expected):
    assert will_it_fly(q, w) is expected
