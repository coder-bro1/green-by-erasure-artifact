"""Benchmark preparation, before pipeline execution. Raw pairs never enter policies."""
import json
import ast
import hashlib
import random
import urllib.request
from collections import defaultdict

from .execute import execute
from .util import ROOT, digest, read_json, write_json


def fetch(url):
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def download():
    target = ROOT / 'data' / 'raw'
    target.mkdir(parents=True, exist_ok=True)
    pin = target / 'dataset.json'
    metadata = read_json(ROOT / 'configs' / 'dataset.json')
    if pin.exists() and read_json(pin)['revision'] != metadata['revision']:
        raise ValueError('Cached dataset revision differs from pinned configuration')
    if not pin.exists():
        write_json(pin, metadata)
    raw = target / 'python.parquet'
    if not raw.exists():
        raw.write_bytes(fetch('https://huggingface.co/datasets/bigcode/humanevalpack/resolve/' +
                              metadata['revision'] + '/' + metadata['file']))
    if hashlib.sha256(raw.read_bytes()).hexdigest() != metadata['file_sha256']:
        raise ValueError('Raw dataset hash differs from pinned configuration')
    import pyarrow.parquet as pq
    rows = pq.read_table(raw).to_pylist()
    if len(rows) != 164:
        raise ValueError(f'Expected 164 Python rows, got {len(rows)}')
    return rows, metadata


def program(row, condition):
    if 'programs' in row:  # QuixBugs: normalised versions prepared by gbe.quixbugs
        return row['programs'][condition]
    body = row['canonical_solution' if condition == 'fixed' else 'buggy_solution']
    # The pinned revision separates the docstring from declaration. Restore it in
    # the function so code input contains the specification required by section 4.1.
    function = next(n for n in ast.parse(row['prompt']).body
                    if isinstance(n, ast.FunctionDef) and n.name == row['entry_point'])
    docstring = ast.get_source_segment(row['prompt'], function.body[0])
    return row['import'] + '\n' + row['declaration'] + '    ' + docstring + '\n' + body


def humanevalfix_sanity(rows):
    """Benchmark tests on both versions, cached in data/raw/sanity.json and bound to source hashes."""
    cache = ROOT / 'data' / 'raw' / 'sanity.json'
    evidence = read_json(cache) if cache.exists() else {}
    for index, row in enumerate(rows):
        key = row['task_id']
        source_hashes = {c: digest(program(row, c)) for c in ('fixed', 'buggy')}
        if key not in evidence or evidence[key].get('source_hashes') != source_hashes:
            test = 'def test_benchmark():\n    check(' + row['entry_point'] + ')\n'
            prelude = 'from solution import *\n' + row.get('test_setup', '') + '\n' + row['test']
            outcomes = {condition: execute(program(row, condition), prelude, test, timeout=15)
                        for condition in ('fixed', 'buggy')}
            evidence[key] = {c: o['outcome'] for c, o in outcomes.items()}
            evidence[key]['source_hashes'] = source_hashes
            write_json(cache, evidence)
    return evidence


def prepare(run_dir):
    rows, metadata = download()
    cache = ROOT / 'data' / 'raw' / 'sanity.json'
    evidence = read_json(cache) if cache.exists() else {}
    valid = defaultdict(list)
    for index, row in enumerate(rows):
        key = row['task_id']
        source_hashes = {c: digest(program(row, c)) for c in ('fixed', 'buggy')}
        if key not in evidence or evidence[key].get('source_hashes') != source_hashes:
            test = 'def test_benchmark():\n    check(' + row['entry_point'] + ')\n'
            prelude = 'from solution import *\n' + row.get('test_setup', '') + '\n' + row['test']
            outcomes = {condition: execute(program(row, condition), prelude, test, timeout=15)
                        for condition in ('fixed', 'buggy')}
            evidence[key] = {c: o['outcome'] for c, o in outcomes.items()}
            evidence[key]['source_hashes'] = source_hashes
            write_json(cache, evidence)
        result = evidence[key]
        if result['fixed'] == 'PASS' and result['buggy'] != 'PASS':
            valid[row['bug_type']].append(row)
        print(f'Sanity {index + 1}/{len(rows)}: {key} {result}', flush=True)
    rng = random.Random(20261008)
    types = sorted(valid)
    if len(types) != 6:
        raise ValueError(f'Expected six bug types: {types}')
    extras = set(rng.sample(types, 2))
    selected = []
    for kind in types:
        selected.extend(rng.sample(valid[kind], 4 if kind in extras else 3))
    write_json(run_dir / 'pairs.json', [{'pair_id': r['task_id'], 'bug_type': r['bug_type']} for r in selected])
    write_json(run_dir / 'sanity.json', evidence)
    return selected, metadata


def support_text(row):
    # Support modules (QuixBugs' node.py) are identical in both versions and contain no tests.
    return ''.join(f"\n\n# Support module {name}, importable in tests as `{name[:-3]}`:\n{text}"
                   for name, text in sorted(row.get('support', {}).items()))


def view(row, condition, gen_input):
    # This is the complete pipeline boundary: no second version or benchmark tests.
    source = program(row, condition)
    spec = row['prompt'] + support_text(row)
    context = {'program': source, 'spec': spec, 'entry_point': row['entry_point'],
               'generation_input': (source + support_text(row)) if gen_input == 'code' else spec,
               'support': dict(row.get('support', {}))}
    if 'runtime' in row:  # Stage C (BugsInPy): this version's environment and the module to import from
        context.update(runtime=row['runtime'][condition], module=row['module'], project=row['project'],
                       generate_prompt='generate_c1_v1')
    return context


def benchmark_name(row):
    return row.get('benchmark', 'HumanEvalFix')


def all_tasks():
    """HumanEvalFix rows (164), QuixBugs tasks (40), the disguised HumanEvalFix pairs (40) and the natural
    LLM faults of HumanEval+ (S2; empty until built), each with a 'benchmark' field."""
    from . import c1, disguised, natural
    from .quixbugs import load
    rows, metadata = download()
    return ([dict(r, benchmark='HumanEvalFix') for r in rows] + load() + disguised.load() + natural.load()
            + c1.load(), metadata)
