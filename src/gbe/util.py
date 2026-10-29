import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[2]


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    if not isinstance(value, str):
        value = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(value.encode()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    # Flush the data to disk before the rename: after a hard power-off on 13 October 2026, NTFS had kept
    # the rename of the seed-1 manifest but not its contents (the file was all null bytes).
    with open(temp, 'w', encoding='utf-8') as handle:
        handle.write(json.dumps(value, indent=2, ensure_ascii=False))
        handle.flush()
        os.fsync(handle.fileno())
    # Windows readers and virus scanners can briefly deny delete-sharing on the
    # destination. Keep atomic publication and retry the replace, not the work unit.
    for attempt in range(40):
        try:
            os.replace(temp, path)
            break
        except PermissionError:
            if attempt == 39:
                raise
            time.sleep(.05)


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


@contextmanager
def run_lock(path):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a+b') as handle:
        if path.stat().st_size==0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        try:
            if os.name=='nt':
                import msvcrt
                msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as exc:
            raise RuntimeError('This run already has an active worker') from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name=='nt':
                msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)
            else:
                fcntl.flock(handle.fileno(),fcntl.LOCK_UN)
