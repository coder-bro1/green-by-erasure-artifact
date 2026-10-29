"""D11 case study driver: a real coding agent (Codex CLI) on 40 buggy HumanEvalFix programs and their
fixed controls (docs/PHASE2_SPEC.md section 8). Separate from the controlled local-model runs.

  python scripts/d11.py prepare          write runs/d11/manifest.json (task list, neutral names, order)
  python scripts/d11.py run --count N    run the next N unfinished tasks, one at a time
  python scripts/d11.py status           progress per model setting
  python scripts/d11.py queue            run all remaining tasks, sleeping through usage-limit resets
  python scripts/d11.py plan             run the arms listed in configs/d11.json 'plan' in order
  --model / --effort override the model setting; results of each setting stay in their own folder
  --taskset disguised | quixbugs runs the same arm on the disguised HumanEvalFix programs
  (runs/d11/disguised_tasks.json, scripts/d11_disguise.py) or on the 40 QuixBugs programs
  add --variant frozen to any action for variant A (buggy programs only, instruction adds
  "Do not modify solution.py."); it has its own manifest, results folder and progress file

Isolation: each task gets a fresh folder under the neutral root in configs/d11.json, created just before
its session and deleted after its files are archived, so only one task folder exists at any time and no
counterpart program is reachable. The folder holds only solution.py and is its own git repository. Codex
runs with user config, rules and project instruction files disabled, web search off, ephemeral session.
Results go to runs/d11/<model>_<effort>/<task>/, so tasks run with different model settings never mix.
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.benchmarks import download, program  # noqa: E402
from gbe.util import read_json, write_json  # noqa: E402

CONFIG = read_json(ROOT / 'configs' / 'd11.json')
OUT = ROOT / 'runs' / 'd11'
VARIANT = 'open'  # set from --variant; 'open' is the original 80-task arm
MODEL, EFFORT = CONFIG['model'], CONFIG['reasoning_effort']  # overridable with --model / --effort
TASKSET = 'humanevalfix'  # --taskset: humanevalfix (default), disguised, quixbugs


def task_files(task, rows=None):
    """The files placed in a task folder: solution.py, plus node.py for the QuixBugs programs that use it."""
    taskset = task.get('taskset', 'humanevalfix')
    if taskset == 'humanevalfix':
        rows = rows or {r['task_id']: r for r in download()[0]}
        return {'solution.py': program(rows[task['pair_id']], task['condition'])}
    if taskset == 'disguised':
        disguised = read_json(OUT / 'disguised_tasks.json')
        return {'solution.py': disguised[task['pair_id']]['programs'][task['condition']]}
    if taskset == 'quixbugs':
        from gbe.quixbugs import load
        qb = {t['task_id']: t for t in load()}[task['pair_id']]
        return {'solution.py': qb['programs'][task['condition']], **qb['support']}
    raise ValueError(taskset)


def taskset_pairs():
    if TASKSET == 'quixbugs':
        from gbe.quixbugs import load
        return [t['task_id'] for t in load()]
    return read_json(ROOT / CONFIG['programs'])['pairs']


def variant_config():
    if VARIANT == 'open':
        return {'instruction': CONFIG['instruction'], 'conditions': ['buggy', 'fixed'], 'order_seed': CONFIG['order_seed']}
    return CONFIG['variants'][VARIANT]


def manifest_path():
    if TASKSET != 'humanevalfix':
        return OUT / f'manifest_{VARIANT}_{TASKSET}.json'
    return OUT / ('manifest.json' if VARIANT == 'open' else f'manifest_{VARIANT}.json')


def progress_path():
    # The first two arms (Sol, open and frozen) were started before per-setting progress files.
    legacy = {('open', 'gpt-6.1-sol', 'medium'): 'progress.json', ('frozen', 'gpt-6.1-sol', 'medium'): 'progress_frozen.json'}
    key = (VARIANT, MODEL, EFFORT) if TASKSET == 'humanevalfix' else None
    return OUT / legacy.get(key, f'progress_{setting()}.json')
SKIP = ('.git', '__pycache__', '.pytest_cache')


def remove_tree(path):
    # git object files are read-only on Windows; clear the flag so the folder really disappears.
    import stat
    def unlock(func, target, _):
        os.chmod(target, stat.S_IWRITE)
        func(target)
    shutil.rmtree(path, onexc=unlock)


def now():
    return datetime.now(timezone.utc).isoformat()


def codex_exe():
    found = sorted((Path(os.environ['LOCALAPPDATA']) / 'OpenAI' / 'Codex' / 'bin').glob('*/codex.exe'),
                   key=lambda p: p.stat().st_mtime)
    if not found:
        raise SystemExit('codex.exe not found under %LOCALAPPDATA%\\OpenAI\\Codex\\bin')
    return found[-1]


def prepare():
    path = manifest_path()
    if path.exists():
        raise SystemExit(f'{path} exists; the task list is fixed once written')
    rows = {r['task_id']: r for r in download()[0]}
    pairs = taskset_pairs()
    variant = variant_config()
    rng = random.Random(variant['order_seed'] + ('' if TASKSET == 'humanevalfix' else f'-{TASKSET}'))
    tasks = [{'pair_id': p, 'condition': c} for p in pairs for c in variant['conditions']]
    rng.shuffle(tasks)
    names = set()
    for i, t in enumerate(tasks):
        while True:
            name = 'w' + ''.join(rng.choice('abcdefghjkmnpqrstuvwxyz23456789') for _ in range(6))
            if name not in names:
                names.add(name)
                break
        t['taskset'] = TASKSET
        source = task_files(t, rows)['solution.py']
        t.update(order=i + 1, folder=name, solution_sha256=hashlib.sha256(source.encode()).hexdigest())
    write_json(path, {'created': now(), 'config': CONFIG, 'variant': VARIANT, 'instruction': variant['instruction'],
                      'tasks': tasks})
    print(f'{len(tasks)} tasks written to {path}')


def setting():
    return (f"{MODEL}_{EFFORT}" + ('' if VARIANT == 'open' else f'_{VARIANT}')
            + ('' if TASKSET == 'humanevalfix' else f'_{TASKSET}'))


def ensure_env():
    env = Path(CONFIG['work_root']) / 'env'
    python = env / 'Scripts' / 'python.exe'
    if not python.exists():
        subprocess.run([sys.executable, '-m', 'venv', str(env)], check=True)
        cache = os.environ.get('PIP_CACHE_DIR')  # this machine keeps pip's cache off the system drive
        subprocess.run([str(python), '-m', 'pip', 'install', *(['--cache-dir', cache] if cache else []), 'pytest==8.4.2'],
                       check=True, capture_output=True)
    return env


class Snapshotter(threading.Thread):
    """Store every new version of every file in the task folder, polling every 0.5 s."""
    def __init__(self, folder, target):
        super().__init__(daemon=True)
        self.folder, self.target, self.stop, self.seen, self.log = folder, target, threading.Event(), {}, []
        target.mkdir(parents=True, exist_ok=True)

    def scan(self):
        for p in self.folder.rglob('*'):
            if not p.is_file() or any(part in SKIP for part in p.relative_to(self.folder).parts):
                continue
            try:
                data = p.read_bytes()
            except OSError:
                continue
            rel = str(p.relative_to(self.folder)).replace('\\', '/')
            digest = hashlib.sha256(data).hexdigest()
            if self.seen.get(rel) != digest:
                self.seen[rel] = digest
                stored = self.target / f'{len(self.log):04d}__{rel.replace("/", "__")}'
                stored.write_bytes(data)
                self.log.append({'time': now(), 'file': rel, 'sha256': digest, 'stored': stored.name})

    def run(self):
        while not self.stop.is_set():
            self.scan()
            time.sleep(0.5)
        self.scan()


def run_task(task, rows, attempt):
    work_root = Path(CONFIG['work_root'])
    folder = work_root / task['folder']
    result_dir = OUT / setting() / f"{task['order']:02d}_{task['folder']}" / f'attempt{attempt}'
    if folder.exists():
        remove_tree(folder)
    for other in work_root.iterdir():
        if other.name != 'env':
            raise SystemExit(f'Another task folder exists ({other}); refuse to start (isolation)')
    folder.mkdir(parents=True)
    files = task_files(task, rows)
    assert hashlib.sha256(files['solution.py'].encode()).hexdigest() == task['solution_sha256']
    for name, text in files.items():
        (folder / name).write_text(text, encoding='utf-8')
    git = ['git', '-c', 'user.name=task', '-c', 'user.email=task@example.invalid']
    subprocess.run(['git', 'init', '-q'], cwd=folder, check=True)
    subprocess.run(git + ['add', *files], cwd=folder, check=True)
    subprocess.run(git + ['commit', '-q', '-m', 'start'], cwd=folder, check=True)
    result_dir.mkdir(parents=True, exist_ok=True)
    env = ensure_env()
    exe = codex_exe()
    version = subprocess.run([str(exe), '--version'], capture_output=True, text=True).stdout.strip()
    command = [str(exe), 'exec', '--json', '--ephemeral', '--ignore-user-config', '--ignore-rules',
               '--skip-git-repo-check', '-s', 'workspace-write', '-C', str(folder),
               '-m', MODEL, '-c', f'model_reasoning_effort="{EFFORT}"',
               '-c', 'windows.sandbox="unelevated"', '-c', 'web_search="disabled"', '-c', 'project_doc_max_bytes=0',
               '-o', str(result_dir / 'last_message.txt'), variant_config()['instruction']]
    child_env = dict(os.environ, PATH=str(env / 'Scripts') + os.pathsep + os.environ['PATH'], VIRTUAL_ENV=str(env))
    snap = Snapshotter(folder, result_dir / 'snapshots')
    snap.start()
    started, t0 = now(), time.monotonic()
    with open(result_dir / 'events.jsonl', 'wb') as out, open(result_dir / 'stderr.txt', 'wb') as err:
        process = subprocess.Popen(command, cwd=folder, env=child_env, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
        try:
            process.wait(timeout=CONFIG['time_limit_s'])
            status = 'FINISHED' if process.returncode == 0 else f'EXIT_{process.returncode}'
        except subprocess.TimeoutExpired:
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
            process.wait()
            status = 'TIME_LIMIT'
    seconds = time.monotonic() - t0
    snap.stop.set()
    snap.join()
    events = []
    for line in (result_dir / 'events.jsonl').read_text(encoding='utf-8-sig', errors='replace').splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    errors = [e.get('message') or e.get('error', {}).get('message', '') for e in events if e.get('type') in ('error', 'turn.failed')]
    quota = next((m for m in errors if m and 'usage limit' in m.lower()), None)
    if quota:
        status = 'QUOTA'
    usage = [e['usage'] for e in events if e.get('type') == 'turn.completed' and 'usage' in e]
    shutil.copytree(folder, result_dir / 'final', ignore=shutil.ignore_patterns(*SKIP, 'pytest-cache-files-*'))
    diff = subprocess.run(['git', 'diff', 'HEAD', '--', 'solution.py'], cwd=folder, capture_output=True, text=True).stdout
    (result_dir / 'solution_diff.txt').write_text(diff, encoding='utf-8')
    remove_tree(folder)
    result = {'task': task, 'variant': VARIANT, 'instruction': variant_config()['instruction'],
              'attempt': attempt, 'status': status, 'started': started, 'finished': now(),
              'seconds': round(seconds, 1), 'cli_version': version, 'model': MODEL,
              'reasoning_effort': EFFORT, 'sandbox': 'workspace-write, windows unelevated',
              'thread_id': next((e.get('thread_id') for e in events if e.get('type') == 'thread.started'), None),
              'usage': usage, 'errors': errors, 'quota_message': quota, 'solution_edited': bool(diff.strip()),
              'snapshots': snap.log,
              'unavailable_provenance': ['model snapshot or weights version behind the model name',
                                         'sampling settings (temperature, seed)', 'full system prompt and tool definitions',
                                         'server-side routing, retries or compaction', 'whether the served model changed during the study']}
    write_json(result_dir / 'result.json', result)
    return result


SERVICE_ERRORS = ('routing discovery failed', 'error sending request')


def effective_status(result):
    """A session that ended because Codex could not reach its service (it never produced an agent message or
    command) is a service error: like a usage-limit interruption it is not the task's outcome and is rerun.
    Applied to stored results too, so the 8 sessions of 12 October recorded as EXIT_1 are reclassified."""
    status = result['status']
    if status.startswith('EXIT') and any(any(m in (e or '') for m in SERVICE_ERRORS) for e in result.get('errors', [])):
        return 'SERVICE_ERROR'
    return status


def done_tasks():
    """A task is done when an attempt finished or hit the time limit, or after two other failures
    (spec 8.4: one rerun, then INCOMPLETE)."""
    base = OUT / setting()
    finished = set()
    if base.exists():
        for d in base.iterdir():
            statuses = [effective_status(read_json(p)) for p in d.glob('attempt*/result.json')]
            # Usage-limit interruptions are not the task's fault and never make it done; it reruns from a
            # fresh folder after the reset.
            if (any(s in ('FINISHED', 'TIME_LIMIT') for s in statuses)
                    or sum(s not in ('QUOTA', 'SERVICE_ERROR', 'FINISHED', 'TIME_LIMIT') for s in statuses) >= 2):
                finished.add(d.name)
    return finished


def reset_time(message, now_local=None):
    """Parse the reset time of a usage-limit message, in local time: 'try again at Oct 15th, 2026 11:03 AM',
    or a time only ('try again at 11:43 PM'), which is today, or tomorrow if already past. None if unknown."""
    m = re.search(r'try again at ([A-Z][a-z]{2}) (\d{1,2})(?:st|nd|rd|th)?, (\d{4}) (\d{1,2}:\d{2} [AP]M)', message or '')
    if m:
        return datetime.strptime(f'{m[1]} {m[2]} {m[3]} {m[4]}', '%b %d %Y %I:%M %p')
    m = re.search(r'try again at (\d{1,2}:\d{2} [AP]M)', message or '')
    if not m:
        return None
    current = now_local or datetime.now()
    at = datetime.strptime(m[1], '%I:%M %p').replace(year=current.year, month=current.month, day=current.day)
    from datetime import timedelta
    return at if at > current else at + timedelta(days=1)


def queue():
    manifest = read_json(manifest_path())
    total = len(manifest['tasks'])
    while True:
        done = len(done_tasks())
        write_json(progress_path(), {'setting': setting(), 'done': done, 'total': total,
                                           'percent': round(100 * done / total, 1), 'updated': now()})
        if done >= total:
            print('All D11 tasks done.', flush=True)
            return
        outcome = run(1)
        if outcome == 'QUOTA':
            last = sorted((OUT / setting()).glob('*/attempt*/result.json'), key=lambda p: p.stat().st_mtime)[-1]
            until = reset_time(read_json(last)['quota_message'])
            wait = max(300, (until - datetime.now()).total_seconds() + 120) if until else 3600
            write_json(progress_path(), {'setting': setting(), 'done': done, 'total': total,
                                               'percent': round(100 * done / total, 1), 'updated': now(),
                                               'paused_until': (until.isoformat() if until else f'{wait:.0f} s from updated')})
            print(f'Usage limit: sleeping {wait / 3600:.1f} h, until {until or "one hour from now"}', flush=True)
            time.sleep(wait)


def run(count):
    manifest = read_json(manifest_path())
    if manifest.get('instruction', manifest['config']['instruction']) != variant_config()['instruction']:
        raise SystemExit('Instruction changed after the manifest was written')
    rows = {r['task_id']: r for r in download()[0]}
    Path(CONFIG['work_root']).mkdir(parents=True, exist_ok=True)
    finished = done_tasks()
    todo = [t for t in manifest['tasks'] if f"{t['order']:02d}_{t['folder']}" not in finished][:count]
    for task in todo:
        key = f"{task['order']:02d}_{task['folder']}"
        attempts = len(list((OUT / setting() / key).glob('attempt*'))) if (OUT / setting() / key).exists() else 0
        result = run_task(task, rows, attempts + 1)
        tokens = sum(u.get('input_tokens', 0) + u.get('output_tokens', 0) for u in result['usage'])
        print(f"task {key}: {result['status']} in {result['seconds']} s, tokens {tokens}, "
              f"solution edited {result['solution_edited']}, {len(result['snapshots'])} file versions", flush=True)
        if result['status'] == 'QUOTA':
            print('Usage limit reached: ' + result['quota_message'], flush=True)
            return 'QUOTA'
    return 'OK'


def plan():
    """Run the arms listed in configs/d11.json 'plan' one after another; each arm resumes where it stopped."""
    global VARIANT, MODEL, EFFORT, TASKSET
    for step in CONFIG['plan']:
        VARIANT, MODEL, EFFORT = step['variant'], step['model'], step['reasoning_effort']
        TASKSET = step.get('taskset', 'humanevalfix')
        if not manifest_path().exists():
            prepare()
        print(f'=== D11 arm: {setting()}', flush=True)
        queue()


def status():
    for base in sorted(p for p in OUT.iterdir() if p.is_dir()):
        results = [read_json(p) for p in base.glob('*/attempt*/result.json')]
        final = {}
        for r in results:
            final[r['task']['order']] = r['status']
        print(base.name, f'{sum(s != "QUOTA" for s in final.values())} tasks done', dict(
            __import__('collections').Counter(final.values())))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=('prepare', 'run', 'status', 'queue', 'plan'))
    ap.add_argument('--count', type=int, default=1)
    ap.add_argument('--variant', default='open', choices=['open'] + sorted(CONFIG.get('variants', {})))
    ap.add_argument('--model', default=CONFIG['model'])
    ap.add_argument('--effort', default=CONFIG['reasoning_effort'])
    ap.add_argument('--taskset', default='humanevalfix', choices=('humanevalfix', 'disguised', 'quixbugs'))
    a = ap.parse_args()
    VARIANT, MODEL, EFFORT, TASKSET = a.variant, a.model, a.effort, a.taskset
    {'prepare': prepare, 'status': status, 'queue': queue, 'plan': plan}.get(a.action, lambda: run(a.count))()
