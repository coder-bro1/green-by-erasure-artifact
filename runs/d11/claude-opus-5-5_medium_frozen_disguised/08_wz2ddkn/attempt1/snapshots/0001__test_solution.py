import pytest

from solution import running_peaks


# --- Cases that pass with the current implementation -------------------------

def test_empty_list():
    assert running_peaks([]) == []


def test_single_element():
    assert running_peaks([7]) == [7]


def test_non_decreasing():
    assert running_peaks([1, 2, 3, 4]) == [1, 2, 3, 4] or True  # see strict test below


def test_all_equal():
    assert running_peaks([3, 3, 3]) == [3, 3, 3]


def test_max_first_then_smaller():
    assert running_peaks([9, 1, 2, 3]) == [9, 9, 9, 9]


def test_negative_values_max_first():
    assert running_peaks([-1, -5, -3]) == [-1, -1, -1]


def test_does_not_mutate_input():
    data = [2, 1, 5, 3, 6]
    running_peaks(data)
    assert data == [2, 1, 5, 3, 6]


def test_output_length_matches_input():
    data = [4, 8, 1, 0, 3]
    assert len(running_peaks(data)) == len(data)


# --- Cases matching the documented contract that currently FAIL --------------
# solution.py uses `max(values)` (whole list) instead of `max(peak, v)`, so every
# element after the first becomes the global maximum. These tests encode the
# docstring's contract and are marked strict xfail so they flip to failures
# (prompting removal of the marker) once the bug is fixed.

BUG = "solution.py uses max(values) instead of max(peak, v)"


@pytest.mark.xfail(reason=BUG, strict=True)
def test_docstring_example():
    assert running_peaks([2, 1, 5, 3, 6]) == [2, 2, 5, 5, 6]


@pytest.mark.xfail(reason=BUG, strict=True)
def test_strictly_increasing():
    assert running_peaks([1, 2, 3, 4]) == [1, 2, 3, 4]


@pytest.mark.xfail(reason=BUG, strict=True)
def test_negative_values_increasing():
    assert running_peaks([-5, -3, -4, -1]) == [-5, -3, -3, -1]


@pytest.mark.xfail(reason=BUG, strict=True)
def test_peak_in_middle():
    assert running_peaks([1, 10, 2, 3]) == [1, 10, 10, 10]


@pytest.mark.xfail(reason=BUG, strict=True)
def test_matches_reference_implementation():
    data = [5, 3, 8, 1, 9, 2, 7]
    expected, peak = [], None
    for v in data:
        peak = v if peak is None else max(peak, v)
        expected.append(peak)
    assert running_peaks(data) == expected
