import pytest

from solution import max_sublist_sum


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([], 0, id="empty-list"),
        pytest.param([7], 7, id="single-positive"),
        pytest.param([-7], 0, id="single-negative-empty-sublist-wins"),
        pytest.param([0], 0, id="single-zero"),
        pytest.param([-5, -2, -9], 0, id="all-negative"),
        pytest.param([0, 0, 0], 0, id="all-zero"),
        pytest.param([1, 2, 3, 4], 10, id="all-positive"),
        pytest.param([2, 0, 3, 0], 5, id="positive-with-zeros"),
        pytest.param([5, -1, 2], 6, id="best-sublist-spans-negative"),
        pytest.param([5, -1, -2], 5, id="best-sublist-at-start"),
        pytest.param([3, -3, 3], 3, id="tied-maxima"),
        pytest.param([10**100, -1, 10**100], 2 * 10**100 - 1, id="large-integers"),
    ],
)
def test_max_sublist_sum(arr, expected):
    assert max_sublist_sum(arr) == expected


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Docstring promises the maximum over all sublists, but the implementation "
        "only tracks prefix sums and never restarts after a negative running sum."
    ),
)
@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([4, -5, 2, 1, -1, 3], 5, id="docstring-example"),
        pytest.param([-2, 3], 3, id="skip-negative-prefix"),
        pytest.param([5, -10, 7], 7, id="restart-after-negative-running-sum"),
        pytest.param([-3, 5, -1, -10], 5, id="best-sublist-in-middle"),
        pytest.param([1, -2, 3, -1, 4], 6, id="later-sublist-spans-negative"),
    ],
)
def test_max_sublist_sum_can_start_after_first_element(arr, expected):
    assert max_sublist_sum(arr) == expected


def test_max_sublist_sum_does_not_modify_input():
    arr = [5, -1, 2, 0, -3]
    original = arr.copy()

    max_sublist_sum(arr)

    assert arr == original
