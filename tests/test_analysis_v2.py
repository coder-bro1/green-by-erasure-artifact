import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'analysis'))
from change_modes_v2 import change_modes_v2  # noqa: E402
from judge_replay import split_v1_prompt, verdict  # noqa: E402

PRE = 'from solution import *\n'
TEST = 'def test_x():\n    assert f(1) == 2\n'


def test_shadow_in_prelude_with_unchanged_test():
    after = PRE + 'def f(a):\n    return a + 1\n' + TEST
    assert change_modes_v2(PRE + TEST, after, 'f') == ['FUNCTION_SHADOWED']


def test_shadow_by_assignment_and_monkeypatch():
    assert 'FUNCTION_SHADOWED' in change_modes_v2(PRE + TEST, PRE + 'f = lambda a: a + 1\n' + TEST, 'f')
    patched = PRE + 'def test_x(monkeypatch):\n    monkeypatch.setattr("solution.f", lambda a: 2)\n    assert f(1) == 2\n'
    assert 'FUNCTION_SHADOWED' in change_modes_v2(PRE + TEST, patched, 'f')


def test_v1_modes_are_kept_and_other_is_refined():
    assert change_modes_v2(PRE + TEST, PRE + TEST.replace('== 2', '== 3'), 'f') == ['EXPECTED_CHANGED']
    assert change_modes_v2(PRE + TEST, 'import math\n' + PRE + TEST, 'f') == ['SETUP_CHANGED']
    added = PRE + 'def test_x():\n    assert f(1) == 2\n    assert f(2) == 3\n'
    assert 'ASSERT_ADDED' in change_modes_v2(PRE + TEST, added, 'f')
    rewritten = PRE + 'def test_x():\n    y = f(1)\n    assert y == 2\n'
    assert change_modes_v2(PRE + TEST, rewritten, 'f') == ['TEST_REWRITTEN']
    assert change_modes_v2(PRE + TEST, PRE + TEST, 'f') == []


def test_unparseable_source_is_other():
    assert change_modes_v2(PRE + TEST, 'def broken(:\n', 'f') == ['OTHER']


def test_judge_verdict_mapping():
    assert verdict('v2a', '```json\n{"spec_expectation": "x", "verdict": "TEST_WRONG", "reason": "r"}\n```') == 'TEST_WRONG'
    assert verdict('v2b', '{"spec_expectation": "x", "answer": "YES", "reason": "r"}') == 'BUG'
    assert verdict('v2b', '{"answer": "NO"}') == 'TEST_WRONG'
    assert verdict('v2b', 'no json') == 'UNSURE'


def test_split_v1_prompt():
    prompt = ('Judge whether ...\nSpecification (signature and docstring):\ndef f(a):\n    """doc"""\n'
              'Test (contains its expected values):\nT\nObserved behaviour:\n{"outcome": "ASSERT_FAIL"}\n'
              'Return only JSON: {...}')
    fields = split_v1_prompt(prompt)
    assert fields == {'spec': 'def f(a):\n    """doc"""', 'test': 'T', 'feedback': '{"outcome": "ASSERT_FAIL"}'}
