"""S2: the natural-fault benchmark loader is empty until the pairs are built, then pinned."""
import json

from gbe import natural
from gbe.util import read_json, write_json


def test_empty_until_built(monkeypatch, tmp_path):
    monkeypatch.setattr(natural, 'ROOT', tmp_path)
    assert natural.load() == []


def test_loads_pinned_pairs_and_rejects_changed_files(monkeypatch, tmp_path):
    import hashlib
    import pytest
    monkeypatch.setattr(natural, 'ROOT', tmp_path)
    data = {'HumanEval/7': {'entry_point': 'f', 'prompt': 'def f(x):\n    """Return x."""\n', 'author_model': 'm',
                            'seed': 1, 'n_inputs': 3, 'n_differ': 1,
                            'programs': {'buggy': 'def f(x):\n    """Return x."""\n    return x + 1\n',
                                         'fixed': 'def f(x):\n    """Return x."""\n    return x\n'}}}
    (tmp_path / 'data' / 's2').mkdir(parents=True)
    path = tmp_path / 'data' / 's2' / 'natural_faults.json'
    path.write_text(json.dumps(data), encoding='utf-8')
    write_json(tmp_path / 'configs' / 'natural.json', {'file': 'data/s2/natural_faults.json',
                                                         'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    (task,) = natural.load()
    assert task['task_id'] == 'HumanEvalPlusNatural/7' and task['benchmark'] == 'HumanEvalPlusNatural'
    assert task['programs']['buggy'] != task['programs']['fixed'] and task['author_model'] == 'm'
    path.write_text(json.dumps(data) + ' ', encoding='utf-8')
    with pytest.raises(ValueError):
        natural.load()


def test_write_json_round_trips(tmp_path):
    write_json(tmp_path / 'a' / 'b.json', {'x': [1, 2]})
    assert read_json(tmp_path / 'a' / 'b.json') == {'x': [1, 2]}
    assert not (tmp_path / 'a' / 'b.json.tmp').exists()
