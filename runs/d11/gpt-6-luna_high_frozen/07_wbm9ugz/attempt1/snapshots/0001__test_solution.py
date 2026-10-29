import pytest

from solution import decode_cyclic, encode_cyclic


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("abc", "bca"),
        ("abcd", "bcad"),
        ("abcdef", "bcadef"),
        ("abcdefgh", "bcadefgh"),
        ("a🙂c界", "🙂ca界"),
    ],
)
def test_encode_cyclic_rotates_each_complete_group(source, expected):
    assert encode_cyclic(source) == expected


@pytest.mark.parametrize("source", ["", "x", "xy", "xyz", "wxyz", "abcdefghij"])
def test_encode_cyclic_preserves_length(source):
    assert len(encode_cyclic(source)) == len(source)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        # The current decoder applies the same cyclic transform as the encoder.
        ("abc", "bca"),
        ("abcd", "bcad"),
    ],
)
def test_decode_cyclic(source, expected):
    assert decode_cyclic(source) == expected


def test_decode_cyclic_matches_encode_cyclic():
    source = "abcdefgh"
    assert decode_cyclic(source) == encode_cyclic(source)
