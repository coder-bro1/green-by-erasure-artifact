import pytest

from solution import add


# --- Behaviour that agrees with both the docstring spec and the implementation ---

@pytest.mark.parametrize(
    "lst, expected",
    [
        ([4, 88], 88),              # single odd index, even value
        ([4, 5], 0),                # odd-index value is odd
        ([7], 0),                   # single element: no odd indices
        ([2], 0),                   # index 0 is ignored even if even
        ([1, 3, 5, 7], 0),          # no even values anywhere
        ([0, 0], 0),                # zero is even, sums to 0
        ([1, -4], -4),              # negative even value
        ([5, 2, 7, 4], 6),          # even indices hold odd values
    ],
)
def test_add_spec_consistent(lst, expected):
    assert add(lst) == expected


def test_index_zero_never_counted():
    assert add([100, 1, 3]) == 0


def test_does_not_mutate_input():
    lst = [4, 2, 6, 7]
    add(lst)
    assert lst == [4, 2, 6, 7]


def test_returns_int():
    assert isinstance(add([1, 2]), int)


# --- Actual implementation behaviour (iterates every index >= 1) ---

@pytest.mark.parametrize(
    "lst, expected",
    [
        ([4, 2, 6, 7], 8),          # 2 (idx1) + 6 (idx2)
        ([4, 4, 6, 8], 18),         # 4 + 6 + 8
        ([1, 3, 2, 5], 2),          # even value at even index 2 is counted
        ([0, 2, 4, 6, 8, 10], 30),
    ],
)
def test_add_actual_behaviour(lst, expected):
    assert add(lst) == expected


# --- Documented spec where the implementation diverges (known bug) ---

@pytest.mark.xfail(
    strict=True,
    reason="Bug: range step is 1, so even-index elements (>=2) are also summed",
)
@pytest.mark.parametrize(
    "lst, expected",
    [
        ([4, 2, 6, 7], 2),          # docstring example
        ([4, 4, 6, 8], 12),
        ([4, 0, 6, 7], 0),
    ],
)
def test_add_docstring_spec(lst, expected):
    assert add(lst) == expected
