import pytest

from solution import weave_separator


# The implementation omits the last item for every nonempty input. Keep the
# documented contract visible without changing solution.py. Strict xfail means
# fixing this bug will require removing these markers rather than passing silently.
missing_final_item = pytest.mark.xfail(
    strict=True,
    reason="Known bug: weave_separator omits the final input item",
)


@pytest.mark.parametrize(
    ("values", "sep", "expected"),
    [
        ([], 2, []),
        pytest.param([7], 0, [7], marks=missing_final_item),
        pytest.param([7, 8], 0, [7, 0, 8], marks=missing_final_item),
        pytest.param([5, 5, 5], -1, [5, -1, 5, -1, 5], marks=missing_final_item),
        pytest.param([-3, 0, 4], 9, [-3, 9, 0, 9, 4], marks=missing_final_item),
        pytest.param([2, 2], 2, [2, 2, 2], marks=missing_final_item),
        pytest.param([1, 2, 3, 4], 0, [1, 0, 2, 0, 3, 0, 4], marks=missing_final_item),
    ],
    ids=["empty", "singleton", "two-items", "duplicates", "mixed-signs", "same-separator", "four-items"],
)
def test_weave_separator_contract(values, sep, expected):
    assert weave_separator(values, sep) == expected


@pytest.mark.parametrize("values", [[], [7], [7, 8], [5, 5, 5]])
def test_returns_new_list_without_modifying_input(values):
    original = values.copy()

    result = weave_separator(values, -1)

    assert isinstance(result, list)
    assert result is not values
    assert values == original

    result.append(99)
    assert values == original


def test_calls_return_independent_lists():
    first = weave_separator([], 2)
    second = weave_separator([], 2)

    assert first is not second
    first.append(99)
    assert second == []
