"""Cost and provenance of the Phase 2 local-model runs, for the Phase 2 report (section 6).

Per run: model and digest, harness commit, start and end, LLM calls by purpose and tokens from
runs/<run>/llm_calls.jsonl, wall-clock time from the manifest. Also counts the S4 replay calls and the S2
generation calls. Writes review/out/phase2_cost.md. Usage: python analysis/phase2_cost.py
"""
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ['phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code', 'phase2_qwen25_spec', 'phase2_qwen25_seed1',
        'phase2_qwen25_seed2', 'phase2_qwen25_seed3', 'phase2_qwen25_disguised', 'phase2_qwen35_disguised',
        'phase2_gemma4_disguised', 'phase2_qwen25_natural', 'phase2_qwen35_natural', 'phase2_gemma4_natural']


def calls(path):
    purposes, tokens_in, tokens_out, n = Counter(), 0, 0, 0
    if not path.exists():
        return purposes, 0, 0, 0
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            try:
                c = json.loads(line)
            except ValueError:
                continue
            n += 1
            purposes[c.get('purpose', '?')] += 1
            resp = c.get('response') or {}
            if isinstance(resp, dict):
                tokens_in += int(resp.get('prompt_eval_count') or 0)
                tokens_out += int(resp.get('eval_count') or 0)
    return purposes, tokens_in, tokens_out, n


def hours(a, b):
    if not a or not b:
        return None
    f = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
    return (f(b) - f(a)).total_seconds() / 3600


def main():
    lines = ['# Phase 2 cost and provenance', '', 'Computed by `analysis/phase2_cost.py` from each run\'s manifest.json and llm_calls.jsonl.',
             'Wall clock is manifest start to end (resumed runs include their pauses).', '',
             '| Run | Model | Digest (first 12) | Harness commit | Calls | Generation | Repair (all) | Judge | Input tokens | Output tokens | Wall clock (h) |',
             '|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|']
    tot = Counter()
    for run in RUNS:
        folder = ROOT / 'runs' / run
        m = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
        purposes, tin, tout, n = calls(folder / 'llm_calls.jsonl')
        gen = purposes.get('generate', 0) + purposes.get('generation', 0)
        judge = sum(v for k, v in purposes.items() if 'judge' in k)
        repair = n - gen - judge
        h = hours(m.get('start_time'), m.get('end_time'))
        tot.update({'calls': n, 'in': tin, 'out': tout})
        lines.append(f"| {run} | {m['model']} | {m['model_digest'][:12]} | {m['harness_commit'][:7]} | {n:,} | {gen:,} | {repair:,} | "
                     f"{judge:,} | {tin:,} | {tout:,} | {h:.1f} |" if h is not None else f"| {run} | {m['model']} | - | - | {n:,} | | | | | | - |")
    lines += ['', f"Total over the {len(RUNS)} runs: {tot['calls']:,} calls, {tot['in']:,} input and {tot['out']:,} output tokens.", '']
    purposes_all = Counter()
    for run in RUNS:
        purposes_all.update(calls(ROOT / 'runs' / run / 'llm_calls.jsonl')[0])
    lines.append('Calls by purpose, all runs: ' + ', '.join(f'{k} {v:,}' for k, v in purposes_all.most_common()) + '.')
    for name, path in (('S4 judge replay', ROOT / 'runs' / 's4_judge_specs'), ('S2 generation', ROOT / 'runs' / 's2_natural' / 'generation')):
        n = 0
        for f in path.rglob('llm_calls.jsonl') if path.exists() else []:
            n += calls(f)[3]
        lines.append(f'{name}: {n:,} calls.')
    ollama = {json.loads((ROOT / 'runs' / r / 'manifest.json').read_text(encoding='utf-8')).get('ollama_version') for r in RUNS}
    lines.append(f"Ollama versions recorded: {', '.join(sorted(v for v in ollama if v))}.")
    (ROOT / 'review' / 'out' / 'phase2_cost.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
