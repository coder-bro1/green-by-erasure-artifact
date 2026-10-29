"""S4: specification variants for the judge replay (scripts/s4_judge_specs.py)."""
import ast
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('s4', Path(__file__).resolve().parents[1] / 'scripts' / 's4_judge_specs.py')
s4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s4)

HUMANEVAL = '''from typing import List


def sort_array(arr: List[int]) -> List[int]:
    """Sort the array in ascending order, ignoring negative numbers.
    If the array is empty, return an empty list.

    For example:
    >>> sort_array([3, 1, 2])
    [1, 2, 3]
    >>> sort_array([])
    []
    """
'''

PROSE = '''def f(coins, total):
    """Count ways.

    Output:
        The number of ways. For example, there are four ways for 11:
            1. {1: 11}
            2. {1: 6, 5: 1}

    Preconditions:
        total >= 0
    """
'''


def test_no_examples_keeps_rules_and_removes_examples():
    out = s4.transform(HUMANEVAL, 'no_examples', 'sort_array')
    assert 'If the array is empty, return an empty list.' in out and 'ignoring negative numbers' in out
    assert '>>>' not in out and '[1, 2, 3]' not in out and 'For example' not in out
    assert out.startswith('from typing import List') and isinstance(ast.parse(out).body[-1], ast.FunctionDef)


def test_prose_example_is_cut_to_the_end_of_its_paragraph():
    out = s4.transform(PROSE, 'no_examples', 'f')
    assert 'The number of ways.' in out and 'four ways' not in out and '{1: 11}' not in out
    assert 'total >= 0' in out


def test_signature_only_has_no_docstring():
    out = s4.transform(HUMANEVAL, 'signature_only', 'sort_array')
    fn = ast.parse(out).body[-1]
    assert ast.get_docstring(fn) is None and 'def sort_array(arr: List[int]) -> List[int]:' in out


def test_description_after_an_import_inside_the_function():
    src = 'def g(x):\n    import math\n    """Return x squared.\n\n    Example:\n        g(2) -> 4\n    """\n'
    out = s4.transform(src, 'no_examples', 'g')
    assert 'Return x squared.' in out and 'g(2)' not in out and 'import math' in out


def test_split_prompt_round_trips_and_rejects_edits():
    prompt = s4.TEMPLATE.format_map({'spec': HUMANEVAL, 'test': 'def test_a():\n    assert sort_array([2, 1]) == [1, 2]'})
    spec_text, test_text = s4.split_prompt(prompt)
    assert spec_text == HUMANEVAL and test_text.startswith('def test_a')
    with pytest.raises(ValueError):
        s4.split_prompt(prompt.replace('Question: if', 'Question: if', 1).replace('You review', 'You check'))
