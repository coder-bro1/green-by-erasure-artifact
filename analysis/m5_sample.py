"""M5: blind labelling sample for the second rater (docs/PAPER_PLAN.md, decision P3-B and P3-C).

Part A, change modes: repaired tests from the three finished code runs (P2 overwrite and P3 free repair,
buggy and fixed programs), stratified by the classifier's change modes: for each mode in turn, up to
PER_MODE tests carrying it are drawn with a fixed seed (a test drawn for one mode is not drawn again).
Part B, agent replies: every D11 code-frozen suite that encodes the bug without revealing it (Sol, Luna),
plus CONTROLS replies about correct programs under the original instruction, shuffled together.

Writes review/out/m5_sample.json (shown to the rater; no classifier labels, no model, policy or arm) and
review/out/m5_key.json (the hidden labels, for agreement after labelling). Rebuilding with the same seed
gives the same sample. Usage: python analysis/m5_sample.py
"""
import csv
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.benchmarks import all_tasks, view  # noqa: E402
from gbe.util import read_json, write_json  # noqa: E402

RUNS = ['phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code']
MODES = ['ASSERT_REMOVED', 'ASSERT_WEAKENED', 'ASSERT_ADDED', 'INPUT_CHANGED', 'SETUP_CHANGED', 'TEST_REWRITTEN',
         'EXCEPTION_EXPECTED', 'FUNCTION_SHADOWED', 'EXPECTED_CHANGED']  # rarest first, so rare modes are filled
PER_MODE = 12
CONTROLS = 20
SEED = 'gbe-m5-sample-v1'


def part_a(rng, tasks):
    candidates = []
    for run in RUNS:
        with open(ROOT / 'runs' / run / 'tests.csv', encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                if r['stage'] in ('P2', 'P3') and r['final_status'] == 'KEPT' and r['change_modes']:
                    candidates.append((run, r))
    chosen, used = [], set()
    for mode in MODES:
        pool = [c for c in candidates if mode in c[1]['change_modes'].split('|') and c[1]['test_id'] + c[1]['stage'] not in used]
        pool.sort(key=lambda c: (c[0], c[1]['test_id'], c[1]['stage']))
        for run, r in rng.sample(pool, min(PER_MODE, len(pool))):
            used.add(r['test_id'] + r['stage'])
            chosen.append((run, r))
    items, key = [], {}
    for run, r in chosen:
        unit = ROOT / 'runs' / run / 'units' / r['unit_id']
        i = int(r['test_id'].rsplit('/t', 1)[1])
        suite = read_json(unit / 'generated.json')
        final = read_json(unit / f"policy_{r['stage']}.json")['tests'][i]
        task = tasks[r['pair_id']]
        items.append({'before': suite['prelude'] + '\n' + suite['tests'][i]['source'],
                      'after': final['prelude'] + '\n' + final['source'],
                      'spec': view(task, r['condition'], 'code')['spec'], 'function': task['entry_point']})
        key[str(len(items) - 1)] = {'run': run, 'test_id': r['test_id'], 'policy': r['stage'],
                                    'condition': r['condition'], 'classifier': r['change_modes'].split('|'),
                                    'gen_label': r['gen_label'], 'label': r['label']}
    order = list(range(len(items)))
    rng.shuffle(order)
    return [dict(items[j], id=f'A{k + 1:03d}') for k, j in enumerate(order)], \
           {f'A{k + 1:03d}': key[str(j)] for k, j in enumerate(order)}


def part_b(rng):
    replies = []
    for arm in ('gpt-6.1-sol_medium_frozen', 'gpt-6.1-sol_medium_frozen_disguised', 'gpt-6.1-sol_medium_frozen_quixbugs',
                'gpt-6-luna_high_frozen'):
        for x in json.loads((ROOT / 'runs' / 'd11' / arm / 'evaluation.json').read_text(encoding='utf-8')):
            if x['condition'] == 'buggy' and x['suite_encodes_bug'] and not x['suite_reveals_bug']:
                replies.append((arm, x, 'locked'))
    controls = []
    for arm in ('gpt-6.1-sol_medium', 'gpt-6-luna_high'):
        for x in json.loads((ROOT / 'runs' / 'd11' / arm / 'evaluation.json').read_text(encoding='utf-8')):
            if x['condition'] == 'fixed':
                controls.append((arm, x, 'control'))
    controls.sort(key=lambda c: (c[0], c[1]['order']))
    replies += rng.sample(controls, CONTROLS)
    rng.shuffle(replies)
    items, key = [], {}
    for k, (arm, x, kind) in enumerate(replies):
        folder = next((ROOT / 'runs' / 'd11' / arm).glob(f"{x['order']:02d}_*"))
        attempt = sorted(folder.glob('attempt*'))[-1]
        message = (attempt / 'last_message.txt').read_text(encoding='utf-8', errors='replace')
        rid = f'B{k + 1:03d}'
        items.append({'id': rid, 'message': message})
        key[rid] = {'arm': arm, 'order': x['order'], 'pair_id': x['pair_id'], 'condition': x['condition'],
                    'kind': kind, 'regex_flag': x['message_flags_mismatch']}
    return items, key


def main():
    rng = random.Random(SEED)
    tasks = {t['task_id']: t for t in all_tasks()[0]}
    a_items, a_key = part_a(rng, tasks)
    b_items, b_key = part_b(rng)
    write_json(ROOT / 'review' / 'out' / 'm5_sample.json', {'seed': SEED, 'part_a': a_items, 'part_b': b_items})
    write_json(ROOT / 'review' / 'out' / 'm5_key.json', {'seed': SEED, 'part_a': a_key, 'part_b': b_key})
    print(f'Part A: {len(a_items)} repaired tests; Part B: {len(b_items)} agent replies')


if __name__ == '__main__':
    main()
