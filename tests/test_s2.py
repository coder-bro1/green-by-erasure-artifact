"""S2: building buggy programs from model answers and comparing outputs (scripts/s2_natural_faults.py)."""
import ast
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('s2', Path(__file__).resolve().parents[1] / 'scripts' / 's2_natural_faults.py')
s2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s2)

TASK = {'entry_point': 'add_all', 'prompt': 'from typing import List\n\n\ndef add_all(xs: List[int]) -> int:\n    """Return the sum of xs.\n    >>> add_all([1, 2])\n    3\n    """\n'}

ANSWER = '''Here is the function:

```python
from typing import List
import math


def add_all(xs: List[int]) -> int:
    """My own docstring that must not survive."""
    return helper(xs) + 1


def helper(xs):
    return sum(xs)
```
'''


def test_extract_keeps_the_task_prompt_and_takes_the_models_body_and_helpers():
    program = s2.extract(ANSWER, TASK)
    assert program.startswith(TASK['prompt'].rstrip('\n'))
    assert 'My own docstring' not in program and 'return helper(xs) + 1' in program
    assert 'def helper(xs):' in program and 'import math' in program
    fn = next(n for n in ast.parse(program).body if isinstance(n, ast.FunctionDef) and n.name == 'add_all')
    assert ast.get_docstring(fn).startswith('Return the sum of xs.')
    namespace = {}
    exec(program, namespace)
    assert namespace['add_all']([1, 2]) == 4  # the model's (wrong) behaviour is preserved


def test_extract_rejects_answers_without_the_function_or_with_only_a_docstring():
    assert s2.extract('```python\ndef other():\n    return 1\n```', TASK) is None
    assert s2.extract('```python\ndef add_all(xs):\n    """Only text."""\n```', TASK) is None
    assert s2.extract('not code at all (', TASK) is None


def test_same_uses_tolerance_for_floats_and_exact_types_elsewhere():
    assert s2.same(0.1 + 0.2, 0.3, 0) and not s2.same(0.3, 0.31, 0)
    assert s2.same([1, (2.0, 'a')], [1, (2.0000000001, 'a')], 0)
    assert not s2.same([1, 2], (1, 2), 0) and not s2.same(None, 0, 0)
    assert s2.same(True, 1, 0)  # equal under ==, which HumanEval's own assertions use
