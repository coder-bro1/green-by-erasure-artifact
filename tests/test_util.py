from gbe import util
import pytest


def test_atomic_json_retries_windows_sharing_violation(tmp_path, monkeypatch):
    original=util.os.replace
    attempts=[]
    def transient(source,target):
        attempts.append(1)
        if len(attempts)<3:
            raise PermissionError('transient Windows sharing violation')
        original(source,target)
    monkeypatch.setattr(util.os,'replace',transient)
    monkeypatch.setattr(util.time,'sleep',lambda delay: None)
    path=tmp_path/'progress.json'
    util.write_json(path,{'percent':50})
    assert util.read_json(path)=={'percent':50} and len(attempts)==3


def test_one_worker_lock_is_released(tmp_path):
    path=tmp_path/'run.lock'
    with util.run_lock(path):
        with pytest.raises(RuntimeError,match='active worker'):
            with util.run_lock(path):
                pass
    with util.run_lock(path):
        pass
