"""Resumable run driver. Each run ID is described in configs/runs.json (model, inputs, benchmarks,
seed, temperature, task subset); Phase 1 pilots used the earlier single-model version of this file."""
import argparse
import csv
import inspect
import itertools
import subprocess
import time

from .benchmarks import all_tasks, benchmark_name, humanevalfix_sanity, program, view
from .evaluate import evaluate_unit
from .execute import execute
from .generate import parse_suite, suite_hash
from .llm import Client, MODELS, OPTIONS, http
from .policies import JUDGE_ABLATION_PROMPT, JUDGE_PROMPT, judge_v2b_parse, repair_policy
from .util import ROOT, digest, now, read_json, write_json, run_lock


def harness_hashes():
    files=list((ROOT/'src').rglob('*.py'))+list((ROOT/'prompts').glob('*.txt'))
    files.extend(p for p in (ROOT/'pyproject.toml',ROOT/'requirements.txt') if p.exists())
    return {str(p.relative_to(ROOT)).replace('\\','/'):digest(p.read_text(encoding='utf-8')) for p in files}


def harness_commit():
    """The git commit of the harness, or a marker when the code runs from an exported package (no .git)."""
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 'unknown (not a git checkout; see harness_files_sha256)'


def judge_fingerprint():
    prompts = {name: digest((ROOT / 'prompts' / f'{name}.txt').read_text(encoding='utf-8'))
               for name in (JUDGE_PROMPT, JUDGE_ABLATION_PROMPT)}
    return {'prompt': JUDGE_PROMPT, 'ablation_prompt': JUDGE_ABLATION_PROMPT, 'prompt_sha256': prompts,
            'parser_sha256': digest(inspect.getsource(judge_v2b_parse))}


def check_judge_frozen():
    # Decision Q1: the selected prompt and parser are frozen before full runs.
    if judge_fingerprint() != read_json(ROOT / 'configs' / 'judge.json'):
        raise ValueError('Judge prompt or parser differs from configs/judge.json')


def generate_unit(folder, context, client, unit_id):
    path = folder / 'generated.json'
    if path.exists():
        return read_json(path)
    responses = []
    for attempt in range(2):
        response = client.call(context.get('generate_prompt', 'generate_v1'), dict(context, reminder='' if attempt == 0 else
            'FORMAT REMINDER: valid Python only, one fenced block, top-level test_* functions.'),
            unit_id=unit_id, purpose='generate', round=attempt)
        responses.append(response)
        try:
            suite = parse_suite(response)
            break
        except (SyntaxError, ValueError):
            suite = {'prelude': '', 'tests': [], 'parse_status': 'GEN_FAIL'}
    suite['raw_response'] = response
    suite['responses'] = responses
    write_json(path, suite)
    return suite


def pipeline_unit(folder, context, client, unit_id, judge_ablation=True):
    suite = generate_unit(folder, context, client, unit_id)
    initial_path = folder / 'initial.json'
    if initial_path.exists():
        initial = read_json(initial_path)
    else:
        initial = [execute(context['program'], suite['prelude'], test['source'], support=context.get('support'),
                           runtime=context.get('runtime'))
                   for test in suite['tests']]
        write_json(initial_path, initial)
    for policy in ('P1', 'P2', 'P3', 'P4'):
        path = folder / f'policy_{policy}.json'
        if not path.exists():
            write_json(path, repair_policy(policy, suite, initial, context, client, unit_id, judge_ablation))
    return suite


def csv_write(path, rows):
    if not rows:
        return
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def task_key(row):
    suffix = row['task_id'].split('/')[-1]
    return (benchmark_name(row), int(suffix) if suffix.isdigit() else 0, suffix)


def usable(evidence):
    # A pair is usable if its fixed version passes the benchmark tests in every recorded run and its
    # buggy version fails (or times out) in every recorded run.
    as_list = lambda value: value if isinstance(value, list) else [value]
    return all(o == 'PASS' for o in as_list(evidence['fixed'])) and all(o != 'PASS' for o in as_list(evidence['buggy']))


def select_tasks(config):
    """Tasks of the configured benchmarks and subset; pairs failing the sanity check are excluded."""
    tasks, dataset = all_tasks()
    tasks = [t for t in tasks if benchmark_name(t) in config['benchmarks']]
    if config.get('subset'):
        wanted = set(read_json(ROOT / config['subset'])['pairs'])
        tasks = [t for t in tasks if t['task_id'] in wanted]
    evidence = humanevalfix_sanity([t for t in tasks if benchmark_name(t) == 'HumanEvalFix'])
    # Benchmarks whose own tests need a special layout keep recorded two-run evidence, bound to source hashes.
    for bench, file in (('QuixBugs', 'quixbugs_sanity.json'), ('HumanEvalFixDisguised', 'disguised_sanity.json'),
                        ('HumanEvalPlusNatural', 'natural_sanity.json'), ('BugsInPy', 'c1_sanity.json')):
        if any(benchmark_name(t) == bench for t in tasks):
            recorded = read_json(ROOT / 'configs' / file)
            for t in tasks:
                if benchmark_name(t) == bench:
                    entry = recorded[t['task_id']]
                    if entry['source_hashes'] != {c: digest(program(t, c)) for c in ('fixed', 'buggy')}:
                        raise ValueError(f'{bench} sanity evidence is stale for {t["task_id"]}')
                    evidence[t['task_id']] = entry
    selected = sorted((t for t in tasks if usable(evidence[t['task_id']])), key=task_key)
    excluded = [{'task_id': t['task_id'],
                 'sanity': {k: v for k, v in evidence[t['task_id']].items() if k != 'source_hashes'}}
                for t in sorted(tasks, key=task_key) if not usable(evidence[t['task_id']])]
    return selected, excluded, dataset


def run(run_id, stop_after=None):
    with run_lock(ROOT/'runs'/run_id/'run.lock'):
        return _run(run_id,stop_after)


def _run(run_id, stop_after=None):
    config = read_json(ROOT / 'configs' / 'runs.json')[run_id]
    run_dir = ROOT / 'runs' / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    models = read_json(ROOT / 'configs' / 'models.json')
    model = config['model']
    if model not in MODELS:
        raise ValueError(f'{model} is not an approved study model')
    options = dict(OPTIONS, temperature=config['temperature'], seed=config['seed'])
    client = Client(run_dir, model, models['models'][model]['digest'], options)
    if http('/api/version')['version'] != models['ollama_version']:
        raise ValueError('Ollama version changed after model checks')
    check_judge_frozen()
    manifest_path = run_dir / 'manifest.json'
    tasks, excluded, dataset = select_tasks(config)
    if manifest_path.exists():
        manifest = read_json(manifest_path)
        if manifest['harness_files_sha256'] != harness_hashes():
            raise ValueError('Harness or prompt files changed; refuse mixed-provenance resume')
        if manifest['config'] != config or manifest['model_digest'] != client.model_digest or manifest['options'] != options:
            raise ValueError('Run configuration, model digest or options changed; refuse mixed-provenance resume')
        if manifest['ollama_version'] != models['ollama_version']:
            raise ValueError('Ollama version changed; refuse mixed-provenance resume')
        if dataset['revision'] != manifest['dataset_revision']:
            raise ValueError('Dataset revision changed; refuse mixed-provenance resume')
        if [t['task_id'] for t in tasks] != [p['pair_id'] for p in read_json(run_dir / 'pairs.json')]:
            raise ValueError('Selected tasks changed; refuse mixed-provenance resume')
    else:
        write_json(run_dir / 'pairs.json', [{'pair_id': t['task_id'], 'benchmark': benchmark_name(t),
                                             'bug_type': t.get('bug_type', '')} for t in tasks])
        manifest = {'run_id': run_id, 'config': config, 'model': model, 'model_digest': client.model_digest,
                    'ollama_version': models['ollama_version'], 'models': models['models'],
                    'options': options, 'think': False, 'dataset': dataset, 'dataset_revision': dataset['revision'],
                    'quixbugs_commit': read_json(ROOT / 'configs' / 'quixbugs.json')['commit']
                                       if 'QuixBugs' in config['benchmarks'] else None,
                    'disguised_sha256': read_json(ROOT / 'configs' / 'disguised.json')['sha256']
                                        if 'HumanEvalFixDisguised' in config['benchmarks'] else None,
                    'natural_sha256': read_json(ROOT / 'configs' / 'natural.json')['sha256']
                                      if 'HumanEvalPlusNatural' in config['benchmarks'] else None,
                    'c1': read_json(ROOT / 'configs' / 'c1.json') if 'BugsInPy' in config['benchmarks'] else None,
                    'judge': judge_fingerprint(), 'excluded_tasks': excluded,
                    'prompt_hashes': {p.name: digest(p.read_text(encoding='utf-8')) for p in (ROOT / 'prompts').glob('*.txt')},
                    'harness_commit': harness_commit(),
                    'harness_files_sha256': harness_hashes(),
                    'start_time': now(), 'end_time': None, 'input_test_hashes': {}, 'unit_seconds': {}}
        write_json(manifest_path, manifest)
    combinations = list(itertools.product(tasks, ('buggy', 'fixed'), config['gen_inputs']))
    ident = lambda row, condition, gen_input: unit_id(row, condition, model, gen_input, config['seed'])
    done = sum((run_dir / 'units' / ident(*c) / 'evaluation.json').exists() for c in combinations)
    total = len(combinations)
    elapsed, completed_here = 0., 0
    def progress():
        previous = list(manifest['unit_seconds'].values())
        # Before the first completed unit, use the pilots' measured mean of about 125 s per unit.
        average = elapsed / completed_here if completed_here else (sum(previous)/len(previous) if previous else 125)
        eta = average * (total - done)
        write_json(run_dir / 'progress.json', {'done': done, 'total': total, 'percent': done / total * 100,
                                              'eta_seconds': eta, 'updated': now()})
        print(f'{done/total*100:.1f}% | {done}/{total} units | ETA {eta/60:.1f} minutes', flush=True)
    progress()
    for row, condition, gen_input in combinations:
        identifier = ident(row, condition, gen_input)
        folder = run_dir / 'units' / identifier
        if (folder / 'evaluation.json').exists():
            continue
        started = time.monotonic()
        suite = pipeline_unit(folder, view(row, condition, gen_input), client, identifier)
        manifest['input_test_hashes'][identifier] = {p: suite_hash(suite) for p in ('P1', 'P2', 'P3', 'P4')}
        write_json(manifest_path, manifest)
        metadata = dict(unit_id=identifier, pair_id=row['task_id'], condition=condition, model=model,
                        seed=config['seed'], gen_input=gen_input)
        evaluate_unit(folder, row, metadata)
        duration = time.monotonic() - started
        manifest['unit_seconds'][identifier] = duration
        elapsed += duration
        completed_here += 1
        done += 1
        write_json(manifest_path, manifest)
        progress()
        if stop_after and completed_here >= stop_after:
            return
    rows = []
    for row, condition, gen_input in combinations:
        rows.extend(read_json(run_dir / 'units' / ident(row, condition, gen_input) / 'evaluation.json'))
    csv_write(run_dir / 'tests.csv', rows)
    manifest['end_time'] = now()
    write_json(manifest_path, manifest)
    from .report import summarize
    summarize(run_dir)
    progress()


def unit_id(row, condition, model, gen_input, seed=0):
    slug = model.replace(':', '-').replace('.', '-')
    return f"{benchmark_name(row)}-{row['task_id'].split('/')[-1]}__{condition}__{slug}__s{seed}__{gen_input}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--stop-after', type=int)
    args = parser.parse_args()
    run(args.run_id, args.stop_after)
