import ast
import json
from pathlib import Path

import pytest

from gbe.benchmarks import view
from gbe.evaluate import change_modes, fate, label
from gbe.execute import execute
from gbe.generate import oracle_locked, parse_suite, suite_hash
from gbe.llm import FakeClient, local_model
from gbe.policies import repair_policy, template_repair
from gbe.runner import pipeline_unit
from gbe.util import ROOT, read_json

GOOD = 'def add(a,b):\n    return a+b\n'
BAD = 'def add(a,b):\n    return a+b+1\n'
PRELUDE = 'from solution import *\n'
TEST = 'def test_add():\n    assert add(1,2)==3'
CONTEXT = {'program': BAD, 'spec': 'def add(a,b):\n    """Return a+b."""', 'entry_point':'add', 'generation_input':BAD}


@pytest.mark.parametrize('program,prelude,source,expected', [
    (GOOD, PRELUDE, TEST, 'PASS'),
    (BAD, PRELUDE, TEST, 'ASSERT_FAIL'),
    ('def add(a,b):\n    raise ValueError("bad")', PRELUDE, TEST, 'PUT_EXCEPTION'),
    (GOOD, PRELUDE, 'def test_x(): missing()', 'TEST_ERROR'),
    (GOOD, PRELUDE, 'def test_x(:', 'COLLECT_ERROR'),
    (GOOD, PRELUDE, 'def test_x():\n    while True: pass', 'TIMEOUT'),
    (GOOD, PRELUDE, 'def test_x(): add(1)', 'TEST_ERROR'),
    ('def add(a,b):\n    assert False', PRELUDE, TEST, 'PUT_EXCEPTION'),
    (GOOD, PRELUDE, 'def test_x(): raise AssertionError("explicit")', 'TEST_ERROR'),
    (GOOD, 'import pytest\n'+PRELUDE, '@pytest.mark.parametrize("x",[2,3])\ndef test_x(x): assert x==2', 'ASSERT_FAIL'),
])
def test_outcomes(program, prelude, source, expected):
    result = execute(program, prelude, source, timeout=1.5 if expected=='TIMEOUT' else 5)
    assert result['outcome'] == expected, result
    json.dumps(result)


@pytest.mark.parametrize('source,expected', [(TEST,'REVEALS'),
    (TEST.replace('==3','==4'),'ENCODES'), ('def test_x(): assert add(1,2)>0','NEUTRAL'),
    (TEST.replace('==3','==9'),'BROKEN')])
def test_toy_labels(source,expected):
    assert label(execute(GOOD,PRELUDE,source)['outcome'], execute(BAD,PRELUDE,source)['outcome']) == expected


def test_p2_and_pass_untouched():
    suite = parse_suite('```python\n'+PRELUDE+TEST+'\n```')
    initial = [execute(BAD, suite['prelude'], suite['tests'][0]['source'])]
    client = FakeClient([])
    result = repair_policy('P2', suite, initial, CONTEXT, client, 'toy')
    final = result['tests'][0]
    assert final['final_status']=='KEPT'
    assert '== 4' in final['source']
    assert final['versions'][1]['action']=='T3'
    initial = [execute(GOOD,suite['prelude'],suite['tests'][0]['source'])]
    kept = repair_policy('P2',suite,initial,dict(CONTEXT,program=GOOD),client,'toy')['tests'][0]
    assert kept['source']==suite['tests'][0]['source'] and len(kept['versions'])==1


def test_nonliteral_fallback():
    source = 'def test_x():\n    expected=3\n    assert add(1,2)==expected'
    outcome=execute(BAD,PRELUDE,source)
    assert template_repair(source,PRELUDE,outcome) is None
    suite=parse_suite(PRELUDE+source)
    client=FakeClient([PRELUDE+TEST.replace('==3','==4')])
    result=repair_policy('P2',suite,[outcome],CONTEXT,client,'toy')
    assert client.calls[0]['purpose']=='overwrite_fallback'
    assert result['tests'][0]['final_status']=='KEPT'


def test_p2_repairs_assertion_in_helper():
    prelude=PRELUDE+'\ndef check_sum():\n    assert add(1,2)==3\n'
    source='def test_x(): check_sum()'
    outcome=execute(BAD,prelude,source)
    fixed,new_prelude,action=template_repair(source,prelude,outcome)
    assert action=='T3' and '== 4' in new_prelude
    assert execute(BAD,new_prelude,fixed)['outcome']=='PASS'
    assert 'EXPECTED_CHANGED' in change_modes(prelude+source,new_prelude+fixed,'add')


@pytest.mark.parametrize('source,program,action', [
    ('def test_x(): assert add(1,2)', 'def add(a,b): return False','T2'),
    ('def test_x(): assert not add(1,2)', GOOD,'T2'),
    ('def test_x(): assert add(1,2) is None', GOOD,'T2'),
    ('def test_x(): assert add(1,2) is not None','def add(a,b): return None','T2'),
    (TEST,'def add(a,b): raise ValueError("bad")','T4'),
])
def test_other_templates(source,program,action):
    outcome=execute(program,PRELUDE,source)
    fixed,prelude,used=template_repair(source,PRELUDE,outcome)
    assert used==action
    assert execute(program,prelude,fixed)['outcome']=='PASS'


def test_oracle_lock_rejects():
    assert not oracle_locked(TEST,TEST.replace('==3','==4'))
    assert not oracle_locked(TEST,TEST.replace('add(1,2)','add(2,2)'))
    assert not oracle_locked('def test_x(): assert add(-1,2)==3', 'def test_x(): assert add(1,2)==3')
    assert not oracle_locked(TEST+', "old message"',TEST+', "new message"')
    assert oracle_locked(TEST,TEST.replace('test_add','test_other'))
    broken=TEST.replace('add(1,2)','missing(1,2)')
    suite=parse_suite(PRELUDE+broken)
    client=FakeClient([PRELUDE+TEST.replace('==3','==4')]*3)
    result=repair_policy('P4',suite,[execute(BAD,PRELUDE,broken)],CONTEXT,client,'toy')
    assert result['tests'][0]['final_status']=='DROPPED'
    assert all(not v['accepted'] for v in result['tests'][0]['versions'][1:])


def test_policy_identical_inputs_and_judge():
    suite=parse_suite(PRELUDE+TEST)
    initial=[execute(BAD,suite['prelude'],suite['tests'][0]['source'])]
    client=FakeClient([PRELUDE+TEST.replace('==3','==4'), '{"answer":"YES","reason":"Sum is wrong."}', 'invalid'])
    results=[repair_policy(p,suite,initial,CONTEXT,client,'toy') for p in ('P1','P2','P3','P4')]
    assert all(r['input_hash']==suite_hash(suite) for r in results)
    p4=results[-1]['tests'][0]
    assert p4['source']==suite['tests'][0]['source'] and p4['final_status']=='QUARANTINED'
    assert p4['judge_verdict']=='BUG' and p4['judge_answer']=='YES'
    assert p4['judge_with_code_verdict']=='UNSURE'
    judge=next(c for c in client.calls if c['purpose']=='judge')
    assert judge['template']=='judge_v2b' and set(judge['fields'])=={'spec','test'}
    prompt=(ROOT/'prompts/judge_v2b.txt').read_text().format_map(judge['fields'])
    assert BAD not in prompt and GOOD not in prompt
    ablation=next(c for c in client.calls if c['purpose']=='judge_with_code')
    # D10: the same fields as the primary judge plus only the implementation.
    assert ablation['template']=='judge_with_code_v2b'
    assert ablation['fields']==dict(judge['fields'],program=BAD)


def test_quarantine_after_setup_repair_retains_generated_bytes_and_outcome():
    source=TEST.replace('add(1,2)','missing(1,2)')
    suite=parse_suite(PRELUDE+source)
    initial=[execute(BAD,suite['prelude'],suite['tests'][0]['source'])]
    client=FakeClient([PRELUDE+TEST,'{"answer":"YES","reason":"Sum wrong."}',
                       '{"answer":"NO","reason":"Ablation only."}'])
    t=repair_policy('P4',suite,initial,CONTEXT,client,'toy')['tests'][0]
    assert t['final_status']=='QUARANTINED' and t['source']==suite['tests'][0]['source']
    assert t['outcome_put']=='TEST_ERROR' and t['judged_outcome']['outcome']=='ASSERT_FAIL'


def test_leakage_boundary():
    row={'canonical_solution':'    return "SECRET_FIXED_BODY"', 'buggy_solution':'    return "buggy"',
         'test':'assert SECRET_BENCHMARK_TEST', 'example_test':'assert SECRET_EXAMPLE',
         'import':'', 'declaration':'def add(a,b):\n', 'prompt':'def add(a,b):\n    """Return sum."""',
         'docstring':'Return sum.', 'entry_point':'add'}
    context=view(row,'buggy','code')
    for path in (ROOT/'prompts').glob('*.txt'):
        fields=dict(context,test=TEST,feedback='AssertionError actual=4 expected=3',reminder='',module='m',project='p')
        prompt=path.read_text().format_map(fields)
        assert all(s not in prompt for s in ('SECRET_FIXED_BODY','SECRET_BENCHMARK_TEST','SECRET_EXAMPLE'))
        if path.name in ('judge_v1.txt','judge_v2b.txt'):
            assert 'return "buggy"' not in prompt
    spec=view(row,'buggy','spec')['generation_input']
    assert spec==row['prompt'] and 'return "buggy"' not in spec


def test_judge_sees_neither_implementation_nor_behaviour():
    program='def add(a,b):\n    raise ValueError("implementation sentinel")'
    suite=parse_suite(PRELUDE+TEST)
    initial=[execute(program,suite['prelude'],suite['tests'][0]['source'])]
    assert 'raise ValueError' in initial[0]['output']
    client=FakeClient(['{"answer":"YES","reason":"Unexpected exception."}']*2)
    repair_policy('P4',suite,initial,dict(CONTEXT,program=program),client,'toy')
    fields=client.calls[0]['fields']
    prompt=(ROOT/'prompts/judge_v2b.txt').read_text().format_map(fields)
    # v2b gets neither the implementation nor the observed behaviour (exception type included).
    assert 'implementation sentinel' not in prompt and 'ValueError' not in prompt


def test_resume_no_repeated_calls(tmp_path):
    responses=[PRELUDE+TEST, PRELUDE+TEST.replace('==3','==4'),
               '{"answer":"YES","reason":"Sum wrong."}', '{"answer":"YES","reason":"Sum wrong."}']
    client=FakeClient(responses)
    interrupted=tmp_path/'interrupted'
    # Crash after P2, before P3 completion. Cached generation and policy files survive.
    from gbe.runner import generate_unit
    generate_unit(interrupted,CONTEXT,client,'toy')
    saved=client.call
    def crash(template,fields,**kwargs):
        if kwargs['purpose']=='free_repair':
            raise RuntimeError('simulated interruption')
        return saved(template,fields,**kwargs)
    client.call=crash
    with pytest.raises(RuntimeError):
        pipeline_unit(interrupted,CONTEXT,client,'toy')
    client.call=saved
    pipeline_unit(interrupted,CONTEXT,client,'toy')
    count=len(client.calls)
    pipeline_unit(interrupted,CONTEXT,client,'toy')
    assert len(client.calls)==count==4
    full=tmp_path/'full'
    pipeline_unit(full,CONTEXT,FakeClient(responses),'toy')
    for name in ('generated.json','policy_P1.json','policy_P2.json','policy_P3.json','policy_P4.json'):
        a,b=read_json(interrupted/name),read_json(full/name)
        a.pop('wall_time_s',None); b.pop('wall_time_s',None)
        # Pytest timing text varies; compare all semantic execution fields.
        def scrub(value):
            if isinstance(value,dict): return {k:scrub(v) for k,v in value.items() if k!='output'}
            if isinstance(value,list): return [scrub(v) for v in value]
            return value
        assert scrub(a)==scrub(b)


@pytest.mark.parametrize('status,final,expected', [('DROPPED','','DROPPED'),
    ('QUARANTINED','REVEALS','REPORTED'),('KEPT','ENCODES','INVERTED'),
    ('KEPT','NEUTRAL','NEUTRALIZED'),('KEPT','FLAKY','OTHER')])
def test_fates(status,final,expected):
    assert fate('REVEALS',status,final)==expected


@pytest.mark.parametrize('after,expected', [
    (TEST.replace('==3','==4'),'EXPECTED_CHANGED'),
    ('def test_add(): pass','ASSERT_REMOVED'),
    ('def test_add(): assert add(1,2) is not None','ASSERT_WEAKENED'),
    ('def test_add(): assert type(add(1,2))==int','ASSERT_WEAKENED'),
    ('def test_add(): assert len([add(1,2)])==1','ASSERT_WEAKENED'),
    (TEST.replace('add(1,2)','add(2,2)'),'INPUT_CHANGED'),
    ('def test_add():\n    with pytest.raises(ValueError):\n        add(1,2)','EXCEPTION_EXPECTED'),
])
def test_changes(after,expected):
    assert expected in change_modes(TEST,after,'add')


def test_cloud_rejected_without_network():
    with pytest.raises(ValueError,match='Cloud'):
        local_model('glm:Cloud')


def test_timeout_kills_child_interpreter(tmp_path):
    import os
    if os.name!='nt':
        pytest.skip('Windows venv launcher regression')
    pidfile=tmp_path/'child.pid'
    source=('def test_hang():\n    import os\n    from pathlib import Path\n    Path('+repr(str(pidfile))+
            ').write_text(str(os.getpid()))\n    while True: pass\n')
    assert execute(GOOD,PRELUDE,source,timeout=1.5)['outcome']=='TIMEOUT'
    assert pidfile.exists()
    import ctypes
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.OpenProcess.restype=ctypes.c_void_p
    kernel.OpenProcess.argtypes=[ctypes.c_uint32,ctypes.c_bool,ctypes.c_uint32]
    kernel.GetExitCodeProcess.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_uint32)]
    kernel.CloseHandle.argtypes=[ctypes.c_void_p]
    handle=kernel.OpenProcess(0x1000,False,int(pidfile.read_text()))
    if handle:
        status=ctypes.c_uint32()
        assert kernel.GetExitCodeProcess(handle,ctypes.byref(status))
        kernel.CloseHandle(handle)
        assert status.value!=259, 'Timed-out interpreter is still active'


def test_runtime_put_exception_from_checkout(tmp_path):
    """Stage C: an exception that leaves the checkout's code is the program's; one raised in the test is not."""
    import sys
    pkg = tmp_path / 'checkout' / 'pkg'
    pkg.mkdir(parents=True)
    (pkg / '__init__.py').write_text('')
    (pkg / 'mod.py').write_text('def f(x):\n    if x < 0:\n        raise ValueError("neg")\n    return x\n')
    runtime = {'python': sys.executable, 'pythonpath': [str(tmp_path / 'checkout')],
               'put_roots': [str(tmp_path / 'checkout')], 'work_root': str(tmp_path / 'exec'),
               'shim': 'from pkg.mod import *\nfrom pkg.mod import f\n', 'timeout': 30}
    prelude = 'from solution import *\n'
    assert execute('', prelude, 'def test_a():\n    assert f(1) == 1', runtime=runtime)['outcome'] == 'PASS'
    assert execute('', prelude, 'def test_b():\n    assert f(1) == 2', runtime=runtime)['outcome'] == 'ASSERT_FAIL'
    assert execute('', prelude, 'def test_c():\n    f(-1)', runtime=runtime)['outcome'] == 'PUT_EXCEPTION'
    assert execute('', prelude, 'def test_d():\n    raise KeyError(1)', runtime=runtime)['outcome'] == 'TEST_ERROR'



def test_probe_end_line_without_end_lineno():
    """Python 3.6 and 3.7 have no end_lineno; the probe must still place a failing assertion (stage C)."""
    from gbe.pytest_probe import end_line
    node = ast.parse('assert f(1) == [\n    1,\n    2]\n').body[0]
    assert end_line(node) == 3
    for n in ast.walk(node):
        n.__dict__.pop('end_lineno', None)
    assert end_line(node) == 3
