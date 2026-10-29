"""Phase 2 harness changes: judge v2b, QuixBugs tasks, support modules, classifier v2, report denominators."""
import csv
import difflib
import json

import pytest

from gbe import report, runner
from gbe.benchmarks import view
from gbe.evaluate import change_modes
from gbe.execute import execute
from gbe.policies import judge_v2b_parse
from gbe.util import ROOT, read_json, write_json


@pytest.mark.parametrize('text,verdict', [
    ('{"spec_expectation": "x", "answer": "YES", "reason": "r"}', 'BUG'),
    ('{"answer": "NO", "reason": "r"}', 'TEST_WRONG'),
    ('{"answer": "UNCLEAR", "reason": "r"}', 'UNSURE'),
    ('```json\n{"answer": "NO", "reason": "fenced"}\n```', 'TEST_WRONG'),
    ('{"answer": "yes"}', 'UNSURE'),            # exact values only
    ('{"answer": "MAYBE"}', 'UNSURE'),
    ('{"verdict": "BUG"}', 'UNSURE'),           # a v1-style answer is not a v2b answer
    ('["YES"]', 'UNSURE'),
    ('no json at all', 'UNSURE'),
    ('', 'UNSURE'),                              # repeat-limit abort recorded as an empty answer
])
def test_v2b_mapping(text, verdict):
    assert judge_v2b_parse(text)['verdict'] == verdict


def test_judge_frozen_in_repository():
    assert runner.judge_fingerprint() == read_json(ROOT / 'configs' / 'judge.json')


def test_d10_prompt_adds_only_the_implementation():
    primary = (ROOT / 'prompts/judge_v2b.txt').read_text(encoding='utf-8').splitlines()
    ablation = (ROOT / 'prompts/judge_with_code_v2b.txt').read_text(encoding='utf-8').splitlines()
    changed = [l for l in difflib.ndiff(primary, ablation) if l[:1] in '+-']
    assert [l for l in changed if l.startswith('-')] == [
        "- You review an automatically generated unit test for a Python function. Automatically generated tests "
        "are often wrong. Decide only from the specification below; you are not shown the function's code or how it behaved."]
    assert [l for l in changed if l.startswith('+')] == [
        "+ You review an automatically generated unit test for a Python function. Automatically generated tests "
        "are often wrong. Decide only from the specification below. You are also shown the function's code, but not how it behaved.",
        '+ ', '+ Implementation (the code under test):', '+ {program}']


def test_execute_places_support_modules():
    program = 'from node import Node\ndef name(n):\n    return n.value\n'
    test = 'def test_x():\n    from node import Node\n    assert name(Node("a")) == "a"'
    support = {'node.py': 'class Node:\n    def __init__(self, value):\n        self.value = value\n'}
    assert execute(program, 'from solution import *\n', test, support=support)['outcome'] == 'PASS'
    assert execute(program, 'from solution import *\n', test)['outcome'] != 'PASS'


def test_harness_classifier_is_v2():
    before = 'from solution import *\ndef test_x():\n    assert add(1, 2) == 3'
    after = 'def add(a, b):\n    return a + b\ndef test_x():\n    assert add(1, 2) == 3'
    assert change_modes(before, after, 'add') == ['FUNCTION_SHADOWED']
    assert change_modes(before, before.replace('== 3', '== 4'), 'add') == ['EXPECTED_CHANGED']


quix = pytest.mark.skipif(not (ROOT / 'data/raw/quixbugs_src/QuixBugs').exists(), reason='QuixBugs not downloaded')


@quix
def test_quixbugs_versions_differ_only_in_the_defect():
    from gbe.quixbugs import load
    tasks = load()
    assert len(tasks) == 40
    for t in tasks:
        changed = [l for l in difflib.unified_diff(t['programs']['buggy'].splitlines(), t['programs']['fixed'].splitlines(),
                                                   lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('---', '+++')]
        assert 1 <= len(changed) <= 2, t['task_id']
        assert t['prompt'] in t['programs']['fixed'] or t['prompt'].split('"""')[1] in t['programs']['fixed']


@quix
def test_quixbugs_view_hides_fixed_program_and_benchmark_tests():
    from gbe.quixbugs import SOURCE, load
    for t in load():
        name = t['entry_point']
        tests = (SOURCE / 'python_testcases' / f'test_{name}.py').read_text(encoding='utf-8')
        json_cases = (SOURCE / 'json_testcases' / f'{name}.json')
        for condition in ('buggy', 'fixed'):
            for arm in ('code', 'spec'):
                context = view(t, condition, arm)
                text = json.dumps({k: v for k, v in context.items()})
                other = t['programs']['fixed' if condition == 'buggy' else 'buggy']
                if arm == 'code':
                    assert other not in text
                assert 'use_correct' not in text and 'load_json_testcases' not in text
                assert tests not in text
                if json_cases.exists():
                    first_case = json_cases.read_text(encoding='utf-8').splitlines()[0]
                    assert first_case not in context['generation_input'] or first_case in t['prompt']
                assert set(context['support']) == ({'node.py'} if name in (
                    'breadth_first_search', 'depth_first_search', 'detect_cycle', 'reverse_linked_list',
                    'shortest_path_length', 'topological_ordering') else set())


def test_report_keeps_gen_fail_units_in_denominators(tmp_path):
    run = tmp_path / 'phase2_toy'
    unit_ok, unit_fail = 'HumanEvalFix-1__buggy__m__s0__code', 'HumanEvalFix-1__fixed__m__s0__code'
    write_json(run / 'pairs.json', [{'pair_id': 'Python/1', 'benchmark': 'HumanEvalFix'}])
    write_json(run / 'units' / unit_ok / 'generated.json', {'parse_status': 'OK', 'tests': [{}]})
    write_json(run / 'units' / unit_fail / 'generated.json', {'parse_status': 'GEN_FAIL', 'tests': []})
    for policy in ('P1', 'P2', 'P3', 'P4'):
        write_json(run / 'units' / unit_ok / f'policy_{policy}.json', {'wall_time_s': 0})
    row = dict(unit_id=unit_ok, pair_id='Python/1', condition='buggy', model='m', seed=0, gen_input='code',
               test_id=unit_ok + '/t0', outcome_fixed='PASS', outcome_buggy='ASSERT_FAIL', label='REVEALS',
               final_status='GENERATED', outcome_put='ASSERT_FAIL', gen_label='REVEALS', fate='',
               change_modes='', judge_verdict='', judge_with_code_verdict='', n_llm_calls=1)
    rows = [dict(row, stage='GEN')] + [dict(row, stage=p, final_status='DROPPED', label='', fate='DROPPED')
                                       for p in ('P1', 'P2', 'P3', 'P4')]
    with (run / 'tests.csv').open('w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) + ['stage'])
        w.writeheader()
        w.writerows(rows)
    write_json(run / 'manifest.json', {'config': {'benchmarks': ['HumanEvalFix'], 'gen_inputs': ['code']},
                                       'unit_seconds': {}, 'models': {}, 'model': 'm', 'ollama_version': 'test',
                                       'start_time': '2026-10-09T00:00:00+00:00', 'end_time': None})
    (run / 'llm_calls.jsonl').write_text('', encoding='utf-8')
    report.summarize(run)
    text = (run / 'go_no_go.txt').read_text(encoding='utf-8')
    assert 'Verdict:' not in text
    assert 'Buggy pre-repair signal: 1/1 pairs; 1/1 units' in text
    assert f'GEN_FAIL units (counted in all unit denominators): 1 of 2: {unit_fail}' in text
