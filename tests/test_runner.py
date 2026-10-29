import shutil
import pytest

from gbe import runner, report, evaluate
from gbe.llm import FakeClient
from gbe.util import ROOT, read_json, write_json


def test_two_pair_run_resumes_after_first_unit(tmp_path,monkeypatch):
    actual_root=ROOT
    monkeypatch.setattr(runner,'ROOT',tmp_path)
    shutil.copytree(actual_root/'prompts',tmp_path/'prompts')
    write_json(tmp_path/'configs/models.json',{'ollama_version':'test',
        'models':{'qwen2.5-coder:7b-instruct':{'digest':'a'*64}}})
    config={'model':'qwen2.5-coder:7b-instruct','gen_inputs':['code','spec'],'benchmarks':['HumanEvalFix'],
            'seed':0,'temperature':0,'subset':None}
    write_json(tmp_path/'configs/runs.json',{'interrupted':config,'full':config,'changed':dict(config,seed=1)})
    write_json(tmp_path/'configs/judge.json',runner.judge_fingerprint())
    pairs=[{'task_id':f'Python/{i}','import':'','declaration':'def add(a,b):\n',
        'canonical_solution':'    return a+b\n','buggy_solution':'    return a+b+1\n',
        'docstring':'Return the sum.', 'prompt':'def add(a,b):\n    """Return the sum."""',
        'entry_point':'add','benchmark':'HumanEvalFix'} for i in (1,2,3)]
    monkeypatch.setattr(runner,'all_tasks',lambda: (pairs,{'revision':'test'}))
    # Pair 3 fails the sanity check (its buggy version passes) and must be excluded and listed.
    monkeypatch.setattr(runner,'humanevalfix_sanity',lambda rows: {
        r['task_id']:{'fixed':'PASS','buggy':'PASS' if r['task_id']=='Python/3' else 'ASSERT_FAIL'} for r in rows})
    monkeypatch.setattr(runner,'http',lambda endpoint: {'version':'test'})
    monkeypatch.setattr(report,'summarize',lambda folder: None)
    evaluation_calls=[]
    def evaluate_stub(programs,prelude,source,support=None,runtimes=None):
        evaluation_calls.append(source)
        return {'outcome_fixed':'PASS','outcome_buggy':'PASS','label':'NEUTRAL','executions':{}}
    monkeypatch.setattr(evaluate,'evaluate_test',evaluate_stub)
    clients={}
    def client(folder,*args):
        key=str(folder)
        if key not in clients:
            clients[key]=FakeClient(['from solution import add\ndef test_x(): assert add(1,2)>0']*8)
            clients[key].model_digest='a'*64
        return clients[key]
    monkeypatch.setattr(runner,'Client',client)
    runner.run('interrupted',stop_after=1)
    assert read_json(tmp_path/'runs/interrupted/progress.json')['done']==1
    runner.run('interrupted')
    runner.run('full')
    for name in ('tests.csv','pairs.json'):
        assert (tmp_path/'runs/interrupted'/name).read_bytes()==(tmp_path/'runs/full'/name).read_bytes()
    manifest=read_json(tmp_path/'runs/full/manifest.json')
    assert [p['pair_id'] for p in read_json(tmp_path/'runs/full/pairs.json')]==['Python/1','Python/2']
    assert [e['task_id'] for e in manifest['excluded_tasks']]==['Python/3']
    assert manifest['judge']==read_json(tmp_path/'configs/judge.json')
    assert any(u.startswith('HumanEvalFix-1__buggy__qwen2-5-coder-7b-instruct__s0__') for u in manifest['unit_seconds'])
    for run_name in ('interrupted','full'):
        assert len(clients[str(tmp_path/'runs'/run_name)].calls)==8
        assert read_json(tmp_path/'runs'/run_name/'progress.json')['percent']==100
    a=read_json(tmp_path/'runs/interrupted/manifest.json')
    assert a['input_test_hashes']==manifest['input_test_hashes']
    assert len(evaluation_calls)==80  # 2 jobs * 8 units * (GEN + 4 final policies)
    # A changed run configuration under an existing run ID is refused.
    runs=read_json(tmp_path/'configs/runs.json')
    write_json(tmp_path/'configs/runs.json',dict(runs,full=dict(config,temperature=0.8)))
    with pytest.raises(ValueError,match='Run configuration'):
        runner.run('full')
    write_json(tmp_path/'configs/runs.json',runs)
    # A changed judge prompt is refused before any work (decision Q1: frozen before full runs).
    judge=tmp_path/'prompts/judge_v2b.txt'
    original=judge.read_bytes()
    judge.write_bytes(original+b'\nchanged')
    with pytest.raises(ValueError,match='Judge prompt'):
        runner.run('changed')
    judge.write_bytes(original)
    prompt=tmp_path/'prompts/generate_v1.txt'
    prompt.write_text(prompt.read_text()+'\nchanged template')
    with pytest.raises(ValueError,match='Harness or prompt'):
        runner.run('interrupted')
