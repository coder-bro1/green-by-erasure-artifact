import pytest
import sys
from pathlib import Path

# Keep imports working when pytest is launched via its console script, which
# does not always put the repository root on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solution import is_sorted


@pytest.mark.parametrize(
    "values",
    [
        [],
        [5],
        [1, 2, 3, 4, 5],
        [1, 2, 2, 3, 3, 4],
        [0, 0, 1, 1, 2, 2],
    ],
)
def test_is_sorted_accepts_ascending_lists(values):
    assert is_sorted(values) is True


@pytest.mark.parametrize(
    "values",
    [
        [1, 3, 2, 4, 5],
        [3, 2, 1],
        [1, 2, 3, 2],
    ],
)
def test_is_sorted_rejects_lists_with_a_decrease(values):
    assert is_sorted(values) is False


def test_is_sorted_does_not_modify_input():
    values = [1, 2, 2, 3]
    original = values.copy()

    is_sorted(values)

    assert values == original
