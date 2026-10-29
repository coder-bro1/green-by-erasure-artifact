import pytest

from solution import bf


PLANETS = (
    "Mercury", "Venus", "Earth", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune",
)


@pytest.mark.parametrize(
    ("planet1", "planet2", "expected"),
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
def test_all_planet_pairs(planet1, planet2):
    """Cover both argument orders, equal planets, and adjacent orbits."""
    lower, upper = sorted((PLANETS.index(planet1), PLANETS.index(planet2)))
    expected = PLANETS[lower + 1:upper]

    result = bf(planet1, planet2)

    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.parametrize(
    "invalid_name",
    ["", "Pluto", "Jupyter", "earth", "EARTH", " Earth", "Earth "],
)
@pytest.mark.parametrize("invalid_position", [0, 1])
def test_invalid_planet_name(invalid_name, invalid_position):
    planets = ["Mercury", "Neptune"]
    planets[invalid_position] = invalid_name

    assert bf(*planets) == ()


def test_both_planet_names_invalid():
    assert bf("Pluto", "Sun") == ()
