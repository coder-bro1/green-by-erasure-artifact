"""Tests for the solar-system ordering contract documented by ``bf``."""

from itertools import product

import pytest

from solution import bf


PLANETS = (
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
)


@pytest.mark.parametrize(
    ("planet1", "planet2", "expected"),
    [
        ("Jupiter", "Neptune", ("Saturn", "Uranus")),
        ("Earth", "Mercury", ("Venus",)),
        ("Mercury", "Uranus", ("Venus", "Earth", "Mars", "Jupiter", "Saturn")),
    ],
)
def test_docstring_examples(planet1, planet2, expected):
    result = bf(planet1, planet2)

    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.parametrize(("planet1", "planet2"), product(PLANETS, repeat=2))
def test_every_valid_planet_pair(planet1, planet2):
    """Cover both directions, identical endpoints, and adjacent orbits."""
    first_position = PLANETS.index(planet1)
    second_position = PLANETS.index(planet2)
    expected = tuple(
        planet
        for position, planet in enumerate(PLANETS)
        if min(first_position, second_position)
        < position
        < max(first_position, second_position)
    )

    result = bf(planet1, planet2)

    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.parametrize(
    "invalid_name",
    ["", "Pluto", "Sun", "Moon", "mercury", "EARTH", " Earth", "Earth ", "Mars\n"],
)
@pytest.mark.parametrize("valid_name", PLANETS)
def test_invalid_planet_names_return_empty_tuple(invalid_name, valid_name):
    assert bf(invalid_name, valid_name) == ()
    assert bf(valid_name, invalid_name) == ()
    assert bf(invalid_name, invalid_name) == ()


def test_two_distinct_invalid_planet_names_return_empty_tuple():
    assert bf("Pluto", "Sun") == ()
