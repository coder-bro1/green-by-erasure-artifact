"""Natural LLM faults from HumanEval+ as a benchmark (S2, docs/PHASE2_SPEC.md 8.8).

Each pair is a wrong solution that a local model wrote for a HumanEval+ task (passes HumanEval's own tests,
differs from the canonical solution on at least one HumanEval+ input) and the canonical solution, both
under the task's original prompt. Built by scripts/s2_natural_faults.py into data/s2/natural_faults.json,
pinned by configs/natural.json; sanity evidence (HumanEval+ inputs, twice per version) in
configs/natural_sanity.json. Until the pairs exist, the benchmark is empty.
"""
import hashlib
import json

from .util import ROOT, read_json

BENCHMARK = 'HumanEvalPlusNatural'


def load():
    pin = ROOT / 'configs' / 'natural.json'
    if not pin.exists():
        return []
    pinned = read_json(pin)
    path = ROOT / pinned['file']
    if hashlib.sha256(path.read_bytes()).hexdigest() != pinned['sha256']:
        raise ValueError('Natural-fault file differs from the pinned hash')
    tasks = []
    for tid, p in sorted(json.loads(path.read_text(encoding='utf-8')).items(), key=lambda kv: int(kv[0].split('/')[-1])):
        tasks.append({'task_id': f"{BENCHMARK}/{tid.split('/')[-1]}", 'benchmark': BENCHMARK,
                      'entry_point': p['entry_point'], 'programs': dict(p['programs']), 'prompt': p['prompt'],
                      'support': {}, 'bug_type': '', 'original_task_id': tid, 'author_model': p['author_model'],
                      'hidden_test': f"# HumanEval+ inputs of {tid}: the canonical solution's outputs are the oracle"})
    return tasks
