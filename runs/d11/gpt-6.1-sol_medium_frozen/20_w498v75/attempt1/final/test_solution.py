"""Tests for bf's documented contract, including its known Jupiter typo."""

from itertools import product

import pytest

from solution import bf


PLANETS = (
    "Mercury", "Venus", "Earth", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune",
)
JUPITER_TYPO = pytest.mark.xfail(
    strict=True,
    reason="solution.py spells Jupiter as Jupyter",
)


def planet_pair_cases():
    for first_index, second_index in product(range(len(PLANETS)), repeat=2):
        lower, upper = sorted((first_index, second_index))
        expected = PLANETS[lower + 1:upper] if lower != upper else ()
        first, second = PLANETS[first_index], PLANETS[second_index]
        affected = "Jupiter" in expected or (
            bool(expected) and "Jupiter" in (first, second)
        )
        yield pytest.param(
            first, second, expected,
            marks=[JUPITER_TYPO] if affected else [],
            id=f"{first}-{second}",
        )


@pytest.mark.parametrize("first,second,expected", planet_pair_cases())
def test_all_planet_pairs(first, second, expected):
    """Include both orders, equal planets, adjacent planets, and extremes."""
    result = bf(first, second)
    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.parametrize(
    "invalid",
    ["", "Pluto", "Sun", "earth", "EARTH", " Earth", "Earth ", "Mars\n"],
)
@pytest.mark.parametrize("invalid_first", [True, False])
def test_invalid_planet_in_either_position(invalid, invalid_first):
    args = (invalid, "Earth") if invalid_first else ("Earth", invalid)
    assert bf(*args) == ()


def test_both_planets_invalid():
    assert bf("Pluto", "Sun") == ()


@JUPITER_TYPO
@pytest.mark.parametrize("first,second", [("Jupyter", "Neptune"), ("Mercury", "Jupyter")])
def test_misspelled_jupiter_is_invalid(first, second):
    assert bf(first, second) == ()
