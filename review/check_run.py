"""Independent reviewer checks for a finished run (Phase 1 pilot or Phase 2) (REVIEW_PROTOCOL.md section 2).

Written by the reviewer, separately from the harness. Programs are rebuilt directly from the
pinned dataset (import + declaration + solution) and the raw QuixBugs files, not through gbe.benchmarks.

Usage (from next_paper):  .venv\\Scripts\\python.exe review\\check_run.py <run_id>
"""
import collections
import csv
import json
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.policies import judge_parse, judge_v2b_parse  # harness parsers, chosen per logged prompt template

RUN = sys.argv[1] if len(sys.argv) > 1 else 'phase1_pilot'
RUN_DIR = ROOT / 'runs' / RUN
OUT = ROOT / 'review' / 'out' / RUN
OUT.mkdir(parents=True, exist_ok=True)


def private_tmp():
    """Temporary folder under a parent private to this process (pytest fails on sibling folders that
    other processes delete during collection)."""
    parent = ROOT / '.scratch' / 'review_tmp' / str(os.getpid())
    parent.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=parent)


def load_dataset():
    """Reviewer-side rows built from the raw benchmark files, not through gbe.benchmarks.

    Each row: prompt (material the pipeline may see), fixed/buggy program sources, hidden test material,
    and support modules. QuixBugs programs are the raw files; their description string and missing
    docstring do not change behaviour.
    """
    import pyarrow.parquet as pq
    data = {}
    for r in pq.read_table(ROOT / 'data/raw/python.parquet').to_pylist():
        data[r['task_id']] = {'prompt': r['prompt'], 'support': {},
                              'fixed': r['import'] + '\n' + r['declaration'] + r['canonical_solution'],
                              'buggy': r['import'] + '\n' + r['declaration'] + r['buggy_solution'],
                              'bodies': {'fixed': r['canonical_solution'], 'buggy': r['buggy_solution']},
                              'hidden_tests': r['test'] + '\n' + (r.get('example_test') or '')}
    quix = ROOT / 'data/raw/quixbugs_src/QuixBugs'
    if quix.exists():
        node = (quix / 'python_programs/node.py').read_text(encoding='utf-8')
        for f in sorted((quix / 'python_programs').glob('*.py')):
            if f.stem.endswith('_test') or f.stem == 'node':
                continue
            buggy = f.read_text(encoding='utf-8')
            fixed = (quix / 'correct_python_programs' / f.name).read_text(encoding='utf-8')
            tests = (quix / 'python_testcases' / f'test_{f.stem}.py').read_text(encoding='utf-8')
            cases = quix / 'json_testcases' / f'{f.stem}.json'
            description = buggy[buggy.rindex('"""', 0, buggy.rindex('"""')):]
            code = lambda s: s.split('\n"""')[0]
            # The pipeline sees the signature plus the description, so both count as allowed material.
            signature = next(l for l in buggy.splitlines() if l.startswith(f'def {f.stem}('))
            data[f'QuixBugs/{f.stem}'] = {
                'prompt': signature + '\n' + description, 'support': {'node.py': node} if 'from node import' in tests else {},
                'fixed': fixed, 'buggy': buggy, 'bodies': {'fixed': code(fixed), 'buggy': code(buggy)},
                'hidden_tests': tests + '\n' + (cases.read_text(encoding='utf-8') if cases.exists() else '')}
    # Disguised HumanEvalFix pairs (S1), straight from the D11 task file; the pipeline sees the signature
    # and docstring of the entry function, the hidden material is HumanEval's test of the original pair.
    import ast
    disguised = ROOT / 'runs/d11/disguised_tasks.json'
    if disguised.exists():
        for pid, t in json.loads(disguised.read_text(encoding='utf-8')).items():
            fixed, buggy = t['programs']['fixed'], t['programs']['buggy']
            tree = ast.parse(fixed)
            fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == t['entry_point'])
            lines = fixed.splitlines()
            # Module imports are part of the specification the pipeline sees (like HumanEval's prompt).
            imports = [ast.get_source_segment(fixed, n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
            prompt = '\n'.join(imports + lines[fn.lineno - 1:fn.body[0].end_lineno])
            original = data[pid]
            data[f"HumanEvalFixDisguised/{pid.split('/')[-1]}"] = {
                'prompt': prompt, 'support': {}, 'fixed': fixed, 'buggy': buggy,
                'bodies': {'fixed': fixed, 'buggy': buggy}, 'hidden_tests': original['hidden_tests']}
    # Natural LLM faults (S2), straight from the selected pair file; the pipeline sees the HumanEval prompt.
    natural = ROOT / 'data/s2/natural_faults.json'
    if natural.exists():
        for tid, p in json.loads(natural.read_text(encoding='utf-8')).items():
            data[f"HumanEvalPlusNatural/{tid.split('/')[-1]}"] = {
                'prompt': p['prompt'], 'support': {}, 'fixed': p['programs']['fixed'], 'buggy': p['programs']['buggy'],
                'bodies': {'fixed': p['programs']['fixed'], 'buggy': p['programs']['buggy']}, 'hidden_tests': ''}
    return data


def program(row, version):
    return row[version]


def run_test(row, version, prelude, source):
    with private_tmp() as d:
        Path(d, 'solution.py').write_text(program(row, version), encoding='utf-8')
        for name, text in row['support'].items():
            Path(d, name).write_text(text, encoding='utf-8')
        Path(d, 'test_review.py').write_text(prelude + '\n' + source + '\n', encoding='utf-8')
        try:
            p = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'test_review.py'],
                               cwd=d, capture_output=True, text=True, timeout=10)
            return 'PASS' if p.returncode == 0 else 'FAIL'
        except subprocess.TimeoutExpired:
            return 'TIMEOUT'


def label(fixed, buggy):
    if fixed == 'PASS' and buggy == 'PASS':
        return 'NEUTRAL'
    if fixed == 'PASS':
        return 'REVEALS'
    if buggy == 'PASS':
        return 'ENCODES'
    return 'BROKEN'


def text_of(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        if 'message' in x:
            return (x['message'] or {}).get('content', '')
        if 'messages' in x:
            return '\n'.join(m.get('content', '') for m in x['messages'])
        return json.dumps(x)
    if isinstance(x, list):
        return '\n'.join(text_of(i) for i in x)
    return ''


def main():
    data = load_dataset()
    rows = list(csv.DictReader(open(RUN_DIR / 'tests.csv', encoding='utf-8')))
    units = {}
    for u in (RUN_DIR / 'units').iterdir():
        units[u.name] = {'generated': json.loads((u / 'generated.json').read_text(encoding='utf-8')),
                         **{p: json.loads((u / f'policy_{p}.json').read_text(encoding='utf-8'))
                            for p in ('P1', 'P2', 'P3', 'P4')}}
    results = {}

    def source_of(r):
        unit = units[r['unit_id']]
        if r['stage'] == 'GEN':
            k = int(r['test_id'].rsplit('/t', 1)[1])
            return unit['generated']['prelude'], unit['generated']['tests'][k]['source']
        t = next(t for t in unit[r['stage']]['tests'] if t['test_id'] == r['test_id'])
        return t['prelude'], t['source']

    # P1-d: independent labels on a stratified sample of 30 final/generated tests.
    rng = random.Random(20261009)
    strata = collections.defaultdict(list)
    for r in rows:
        if r['label'] != 'FLAKY' and r['final_status'] != 'DROPPED':
            strata[(r['stage'], r['label'])].append(r)
    sample = []
    keys = sorted(strata)
    while len(sample) < 30 and any(strata.values()):
        for k in keys:
            if strata[k] and len(sample) < 30:
                sample.append(strata[k].pop(rng.randrange(len(strata[k]))))
    mismatches = []
    for r in sample:
        prelude, src = source_of(r)
        row = data[r['pair_id']]
        f, b = run_test(row, 'fixed', prelude, src), run_test(row, 'buggy', prelude, src)
        mine = label(f, b)
        if mine != r['label']:
            mismatches.append({'test_id': r['test_id'], 'stage': r['stage'], 'harness': r['label'],
                               'reviewer': mine, 'fixed': f, 'buggy': b})
    results['P1-d_labels'] = {'sampled': len(sample), 'strata': len(keys), 'mismatches': mismatches}

    # P1-c: identical inputs across policies.
    diff = [u for u, v in units.items() if len({v[p]['input_hash'] for p in ('P1', 'P2', 'P3', 'P4')}) != 1]
    results['P1-c_same_input'] = {'units': len(units), 'units_with_different_hashes': diff}

    # P1-e: policy invariants.
    calls = [json.loads(l) for l in open(RUN_DIR / 'llm_calls.jsonl', encoding='utf-8')]
    p1_calls = sum(1 for c in calls if c.get('policy') == 'P1')
    not_green = [(r['test_id'], r['stage'], r['outcome_put']) for r in rows
                 if r['stage'] in ('P1', 'P2', 'P3') and r['final_status'] == 'KEPT' and r['outcome_put'] != 'PASS']
    quarantined_elsewhere = [r['test_id'] for r in rows if r['stage'] in ('P1', 'P2', 'P3') and r['final_status'] == 'QUARANTINED']
    changed_quarantine = []
    for u, v in units.items():
        gen = {f"{u}/t{i}": t['source'] for i, t in enumerate(v['generated']['tests'])}
        for t in v['P4']['tests']:
            if t['final_status'] == 'QUARANTINED' and t['source'] != gen.get(t['test_id']):
                changed_quarantine.append(t['test_id'])
    results['P1-e_invariants'] = {'P1_llm_calls': p1_calls, 'P1-P3_kept_not_PASS': not_green,
                                  'P1-P3_quarantined': quarantined_elsewhere,
                                  'P4_quarantined_tests_changed': changed_quarantine}

    # P1-b / P1-m: leakage. A line counts if it is non-trivial (>= 25 chars stripped) and is not
    # also present in the material the pipeline may see for that condition.
    unit_meta = {r['unit_id']: (r['pair_id'], r['condition']) for r in rows}
    leaks, judge_body = [], []
    for c in calls:
        if c.get('unit_id') not in unit_meta:
            continue
        pair, cond = unit_meta[c['unit_id']]
        row = data[pair]
        prompt = text_of(c.get('prompt'))
        allowed = row['prompt'] + program(row, cond) + ''.join(row['support'].values())
        forbidden = []
        hidden = row['hidden_tests'] + '\n' + row['bodies']['fixed' if cond == 'buggy' else 'buggy']
        for line in hidden.splitlines():
            s = line.strip()
            if len(s) >= 25 and s not in allowed and s in prompt:
                forbidden.append(s)
        if forbidden:
            leaks.append({'call_id': c.get('call_id'), 'purpose': c.get('purpose'), 'lines': forbidden[:3]})
        if c.get('purpose') == 'judge':
            for line in (row['bodies']['buggy'] + '\n' + row['bodies']['fixed']).splitlines():
                s = line.strip()
                if len(s) >= 25 and s in prompt and s not in row['prompt']:
                    judge_body.append({'call_id': c.get('call_id'), 'line': s})
                    break
    results['P1-b_leakage'] = {'calls_checked': len(calls), 'violations': leaks[:20], 'n_violations': len(leaks)}
    results['P1-m_judge_sees_body'] = {'n': len(judge_body), 'examples': judge_body[:5]}

    # Verdict recovery: re-parse raw judge responses with the parser matching each call's logged prompt template.
    verdicts = {}
    for c in calls:
        if c.get('purpose') in ('judge', 'judge_with_code'):
            parse = judge_v2b_parse if c.get('prompt_template', '').endswith('v2b') else judge_parse
            verdicts[(c['test_id'], c['purpose'])] = parse(text_of(c.get('response')))['verdict']
    by_id = collections.defaultdict(dict)
    for (tid, purpose), v in verdicts.items():
        by_id[tid][purpose] = v
    gen_label = {r['test_id']: r['label'] for r in rows if r['stage'] == 'GEN'}
    p2_rows = {r['test_id']: r for r in rows if r['stage'] == 'P2'}
    confusion = collections.Counter()
    variants = collections.defaultdict(collections.Counter)
    recovered_rows = []
    for r in rows:
        if r['stage'] != 'P4':
            continue
        v = by_id.get(r['test_id'], {})
        judge = v.get('judge', '')
        recovered_rows.append({'test_id': r['test_id'], 'condition': r['condition'], 'gen_input': r['gen_input'],
                               'stored_verdict': r['judge_verdict'], 'recovered_verdict': judge,
                               'recovered_with_code': v.get('judge_with_code', ''), 'gen_label': gen_label.get(r['test_id'], '')})
        if judge:
            confusion[(r['condition'], judge, gen_label.get(r['test_id']))] += 1
        for name in ('P4_DEFAULT', 'P4_STRICT', 'P4_KEEP_ALL', 'P4_HYBRID'):
            status, lab = r['final_status'], r['label']
            if judge:
                if name == 'P4_STRICT':
                    status = 'QUARANTINED' if judge == 'BUG' else 'DROPPED'
                elif name == 'P4_KEEP_ALL':
                    status, lab = 'QUARANTINED', gen_label.get(r['test_id'])
                elif name == 'P4_DEFAULT':
                    status = 'QUARANTINED' if judge in ('BUG', 'UNSURE') else 'DROPPED'
                elif judge == 'TEST_WRONG':
                    status, lab = p2_rows[r['test_id']]['final_status'], p2_rows[r['test_id']]['label']
                else:
                    status = 'QUARANTINED'
            if status != 'DROPPED' and lab != 'FLAKY':
                key = f"{r['condition']}|{r['gen_input']}|{name}"
                variants[key]['final_size'] += 1
                variants[key][status] += 1
                if status == 'QUARANTINED':
                    variants[key]['QUARANTINED_' + str(lab)] += 1
    with open(OUT / 'recovered_verdicts.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(recovered_rows[0]))
        w.writeheader()
        w.writerows(recovered_rows)
    results['verdicts'] = {
        'stored': dict(collections.Counter(r['stored_verdict'] for r in recovered_rows if r['stored_verdict'])),
        'recovered_judge': dict(collections.Counter(r['recovered_verdict'] for r in recovered_rows if r['recovered_verdict'])),
        'recovered_with_code': dict(collections.Counter(r['recovered_with_code'] for r in recovered_rows if r['recovered_with_code'])),
        'confusion_condition_verdict_genlabel': {'|'.join(map(str, k)): n for k, n in sorted(confusion.items())},
        'variants': {k: dict(v) for k, v in sorted(variants.items())}}

    # P1-f: erasure events for hand reading.
    events = [r for r in rows if r['stage'] in ('P2', 'P3') and r['fate'] in ('INVERTED', 'NEUTRALIZED')]
    rng.shuffle(events)
    picked = [e for e in events if e['stage'] == 'P2'][:5] + [e for e in events if e['stage'] == 'P3'][:5]
    with open(OUT / 'erasure_samples.md', 'w', encoding='utf-8') as fh:
        for e in picked:
            g = next(r for r in rows if r['stage'] == 'GEN' and r['test_id'] == e['test_id'])
            fh.write(f"## {e['stage']} {e['fate']} {e['test_id']} ({e['pair_id']})\n")
            fh.write(f"generated label {g['label']}, final label {e['label']}, change modes {e['change_modes']}\n\n")
            fh.write('Generated:\n```python\n' + source_of(g)[1] + '\n```\nFinal:\n```python\n' + source_of(e)[1] + '\n```\n\n')
    results['P1-f_erasure_samples'] = {'available': len(events), 'written': len(picked)}

    (OUT / 'results.json').write_text(json.dumps(results, indent=1), encoding='utf-8')
    print(json.dumps(results, indent=1)[:6000])


if __name__ == '__main__':
    main()
