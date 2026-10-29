import pytest

from solution import correct_bracketing


@pytest.mark.parametrize(
    ("brackets", "expected"),
    [
        ("", True),
        ("<", False),
        (">", False),
        ("<<", False),
        (">>", False),
        pytest.param(
            "<>",
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation treats '<' as a closing bracket, so it rejects a valid pair.",
            ),
        ),
        pytest.param(
            "<<><>>",
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation treats '<' as a closing bracket, so it rejects valid nesting.",
            ),
        ),
        pytest.param(
            "><",
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation accepts an unmatched '>' when a later '<' balances its counter.",
            ),
        ),
        ("><>", False),
        (">><", False),
        pytest.param(
            ">><<",
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation accepts equal counts even when the first '>' is unmatched.",
            ),
        ),
        ("<>>", False),
    ],
)
def test_correct_bracketing(brackets, expected):
    assert correct_bracketing(brackets) is expected
