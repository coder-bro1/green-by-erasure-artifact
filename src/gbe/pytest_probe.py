"""Copied into each isolated pytest workspace; never imports benchmark data."""
import ast
import json
import os
from pathlib import Path

import pytest

records = []
comparisons = []


def end_line(node):
    """Last line of a statement. Python 3.8 added end_lineno; stage C environments run Python 3.6 and 3.7,
    where the largest line number inside the statement is used instead."""
    end = getattr(node, 'end_lineno', None)
    return end if end is not None else max(getattr(n, 'lineno', node.lineno) for n in ast.walk(node))


def value_info(value):
    representation = repr(value)
    try:
        decoded = ast.literal_eval(representation)
        literal = type(decoded) is type(value) and decoded == value
    except (ValueError, SyntaxError):
        literal = False
    return {'repr': representation, 'literal': literal}


def pytest_assertrepr_compare(config, op, left, right):
    comparisons.append({'operator': op, 'left': value_info(left), 'right': value_info(right)})


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    result = yield
    report = result.get_result()
    if not report.failed and report.when != 'call':
        return
    row = {'outcome': 'PASS', 'nodeid': item.nodeid, 'phase': report.when,
           'frames': [], 'comparisons': list(comparisons)}
    if report.skipped:
        row.update(outcome='TEST_ERROR', message='Skipped or expected-failure cases are not passing tests')
    comparisons.clear()
    if call.excinfo:
        frames = [{'file': Path(str(frame.path)).name, 'line': frame.lineno + 1,
                   'function': frame.name} for frame in call.excinfo.traceback]
        last = frames[-1] if frames else {}
        exc = call.excinfo
        row.update(exception_type=exc.type.__name__, message=str(exc.value), frames=frames)
        # Stage C: the program under test is a module of a checkout (GBE_PUT_ROOTS), not solution.py. The
        # exception counts as the program's when, after the test's last frame, the traceback enters the checkout.
        roots = [os.path.normcase(os.path.abspath(r)) for r in os.environ.get('GBE_PUT_ROOTS', '').split(os.pathsep) if r]
        in_put = False
        if roots and last.get('file') != 'test_generated.py':
            paths = [os.path.normcase(os.path.abspath(str(e.path))) for e in exc.traceback]
            after = max((i for i, f in enumerate(frames) if f['file'] == 'test_generated.py'), default=-1)
            in_put = any(p.startswith(r + os.sep) for p in paths[after + 1:] for r in roots)
            row['put_frames'] = sum(any(p.startswith(r + os.sep) for r in roots) for p in paths[after + 1:])
        if last.get('file') == 'solution.py' or in_put:
            row['outcome'] = 'PUT_EXCEPTION'
        elif exc.type is AssertionError and last.get('file') == 'test_generated.py':
            tree = ast.parse(Path('test_generated.py').read_text(encoding='utf-8'))
            line = last['line']
            row['outcome'] = 'ASSERT_FAIL' if any(
                isinstance(n, ast.Assert) and n.lineno <= line <= end_line(n)
                for n in ast.walk(tree)) else 'TEST_ERROR'
        else:
            row['outcome'] = 'TEST_ERROR'
    records.append(row)


def pytest_collectreport(report):
    if report.failed:
        records.append({'outcome': 'COLLECT_ERROR', 'message': str(report.longrepr),
                        'frames': [], 'comparisons': []})


def pytest_sessionfinish(session, exitstatus):
    Path('probe.json').write_text(json.dumps(records), encoding='utf-8')
