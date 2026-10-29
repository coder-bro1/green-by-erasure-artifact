"""S6: overwrite with the model only, to separate the effect of the copy rules from that of the model.

Overwrite (P2) first tries fixed rules that copy the observed value into a failing test (gbe.policies
.template_repair) and asks the model only when no rule applies, so nearly all of its inversions come from the rules
(805 of 806 with Qwen2.5, 737 of 826 with Gemma 4). This run repeats P2 on the same generated tests with the rules
switched off for this process, so every repair goes to the model with overwrite's own prompt
(prompts/overwrite_fallback_v1.txt). Nothing else changes: generated.json and initial.json are read from the source
run's units and never regenerated, and the model, digest, options and Ollama version are the source run's. The
harness files are not edited, so the source runs' provenance hashes stay valid. The policy is stored as P2M (the
model-call log still names it P2, the policy the code runs).

Evaluation follows gbe.evaluate (each kept test twice per version, 5 s limit); a test with a TIMEOUT execution is
re-executed twice per version with the 30 s limit of analysis/timeout_recheck.py and relabelled, so the labels are
comparable with the source run's tests_rechecked.csv, whose GEN labels are used for the fates. Buggy units run
first. Resumable per unit and per model call (cache under the run folder).

  python scripts/s6_model_only_overwrite.py --source phase2_gemma4_code [--limit N]
Writes runs/s6_model_only_<model>/units/<unit>/{policy_P2M,evaluation_P2M}.json, tests.csv and progress.json.
"""
import argparse
import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe import policies  # noqa: E402
from gbe.benchmarks import all_tasks, program, view  # noqa: E402
from gbe.evaluate import change_modes, evaluate_test, fate, label  # noqa: E402
from gbe.execute import execute  # noqa: E402
from gbe.llm import Client, http  # noqa: E402
from gbe.runner import csv_write, unit_id  # noqa: E402
from gbe.util import now, read_json, run_lock, write_json  # noqa: E402

RECHECK_LIMIT = 30


def evaluated(task, prelude, source):
    """Labels as in gbe.evaluate, with the timeout recheck of analysis/timeout_recheck.py applied at once."""
    programs = {c: program(task, c) for c in ('buggy', 'fixed')}
    result = evaluate_test(programs, prelude, source, task.get('support'), task.get('runtime'))
    if any(e['outcome'] == 'TIMEOUT' for runs in result['executions'].values() for e in runs):
        runtimes = {c: dict(task['runtime'][c], timeout=RECHECK_LIMIT) for c in programs} if 'runtime' in task else {}
        new = {c: [execute(programs[c], prelude, source, timeout=RECHECK_LIMIT, support=task.get('support'),
                           runtime=runtimes.get(c))['outcome'] for _ in range(2)] for c in programs}
        flaky = any(runs[0] != runs[1] for runs in new.values())
        result = {'outcome_fixed': new['fixed'][0], 'outcome_buggy': new['buggy'][0],
                  'label': 'FLAKY' if flaky else label(new['fixed'][0], new['buggy'][0]), 'rechecked': True}
    return {k: v for k, v in result.items() if k != 'executions'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True)
    ap.add_argument('--limit', type=int)
    a = ap.parse_args()
    source = ROOT / 'runs' / a.source
    out = ROOT / 'runs' / ('s6_model_only_' + a.source.split('_')[1])
    out.mkdir(parents=True, exist_ok=True)
    with run_lock(out / 'run.lock'):
        run(source, out, a.limit)


def run(source, out, limit):
    manifest = read_json(source / 'manifest.json')
    config, model = manifest['config'], manifest['model']
    if http('/api/version')['version'] != manifest['ollama_version']:
        raise ValueError('Ollama version differs from the source run')
    client = Client(out, model, manifest['model_digest'], manifest['options'])
    if not (out / 'manifest.json').exists():
        write_json(out / 'manifest.json', {'source_run': source.name, 'model': model,
                                           'model_digest': manifest['model_digest'], 'options': manifest['options'],
                                           'ollama_version': manifest['ollama_version'], 'policy': 'P2M',
                                           'prompt': 'overwrite_fallback_v1', 'rules': 'off', 'start_time': now()})
    with open(source / 'tests_rechecked.csv', encoding='utf-8') as fh:
        gen_label = {r['test_id']: r['label'] for r in csv.DictReader(fh) if r['stage'] == 'GEN'}
    tasks = {t['task_id']: t for t in all_tasks()[0]}
    pairs = read_json(source / 'pairs.json')
    combos = [(tasks[p['pair_id']], cond, g) for cond in ('buggy', 'fixed') for p in pairs
              for g in config['gen_inputs']][:limit]
    policies.template_repair = lambda *args, **kwargs: None  # the rules are off in this process only
    rows, started = [], time.monotonic()
    for n, (task, cond, g) in enumerate(combos, 1):
        uid = unit_id(task, cond, model, g, config['seed'])
        src, dst = source / 'units' / uid, out / 'units' / uid
        suite = read_json(src / 'generated.json')
        policy_path = dst / 'policy_P2M.json'
        if not policy_path.exists():
            result = policies.repair_policy('P2', suite, read_json(src / 'initial.json'), view(task, cond, g), client, uid)
            write_json(policy_path, dict(result, policy='P2M'))
        eval_path = dst / 'evaluation_P2M.json'
        if not eval_path.exists():
            meta = dict(unit_id=uid, pair_id=task['task_id'], condition=cond, model=model, seed=config['seed'],
                        gen_input=g)
            unit_rows = []
            for i, test in enumerate(read_json(policy_path)['tests']):
                kept = test['final_status'] != 'DROPPED'
                result = evaluated(task, test['prelude'], test['source']) if kept else {
                    'outcome_fixed': '', 'outcome_buggy': '', 'label': ''}
                original = gen_label[test['test_id']]
                unit_rows.append(dict(meta, stage='P2M', test_id=test['test_id'],
                    outcome_fixed=result['outcome_fixed'], outcome_buggy=result['outcome_buggy'], label=result['label'],
                    final_status=test['final_status'], outcome_put=test['outcome_put'], gen_label=original,
                    fate=fate(original, test['final_status'], result['label']) if cond == 'buggy' else '',
                    change_modes='|'.join(change_modes(suite['prelude'] + '\n' + suite['tests'][i]['source'],
                                                       test['prelude'] + '\n' + test['source'], task['entry_point'])),
                    n_llm_calls=test['n_llm_calls'], rechecked=bool(result.get('rechecked'))))
            write_json(eval_path, unit_rows)
        rows.extend(read_json(eval_path))
        elapsed = time.monotonic() - started
        write_json(out / 'progress.json', {'done': n, 'total': len(combos), 'percent': round(100 * n / len(combos), 1),
                                           'last': uid, 'elapsed_minutes': round(elapsed / 60, 1), 'updated': now()})
        print(f'{n}/{len(combos)} {uid}', flush=True)
    csv_write(out / 'tests.csv', rows)
    buggy = [r for r in rows if r['condition'] == 'buggy' and r['gen_label'] == 'REVEALS']
    fates = {f: sum(r['fate'] == f for r in buggy) for f in ('INVERTED', 'NEUTRALIZED', 'DROPPED', 'OTHER')}
    print(f'bug-revealing tests on buggy units: {len(buggy)}; fates under P2M: {fates}')
    manifest = read_json(out / 'manifest.json')
    write_json(out / 'manifest.json', dict(manifest, end_time=now(), units=len(combos)))


if __name__ == '__main__':
    main()
