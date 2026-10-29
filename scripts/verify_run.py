"""Implementer self-checks for a finished run, including independent pass/fail re-execution.

Phase 1 pilots and Phase 2 runs (QuixBugs tasks, support modules, judge v2b).
This is evidence for hand-off, not the independent reviewer's verdict.
"""
import argparse
import ast
import csv
import json
import os
import random
import subprocess
import sys
import uuid
from collections import Counter, defaultdict

from gbe.benchmarks import all_tasks, benchmark_name, program
from gbe.generate import oracle_locked, suite_hash
from gbe.util import ROOT, digest, read_json, write_json


def plain_run(source, test, timeout=5, support=None):
    folder = ROOT/'.scratch'/'independent'/uuid.uuid4().hex
    folder.mkdir(parents=True)
    (folder/'solution.py').write_text(source,encoding='utf-8')
    for name, text in (support or {}).items():
        (folder/name).write_text(text,encoding='utf-8')
    (folder/'test_check.py').write_text(test,encoding='utf-8')
    process = subprocess.Popen([sys.executable,'-m','pytest','-q','--rootdir=.',
            '--confcutdir=.','-p','no:cacheprovider','test_check.py'],cwd=folder,
            env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            text=True,encoding='utf-8',errors='replace',start_new_session=os.name!='nt')
    try:
        stdout,stderr=process.communicate(timeout=timeout)
        return process.returncode==0,stdout+stderr
    except subprocess.TimeoutExpired:
        if os.name=='nt':
            subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True)
        else:
            import signal
            os.killpg(process.pid,signal.SIGKILL)
        process.kill()
        process.communicate()
        return False,'TIMEOUT'


def independent_label(pair, prelude, source):
    passed={c:[plain_run(program(pair,c),prelude+'\n'+source,support=pair.get('support'))[0] for _ in range(2)]
            for c in ('fixed','buggy')}
    if any(v[0]!=v[1] for v in passed.values()):
        return 'FLAKY'
    return {(True,False):'REVEALS',(False,True):'ENCODES',(True,True):'NEUTRAL',
            (False,False):'BROKEN'}[(passed['fixed'][0],passed['buggy'][0])]


def verify(run_id):
    folder=ROOT/'runs'/run_id
    pairs,_=all_tasks()
    pairs={p['task_id']:p for p in pairs}
    manifest=read_json(folder/'manifest.json')
    rows=list(csv.DictReader((folder/'tests.csv').open(encoding='utf-8')))
    calls=[json.loads(line) for line in (folder/'llm_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    results={}
    sanity=[]
    recorded={}
    for file in ('quixbugs_sanity.json','disguised_sanity.json','natural_sanity.json'):
        if (ROOT/'configs'/file).exists():
            recorded.update(read_json(ROOT/'configs'/file))
    for selected in read_json(folder/'pairs.json'):
        pair=pairs[selected['pair_id']]
        if benchmark_name(pair) in ('QuixBugs','HumanEvalFixDisguised','HumanEvalPlusNatural'):
            # QuixBugs' own tests need its directory layout and the disguised pairs need name aliases;
            # reuse the recorded two-run evidence, valid only while the sources still match its hashes.
            entry=recorded[pair['task_id']]
            current={c:digest(program(pair,c)) for c in ('fixed','buggy')}
            statuses={'fixed':entry['source_hashes']==current and all(o=='PASS' for o in entry['fixed']),
                      'buggy':not (entry['source_hashes']==current and all(o!='PASS' for o in entry['buggy']))}
        else:
            check='from solution import *\n'+pair['test_setup']+'\n'+pair['test']+'\ndef test_dataset_completed(): pass\n'
            statuses={c:plain_run(program(pair,c),check,15)[0] for c in ('fixed','buggy')}
        sanity.append({'pair_id':pair['task_id'],**statuses})
    results['P1-a']={'pass':all(s['fixed'] and not s['buggy'] for s in sanity),'pairs':sanity}
    policy_errors=[]
    hashes=[]
    for unit_folder in sorted((folder/'units').iterdir()):
        suite=read_json(unit_folder/'generated.json')
        expected=suite_hash(suite)
        hashes.append(all(h==expected for h in manifest['input_test_hashes'][unit_folder.name].values()))
        for p in ('P1','P2','P3','P4'):
            data=read_json(unit_folder/f'policy_{p}.json')
            hashes.append(data['input_hash']==expected)
            for i,t in enumerate(data['tests']):
                if p=='P1' and t['n_llm_calls']:
                    policy_errors.append([t['test_id'],p,'P1 LLM call'])
                if p!='P4' and t['final_status']=='KEPT' and t['outcome_put']!='PASS':
                    policy_errors.append([t['test_id'],p,'Invalid kept test'])
                if t['final_status']=='QUARANTINED' and (t['source']!=suite['tests'][i]['source'] or t['prelude']!=suite['prelude']):
                    policy_errors.append([t['test_id'],p,'Changed quarantine'])
                if p=='P4':
                    for version in t['versions'][1:]:
                        if version['accepted'] and not oracle_locked(suite['prelude']+'\n'+suite['tests'][i]['source'],
                                                                   version['prelude']+'\n'+version['source']):
                            policy_errors.append([t['test_id'],p,'Oracle lock violation'])
                if p=='P2':
                    from gbe.policies import template_repair
                    current=t['versions'][0]
                    for v in t['versions'][1:]:
                        if v['action'] in ('T2','T3','T4'):
                            expected_repair=template_repair(current['source'],current['prelude'],current['outcome'])
                            if not expected_repair or (v['source'],v['prelude'],v['action'])!=expected_repair:
                                policy_errors.append([t['test_id'],p,'Unexpected template change'])
                        if v['accepted']:
                            current=v
    results['P1-c']={'pass':all(hashes),'checks':len(hashes)}
    results['P1-e']={'pass':not policy_errors,'errors':policy_errors}
    unit_pair={r['unit_id']:pairs[r['pair_id']] for r in rows}
    # A GEN_FAIL unit has no rows in tests.csv; its calls map to the pair named in the unit ID
    # (HumanEvalFix-59__buggy__... -> Python/59).
    for call in calls:
        if call['unit_id'] not in unit_pair:
            bench,_,name=call['unit_id'].split('__')[0].partition('-')
            unit_pair[call['unit_id']]=pairs[{'QuixBugs':'QuixBugs/','HumanEvalFixDisguised':'HumanEvalFixDisguised/',
                                              'HumanEvalPlusNatural':'HumanEvalPlusNatural/'}.get(bench,'Python/')+name]
    overlaps=[]
    leakage=[]
    for call in calls:
        pair=unit_pair[call['unit_id']]
        prompt=call['prompt']
        context_version='buggy' if '__buggy__' in call['unit_id'] else 'fixed'
        normalized=lambda text: '\n'+'\n'.join(line.strip() for line in text.splitlines() if line.strip())+'\n'
        prompt_lines={line.strip() for line in prompt.splitlines()}
        if benchmark_name(pair)=='QuixBugs':
            # Hidden material: the other version's program and the benchmark's own test files.
            from gbe.quixbugs import SOURCE
            name=pair['entry_point']
            hidden={'other_version':pair['programs']['fixed' if context_version=='buggy' else 'buggy'],
                    'test':(SOURCE/'python_testcases'/f'test_{name}.py').read_text(encoding='utf-8')}
            cases=SOURCE/'json_testcases'/f'{name}.json'
            if cases.exists():
                hidden['json_cases']=cases.read_text(encoding='utf-8')
            own=program(pair,context_version)+pair['prompt']
            for field,raw in hidden.items():
                for line in raw.splitlines():
                    line=line.strip()
                    if len(line)>=15 and line in prompt_lines and line not in own:
                        overlaps.append({'call_id':call['call_id'],'field':field,'line':line})
                if field!='other_version' and normalized(raw) in normalized(prompt):
                    leakage.append({'call_id':call['call_id'],'field':field,'kind':'full_field'})
            if call['purpose']=='generate' and normalized(hidden['other_version']) in normalized(prompt):
                leakage.append({'call_id':call['call_id'],'field':'other_version','kind':'full_field'})
        elif benchmark_name(pair) in ('HumanEvalFixDisguised','HumanEvalPlusNatural'):
            # Hidden material: the other version's program and HumanEval's own test (with name aliases).
            hidden={'other_version':pair['programs']['fixed' if context_version=='buggy' else 'buggy'],
                    'test':pair['hidden_test']}
            own=program(pair,context_version)+pair['prompt']
            for field,raw in hidden.items():
                for line in raw.splitlines():
                    line=line.strip()
                    if len(line)>=15 and line in prompt_lines and line not in own:
                        overlaps.append({'call_id':call['call_id'],'field':field,'line':line})
                if field!='other_version' and normalized(raw) in normalized(prompt):
                    leakage.append({'call_id':call['call_id'],'field':field,'kind':'full_field'})
            if call['purpose']=='generate' and normalized(hidden['other_version']) in normalized(prompt):
                leakage.append({'call_id':call['call_id'],'field':'other_version','kind':'full_field'})
        elif context_version=='buggy':
            # Full fields and fixed-only implementation lines detect copied ground truth.
            # Shared code and independently generated matching assertions are reported separately.
            for field in ('canonical_solution','test','example_test'):
                raw=pair[field].strip()
                if raw and normalized(raw) in normalized(prompt) and (field!='canonical_solution' or
                        normalized(raw) not in normalized(program(pair,'buggy'))):
                    leakage.append({'call_id':call['call_id'],'field':field,'kind':'full_field'})
                for line in raw.splitlines():
                    line=line.strip()
                    if len(line)<15 or line not in prompt_lines:
                        continue
                    overlaps.append({'call_id':call['call_id'],'field':field,'line':line})
                    if field=='canonical_solution' and line not in pair['buggy_solution'] and line not in pair['prompt']:
                        # A model may independently propose a corrected line in a test or repair.
                        # Keep such cases for explicit inspection instead of treating a match as proven leakage.
                        overlaps[-1]['fixed_only_match']=True
        if call['purpose']=='judge':
            template=call.get('prompt_template','judge_v1')
            text=(ROOT/'prompts'/f'{template}.txt').read_text()
            # v1 must not carry a program field before its observed behaviour; v2b has no program field
            # and no behaviour at all. A raw traceback is forbidden in both.
            expected=text.split('Observed behaviour:')[0] if template=='judge_v1' else text
            if '{program}' in expected or ('{feedback}' in expected and template!='judge_v1') or 'solution.py:' in prompt:
                leakage.append({'call_id':call['call_id'],'kind':'judge_implementation_traceback'})
    write_json(folder/'prompt_overlaps.json',overlaps)
    results['P1-b']={'pass':not leakage,'violations':leakage,'textual_overlaps':len(overlaps),
                     'note':'Textual overlaps are retained for manual inspection; coincidence does not establish data access.'}
    strata=defaultdict(list)
    for row in rows:
        if row['stage']!='GEN' and row['final_status']!='DROPPED':
            strata[(row['stage'],row['label'])].append(row)
    rng=random.Random(20261008)
    for group in strata.values():
        rng.shuffle(group)
    sampled=[]
    while len(sampled)<30 and any(strata.values()):
        for key in sorted(strata):
            if strata[key] and len(sampled)<30:
                sampled.append(strata[key].pop())
    verified=[]
    for row in sampled:
        data=read_json(folder/'units'/row['unit_id']/f"policy_{row['stage']}.json")
        t=next(t for t in data['tests'] if t['test_id']==row['test_id'])
        actual=independent_label(pairs[row['pair_id']],t['prelude'],t['source'])
        verified.append({'test_id':row['test_id'],'policy':row['stage'],'expected':row['label'],'actual':actual})
    results['P1-d']={'pass':len(verified)==30 and all(r['expected']==r['actual'] for r in verified),'sample':verified}
    events=[]
    for policy in ('P2','P3'):
        candidates=[r for r in rows if r['stage']==policy and r['fate'] in ('INVERTED','NEUTRALIZED')]
        rng.shuffle(candidates)
        for row in candidates[:5]:
            suite=read_json(folder/'units'/row['unit_id']/'generated.json')
            i=int(row['test_id'].rsplit('/t',1)[1])
            before=suite['tests'][i]['source']
            t=read_json(folder/'units'/row['unit_id']/f'policy_{policy}.json')['tests'][i]
            gen=independent_label(pairs[row['pair_id']],suite['prelude'],before)
            final=independent_label(pairs[row['pair_id']],t['prelude'],t['source'])
            events.append(dict(test_id=row['test_id'],policy=policy,gen_actual=gen,final_actual=final,
                               expected_final=row['label'],before=before,after=t['source'],change_modes=row['change_modes']))
    write_json(folder/'erasure_examples.json',events)
    results['P1-f']={'pass':len(events)==10 and all(e['gen_actual']=='REVEALS' and e['final_actual']==e['expected_final']
                                                  and e['final_actual'] in ('ENCODES','NEUTRAL') for e in events),
                     'verified':len(events),'required':10}
    required=('model_digest','ollama_version','prompt_hashes','dataset_revision','harness_commit','options')
    results['P1-i']={'pass':all(k in manifest for k in required),'fields':list(required)}
    results['P1-m']={'pass':not any(x.get('kind')=='judge_implementation_traceback' for x in leakage)}
    results['P1-h']={'pass':True,'evidence':'Offline test_resume_no_repeated_calls and persistent client-cache test; timing fields differ by construction.'}
    unit_test=subprocess.run([sys.executable,'-m','pytest','-q','--basetemp=.scratch/final-check'],cwd=ROOT,
                              capture_output=True,text=True,encoding='utf-8',errors='replace')
    results['section8_all_pass']=unit_test.returncode==0
    results['P1-h']['pass']=unit_test.returncode==0
    results['unit_test_output']=unit_test.stdout+unit_test.stderr
    write_json(folder/'verification.json',results)
    print(json.dumps(results,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-id',default='phase1_pilot')
    verify(parser.parse_args().run_id)
