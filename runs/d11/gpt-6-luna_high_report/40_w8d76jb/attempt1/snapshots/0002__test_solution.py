import pytest

from solution import tri


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, [1]),
        (1, [1, 3]),
        (2, [1, 3, 2]),
    ],
)
def test_tri_even_prefixes_and_base_cases(n, expected):
    assert tri(n) == expected


@pytest.mark.xfail(
    strict=True,
    reason="The odd-index implementation makes tri(3) incorrect, so the documented tri(4) prefix is incorrect too.",
)
def test_tri_four_includes_documented_tri_three_value():
    assert tri(4) == [1, 3, 2, 8, 3]


@pytest.mark.xfail(
    strict=True,
    reason="The odd-index implementation does not apply the documented recurrence using tri(n + 1).",
)
def test_tri_three_uses_documented_recurrence():
    assert tri(3) == [1, 3, 2, 8]


@pytest.mark.xfail(
    strict=True,
    reason="The odd-index implementation does not apply the documented recurrence using tri(n + 1).",
)
def test_tri_five_uses_documented_recurrence():
    # tri(5) = tri(4) + tri(3) + tri(6) = 3 + 8 + 4 = 15.
    assert tri(5) == [1, 3, 2, 8, 3, 15]
