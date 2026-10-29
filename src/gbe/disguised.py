"""Disguised HumanEvalFix pairs as a third benchmark (S1 contamination control, docs/PHASE2_SPEC.md 8.8).

The 40 pairs of configs/phase2_seed_subset.json with new function and variable names, a new description
and new examples computed from the fixed program, built and verified by scripts/d11_disguise.py for the
D11 agent study. The task file is pinned by its hash in configs/disguised.json. Sanity evidence (HumanEval's
own tests, called through name aliases, twice per version) is recorded in configs/disguised_sanity.json by
scripts/disguised_sanity.py.
"""
import hashlib
import json

from .quixbugs import signature_spec
from .util import ROOT, read_json

BENCHMARK = 'HumanEvalFixDisguised'


def hidden_parts(row, task):
    """HumanEval's own test for a disguised task as (prelude, test): aliases from the new names to the
    original ones and the original check function, then a test that calls it. Hidden from the pipeline;
    used for sanity and for the leakage check."""
    import ast
    top = {n.name for n in ast.parse(task['programs']['fixed']).body if isinstance(n, ast.FunctionDef)}
    aliases = '\n'.join(f'from solution import {new} as {old}' for old, new in task['names'].items() if new in top)
    prelude = aliases + '\n' + row.get('test_setup', '') + '\n' + row['test']
    return prelude, f"def test_benchmark():\n    check({task['original_entry_point']})\n"


def hidden_test(row, task):
    prelude, test = hidden_parts(row, task)
    return prelude + '\n\n' + test


def load():
    """Return the 40 disguised tasks after checking the task file against its pinned hash."""
    from .benchmarks import download
    pinned = read_json(ROOT / 'configs' / 'disguised.json')
    path = ROOT / pinned['file']
    if hashlib.sha256(path.read_bytes()).hexdigest() != pinned['sha256']:
        raise ValueError('Disguised task file differs from the pinned hash')
    rows = {r['task_id']: r for r in download()[0]}
    tasks = []
    for pid, task in sorted(json.loads(path.read_text(encoding='utf-8')).items(), key=lambda kv: int(kv[0].split('/')[-1])):
        row = rows[pid]
        programs = dict(task['programs'])
        tasks.append({'task_id': f"{BENCHMARK}/{pid.split('/')[-1]}", 'benchmark': BENCHMARK,
                      'entry_point': task['entry_point'], 'programs': programs,
                      'prompt': signature_spec(programs['fixed'], task['entry_point']), 'support': {},
                      'bug_type': row['bug_type'], 'original_pair_id': pid,
                      'hidden_test': hidden_test(row, task)})
    return tasks
