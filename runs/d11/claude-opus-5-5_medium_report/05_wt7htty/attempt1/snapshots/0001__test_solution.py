import pytest

from solution import add

BUG = (
    "solution.add iterates range(1, len(lst), 1) instead of step 2, so even "
    "elements at even indices >= 2 are also summed"
)


# Cases where the implementation happens to agree with the spec
# (no even values at even indices >= 2).
@pytest.mark.parametrize(
    "lst, expected",
    [
        ([1], 0),                 # single element, no odd indices
        ([4], 0),                 # even element at index 0 is ignored
        ([1, 2], 2),
        ([1, 3], 0),              # odd value at odd index
        ([4, 88], 88),
        ([4, 5, 7, 2, 122], 124 - 2 + 2 - 122 + 122 if False else 2 + 0)  # placeholder replaced below
        if False else ([3, 4, 5, 6], 10),
        ([0, 0], 0),
        ([1, -2, 3, -4], -6),     # negative evens
        ([2, 1, 3, 1, 5], 0),     # all odd-index values odd
    ],
)
def test_add_matches_spec(lst, expected):
    assert add(lst) == expected


def test_does_not_mutate_input():
    lst = [1, 2, 3, 4]
    add(lst)
    assert lst == [1, 2, 3, 4]


# Cases that expose the bug: expected values follow the docstring.
@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example():
    assert add([4, 2, 6, 7]) == 2


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "lst, expected",
    [
        ([4, 88, 2], 88),             # 2 at index 2 must be excluded
        ([4, 5, 6, 7, 2, 122], 122),
        ([4, 0, 6, 7], 0),
        ([4, 4, 6, 8], 12),
    ],
)
def test_even_values_at_even_indices_excluded(lst, expected):
    assert add(lst) == expected
