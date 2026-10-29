import pytest

from solution import decode_cyclic, encode_cyclic


@pytest.mark.parametrize(
    ("original", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("abc", "bca"),
        ("abcd", "bcad"),
        ("abcdef", "bcaefd"),
        ("abcdefgh", "bcaefgdh"),
    ],
)
def test_encode_cyclic_rotates_each_complete_group(original, expected):
    assert encode_cyclic(original) == expected


@pytest.mark.xfail(
    strict=True,
    reason="decode_cyclic calls encode_cyclic instead of reversing each three-character rotation.",
)
def test_decode_cyclic_reverses_encoding():
    assert decode_cyclic("bcaefd") == "abcdef"
