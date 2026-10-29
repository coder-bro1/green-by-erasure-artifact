"""Stage C (docs/C1_PROTOCOL.md): eligibility steps 2 (installation) and 3 (developer test) per bug, in selection order.

For every bug that passed steps 1 and 4 (runs/c1/selection.json), in project order and then bug order, until 8
eligible bugs per project or 30 in all:
- buggy checkout: the buggy commit plus the developer's test files and test data from the fixed commit (the
  bug.info test files and every file under a test path that the fix commit adds or changes); fixed checkout: the
  same plus the developer's fix patch (bug_patch.txt), so the two differ only by the patch. Git worktrees of a
  blobless clone.
- one virtual environment per checkout from the bug's Python (python.org NuGet build; 3.6.9 -> 3.6.8), installed as
  bugsinpy-compile does: every requirement line on its own, then the bug's setup.sh lines from the checkout root,
  then the requirement lines again if there were setup lines. A failing requirement line or pip line of setup.sh
  is retried once with --prefer-binary (protocol change 3: today's newest source release in a 2020 version range
  may need build tools that do not exist for the old Python); lines failing again are logged and skipped, as there.
  Lines that install the project itself are skipped (the checkout is on PYTHONPATH).
- the developer's test command from run_test.sh (pytest, py.test and tox run as `python -m pytest`), with
  PYTHONPATH = the bug.info pythonpath entries and the checkout root, PYTHONUTF8=1, run buggy, fixed, buggy, fixed.
  For a tox command, the [testenv] deps of the checkout's tox.ini are installed first, as tox would.
Step 2 fails when an environment cannot be created or a checkout's test cannot import the project or a
dependency (on the buggy checkout: no test ran and the output shows an import error). Step 3 passes when the buggy run fails (tests ran) and the fixed run passes, twice each. A project
whose first 3 attempted bugs fail step 2 is not tried further (protocol section 9, change 2).

Work happens in <work> (no spaces in the path; caches and temporary files there too). Resumable: one result file
per bug in runs/c1/install/; a bug interrupted half way restarts from scratch. Environments and worktrees of bugs
that leave are deleted; eligible bugs keep theirs for the pipeline. Writes runs/c1/install_progress.json and
review/out/c1_install.md after every bug.
Usage: .venv-c2\\Scripts\\python.exe analysis\\c1_install.py
"""
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIP = ROOT / 'data' / 'c1' / 'BugsInPy' / 'projects'
W = Path(r'<work>')
OUT = ROOT / 'runs' / 'c1' / 'install'
PER_PROJECT, TOTAL, PROJECT_STOP = 8, 30, 3
PY = {'3.6.9': '3.6.8'}
T_PIP, T_SETUP, T_TEST = 900, 1800, 900
IMPORT_ERR = re.compile(r'ModuleNotFoundError|ImportError|No module named|DLL load failed')
TEST_PATH = re.compile(r'(^|/)(tests?|testing)/|(^|/)test_[^/]*\.py$|_test\.py$|conftest\.py$')  # as c1_select.py


def read_text(path):
    raw = path.read_bytes()
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
        return raw.decode('utf-16')
    return raw.decode('utf-8-sig', errors='replace')


def info(path):
    out = {}
    for line in read_text(path).splitlines():
        m = re.match(r'\s*(\w+)\s*=\s*"(.*)"', line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def lines_of(path):
    if not path.exists():
        return []
    return [l.strip() for l in read_text(path).splitlines() if l.strip() and not l.strip().startswith('#')]


class Log:
    def __init__(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.f = open(path, 'a', encoding='utf-8', errors='replace')

    def __call__(self, text):
        self.f.write(text.rstrip('\n') + '\n')
        self.f.flush()


def run(cmd, cwd, env, timeout, log, shell=False):
    """(exit code or 'timeout', output)."""
    log(f'$ {cmd if isinstance(cmd, str) else " ".join(cmd)}   [cwd {cwd}]')
    p = subprocess.Popen(cmd, cwd=cwd, env=env, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    try:
        out, _ = p.communicate(timeout=timeout)
        code = p.returncode
    except subprocess.TimeoutExpired:
        subprocess.run(['taskkill', '/T', '/F', '/PID', str(p.pid)], capture_output=True)
        out, _ = p.communicate()
        code = 'timeout'
    out = out.decode('utf-8', errors='replace')
    log(out[-20000:])
    log(f'-> exit {code}')
    return code, out


def base_env():
    env = dict(os.environ)
    for k in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV', 'CONDA_PREFIX', 'PYTHONIOENCODING'):
        env.pop(k, None)
    env.update(TEMP=str(W / 'tmp'), TMP=str(W / 'tmp'), PIP_CACHE_DIR=str(W / 'pipcache'),
               PIP_DISABLE_PIP_VERSION_CHECK='1', PIP_NO_INPUT='1', PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    return env


def venv_env(venv, extra_path=None):
    env = base_env()
    env['VIRTUAL_ENV'] = str(venv)
    env['PATH'] = str(venv / 'Scripts') + os.pathsep + env['PATH']
    if extra_path:
        env['PYTHONPATH'] = os.pathsep.join(extra_path)
    return env


def git(args, cwd, log, timeout=1800):
    code, out = run(['git', *args], cwd, base_env(), timeout, log)
    if code != 0:
        raise RuntimeError(f'git {" ".join(args)} failed: {out[-500:]}')
    return out


def ensure_clone(project, url, log):
    repo = W / 'repos' / project
    if not (repo / '.git').exists():
        if repo.exists():
            shutil.rmtree(repo)
        repo.parent.mkdir(parents=True, exist_ok=True)
        git(['clone', '-c', 'core.autocrlf=false', '--filter=blob:none', '--no-checkout', url, str(repo)], W, log, timeout=3600)
        git(['config', 'core.longpaths', 'true'], repo, log)
    # Files as committed (LF), as on BugsInPy's Linux setup; Git for Windows converts to CRLF by default.
    git(['config', 'core.autocrlf', 'false'], repo, log)
    git(['config', 'core.eol', 'lf'], repo, log)
    return repo


def remove_bug_dir(repo, bug_dir, log):
    for wt in ('buggy', 'fixed'):
        if (bug_dir / wt).exists() and repo.exists():
            run(['git', 'worktree', 'remove', '--force', str(bug_dir / wt)], repo, base_env(), 600, log)
    if bug_dir.exists():
        shutil.rmtree(bug_dir, ignore_errors=True)
    if repo.exists():
        run(['git', 'worktree', 'prune'], repo, base_env(), 600, log)


def self_install(line, project):
    name = project.lower().replace('-', '_')
    low = line.lower().replace('-', '_')
    if f'egg={name}' in low:
        return True
    pkg = re.split(r'[=<>!~\[ ;]', low, maxsplit=1)[0]
    return pkg == name


def pip_args(req):
    """A requirement line as pip arguments: options (-e, -r, ...) split like a shell; a requirement with an
    environment marker stays one argument; inline comments are dropped."""
    req = re.sub(r'\s+#.*$', '', req).strip()
    return shlex.split(req) if req.startswith('-') else [req]


def tox_deps(wt):
    """The [testenv] deps of the checkout's tox.ini as pip argument lists (what tox installs before running)."""
    import configparser
    cfg = configparser.ConfigParser(interpolation=None, strict=False)
    try:
        cfg.read(wt / 'tox.ini', encoding='utf-8')
        raw = cfg.get('testenv', 'deps', fallback='')
    except configparser.Error:
        return []
    out = []
    for dep in (d.strip() for d in raw.splitlines()):
        if not dep or dep.startswith('#'):
            continue
        m = re.match(r'-r\s*(\S+)$', dep)
        out.append(['-r', m.group(1)] if m else pip_args(dep))
    return out


def setup_command(line):
    line = re.sub(r'^pip3?\s', 'python -m pip ', line)
    line = re.sub(r'^python3\s', 'python ', line)
    return line


def test_command(line, py):
    parts = shlex.split(line)
    if parts[0] in ('pytest', 'py.test', 'tox'):
        return [py, '-m', 'pytest', *parts[1:]]
    if parts[0] in ('python', 'python3'):
        return [py, *parts[1:]]
    return [py, '-m', *parts]


def install(version, wt, venv, bug_path, project, python, log):
    """Returns a dict with created, failed requirement and setup lines."""
    rec = {'created': False, 'requirements': 0, 'failed_requirements': [], 'setup': [], 'failed_setup': [],
           'prefer_binary': []}
    code, _ = run([str(python), '-m', 'venv', str(venv)], W, base_env(), T_PIP, log)
    if code != 0 or not (venv / 'Scripts' / 'python.exe').exists():
        return rec
    rec['created'] = True
    env = venv_env(venv)
    py = str(venv / 'Scripts' / 'python.exe')
    reqs = [l for l in lines_of(bug_path / 'requirements.txt') if not self_install(l, project)]
    rec['requirements'] = len(reqs)
    setups = lines_of(bug_path / 'setup.sh')
    rec['setup'] = setups

    def requirements(record):
        for req in reqs:
            code, _ = run([py, '-m', 'pip', 'install', *pip_args(req)], wt, env, T_PIP, log)
            if code != 0:
                code, _ = run([py, '-m', 'pip', 'install', '--prefer-binary', *pip_args(req)], wt, env, T_PIP, log)
                if record:
                    rec['prefer_binary' if code == 0 else 'failed_requirements'].append(req)

    requirements(True)
    for line in setups:
        m = re.match(r'touch\s+(\S+)$', line)
        if m:
            (wt / m.group(1)).parent.mkdir(parents=True, exist_ok=True)
            (wt / m.group(1)).touch()
            continue
        cmd = setup_command(line)
        code, _ = run(cmd, wt, env, T_SETUP, log, shell=True)
        if code != 0 and cmd.startswith('python -m pip install '):
            code, _ = run(cmd.replace('python -m pip install ', 'python -m pip install --prefer-binary ', 1), wt, env,
                          T_SETUP, log, shell=True)
            if code == 0:
                rec['prefer_binary'].append(line)
        if code != 0:
            rec['failed_setup'].append(line)
    if setups:
        requirements(False)
    if any(re.match(r'tox(\s|$)', l) for l in lines_of(bug_path / 'run_test.sh')):
        rec['tox_deps'], rec['failed_tox_deps'] = [], []
        for args in tox_deps(wt):
            code, _ = run([py, '-m', 'pip', 'install', *args], wt, env, T_PIP, log)
            if code != 0:
                code, _ = run([py, '-m', 'pip', 'install', '--prefer-binary', *args], wt, env, T_PIP, log)
            rec['tox_deps' if code == 0 else 'failed_tox_deps'].append(' '.join(args))
    return rec


def outcome(cmd_kind, code, out):
    """pass, fail (tests ran and failed), norun (nothing ran), timeout."""
    if code == 'timeout':
        return 'timeout'
    if code == 0:
        return 'pass' if cmd_kind == 'pytest' or re.search(r'Ran [1-9]\d* tests?', out) else 'norun'
    if cmd_kind == 'pytest':
        return 'fail' if code in (1, 2) and not re.search(r'no tests ran|ERROR: (file or directory )?not found', out) else 'norun'
    return 'fail' if re.search(r'Ran [1-9]\d* tests?', out) else 'norun'


def last_line(out):
    tail = [l for l in out.strip().splitlines() if l.strip()]
    return tail[-1][:300] if tail else ''


def process(row, bug_dir, log):
    project, bug = row['project'], row['bug']
    bug_path = BIP / project / 'bugs' / str(bug)
    binfo = info(bug_path / 'bug.info')
    pinfo = info(BIP / project / 'project.info')
    res = {'project': project, 'bug': bug, 'python_pinned': row['python_version'],
           'python_used': PY.get(row['python_version'], row['python_version']), 'started': time.strftime('%Y-%m-%d %H:%M:%S')}
    t0 = time.time()
    repo = ensure_clone(project, pinfo['github_url'].rstrip('/'), log)
    remove_bug_dir(repo, bug_dir, log)
    bug_dir.mkdir(parents=True)
    tests = [t.strip() for t in binfo.get('test_file', '').split(';') if t.strip()]
    fixed_id = binfo['fixed_commit_id']
    changed = git(['show', '--name-only', '--format=', fixed_id], repo, log).split()
    for path in changed:
        exists = run(['git', 'cat-file', '-e', f'{fixed_id}:{path}'], repo, base_env(), 120, log)[0] == 0
        if TEST_PATH.search(path) and path not in tests and exists:
            tests.append(path)
    res['test_files'] = tests
    res['checkout_eol'] = 'lf'
    for version in ('buggy', 'fixed'):
        wt = bug_dir / version
        git(['worktree', 'add', '--detach', '--force', str(wt), binfo['buggy_commit_id']], repo, log)
        if not prepare(wt, version, binfo, bug_path, tests, log):
            res.update(step2='fail: developer patch does not apply to the buggy commit', seconds=round(time.time() - t0))
            return res
    python = W / 'pythons' / res['python_used'] / 'python.exe'
    for version in ('buggy', 'fixed'):
        rec = install(version, bug_dir / version, bug_dir / f'env-{version}', bug_path, project, python, log)
        res[f'install_{version}'] = rec
        if not rec['created']:
            res.update(step2=f'fail: environment not created ({version})', seconds=round(time.time() - t0))
            return res
    return test_rounds(res, bug_dir, binfo, bug_path, log, t0)


def prepare(wt, version, binfo, bug_path, tests, log):
    """Write the checkout's tracked files afresh from the buggy commit (LF endings; untracked build outputs stay),
    then the fix patch (fixed only) and the test files and data from the fixed commit. False if the patch fails."""
    index = Path(git(['rev-parse', '--git-path', 'index'], wt, log).strip().splitlines()[-1])
    index = index if index.is_absolute() else wt / index
    if index.exists():
        index.unlink()
    git(['reset', '-q', '--hard', binfo['buggy_commit_id']], wt, log)
    if version == 'fixed':
        # The BugsInPy clone on this machine has CRLF files; the patch as committed upstream has LF endings.
        lf = W / 'tmp' / f"{bug_path.parent.parent.name}-{bug_path.name}.patch"
        lf.write_bytes((bug_path / 'bug_patch.txt').read_bytes().replace(b'\r\n', b'\n'))
        code, _ = run(['git', 'apply', '--whitespace=nowarn', str(lf)], wt, base_env(), 600, log)
        if code != 0:
            code, _ = run(['git', 'apply', '--whitespace=nowarn', str(bug_path / 'bug_patch.txt')], wt, base_env(), 600, log)
        if code != 0:
            return False
    if tests:
        git(['checkout', binfo['fixed_commit_id'], '--', *tests], wt, log)
    return True


def test_rounds(res, bug_dir, binfo, bug_path, log, t0):
    pp = [p for p in binfo.get('pythonpath', '').split(';') if p.strip()]
    runs = []
    commands = lines_of(bug_path / 'run_test.sh')
    res['test_commands'] = commands
    for rnd in (1, 2):
        for version in ('buggy', 'fixed'):
            wt = bug_dir / version
            venv = bug_dir / f'env-{version}'
            paths = [str(wt / Path(p.strip().strip('/')).relative_to(Path(p.strip().strip('/')).parts[0])) for p in pp
                     if len(Path(p.strip().strip('/')).parts) > 1] + [str(wt)]
            env = venv_env(venv, paths)
            results = []
            for line in commands:
                cmd = test_command(line, str(venv / 'Scripts' / 'python.exe'))
                kind = 'pytest' if cmd[2:3] == ['pytest'] else 'unittest'
                code, out = run(cmd, wt, env, T_TEST, log)
                results.append({'command': line, 'exit': code, 'outcome': outcome(kind, code, out),
                                'import_error': bool(IMPORT_ERR.search(out)), 'last_line': last_line(out)})
            agg = ('pass' if all(r['outcome'] == 'pass' for r in results)
                   else 'fail' if any(r['outcome'] == 'fail' for r in results) else
                   'timeout' if any(r['outcome'] == 'timeout' for r in results) else 'norun')
            runs.append({'round': rnd, 'version': version, 'outcome': agg, 'commands': results})
            res['runs'] = runs
            if version == 'fixed' and agg != 'pass':
                if any(r['import_error'] for r in results):
                    res['step2'] = 'fail: the fixed checkout cannot import the project or a dependency'
                else:
                    res['step2'] = 'pass'
                    res['step3'] = f'fail: developer test does not pass on the fixed checkout (round {rnd}: {agg})'
                res['seconds'] = round(time.time() - t0)
                return res
            if version == 'buggy' and agg != 'fail' and any(r['import_error'] for r in results):
                res['step2'] = 'fail: the buggy checkout cannot import the project or a dependency'
                res['seconds'] = round(time.time() - t0)
                return res
            if version == 'buggy' and agg != 'fail':
                res['step2'] = 'pass'
                res['step3'] = f'fail: developer test does not fail on the buggy checkout (round {rnd}: {agg})'
                res['seconds'] = round(time.time() - t0)
                return res
    res.update(step2='pass', step3='pass', seconds=round(time.time() - t0))
    return res


def report(sel, results, order):
    lines = ['# C1 attrition, steps 2 and 3', '',
             'Computed by `analysis/c1_install.py` (docs/C1_PROTOCOL.md, section 9 changes 1 to 3). Bugs in selection order;',
             f'stop at {PER_PROJECT} eligible per project or {TOTAL} in all; a project leaves after its first {PROJECT_STOP} attempts fail step 2.', '',
             '| Project | Steps 1+4 | Attempted | Step 2 fails | Step 3 fails | Eligible | Not tried |', '|---|---:|---:|---:|---:|---:|---:|']
    tot = [0] * 6
    for project in order:
        cand = [b for b in sel if b['project'] == project and b['step4'] == 'pass']
        rs = [results[(project, b['bug'])] for b in cand if (project, b['bug']) in results]
        att = [r for r in rs if 'step2' in r]
        s2 = sum(r['step2'] != 'pass' for r in att)
        s3 = sum(r['step2'] == 'pass' and r.get('step3') != 'pass' for r in att)
        el = sum(r.get('step3') == 'pass' for r in att)
        nt = len(cand) - len(att)
        row = [len(cand), len(att), s2, s3, el, nt]
        tot = [a + b for a, b in zip(tot, row)]
        lines.append(f'| {project} | ' + ' | '.join(map(str, row)) + ' |')
    lines.append('| all | ' + ' | '.join(map(str, tot)) + ' |')
    lines += ['', '## Per attempted bug', '', '| Bug | Python | Step 2 | Step 3 | Minutes |', '|---|---|---|---|---:|']
    for project in order:
        for b in sel:
            r = results.get((project, b['bug']))
            if b['project'] == project and r and 'step2' in r:
                lines.append(f"| {project}-{b['bug']} | {r['python_used']} | {r['step2']} | {r.get('step3', '')} | {r.get('seconds', 0) / 60:.0f} |")
    (ROOT / 'review' / 'out' / 'c1_install.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    for d in (W / 'tmp', W / 'pipcache', W / 'logs', OUT):
        d.mkdir(parents=True, exist_ok=True)
    data = json.loads((ROOT / 'runs' / 'c1' / 'selection.json').read_text(encoding='utf-8'))
    sel, order = data['bugs'], data['project_order']
    results = {}
    for f in OUT.glob('*.json'):
        r = json.loads(f.read_text(encoding='utf-8'))
        results[(r['project'], r['bug'])] = r
    progress = ROOT / 'runs' / 'c1' / 'install_progress.json'
    eligible = lambda: sum(r.get('step3') == 'pass' for r in results.values())
    for project in order:
        cand = sorted((b for b in sel if b['project'] == project and b['step4'] == 'pass'), key=lambda b: b['rank_in_project'])
        for b in cand:
            if eligible() >= TOTAL:
                break
            done_p = [results[(project, c['bug'])] for c in cand if (project, c['bug']) in results]
            if sum(r.get('step3') == 'pass' for r in done_p) >= PER_PROJECT:
                break
            first = [results.get((project, c['bug'])) for c in cand[:PROJECT_STOP]]
            if len(cand) > PROJECT_STOP and all(r is not None and r['step2'] != 'pass' for r in first):
                break
            key = (project, b['bug'])
            if key in results:
                continue
            bug_id = f"{project}-{b['bug']}"
            progress.write_text(json.dumps({'current': bug_id, 'eligible': eligible(), 'attempted': len(results),
                                            'time': time.strftime('%Y-%m-%d %H:%M:%S')}, indent=1), encoding='utf-8')
            print(f"[{time.strftime('%H:%M:%S')}] {bug_id} (Python {b['python_version']}); eligible so far {eligible()} of {TOTAL}", flush=True)
            log = Log(W / 'logs' / f'{bug_id}.log')
            log(f'===== {time.strftime("%Y-%m-%d %H:%M:%S")} start')
            bug_dir = W / 'work' / bug_id
            try:
                res = process(b, bug_dir, log)
            except RuntimeError as e:
                res = {'project': project, 'bug': b['bug'], 'python_pinned': b['python_version'],
                       'python_used': PY.get(b['python_version'], b['python_version']), 'step2': f'fail: {str(e)[:300]}'}
            if res.get('step3') != 'pass':
                remove_bug_dir(W / 'repos' / project, bug_dir, log)
            (OUT / f'{bug_id}.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
            results[key] = res
            print(f"    step 2: {res['step2']}; step 3: {res.get('step3', '-')}; {res.get('seconds', 0) / 60:.0f} min", flush=True)
            report(sel, results, order)
        if eligible() >= TOTAL:
            break
    report(sel, results, order)
    progress.write_text(json.dumps({'current': None, 'done': True, 'eligible': eligible(), 'attempted': len(results),
                                    'time': time.strftime('%Y-%m-%d %H:%M:%S')}, indent=1), encoding='utf-8')
    print(f'Done: {eligible()} eligible bugs of {len(results)} attempted. See review/out/c1_install.md', flush=True)


def retest():
    """Protocol change 3(f): rewrite the checkouts of every eligible bug with LF endings and run the four test runs
    again in the existing environments; results whose step 3 failed with a test outcome are removed for a full redo."""
    data = json.loads((ROOT / 'runs' / 'c1' / 'selection.json').read_text(encoding='utf-8'))
    rows = {(b['project'], b['bug']): b for b in data['bugs']}
    for f in sorted(OUT.glob('*.json')):
        r = json.loads(f.read_text(encoding='utf-8'))
        bug_id = f"{r['project']}-{r['bug']}"
        if r['step2'] == 'pass' and r.get('step3') != 'pass':
            f.unlink()
            print(f'{bug_id}: removed for a full redo ({r.get("step3")})', flush=True)
            continue
        if r.get('step3') != 'pass' or r.get('checkout_eol') == 'lf':
            continue
        log = Log(W / 'logs' / f'{bug_id}.log')
        log(f'===== {time.strftime("%Y-%m-%d %H:%M:%S")} retest with LF checkouts')
        bug_path = BIP / r['project'] / 'bugs' / str(r['bug'])
        binfo = info(bug_path / 'bug.info')
        repo = ensure_clone(r['project'], info(BIP / r['project'] / 'project.info')['github_url'].rstrip('/'), log)
        bug_dir = W / 'work' / bug_id
        t0 = time.time()
        for version in ('buggy', 'fixed'):
            assert prepare(bug_dir / version, version, binfo, bug_path, r['test_files'], log)
        old = {k: r.pop(k) for k in ('runs', 'step3', 'seconds')}
        r['runs_crlf'] = old['runs']
        r = test_rounds(r, bug_dir, binfo, bug_path, log, t0)
        r['seconds'] = old['seconds']
        r['checkout_eol'] = 'lf'
        if r.get('step3') != 'pass':
            remove_bug_dir(repo, bug_dir, log)
        f.write_text(json.dumps(r, indent=1), encoding='utf-8')
        print(f"{bug_id}: step 2 {r['step2']}; step 3 {r.get('step3')}", flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--retest':
        retest()
    elif len(sys.argv) > 1 and sys.argv[1] == '--only':
        # Debug helper: run one bug (project-bug) without the selection loop or bookkeeping.
        data = json.loads((ROOT / 'runs' / 'c1' / 'selection.json').read_text(encoding='utf-8'))
        p, n = sys.argv[2].rsplit('-', 1)
        row = next(b for b in data['bugs'] if b['project'] == p and b['bug'] == int(n))
        print(json.dumps(process(row, W / 'work' / sys.argv[2], Log(W / 'logs' / f'{sys.argv[2]}.log')), indent=1))
    else:
        main()
