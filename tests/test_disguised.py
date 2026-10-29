"""S1: the disguised HumanEvalFix pairs as a benchmark of the main harness."""
import ast

from gbe import disguised
from gbe.benchmarks import benchmark_name, program, view
from gbe.runner import select_tasks, unit_id


def test_load_gives_forty_pinned_pairs_with_spec_and_hidden_test():
    tasks = disguised.load()
    assert len(tasks) == 40 and len({t['task_id'] for t in tasks}) == 40
    for t in tasks:
        assert benchmark_name(t) == 'HumanEvalFixDisguised' and t['task_id'].startswith('HumanEvalFixDisguised/')
        assert program(t, 'fixed') != program(t, 'buggy')
        spec = ast.parse(t['prompt']).body[-1]
        # The specification is the signature and docstring only: no implementation statement.
        assert isinstance(spec, ast.FunctionDef) and spec.name == t['entry_point'] and len(spec.body) == 1
        assert t['original_pair_id'].startswith('Python/') and 'def check' in t['hidden_test']
        # The hidden test and the original name never reach the pipeline view.
        v = view(t, 'buggy', 'code')
        assert 'def check' not in v['generation_input'] and v['support'] == {}


def test_select_tasks_uses_recorded_sanity_and_unit_ids_are_distinct():
    config = {'benchmarks': ['HumanEvalFixDisguised'], 'subset': None}
    selected, excluded, _ = select_tasks(config)
    assert len(selected) == 40 and not excluded
    ids = {unit_id(t, c, 'qwen2.5-coder:7b-instruct', 'code') for t in selected for c in ('buggy', 'fixed')}
    assert len(ids) == 80 and all(i.startswith('HumanEvalFixDisguised-') for i in ids)
