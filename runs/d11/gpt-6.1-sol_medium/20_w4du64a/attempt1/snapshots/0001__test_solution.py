import pytest

from solution import tri


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, [1]),
        (1, [1, 3]),
        (2, [1, 3, 2]),
        (3, [1, 3, 2, 8]),
        (4, [1, 3, 2, 8, 3]),
        (5, [1, 3, 2, 8, 3, 15]),
        (10, [1, 3, 2, 8, 3, 15, 4, 24, 5, 35, 6]),
    ],
)
def test_known_sequence_values(n, expected):
    assert tri(n) == expected


@pytest.mark.parametrize("n", range(51))
def test_sequence_length_and_recurrence(n):
    values = tri(n)

    assert isinstance(values, list)
    assert len(values) == n + 1
    assert values[0] == 1
    if n >= 1:
        assert values[1] == 3

    for index in range(2, n + 1):
        if index % 2 == 0:
            assert values[index] == 1 + index // 2
        else:
            # The following even term is defined directly, even when it is
            # beyond the requested prefix of the sequence.
            next_even = 1 + (index + 1) // 2
            assert values[index] == values[index - 1] + values[index - 2] + next_even


def test_each_call_returns_an_independent_list():
    values = tri(3)
    values[0] = -1
    values.append(99)

    assert tri(3) == [1, 3, 2, 8]
