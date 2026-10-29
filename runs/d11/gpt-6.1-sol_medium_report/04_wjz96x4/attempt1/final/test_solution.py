"""Contract tests for the planet ordering documented by solution.bf."""

import pytest

from solution import bf


PLANETS = (
    "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"
)


def planet_pair_cases(*, known_bug=False):
    """Cover all valid endpoints, both directions, and equal endpoints."""
    for first_index, first in enumerate(PLANETS):
        for second_index, second in enumerate(PLANETS):
            lower, upper = sorted((first_index, second_index))
            expected = PLANETS[lower + 1:upper] if lower != upper else ()
            affected = "Jupiter" in expected or (
                "Jupiter" in (first, second) and bool(expected)
            )
            if affected != known_bug:
                continue
            yield pytest.param(first, second, expected, id=f"{first}-{second}")


@pytest.mark.parametrize("first,second,expected", planet_pair_cases())
def test_planets_between_valid_endpoints(first, second, expected):
    result = bf(first, second)
    assert isinstance(result, tuple)
    assert result == expected


@pytest.mark.xfail(
    strict=True,
    reason="The planet list spells Jupiter as Jupyter, rejecting Jupiter endpoints "
    "and returning Jupyter inside ranges instead of the documented Jupiter.",
)
@pytest.mark.parametrize("first,second,expected", planet_pair_cases(known_bug=True))
def test_jupiter_ranges_follow_documented_names(first, second, expected):
    result = bf(first, second)
    assert isinstance(result, tuple)
    assert result == expected


def invalid_name_cases(*, known_bug=False):
    """Invalid strings must be rejected in either argument position."""
    for invalid in ("", "Pluto", "earth", "MERCURY", " Earth ", "Jupyter"):
        for valid in PLANETS:
            affected = invalid == "Jupyter" and valid in (
                "Mercury", "Venus", "Earth", "Uranus", "Neptune"
            )
            if affected != known_bug:
                continue
            for reverse in (False, True):
                first, second = (valid, invalid) if reverse else (invalid, valid)
                yield pytest.param(first, second, id=f"{first!r}-{second!r}")


@pytest.mark.parametrize("first,second", invalid_name_cases())
def test_invalid_planet_names_return_empty_tuple(first, second):
    result = bf(first, second)
    assert isinstance(result, tuple)
    assert result == ()


@pytest.mark.xfail(
    strict=True,
    reason="Jupyter is not a documented planet name, but the implementation "
    "accepts it and returns nonempty ranges instead of an empty tuple.",
)
@pytest.mark.parametrize("first,second", invalid_name_cases(known_bug=True))
def test_misspelled_jupyter_is_rejected(first, second):
    result = bf(first, second)
    assert isinstance(result, tuple)
    assert result == ()


@pytest.mark.parametrize(
    "first,second",
    [("", ""), ("Pluto", "Ceres"), ("Jupyter", "Jupyter"), ("earth", "mars")],
)
def test_two_invalid_names_return_empty_tuple(first, second):
    assert bf(first, second) == ()
