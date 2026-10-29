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
        (9, [1, 3, 2, 8, 3, 15, 4, 24, 5, 35]),
    ],
)
def test_known_sequences(n, expected):
    assert tri(n) == expected


@pytest.mark.parametrize("n", [0, 1, 2, 3, 10, 99, 100, 1000])
def test_sequence_length_and_initial_values(n):
    result = tri(n)

    assert isinstance(result, list)
    assert len(result) == n + 1
    assert result[0] == 1
    if n >= 1:
        assert result[1] == 3


def test_even_terms_follow_definition():
    result = tri(100)

    for index in range(2, 101, 2):
        assert result[index] == 1 + index // 2


def test_odd_terms_follow_definition():
    result = tri(100)

    for index in range(3, 100, 2):
        assert result[index] == (
            result[index - 1] + result[index - 2] + result[index + 1]
        )


@pytest.mark.parametrize("n", [0, 1, 2, 3, 9, 10, 99])
def test_extending_sequence_preserves_prefix(n):
    assert tri(n + 1)[:-1] == tri(n)


def test_calls_return_independent_lists():
    first = tri(3)
    second = tri(3)

    assert first is not second
    first[0] = -1
    first.append(-1)
    assert second == [1, 3, 2, 8]
    assert tri(3) == [1, 3, 2, 8]
