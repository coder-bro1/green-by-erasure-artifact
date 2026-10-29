import pytest

from solution import running_peaks


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], [], id="empty"),
        pytest.param([7], [7], id="single-positive"),
        pytest.param([-7], [-7], id="single-negative"),
        pytest.param([0], [0], id="single-zero"),
        pytest.param([2, 5], [2, 5], id="two-increasing"),
        pytest.param([5, 2], [5, 5], id="two-decreasing"),
        pytest.param([4, 4, 4], [4, 4, 4], id="equal-values"),
        pytest.param([9, 5, 2, -1], [9, 9, 9, 9], id="decreasing"),
        pytest.param([1, 2, 3, 4], [1, 2, 3, 4], id="increasing"),
        pytest.param([2, 1, 5, 3, 6], [2, 2, 5, 5, 6], id="docstring-example"),
        pytest.param([-8, -5, -7, -2], [-8, -5, -5, -2], id="negative-values"),
        pytest.param([-3, 0, -1, 4], [-3, 0, 0, 4], id="mixed-signs"),
        pytest.param([2, 2, 5, 5, 3], [2, 2, 5, 5, 5], id="repeated-peaks"),
        pytest.param([0, 0, 0, 1], [0, 0, 0, 1], id="late-peak"),
        pytest.param(
            [10**100, -(10**100), 0],
            [10**100, 10**100, 10**100],
            id="large-integers",
        ),
    ],
)
def test_running_peaks(values, expected):
    assert running_peaks(values) == expected


def test_running_peaks_does_not_mutate_input():
    values = [2, 1, 5, 3, 6]
    original = values.copy()

    running_peaks(values)

    assert values == original


def test_running_peaks_returns_a_fresh_list():
    values = [5, 3, 1]

    result = running_peaks(values)

    assert isinstance(result, list)
    assert result is not values
    result.append(99)
    assert values == [5, 3, 1]


def test_running_peaks_calls_are_independent():
    first = running_peaks([9, 1])
    second = running_peaks([-2, -3])

    assert first == [9, 9]
    assert second == [-2, -2]
