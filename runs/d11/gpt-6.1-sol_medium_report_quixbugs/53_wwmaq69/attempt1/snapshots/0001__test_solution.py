"""Tests for the documented nonnegative integer bitcount contract."""

import pytest

from solution import bitcount


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (5, 2),
        (10, 2),
        (42, 3),
        (85, 4),
        (127, 7),
        (128, 1),
        (129, 2),
        (255, 8),
    ],
)
def test_bitcount_known_values(n, expected):
    assert bitcount(n) == expected


@pytest.mark.parametrize("position", [0, 1, 7, 8, 31, 32, 63, 64, 127, 256, 1024])
def test_bitcount_single_set_bit(position):
    assert bitcount(1 << position) == 1


@pytest.mark.parametrize("width", [1, 2, 7, 8, 31, 32, 64, 127, 256, 1024])
def test_bitcount_all_bits_set(width):
    assert bitcount((1 << width) - 1) == width


@pytest.mark.parametrize(
    "positions",
    [(0, 64), (31, 32, 63, 64), (0, 127, 256, 1024)],
)
def test_bitcount_sparse_large_integers(positions):
    n = sum(1 << position for position in positions)
    assert bitcount(n) == len(positions)


def test_bitcount_matches_binary_encoding_for_small_integers():
    for n in range(4096):
        assert bitcount(n) == bin(n).count("1"), f"Incorrect bitcount for {n}"


@pytest.mark.parametrize("n", [0, 1, 127, 128, (1 << 256) - 1])
def test_bitcount_returns_an_integer(n):
    assert type(bitcount(n)) is int
