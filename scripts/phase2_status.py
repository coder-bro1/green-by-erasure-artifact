"""Overall Phase 2 progress from each run's progress.json and the queue state; safe to run at any time.
Usage: .venv\\Scripts\\python.exe scripts/phase2_status.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from gbe.runner import select_tasks  # noqa: E402
from gbe.util import read_json  # noqa: E402

runs = read_json(ROOT / 'configs' / 'runs.json')
done_all = total_all = 0
for run_id, config in ((k, v) for k, v in runs.items() if k != 'phase2_smoke'):
    total = len(select_tasks(config)[0]) * 2 * len(config['gen_inputs'])
    path = ROOT / 'runs' / run_id / 'progress.json'
    done = read_json(path)['done'] if path.exists() else 0
    done_all, total_all = done_all + done, total_all + total
    print(f'{run_id:24s} {done:5d}/{total:5d} units ({100 * done / total:5.1f}%)')
print(f'{"all LLM runs":24s} {done_all:5d}/{total_all:5d} units ({100 * done_all / total_all:5.1f}%)')
state = ROOT / 'runs' / 'phase2_queue' / 'state.json'
if state.exists():
    print('queue:', json.dumps(read_json(state)))
