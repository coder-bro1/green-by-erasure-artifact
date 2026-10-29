"""D11 Claude arm, run through the Claude desktop app's own agent (user decision of 12 October 2026: no
separate Claude Code CLI login; "start like in a new chat or session, as isolated as possible").

Each task is one fresh subagent of the coordinating Claude Code session: model Opus 5.5 (claude-opus-5-5),
effort medium, no earlier conversation, and the arm's instruction as its only message. For the whole arm the
coordinating session's working directory is the neutral folder <work>/work, so the subagent starts there
with no project memory or instruction files. The folder is emptied and refilled for every task (one task at
a time, same files and git setup as scripts/d11.py), and the same manifests as the Sol arms are used, so the
task list and order are identical.

  python scripts/d11_subagent.py begin --variant frozen        prepare the next unfinished task in <work>/work and
                                                               start the snapshotter; prints the instruction
  python scripts/d11_subagent.py end --variant frozen --agent-id ID [--status QUOTA --error TEXT]
                                                               stop the snapshotter, archive the folder and the
                                                               subagent transcript, write result.json, empty the folder
  python scripts/d11_subagent.py status --variant frozen

Results go to runs/d11/claude-opus-5-5_medium_<variant>/<order>_<folder>/attempt<N>/ in the shape of the
Codex results; events.jsonl holds the subagent transcript. Each result records the transcript's working
directory and any context that mentions the research (a leak check), so isolation is verified per session.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import d11  # noqa: E402
from gbe.benchmarks import download  # noqa: E402
from gbe.util import read_json, write_json  # noqa: E402

MODEL, EFFORT = 'claude-opus-5-5', 'medium'
AGENT = 'Claude desktop app subagent (agent type "claude")'
WORK = Path(d11.CONFIG['work_root']) / 'work'
# Words that would reveal the study to the agent if they appeared in its injected context.
LEAK_TERMS = ('erasure', 'green by', 'next_paper', 'thesis', 'new research', 'memory.md', 'humanevalfix',
              'quixbugs', 'bug-revealing', 'd11')


TASKSET = 'humanevalfix'  # --taskset: humanevalfix, disguised or quixbugs (same manifests as the Sol arms)


def configure(variant):
    d11.VARIANT, d11.MODEL, d11.EFFORT, d11.TASKSET = variant, MODEL, EFFORT, TASKSET


def empty_work():
    """Remove everything inside the work folder but keep the folder (it is the coordinating session's cwd)."""
    for child in WORK.iterdir():
        if child.is_dir():
            d11.remove_tree(child)
        else:
            os.chmod(child, 0o666)
            child.unlink()


def current():
    # Kept in the repository, never next to the work folder: it names the program and its condition.
    path = d11.OUT / 'current_subagent_task.json'
    return path, (read_json(path) if path.exists() else None)


def begin(variant):
    configure(variant)
    marker, running = current()
    if running:
        raise SystemExit(f"Task {running['key']} is still open; run 'end' for it first")
    for other in WORK.parent.iterdir():
        if other.name not in ('env', 'work'):
            raise SystemExit(f'Unexpected folder {other}; refuse to start (isolation)')
    WORK.mkdir(exist_ok=True)
    if any(WORK.iterdir()):
        raise SystemExit(f'{WORK} is not empty (left over from an interrupted task); inspect it, then empty it')
    manifest = read_json(d11.manifest_path())
    if manifest['instruction'] != d11.variant_config()['instruction']:
        raise SystemExit('Instruction changed after the manifest was written')
    finished = d11.done_tasks()
    todo = [t for t in manifest['tasks'] if f"{t['order']:02d}_{t['folder']}" not in finished]
    if not todo:
        print(json.dumps({'done': True}))
        return
    task = todo[0]
    key = f"{task['order']:02d}_{task['folder']}"
    base = d11.OUT / d11.setting() / key
    attempt = len(list(base.glob('attempt*'))) + 1 if base.exists() else 1
    result_dir = base / f'attempt{attempt}'
    result_dir.mkdir(parents=True)
    files = d11.task_files(task, {r['task_id']: r for r in download()[0]})
    assert hashlib.sha256(files['solution.py'].encode()).hexdigest() == task['solution_sha256']
    for name, text in files.items():
        (WORK / name).write_text(text, encoding='utf-8')
    git = ['git', '-c', 'user.name=task', '-c', 'user.email=task@example.invalid']
    subprocess.run(['git', 'init', '-q'], cwd=WORK, check=True)
    subprocess.run(git + ['add', *files], cwd=WORK, check=True)
    subprocess.run(git + ['commit', '-q', '-m', 'start'], cwd=WORK, check=True)
    # Snapshotter in its own detached, below-normal-priority process, so it outlives this command.
    flags = 0x8 | 0x200 | 0x4000  # DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP, BELOW_NORMAL_PRIORITY_CLASS
    command = [sys.executable, str(Path(__file__)), 'snap', '--target', str(result_dir)]
    try:
        snap = subprocess.Popen(command, creationflags=flags | 0x01000000, close_fds=True)  # break away from job
    except OSError:
        snap = subprocess.Popen(command, creationflags=flags, close_fds=True)
    state = {'key': key, 'task': task, 'variant': variant, 'attempt': attempt, 'result_dir': str(result_dir),
             'started': d11.now(), 't0': time.time(), 'snapshotter_pid': snap.pid,
             'instruction': d11.variant_config()['instruction']}
    write_json(marker, state)
    print(json.dumps({'key': key, 'attempt': attempt, 'instruction': state['instruction']}))


def snap(target):
    target = Path(target)
    s = d11.Snapshotter(WORK, target / 'snapshots')
    s.start()
    while not (target / 'stop').exists():
        time.sleep(0.5)
    s.stop.set()
    s.join()
    write_json(target / 'snapshots.json', s.log)


def transcript_path(agent_id):
    found = list((Path.home() / '.claude' / 'projects').glob(f'*/*/subagents/agent-{agent_id}.jsonl'))
    if len(found) != 1:
        raise SystemExit(f'Expected one transcript for agent {agent_id}, found {len(found)}')
    return found[0]


def read_transcript(path):
    entries = []
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        try:
            entries.append(json.loads(line))
        except ValueError:
            pass
    return entries


def summarise(entries):
    """Usage, models, effort, working directories, final message and leak check from a subagent transcript."""
    usage_by_id, models, efforts, cwds, final = {}, set(), set(), set(), ''
    for e in entries:
        if e.get('cwd'):
            cwds.add(e['cwd'])
        if e.get('type') != 'assistant':
            continue
        msg = e.get('message', {})
        if msg.get('usage'):
            usage_by_id[msg.get('id')] = msg['usage']  # repeated per content block; keep the last
        if msg.get('model'):
            models.add(msg['model'])
        if e.get('effort'):
            efforts.add(str(e['effort']))
        for c in msg.get('content') or []:
            if c.get('type') == 'tool_use' and c.get('name') == 'SubagentHandback':
                final = c.get('input', {}).get('message', final)
            elif c.get('type') == 'text' and c.get('text', '').strip():
                final = c['text']
    u = list(usage_by_id.values())
    cached = sum(x.get('cache_read_input_tokens', 0) for x in u)
    total_in = sum(x.get('input_tokens', 0) + x.get('cache_creation_input_tokens', 0) + x.get('cache_read_input_tokens', 0) for x in u)
    # Context injected into the agent (everything except its own replies and tool output it produced).
    injected = ' '.join(json.dumps(e.get('attachment') or e.get('message', {}).get('content', ''))
                        for e in entries if e.get('type') in ('user', 'attachment', 'system')
                        and not (isinstance(e.get('message', {}).get('content'), list)
                                 and any(c.get('type') == 'tool_result' for c in e['message']['content'])))
    leaks = sorted(t for t in LEAK_TERMS if t in injected.lower())
    return {'usage': [{'input_tokens': total_in, 'cached_input_tokens': cached,
                       'output_tokens': sum(x.get('output_tokens', 0) for x in u), 'api_calls': len(u),
                       'note': 'from the transcript; output_tokens can undercount (streamed snapshots)'}],
            'served_models': sorted(models), 'effort_recorded': sorted(efforts), 'transcript_cwds': sorted(cwds),
            'context_leak_terms': leaks, 'last_message': final}


def end(variant, agent_id, status, error, reported):
    configure(variant)
    marker, state = current()
    if not state:
        raise SystemExit('No open task')
    result_dir = Path(state['result_dir'])
    (result_dir / 'stop').write_text('', encoding='utf-8')
    for _ in range(120):
        if (result_dir / 'snapshots.json').exists():
            break
        time.sleep(0.5)
    else:
        raise SystemExit('Snapshotter did not finish')
    snapshots = read_json(result_dir / 'snapshots.json')
    seconds = time.time() - state['t0']
    shutil.copytree(WORK, result_dir / 'final', ignore=shutil.ignore_patterns(*d11.SKIP, 'pytest-cache-files-*'))
    diff = subprocess.run(['git', 'diff', 'HEAD', '--', 'solution.py'], cwd=WORK, capture_output=True, text=True).stdout
    (result_dir / 'solution_diff.txt').write_text(diff, encoding='utf-8')
    summary = {'usage': [], 'last_message': ''}
    if agent_id:
        path = transcript_path(agent_id)
        shutil.copy2(path, result_dir / 'events.jsonl')
        meta = path.with_suffix('').with_suffix('.meta.json')
        if meta.exists():
            shutil.copy2(meta, result_dir / 'agent_meta.json')
        summary = summarise(read_transcript(path))
    else:
        (result_dir / 'events.jsonl').write_text('', encoding='utf-8')
    (result_dir / 'last_message.txt').write_text(summary.pop('last_message'), encoding='utf-8')
    empty_work()
    result = {'task': state['task'], 'variant': variant, 'instruction': state['instruction'], 'agent': AGENT,
              'attempt': state['attempt'], 'status': status, 'started': state['started'], 'finished': d11.now(),
              'seconds': round(seconds, 1), 'seconds_reported': (reported.get('duration_ms') or 0) / 1000 or None,
              'cli_version': 'Claude desktop app ' + os.environ.get('CLAUDE_CODE_DESKTOP_APP_VERSION', 'unknown'),
              'model': MODEL, 'reasoning_effort': EFFORT,
              'sandbox': 'none; every tool call of the subagent passes the app\'s auto-mode safety classifier',
              'thread_id': agent_id, 'errors': [error] if error else [],
              'quota_message': error if status == 'QUOTA' else None, 'solution_edited': bool(diff.strip()),
              'reported_by_app': reported, **summary, 'snapshots': snapshots,
              'unavailable_provenance': ['model snapshot behind the model name', 'sampling settings',
                                         'full system prompt and tool definitions of the app subagent',
                                         'server-side routing, retries or compaction',
                                         'whether the served model changed during the study']}
    write_json(result_dir / 'result.json', result)
    marker.unlink()
    print(json.dumps({k: result[k] for k in ('status', 'seconds', 'solution_edited')}
                     | {'tokens': result['usage'], 'cwds': result.get('transcript_cwds'),
                        'leaks': result.get('context_leak_terms'), 'files': len(snapshots)}))


def status(variant):
    configure(variant)
    total = len(read_json(d11.manifest_path())['tasks'])
    done = len(d11.done_tasks())
    write_json(d11.progress_path(), {'setting': d11.setting(), 'done': done, 'total': total,
                                     'percent': round(100 * done / total, 1), 'updated': d11.now()})
    print(f'{d11.setting()}: {done} of {total} tasks done')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=('begin', 'end', 'snap', 'status'))
    ap.add_argument('--variant', choices=sorted(d11.CONFIG['variants']))
    ap.add_argument('--taskset', default='humanevalfix', choices=('humanevalfix', 'disguised', 'quixbugs'))
    ap.add_argument('--target')
    ap.add_argument('--agent-id')
    ap.add_argument('--status', default='FINISHED')
    ap.add_argument('--error')
    # What the app reported when the subagent finished (PowerShell 5.1 mangles JSON arguments, so plain numbers).
    ap.add_argument('--tokens', type=int)
    ap.add_argument('--tool-uses', type=int)
    ap.add_argument('--duration-ms', type=int)
    a = ap.parse_args()
    TASKSET = a.taskset
    if a.action == 'snap':
        snap(a.target)
    elif a.action == 'begin':
        begin(a.variant)
    elif a.action == 'end':
        end(a.variant, a.agent_id, a.status, a.error,
            {'subagent_tokens': a.tokens, 'tool_uses': a.tool_uses, 'duration_ms': a.duration_ms})
    else:
        status(a.variant)
