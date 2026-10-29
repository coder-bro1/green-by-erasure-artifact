"""Tests for count_odd_edged, including its existing digit-2 behavior."""

import pytest

from solution import count_odd_edged


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([31, 25, 12, 9], 3, id="first-docstring-input-current-result"),
        pytest.param([57, -73], 1, id="second-docstring-example"),
        pytest.param([-135, -31, -11, 0, 1, 9, 10], 0, id="at-or-below-threshold"),
        pytest.param([11], 1, id="just-above-threshold"),
        pytest.param([11, 33, 55, 77, 99], 5, id="odd-edge-digits"),
        pytest.param([41, 63, 85], 0, id="even-first-digit"),
        pytest.param([14, 36, 58], 0, id="even-last-digit"),
        pytest.param([44, 66, 88], 0, id="both-edges-even"),
        pytest.param([30, 50, 70, 90, 100], 0, id="trailing-zero"),
        pytest.param([101, 305, 507, 709, 901], 5, id="interior-zero"),
        pytest.param([145, 367, 589, 761, 983], 5, id="interior-even-digits"),
        pytest.param([31, 31, 31, 44], 3, id="duplicates-count-separately"),
        pytest.param([10**100 + 1, 4 * 10**100 + 1], 1, id="large-integers"),
    ],
)
def test_count_odd_edged(values, expected):
    assert count_odd_edged(values) == expected


@pytest.mark.parametrize("value", [12, 21, 22, 25, 32, 202])
def test_digit_two_is_currently_accepted(value):
    # The implementation includes 2 in its accepted digits, despite the
    # docstring's "odd" requirement. These tests record existing behavior.
    assert count_odd_edged([value]) == 1


def test_accepts_tuple():
    assert count_odd_edged((31, 44, 57, -73)) == 2


def test_accepts_single_pass_iterator():
    values = iter([31, 44, 57, -73])
    assert count_odd_edged(values) == 2
    assert list(values) == []


def test_does_not_modify_input_list():
    values = [31, 44, 57, -73]
    original = values.copy()
    assert count_odd_edged(values) == 2
    assert values == original
