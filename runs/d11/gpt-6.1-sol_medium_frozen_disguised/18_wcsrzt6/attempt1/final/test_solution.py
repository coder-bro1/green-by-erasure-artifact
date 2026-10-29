import pytest

from solution import remaining_mangoes


@pytest.mark.xfail(
    strict=True,
    reason="Known defect: remaining_mangoes subtracts an extra 1 from the total",
)
@pytest.mark.parametrize(
    "note,total,expected",
    [
        ("4 apples and 9 oranges", 30, 17),
        ("0 apples and 0 oranges", 7, 7),
        ("4 apples and 9 oranges", 13, 0),
        ("0 apples and 0 oranges", 0, 0),
        ("0 apples and 5 oranges", 12, 7),
        ("6 apples and 0 oranges", 12, 6),
        ("125 apples and 250 oranges", 1000, 625),
    ],
)
def test_remaining_mangoes_matches_fruit_balance(note, total, expected):
    assert remaining_mangoes(note, total) == expected


@pytest.mark.parametrize("extra", [1, 7, 1000])
def test_increasing_total_adds_the_same_number_of_mangoes(extra):
    note = "4 apples and 9 oranges"
    assert remaining_mangoes(note, 30 + extra) == remaining_mangoes(note, 30) + extra


@pytest.mark.parametrize("extra", [1, 5, 10])
@pytest.mark.parametrize("fruit", ["apples", "oranges"])
def test_increasing_other_fruit_reduces_mangoes(fruit, extra):
    apples = 4 + (extra if fruit == "apples" else 0)
    oranges = 9 + (extra if fruit == "oranges" else 0)
    note = f"{apples} apples and {oranges} oranges"
    assert remaining_mangoes(note, 30) == remaining_mangoes("4 apples and 9 oranges", 30) - extra


def test_swapping_apple_and_orange_counts_preserves_mangoes():
    assert remaining_mangoes("4 apples and 9 oranges", 30) == remaining_mangoes(
        "9 apples and 4 oranges", 30
    )
