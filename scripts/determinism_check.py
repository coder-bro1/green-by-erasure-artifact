"""Two explicitly uncached generation repetitions for review check P1-k."""
import argparse
import json
import time

from gbe.llm import http, local_model
from gbe.util import ROOT, digest, now, read_json, write_json

parser=argparse.ArgumentParser()
parser.add_argument('--run-id',default='phase1_pilot')
args=parser.parse_args()
folder=ROOT/'runs'/args.run_id
manifest=read_json(folder/'manifest.json')
local_model(manifest['model'],manifest['model_digest'])
calls=[json.loads(line) for line in (folder/'llm_calls.jsonl').read_text(encoding='utf-8').splitlines()]
generations=[r for r in calls if r['purpose']=='generate' and r['round']==0][:2]
results=[]
for call in generations:
    started=time.monotonic()
    response=http('/api/chat',call['request'])
    results.append(dict(unit_id=call['unit_id'],request=call['request'],response=response,
        model_digest=call['model_digest'],harness_commit=manifest['harness_commit'],timestamp=now(),
        duration_s=time.monotonic()-started,identical_content=response['message']['content']==call['response']['message']['content']))
    write_json(folder/'determinism.json',results)
    print(call['unit_id'],results[-1]['identical_content'],flush=True)
