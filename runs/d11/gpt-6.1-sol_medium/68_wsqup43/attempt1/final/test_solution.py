"""Tests for planets strictly between two orbits, ordered from the Sun."""

import pytest

from solution import bf


PLANETS = (
    "Mercury", "Venus", "Earth", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune",
)


@pytest.mark.parametrize(
    "planet1, planet2, expected",
    [
        ("Jupiter", "Neptune", ("Saturn", "Uranus")),
        ("Earth", "Mercury", ("Venus",)),
        ("Mercury", "Uranus", ("Venus", "Earth", "Mars", "Jupiter", "Saturn")),
    ],
)
def test_documented_examples(planet1, planet2, expected):
    assert bf(planet1, planet2) == expected


@pytest.mark.parametrize("planet1", PLANETS)
@pytest.mark.parametrize("planet2", PLANETS)
def test_every_valid_pair(planet1, planet2):
    result = bf(planet1, planet2)

    # Select by orbital rank, independently of the implementation's slicing.
    ranks = {planet: rank for rank, planet in enumerate(PLANETS)}
    lower, upper = sorted((ranks[planet1], ranks[planet2]))
    expected = tuple(planet for planet in PLANETS if lower < ranks[planet] < upper)

    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.parametrize(
    "invalid_name",
    ["", "Pluto", "Sun", "Moon", "earth", "EARTH", " Earth", "Earth "],
)
@pytest.mark.parametrize("valid_name", PLANETS)
def test_invalid_name_in_either_position(invalid_name, valid_name):
    assert bf(invalid_name, valid_name) == ()
    assert bf(valid_name, invalid_name) == ()


@pytest.mark.parametrize(
    "planet1, planet2",
    [("Pluto", "Sun"), ("", ""), ("earth", "mars")],
)
def test_both_names_invalid(planet1, planet2):
    assert bf(planet1, planet2) == ()
