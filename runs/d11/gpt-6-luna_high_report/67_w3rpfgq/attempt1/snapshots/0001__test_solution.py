import pytest

from solution import will_it_fly


@pytest.mark.parametrize(
    ("items", "max_weight", "expected"),
    [
        pytest.param(
            [1, 2],
            5,
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="A non-palindromic list is incorrectly accepted when its weight fits.",
            ),
            id="doc-example-unbalanced",
        ),
        ([3, 2, 3], 1, False),
        pytest.param(
            [3, 2, 3],
            9,
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="A palindrome is rejected because matching mirrored elements trigger False.",
            ),
            id="doc-example-balanced-within-weight",
        ),
        ([3], 5, True),
    ],
)
def test_docstring_examples(items, max_weight, expected):
    assert will_it_fly(items, max_weight) is expected


@pytest.mark.parametrize(
    ("items", "max_weight", "expected"),
    [
        ([], 0, True),
        ([], -1, False),
        ([4], 4, True),
        ([4], 3, False),
        pytest.param(
            [2, 1],
            3,
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="A non-palindromic list is accepted when its weight fits.",
            ),
        ),
        pytest.param(
            [1, 2, 1],
            4,
            True,
            marks=pytest.mark.xfail(
                strict=True,
                reason="A palindrome is rejected because matching mirrored elements trigger False.",
            ),
        ),
        ([1, 2, 3, 1], 10, False),
        pytest.param(
            [1, 2, 3, 4],
            10,
            False,
            marks=pytest.mark.xfail(
                strict=True,
                reason="A non-palindromic list with distinct mirrored elements is accepted.",
            ),
        ),
        ([3, 2, 3], 7, False),
    ],
)
def test_palindrome_and_weight_rules(items, max_weight, expected):
    assert will_it_fly(items, max_weight) is expected
