"""Tests for the documented single-character Levenshtein distance."""

from itertools import product

import pytest

from solution import levenshtein


@pytest.mark.parametrize(
    ("source", "target", "expected"),
    [
        ("", "", 0),
        ("", "abc", 3),
        ("abc", "", 3),
        ("a", "a", 0),
        ("unchanged", "unchanged", 0),
        ("a", "b", 1),
        ("cat", "cut", 1),
        ("cat", "cats", 1),
        ("cat", "at", 1),
        ("cat", "cart", 1),
        ("cat", "scat", 1),
        ("abc", "xyz", 3),
        ("kitten", "sitting", 3),
        ("electron", "neutron", 3),
        ("ab", "ba", 2),  # Swapping characters is not a permitted single edit.
        ("aaa", "a", 2),
        ("aab", "aba", 2),
        ("Cat", "cat", 1),
        ("a b", "ab", 1),
        ("a\nb", "ab", 1),
        ("café", "cafe", 1),
        ("猫", "犬", 1),
        ("a😀b", "ab", 1),
        ("é", "e\u0301", 2),  # Strings are compared without Unicode normalization.
    ],
)
def test_documented_distance(source, target, expected):
    assert levenshtein(source, target) == expected
    assert levenshtein(target, source) == expected


def _distance_by_edit_graph(source, target):
    """Find the minimum cost path through character positions independently."""
    frontier = {(0, 0)}
    visited = set(frontier)
    distance = 0
    while frontier:
        # Matching characters cost no edits, so close over them at this level.
        pending = list(frontier)
        while pending:
            i, j = pending.pop()
            if i < len(source) and j < len(target) and source[i] == target[j]:
                match = (i + 1, j + 1)
                if match not in visited:
                    visited.add(match)
                    frontier.add(match)
                    pending.append(match)
        if (len(source), len(target)) in frontier:
            return distance
        next_frontier = set()
        for i, j in frontier:
            neighbors = []
            if i < len(source):
                neighbors.append((i + 1, j))  # Delete.
            if j < len(target):
                neighbors.append((i, j + 1))  # Insert.
            if i < len(source) and j < len(target):
                neighbors.append((i + 1, j + 1))  # Substitute.
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_frontier.add(neighbor)
        frontier = next_frontier
        distance += 1
    raise AssertionError("The target should always be reachable")


_SHORT_STRINGS = [
    "".join(characters)
    for length in range(4)
    for characters in product("ab", repeat=length)
]


@pytest.mark.parametrize("source", _SHORT_STRINGS)
@pytest.mark.parametrize("target", _SHORT_STRINGS)
def test_all_short_strings_have_minimum_edit_distance(source, target):
    assert levenshtein(source, target) == _distance_by_edit_graph(source, target)
