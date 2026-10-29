"""Resumable Ollama pulls, with machine-readable progress in the workspace."""
import json
import time
import urllib.request

from gbe.llm import MODELS, http
from gbe.util import ROOT, now, write_json

started = time.monotonic()
for index, model in enumerate(MODELS):
    if 'cloud' in model.lower():
        raise ValueError('Cloud models forbidden')
    installed = {r['name'] for r in http('/api/tags')['models']}
    if model not in installed:
        request = urllib.request.Request('http://localhost:11434/api/pull',
            data=json.dumps({'model': model, 'stream': True}).encode(),
            headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(request, timeout=600) as response:
            last_print = 0
            for line in response:
                row = json.loads(line)
                if 'error' in row:
                    raise RuntimeError(row['error'])
                fraction = row.get('completed',0) / max(row.get('total',1),1)
                percent = (index + fraction) / len(MODELS) * 100
                elapsed = time.monotonic()-started
                eta = elapsed / max(percent, .01) * (100-percent)
                progress = dict(done=index,total=len(MODELS),percent=percent,eta_seconds=eta,
                                updated=now(),model=model,status=row['status'])
                write_json(ROOT/'runs/setup/progress.json', progress)
                if time.monotonic()-last_print>5:
                    print(f'{percent:.1f}% | {model} | {row["status"]} | ETA {eta/60:.1f} min',flush=True)
                    last_print=time.monotonic()
    write_json(ROOT/'runs/setup/progress.json',dict(done=index+1,total=3,percent=(index+1)/3*100,
               eta_seconds=0,updated=now(),model=model,status='complete'))
write_json(ROOT/'runs/setup/tags.json',http('/api/tags'))
