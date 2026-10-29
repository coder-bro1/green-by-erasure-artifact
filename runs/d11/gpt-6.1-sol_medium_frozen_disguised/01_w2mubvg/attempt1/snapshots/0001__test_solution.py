"""Tests for the documented contract, with the known Jupiter typo tracked."""

import pytest

from solution import planets_between


PLANETS = (
    "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"
)
JUPITER_TYPO = pytest.mark.xfail(
    strict=True,
    reason="solution.py uses 'Jupyter' instead of the documented planet 'Jupiter'",
)


def planet_pairs():
    for first_index, inner in enumerate(PLANETS):
        for second_index, outer in enumerate(PLANETS):
            low, high = sorted((first_index, second_index))
            expected = PLANETS[low + 1:high]
            affected = bool(expected) and (
                "Jupiter" in (inner, outer) or "Jupiter" in expected
            )
            yield pytest.param(
                inner, outer, expected,
                marks=JUPITER_TYPO if affected else (),
                id=f"{inner}-{outer}",
            )


@pytest.mark.parametrize("inner,outer,expected", planet_pairs())
def test_all_planet_pairs(inner, outer, expected):
    """Check ordering, exclusion of endpoints, equal names, and adjacency."""
    result = planets_between(inner, outer)
    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.parametrize(
    "invalid",
    [
        "Pluto", "Sun", "mercury", "EARTH", "jupiter", " Earth", "Earth ",
        "", None, 42, [], {},
        pytest.param("Jupyter", marks=JUPITER_TYPO, id="misspelled-jupiter"),
    ],
)
@pytest.mark.parametrize("invalid_is_inner", [True, False])
def test_invalid_name_in_either_position(invalid, invalid_is_inner):
    args = (invalid, "Mercury") if invalid_is_inner else ("Mercury", invalid)
    assert planets_between(*args) == ()


def test_both_names_invalid():
    assert planets_between("Pluto", "Sun") == ()
