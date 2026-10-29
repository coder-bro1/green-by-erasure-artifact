import pytest

from solution import bucketsort


@pytest.mark.parametrize("k", [0, 1, 8])
def test_empty_input(k):
    assert bucketsort([], k) == []


@pytest.mark.parametrize(
    "arr, k, expected",
    [
        pytest.param([0], 1, [0], id="single-zero"),
        pytest.param([4], 5, [4], id="single-upper-bound-minus-one"),
        pytest.param([0, 0, 0], 1, [0, 0, 0], id="all-zeros"),
        pytest.param([2, 2, 2], 3, [2, 2, 2], id="repeated-nonzero"),
        pytest.param([0, 1, 2, 3], 4, [0, 1, 2, 3], id="already-sorted"),
        pytest.param([3, 2, 1, 0], 4, [0, 1, 2, 3], id="reverse-sorted"),
        pytest.param([3, 0, 3, 1, 0], 4, [0, 0, 1, 3, 3], id="mixed-duplicates"),
        pytest.param([2, 0, 1], 10, [0, 1, 2], id="unused-buckets"),
        pytest.param([1, 0, 1, 0, 1], 2, [0, 0, 1, 1, 1], id="length-exceeds-bound"),
        pytest.param([1, 2, 1, 0], 3, [0, 1, 1, 2], id="self-describing-counts"),
        pytest.param([2, 0, 2, 0], 3, [0, 0, 2, 2], id="self-describing-with-gap"),
    ],
)
def test_elements_are_returned_in_sorted_order(arr, k, expected):
    assert all(isinstance(x, int) and 0 <= x < k for x in arr)
    assert bucketsort(arr, k) == expected


@pytest.mark.parametrize("arr, k", [([], 0), ([3, 0, 3, 1, 0], 4)])
def test_input_is_not_modified(arr, k):
    original = arr.copy()
    bucketsort(arr, k)
    assert arr == original
