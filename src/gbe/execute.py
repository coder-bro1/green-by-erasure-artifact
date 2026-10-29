import os
import subprocess
import sys
import signal
import uuid
from pathlib import Path

from .util import ROOT, read_json

_LAST_PYTHON = None  # environment of the previous runtime execution (warm-up when it changes)


def execute(program, prelude, source, timeout=5, work_root=None, support=None, runtime=None):
    """One pytest function (all parametrizations) per fresh process, hard wall timeout.

    `support` maps file names to sources placed next to solution.py (QuixBugs' node.py).
    `runtime` (stage C, real repositories): solution.py becomes `runtime['shim']`, which re-exports the
    module under test from a checkout; pytest runs with that environment's Python and PYTHONPATH, and an
    exception whose last frame lies under `put_roots` counts as raised by the program under test. With a
    runtime a TIMEOUT is confirmed by a second execution: the first import of a large project from a cold
    disk cache can exceed the limit on its own (C1 protocol, change 6). Before the first execution in an
    environment other than the previous one, an unrecorded warm-up imports the module once with a 120 s limit
    (C1 protocol, change 8).
    """
    global _LAST_PYTHON
    if runtime and runtime['python'] != _LAST_PYTHON:
        _execute('', 'from solution import *\n', 'def test_warm_up():\n    pass\n', 120, work_root, None,
                 dict(runtime, timeout=120))
        _LAST_PYTHON = runtime['python']
    row = _execute(program, prelude, source, timeout, work_root, support, runtime)
    if runtime and row['outcome'] == 'TIMEOUT':
        row = dict(_execute(program, prelude, source, timeout, work_root, support, runtime), timeout_retried=True)
    return row


def _execute(program, prelude, source, timeout, work_root, support, runtime):
    if runtime:
        timeout = runtime.get('timeout', timeout)
        work_root = runtime.get('work_root', work_root)
        program = runtime['shim']
    base = Path(work_root or ROOT / '.scratch' / 'execution')
    folder = base / uuid.uuid4().hex
    folder.mkdir(parents=True)
    (folder / 'solution.py').write_text(program, encoding='utf-8')
    for name, text in (support or {}).items():
        (folder / name).write_text(text, encoding='utf-8')
    (folder / 'test_generated.py').write_text(prelude + '\n' + source + '\n', encoding='utf-8')
    (folder / 'conftest.py').write_text(
        Path(__file__).with_name('pytest_probe.py').read_text(encoding='utf-8'), encoding='utf-8')
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONHASHSEED='0',
               PYTHONDONTWRITEBYTECODE='1')
    python = sys.executable
    if runtime:
        for key in ('PYTHONHOME', 'VIRTUAL_ENV', 'PYTHONIOENCODING'):
            env.pop(key, None)
        python = runtime['python']
        env.update(PYTHONPATH=os.pathsep.join(runtime['pythonpath']), PYTHONUTF8='1',
                   GBE_PUT_ROOTS=os.pathsep.join(runtime['put_roots']), TEMP=str(base), TMP=str(base))
    import shutil
    command = [python, '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
               '--tb=short', '--rootdir=.', '--confcutdir=.', 'test_generated.py']
    process = subprocess.Popen(command, cwd=folder, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace',
        start_new_session=os.name != 'nt')
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        # Windows venv python.exe launches a child interpreter. Killing only the
        # launcher leaves infinite tests running, so kill the owned process tree.
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.killpg(process.pid, signal.SIGKILL)
        process.kill()
        process.communicate()
        remove(folder)
        return {'outcome': 'TIMEOUT', 'frames': [], 'comparisons': [], 'output': 'Hard timeout'}
    rows = read_json(folder / 'probe.json') if (folder / 'probe.json').exists() else []
    failures = [row for row in rows if row['outcome'] != 'PASS']
    row = failures[0] if failures else (rows[0] if rows else {
        'outcome': 'COLLECT_ERROR', 'frames': [], 'comparisons': [], 'message': 'No tests collected'})
    row = dict(row)
    row['cases'] = rows
    row['output'] = stdout + stderr
    # Workspaces are disposable and contain generated code only. Preserve structured evidence.
    remove(folder)
    return row


def remove(folder):
    """Delete a workspace. After a killed process tree Windows can hold the folder for a moment, so retry
    briefly and then leave it; cleanup never changes an outcome (stage C, 20 October)."""
    import shutil
    import time
    for _ in range(10):
        try:
            shutil.rmtree(folder)
            return
        except FileNotFoundError:
            return
        except OSError:
            time.sleep(0.5)
    shutil.rmtree(folder, ignore_errors=True)
