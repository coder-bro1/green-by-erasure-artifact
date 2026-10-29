import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from .runner import csv_write
from .util import read_json, write_json


def summarize(run_dir, checks_passed=None):
    run_dir = Path(run_dir)
    rows = list(csv.DictReader((run_dir / 'tests.csv').open(encoding='utf-8')))
    manifest = read_json(run_dir / 'manifest.json')
    calls = [json.loads(line) for line in (run_dir / 'llm_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    groups = defaultdict(list)
    for row in rows:
        groups[(row['condition'], row['model'], row['gen_input'], row['stage'])].append(row)
    summaries = []
    for (condition, model, gen_input, policy), group in sorted(groups.items()):
        final = [r for r in group if r['final_status'] != 'DROPPED' and r['label'] != 'FLAKY']
        counts = Counter(r['label'] for r in final)
        fates = Counter(r['fate'] for r in group if r['gen_label'] == 'REVEALS' and r['label'] != 'FLAKY')
        relevant_calls = [c for c in calls if c['policy'] == ('' if policy == 'GEN' else policy)
                          and f'__{condition}__' in c['unit_id'] and c['unit_id'].endswith('__' + gen_input)]
        wall = 0
        if policy != 'GEN':
            for unit in {r['unit_id'] for r in group}:
                wall += read_json(run_dir / 'units' / unit / f'policy_{policy}.json')['wall_time_s']
        summary = dict(condition=condition, model=model, gen_input=gen_input, policy=policy,
            units=len({r['unit_id'] for r in group}), tests=len(group), final_size=len(final),
            reveals=counts['REVEALS'], encodes=counts['ENCODES'], neutral=counts['NEUTRAL'], broken=counts['BROKEN'],
            flaky=sum(r['label'] == 'FLAKY' for r in group),
            signal_units=len({r['unit_id'] for r in group if r['label'] == 'REVEALS'}),
            encodes_generated=sum(r['label'] == 'ENCODES' and r['gen_label'] == 'ENCODES' for r in final),
            encodes_repaired=sum(r['label'] == 'ENCODES' and r['gen_label'] != 'ENCODES' for r in final),
            quarantined=sum(r['final_status'] == 'QUARANTINED' for r in final),
            quarantined_reveals=sum(r['final_status'] == 'QUARANTINED' and r['label'] == 'REVEALS' for r in final),
            REPORTED=fates['REPORTED'], DROPPED=fates['DROPPED'], INVERTED=fates['INVERTED'],
            NEUTRALIZED=fates['NEUTRALIZED'], OTHER=fates['OTHER'],
            llm_calls=len(relevant_calls), network_calls=sum(not c.get('cache_hit',False) for c in relevant_calls),
            llm_seconds=sum(c['duration_s'] for c in relevant_calls), wall_seconds=wall)
        summaries.append(summary)
    csv_write(run_dir / 'summary.csv', summaries)
    modes = {policy: dict(Counter(mode for r in rows if r['stage'] == policy
                                 and r['label']!='FLAKY'
                                 for mode in r['change_modes'].split('|') if mode)) for policy in ('P2','P3')}
    rewrites={policy:sum(r['stage']==policy and bool(r['change_modes']) and r['label']!='FLAKY' for r in rows)
              for policy in ('P2','P3')}
    # D5 variants use logged decisions and previously evaluated tests only.
    indexed = {(r['test_id'], r['stage']): r for r in rows}
    variants = defaultdict(Counter)
    for r in rows:
        if r['stage'] != 'P4':
            continue
        gen = indexed[(r['test_id'], 'GEN')]
        for name in ('P4_STRICT', 'P4_KEEP_ALL', 'P4_HYBRID'):
            candidate = r
            status = r['final_status']
            if r['judge_verdict']:
                if name == 'P4_STRICT':
                    status = 'QUARANTINED' if r['judge_verdict'] == 'BUG' else 'DROPPED'
                elif name == 'P4_KEEP_ALL':
                    status, candidate = 'QUARANTINED', gen
                elif r['judge_verdict'] == 'TEST_WRONG':
                    candidate = indexed[(r['test_id'], 'P2')]
                    status = candidate['final_status']
            if status != 'DROPPED' and candidate['label'] != 'FLAKY':
                variants[(r['condition'], r['gen_input'], name)]['final_size'] += 1
                variants[(r['condition'], r['gen_input'], name)][candidate['label']] += 1
                variants[(r['condition'], r['gen_input'], name)][status] += 1
    write_json(run_dir / 'variants.json', {'|'.join(key): dict(value) for key,value in variants.items()})
    buggy_gen = [r for r in rows if r['stage'] == 'GEN' and r['condition'] == 'buggy']
    # The spec's 5-of-20 denominator is pair-level, with separate arm counts also printed.
    signal_pairs = {r['pair_id'] for r in buggy_gen if r['label'] == 'REVEALS'}
    signal_units = {r['unit_id'] for r in buggy_gen if r['label'] == 'REVEALS'}
    signal_by_input={arm:len({r['pair_id'] for r in buggy_gen if r['label']=='REVEALS' and r['gen_input']==arm})
                     for arm in sorted({r['gen_input'] for r in rows})}
    erasures = sum(r['fate'] in ('INVERTED','NEUTRALIZED') for r in rows if r['stage'] in ('P2','P3'))
    verification = read_json(run_dir / 'verification.json') if (run_dir / 'verification.json').exists() else {}
    if checks_passed is None:
        checks_passed = verification.get('section8_all_pass', False)
    pairs = read_json(run_dir / 'pairs.json')
    arms = sorted({r['gen_input'] for r in rows}) or manifest.get('config', {}).get('gen_inputs', ['code'])
    n_pairs, n_buggy_units = len(pairs), len(pairs) * len(arms)
    # GEN_FAIL units have no rows in tests.csv; they stay in every unit denominator (decision Q2).
    gen_fail = sorted(p.parent.name for p in (run_dir / 'units').glob('*/generated.json')
                      if read_json(p)['parse_status'] == 'GEN_FAIL')
    pilot = 'config' not in manifest or 'benchmarks' not in manifest['config']
    verdict = ('GO' if signal_by_input.get('code', 0) >= 5 and erasures >= 1 and checks_passed else 'NO-GO') if pilot else 'n/a'
    lines = [f'Run: {run_dir.name}'] + ([f'Verdict: {verdict}'] if pilot else []) + [
             f'Buggy pre-repair signal: {len(signal_pairs)}/{n_pairs} pairs; {len(signal_units)}/{n_buggy_units} units; '
             f'{sum(r["label"] == "REVEALS" for r in buggy_gen)}/{len(buggy_gen)} tests REVEALS.',
             f'GEN_FAIL units (counted in all unit denominators): {len(gen_fail)} of {n_pairs * 2 * len(arms)}'
             + (': ' + ', '.join(gen_fail) if gen_fail else ''),
             f'P2/P3 inversions or neutralizations: {erasures}',
             f'Signal pairs by input (each denominator {n_pairs}): ' + json.dumps(signal_by_input,sort_keys=True)] + (
             ['Signal threshold uses the default code arm (conservative resolution of the 20-unit denominator).',
              f'Section 8 offline checks all pass: {checks_passed}'] if pilot else []) + ['',
             '| Condition | Input | Policy | Final size | REVEALS | ENCODES generated | ENCODES repaired | REPORTED | DROPPED | INVERTED | NEUTRALIZED | OTHER | Quarantined | Quarantined REVEALS | Logical calls | Network calls | LLM seconds | Policy wall seconds |',
             '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for s in summaries:
        keys = ('condition','gen_input','policy','final_size','reveals','encodes_generated','encodes_repaired',
                'REPORTED','DROPPED','INVERTED','NEUTRALIZED','OTHER','quarantined','quarantined_reveals',
                'llm_calls','network_calls','llm_seconds','wall_seconds')
        lines.append('| ' + ' | '.join(f'{s[k]:.3f}' if isinstance(s[k],float) else str(s[k]) for k in keys) + ' |')
    lines.append('')
    for s in summaries:
        if s['policy']=='P4':
            raw_q=[r for r in rows if r['stage']=='P4' and r['condition']==s['condition']
                   and r['gen_input']==s['gen_input'] and r['final_status']=='QUARANTINED']
            if s['condition']=='buggy':
                lines.append(f'P4 buggy/{s["gen_input"]} quarantine precision: {s["quarantined_reveals"]}/{s["quarantined"]} nonflaky tests REVEALS; raw quarantines {len(raw_q)}.')
            else:
                lines.append(f'P4 fixed/{s["gen_input"]}: {len(raw_q)} raw quarantines are false alarms; {s["quarantined"]} nonflaky false alarms.')
    lines.extend(['', 'P2/P3 rewritten tests (change-mode denominators): ' + json.dumps(rewrites,sort_keys=True),
                  'P2/P3 change modes: ' + json.dumps(modes, sort_keys=True),
                  'LLM calls by purpose: ' + json.dumps(dict(Counter(c['purpose'] for c in calls)), sort_keys=True),
                  f'Total tokens (logical requests): {sum(c["prompt_eval_count"] + c["eval_count"] for c in calls)}',
                  f'Logical LLM calls: {len(calls)}; cache hits: {sum(c.get("cache_hit",False) for c in calls)}',
                  f'Mean seconds per uncached LLM call: {sum(c["duration_s"] for c in calls)/max(sum(not c.get("cache_hit",False) for c in calls),1):.3f}',
                  f'Mean seconds per unit: {sum(manifest["unit_seconds"].values())/max(len(manifest["unit_seconds"]),1):.3f}',
                  'Reasoning-bearing calls: ' + str(sum(bool(c['response']['message'].get('thinking')) or
                                                       '<think>' in c['response']['message']['content'] for c in calls)),
                  'Flaky rows (excluded): ' + str(sum(r['label']=='FLAKY' for r in rows)),
                  'Generation failures: ' + str(sum(read_json(p)['parse_status']=='GEN_FAIL' for p in
                                                    (run_dir/'units').glob('*/generated.json')))])
    unique={c['cache_key']:c for c in calls}
    serving_seconds=sum(c.get('request_duration_s',c['duration_s']) for c in unique.values())
    lines.extend([f'Unique network requests: {len(unique)}',
        f'Total tokens (unique network requests): {sum(c["prompt_eval_count"]+c["eval_count"] for c in unique.values())}',
        f'LLM serving seconds (unique requests): {serving_seconds:.3f}'])
    if manifest.get('end_time'):
        lines.append(f'Pilot wall seconds: {(datetime.fromisoformat(manifest["end_time"])-datetime.fromisoformat(manifest["start_time"])).total_seconds():.3f}')
    # Measured serving time per unit and arm (finding P1-R5); no scaling by model-check throughput.
    lines.extend(['', 'Measured serving seconds per unit (unique requests, all purposes):'])
    for arm in arms:
        units = n_pairs * 2
        seconds = sum(c.get('request_duration_s', c['duration_s']) for c in unique.values()
                      if c['unit_id'].endswith('__' + arm))
        lines.append(f'{arm}: {seconds / units:.1f} s per unit over {units} units ({seconds / 3600:.2f} h)')
    lines.extend(['', '| Model | Full digest | Peak GPU MiB | Load seconds | Tokens/s | Fully on GPU | Reasoning returned |',
        '|---|---|---:|---:|---:|---|---|'])
    for model,check in manifest['models'].items():
        lines.append(f'| {model} | {check["digest"]} | {check["peak_gpu_mib"]} | {check["load_seconds"]:.3f} | '
                     f'{check["tokens_per_second"]:.3f} | {check["fully_on_gpu"]} | {check["thinking_returned"]} |')
    lines.append('Ollama version: '+manifest['ollama_version'])
    report = '\n'.join(lines) + '\n'
    (run_dir / 'go_no_go.txt').write_text(report, encoding='utf-8')
    print(report)
    return verdict
