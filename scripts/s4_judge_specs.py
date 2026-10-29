"""S4: the P4 judge replayed with weaker specifications (docs/PHASE2_SPEC.md 8.8, decision P3-B).

Every judge call of a finished run is replayed with the same frozen prompt (prompts/judge_v2b.txt), the same
model, digest and options, and the same test, changing only the specification field:

  full            the logged call itself (no new call; its logged answer is parsed again)
  no_examples     the docstring without its examples (doctest lines, example blocks, lines that call the
                  function under test)
  signature_only  imports and signature only, docstring replaced by '...'

The original specification text is recovered from the logged prompt and checked by re-rendering the prompt
byte for byte. Verdicts are scored as in the run reviews: on buggy programs, a bug-revealing test (generation
label REVEALS) counts as kept when the verdict is not TEST_WRONG; on correct programs, every judged test is a
failing test of a correct program, and a verdict other than TEST_WRONG is a false report.

  python scripts/s4_judge_specs.py --run phase2_qwen25_code --dry      check parsing, write examples, no LLM
  python scripts/s4_judge_specs.py --run phase2_qwen25_code            replay (resumable through the cache)
  python scripts/s4_judge_specs.py --run phase2_qwen25_code --summary  tables only

Outputs in runs/s4_judge_specs/<run>/: llm_calls.jsonl and cache/ (as for every run), results.jsonl,
progress.json, spec_variants.json (every transformed specification), summary.md.
"""
import argparse
import ast
import csv
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.generate import strip_reasoning  # noqa: E402
from gbe.policies import JUDGE_PROMPT, judge_v2b_parse  # noqa: E402
from gbe.util import now, read_json, write_json  # noqa: E402

VARIANTS = ('no_examples', 'signature_only')
TEMPLATE = (ROOT / 'prompts' / f'{JUDGE_PROMPT}.txt').read_text(encoding='utf-8')
HEAD, TAIL = 'Specification (signature and docstring):\n', '\n\nTest:\n'
QUESTION = '\n\nQuestion: if the function behaved exactly as the specification says'
EXAMPLE_HEADER = re.compile(r'^\s*(for\s+)?(examples?|e\.g\.)\b[\s\d:.,]*$', re.I)


def split_prompt(prompt):
    """Recover (spec, test) from a rendered judge_v2b prompt; checked by re-rendering."""
    start = prompt.index(HEAD) + len(HEAD)
    middle = prompt.index(TAIL, start)
    end = prompt.index(QUESTION, middle)
    spec, test = prompt[start:middle], prompt[middle + len(TAIL):end]
    if TEMPLATE.format_map({'spec': spec, 'test': test}) != prompt:
        raise ValueError('Logged prompt does not re-render from the recovered fields')
    return spec, test


def doc_node(function):
    """The function's description string: its docstring, or the first string statement (HumanEval 115 puts
    'import math' before the description)."""
    return next((n for n in function.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
                 and isinstance(n.value.value, str)), None)


def entry_function(tree, entry_point=None):
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and doc_node(n) is not None]
    named = [f for f in functions if f.name == entry_point]
    return (named or functions)[-1 if not named else 0]


EXAMPLE_START = re.compile(r'\b(for example|for instance|example\s*\d*\s*[:,])', re.I)
CODE_LIKE = re.compile(r'''^\s*(->|=>|==>|\w+\s*=\s*[\[\(\'"\d-]|return\s+[\[\(\'"\d-])''')


def strip_examples(doc, name):
    """Remove concrete examples and keep the description. Dropped: doctest lines with their outputs, example
    blocks after an 'Example(s):' header, prose examples from 'For example' or 'Example,' to the end of the
    paragraph, lines that call the function under test, and example-like lines ('-> ...', 'x = [...]',
    'return [...]'). Kept: rules stated in words, including inline 'e.g.' clarifications."""
    kept, in_block = [], False
    for line in doc.split('\n'):
        stripped = line.strip()
        if in_block:
            if not stripped:
                in_block = False
            continue
        if EXAMPLE_HEADER.match(stripped) or stripped.startswith('>>>'):
            in_block = True
            continue
        if re.search(rf'\b{re.escape(name)}\s*\(', line) or CODE_LIKE.match(line):
            continue
        start = EXAMPLE_START.search(line)
        if start:
            head = line[:start.start()].rstrip()
            if head.strip():
                kept.append(head)
            in_block = True
            continue
        kept.append(line)
    text = re.sub(r'\n\s*\n(\s*\n)+', '\n\n', '\n'.join(kept))
    return text.strip('\n')


def transform(spec, variant, entry_point=None):
    """Return the specification text for a variant; the code around the docstring is kept byte for byte."""
    if variant == 'full':
        return spec
    tree = ast.parse(spec)
    function = entry_function(tree, entry_point)
    node = doc_node(function)
    lines = spec.split('\n')
    indent = lines[node.lineno - 1][:len(lines[node.lineno - 1]) - len(lines[node.lineno - 1].lstrip())]
    if variant == 'signature_only':
        replacement = [indent + '...']
    else:
        import inspect
        doc = strip_examples(inspect.cleandoc(node.value.value), function.name)
        body = '\n'.join((indent + l) if l.strip() else '' for l in doc.split('\n'))
        replacement = (indent + '"""' + body.lstrip() + '\n' + indent + '"""').split('\n')
    new_lines = lines[:node.lineno - 1] + replacement + lines[node.end_lineno:]
    result = '\n'.join(new_lines)
    ast.parse(result)  # must stay valid Python
    return result


def judged_tests(run):
    """One record per judged test: the logged judge call plus the ground truth of tests.csv (stage P4)."""
    folder = ROOT / 'runs' / run
    with open(folder / 'tests.csv', encoding='utf-8') as fh:
        truth = {r['test_id']: r for r in csv.DictReader(fh) if r['stage'] == 'P4'}
    entry = {}
    from gbe.benchmarks import all_tasks
    for t in all_tasks()[0]:
        entry[t['task_id']] = t['entry_point']
    records, seen = [], set()
    with open(folder / 'llm_calls.jsonl', encoding='utf-8') as fh:
        for line in fh:
            call = json.loads(line)
            if call.get('purpose') != 'judge' or call['test_id'] in seen:
                continue
            seen.add(call['test_id'])
            row = truth[call['test_id']]
            spec, test = split_prompt(call['prompt'])
            records.append({'test_id': call['test_id'], 'unit_id': call['unit_id'], 'pair_id': row['pair_id'],
                            'condition': row['condition'], 'gen_label': row['gen_label'],
                            'final_status': row['final_status'], 'entry_point': entry[row['pair_id']],
                            'spec': spec, 'test': test,
                            'full': judge_v2b_parse(strip_reasoning(call['response']['message']['content'])),
                            'logged_verdict': row['judge_verdict']})
    for r in records:
        if r['full']['verdict'] != r['logged_verdict']:
            raise ValueError(f"Re-parsed verdict differs from tests.csv for {r['test_id']}")
    return records, truth


def summarise(run, records, truth, results):
    """Kept bug-revealing tests and false reports per variant, scored as in the run reviews."""
    by_variant = {'full': {r['test_id']: r['full']['verdict'] for r in records}}
    for v in VARIANTS:
        by_variant[v] = {x['test_id']: x['verdict'] for x in results if x['variant'] == v}
    judged = {r['test_id'] for r in records}
    revealing = [t for t, r in truth.items() if r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS']
    fixed_judged = [r['test_id'] for r in records if r['condition'] == 'fixed']
    lines = [f'# S4: judge with weaker specifications ({run})', '',
             'Computed by `scripts/s4_judge_specs.py`. Kept: a bug-revealing test on a buggy program is reported',
             'as a likely bug (verdict BUG or UNSURE). False reports: failing tests of correct programs that the',
             'judge does not call wrong. Tests that never reached the judge keep their P4 outcome.', '',
             '| Specification | Bug-revealing tests kept | False reports on correct programs | UNSURE verdicts | Calls done |',
             '|---|---|---|---|---|']
    for v, verdicts in by_variant.items():
        if v != 'full' and len(verdicts) < len(records):
            note = f'{len(verdicts)} of {len(records)}'
        else:
            note = 'all'
        kept = sum(1 for t in revealing if (t in judged and verdicts.get(t, by_variant['full'][t]) != 'TEST_WRONG')
                   or (t not in judged and truth[t]['final_status'] == 'QUARANTINED'))
        false = sum(1 for t in fixed_judged if verdicts.get(t, by_variant['full'][t]) != 'TEST_WRONG')
        unsure = sum(1 for x in verdicts.values() if x == 'UNSURE')
        lines.append(f'| {v} | {kept} of {len(revealing)} ({100 * kept / len(revealing):.0f}%) | '
                     f'{false} of {len(fixed_judged)} ({100 * false / max(1, len(fixed_judged)):.0f}%) | {unsure} | {note} |')
    out = ROOT / 'runs' / 's4_judge_specs' / run / 'summary.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', default='phase2_qwen25_code')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--summary', action='store_true')
    a = ap.parse_args()
    out = ROOT / 'runs' / 's4_judge_specs' / a.run
    out.mkdir(parents=True, exist_ok=True)
    records, truth = judged_tests(a.run)
    variants = {}
    for r in records:
        key = (r['pair_id'], r['condition'])
        if key not in variants:
            variants[key] = {v: transform(r['spec'], v, r['entry_point']) for v in ('full',) + VARIANTS}
    write_json(out / 'spec_variants.json', {f'{p}|{c}': v for (p, c), v in sorted(variants.items())})
    changed = Counter(v['no_examples'] != v['full'] for v in variants.values())
    print(f"{len(records)} judged tests in {len(variants)} program versions; examples removed in "
          f"{changed[True]} of {len(variants)} specifications; fixed {sum(r['condition'] == 'fixed' for r in records)}, "
          f"buggy {sum(r['condition'] == 'buggy' for r in records)}", flush=True)
    results_path = out / 'results.jsonl'
    results = [json.loads(l) for l in results_path.read_text(encoding='utf-8').splitlines()] if results_path.exists() else []
    if a.dry or a.summary:
        if a.summary:
            summarise(a.run, records, truth, results)
        return
    from gbe.llm import Client
    manifest = read_json(ROOT / 'runs' / a.run / 'manifest.json')
    client = Client(out, manifest['model'], manifest['model_digest'], manifest['options'])
    done = {(x['test_id'], x['variant']) for x in results}
    total, t0 = len(records) * len(VARIANTS), time.monotonic()
    with open(results_path, 'a', encoding='utf-8') as fh:
        for i, r in enumerate(records):
            for v in VARIANTS:
                if (r['test_id'], v) in done:
                    continue
                spec = variants[(r['pair_id'], r['condition'])][v]
                decision = judge_v2b_parse(client.call(JUDGE_PROMPT, {'spec': spec, 'test': r['test']},
                                                       unit_id=r['unit_id'], purpose=f'judge_{v}', policy='P4',
                                                       test_id=r['test_id'], round=0))
                row = {'test_id': r['test_id'], 'variant': v, 'condition': r['condition'], 'gen_label': r['gen_label'],
                       **decision}
                fh.write(json.dumps(row) + '\n')
                fh.flush()
                results.append(row)
                done.add((r['test_id'], v))
            n = len(done)
            write_json(out / 'progress.json', {'done': n, 'total': total, 'percent': round(100 * n / total, 1),
                                               'updated': now()})
            if i % 25 == 0:
                print(f'{n}/{total} judge calls ({100 * n / total:.1f}%)', flush=True)
    summarise(a.run, records, truth, results)


if __name__ == '__main__':
    main()
