"""Stage C results (docs/C1_PROTOCOL.md section 7): the replication on 30 BugsInPy bugs next to the benchmark run.

Reads a stage C run (default c1_qwen25_code_r2; tests.csv, or the finished units' evaluation.json while the run
is in progress) and reports, with the same definitions and statistics as analysis/final_numbers.py (cluster
bootstrap over bugs): fates of revealing tests per policy, fix-blocking programs and what overwrite adds over
discard, triage reports and false reports; then per bug and per project, the test labels against the Phase 2 code
run of the same model, and the attrition of steps 1 to 4 (review/out/c1_attrition.md, review/out/c1_install.md).
Writes review/out/c1_results.md for the study run and review/out/c1_results_<run>.md for another run.
Usage: .venv\\Scripts\\python.exe analysis\\c1_results.py [run id]
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import final_numbers as fn  # noqa: E402

RUN = sys.argv[1] if len(sys.argv) > 1 else 'c1_qwen25_code_r2'
BASE = 'phase2_qwen35_code' if 'qwen35' in RUN else 'phase2_qwen25_code'


def load(run):
    folder = ROOT / 'runs' / run
    if (folder / 'tests.csv').exists():
        return fn.rows(run), True
    data = []
    for unit in sorted((folder / 'units').iterdir()):
        path = unit / 'evaluation.json'
        if path.exists():
            data.extend({k: '' if v is None else str(v) for k, v in r.items()}
                        for r in json.loads(path.read_text(encoding='utf-8')))
    return data, False


def labels(data, stage='GEN'):
    c = Counter(r['label'] for r in data if r['stage'] == stage)
    n = sum(c.values())
    return n, {k: c[k] for k in ('REVEALS', 'ENCODES', 'NEUTRAL', 'BROKEN', 'FLAKY')}


def pct(k, n):
    return f'{k} ({100 * k / n:.0f}%)' if n else '-'


def main():
    data, complete = load(RUN)
    units_done = len({r['unit_id'] for r in data})
    out = ['# Stage C: replication on 30 BugsInPy bugs', '',
           f'Computed by `analysis/c1_results.py` from runs/{RUN} '
           + ('(complete run).' if complete else f'(IN PROGRESS: {units_done} of 60 units with tests).'),
           'Same definitions and statistics as review/out/final_numbers.md; intervals: cluster bootstrap over bugs.', '']
    # Test labels before repair, against the benchmark run with the same model.
    out += ['## Generated tests before repair', '', '| Run | Tests | Reveals | Encodes | Neutral | Broken | Flaky |',
            '|---|---:|---:|---:|---:|---:|---:|']
    for name, rows_ in ((RUN, data), (BASE, fn.rows(BASE))):
        for cond in ('buggy', 'fixed'):
            n, c = labels([r for r in rows_ if r['condition'] == cond])
            out.append(f'| {name}, {cond} | {n} | ' + ' | '.join(pct(c[k], n) for k in c) + ' |')
    out.append('')
    if complete:
        out += ['## Fates, fix-blocking and triage', ''] + fn.run_section(RUN)[2:]
    # Per bug.
    flags = fn.program_flags(data, RUN) if complete else None
    by_unit = defaultdict(list)
    for r in data:
        by_unit[(r['pair_id'], r['condition'])].append(r)
    tasks = json.loads((ROOT / 'data' / 'c1' / 'tasks.json').read_text(encoding='utf-8'))
    out += ['## Per bug', '', '| Bug | Entry | Tests (buggy) | Broken | Reveals | Fix-blocking P1/P2/P3/P4 | P4 reports bug | '
            'P4 false report (fixed) |', '|---|---|---:|---:|---:|---|---|---|']
    per_project = defaultdict(Counter)
    for tid, t in tasks.items():
        rs = by_unit.get((tid, 'buggy'), [])
        fx = by_unit.get((tid, 'fixed'), [])
        gen = [r for r in rs if r['stage'] == 'GEN']
        fb = [any(r['stage'] == p and r['final_status'] == 'KEPT' and r['label'] == 'ENCODES' for r in rs) for p in ('P1', 'P2', 'P3', 'P4')]
        ev = any(r['stage'] == 'P4' and r['final_status'] == 'QUARANTINED' and r['gen_label'] == 'REVEALS' for r in rs)
        fr = any(r['stage'] == 'P4' and r['final_status'] == 'QUARANTINED' for r in fx)
        nrev = sum(r['label'] == 'REVEALS' for r in gen)
        done = any(r['stage'] == 'P4' for r in rs)
        out.append(f"| {tid.split('/')[1]} | {t['qualname']} | {len(gen)} | {sum(r['label'] == 'BROKEN' for r in gen)} | {nrev} | "
                   + ('/'.join('x' if b else '.' for b in fb) if done else 'pending') + f" | {'yes' if ev else ('no' if done else '')} | "
                   + ('yes' if fr else ('no' if fx else '')) + ' |')
        if done:
            pc = per_project[t['project']]
            pc['bugs'] += 1
            pc['signal'] += nrev > 0
            pc['P1'] += fb[0]
            pc['P2'] += fb[1]
            pc['P2_only'] += fb[1] and not fb[0]
            pc['evidence'] += ev
            pc['false'] += fr
    out += ['', '## Per project (buggy programs done)', '', '| Project | Bugs | With a revealing test | Fix-blocking discard | '
            'Fix-blocking overwrite | Added by overwrite | P4 reports bug | P4 false report |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for p, c in sorted(per_project.items()):
        out.append(f"| {p} | {c['bugs']} | {c['signal']} | {c['P1']} | {c['P2']} | {c['P2_only']} | {c['evidence']} | {c['false']} |")
    # Attrition.
    out += ['', '## Attrition', '', 'Steps 1 and 4: review/out/c1_attrition.md; steps 2 and 3: review/out/c1_install.md.']
    install = [json.loads(f.read_text(encoding='utf-8')) for f in (ROOT / 'runs' / 'c1' / 'install').glob('*.json')]
    sel = json.loads((ROOT / 'runs' / 'c1' / 'selection.json').read_text(encoding='utf-8'))['bugs']
    out.append(f"BugsInPy bugs {len(sel)}; step 1 (one function in one file) {sum(b['step1'] == 'pass' for b in sel)}; "
               f"step 4 (prompt fits) {sum(b['step4'] == 'pass' for b in sel)}; attempted in order {len(install)}; "
               f"step 2 failures {sum(r['step2'] != 'pass' for r in install)}; step 3 failures "
               f"{sum(r['step2'] == 'pass' and r.get('step3') != 'pass' for r in install)}; eligible {sum(r.get('step3') == 'pass' for r in install)}.")
    name = 'c1_results.md' if RUN == 'c1_qwen25_code_r2' else f'c1_results_{RUN[3:]}.md'
    (ROOT / 'review' / 'out' / name).write_text('\n'.join(out) + '\n', encoding='utf-8')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
