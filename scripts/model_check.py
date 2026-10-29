"""Pre-run local-model checks with sampled device memory and complete raw calls."""
import json
import argparse
import subprocess
import threading
import time

from gbe.llm import MODELS, OPTIONS, http, local_model
from gbe.util import ROOT, digest, now, read_json, write_json


def check(selected=None):
    directory = ROOT / 'runs' / 'setup'
    config = {'ollama_version': http('/api/version')['version'], 'models': {}, 'checked': now()}
    source_hash=digest((ROOT/'scripts/model_check.py').read_text(encoding='utf-8'))
    previous=directory/'model_check.json'
    if previous.exists():
        saved=read_json(previous)
        if saved['ollama_version']!=config['ollama_version']:
            raise ValueError('Ollama version changed during model preparation')
        if saved.get('check_source_sha256')==source_hash:
            config=saved
    config['check_source_sha256']=source_hash
    for model in selected or MODELS:
        info = local_model(model)
        if model in config['models'] and config['models'][model]['digest']==info['digest']:
            print(model,'completed check reused',flush=True)
            continue
        # Unload other local models to measure each one alone at the study context size.
        for loaded in http('/api/ps').get('models', []):
            if 'cloud' in loaded['name'].lower():
                raise ValueError('Unexpected remote model')
            http('/api/generate', {'model': loaded['name'], 'keep_alive': 0, 'stream': False, 'think': False})
        samples, stop = [], threading.Event()
        def sample():
            while not stop.is_set():
                result = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.used',
                                                  '--format=csv,noheader,nounits'], text=True)
                samples.append(int(result.strip().splitlines()[0]))
                stop.wait(.2)
        worker = threading.Thread(target=sample)
        worker.start()
        request = {'model': model, 'stream': False, 'think': False, 'options': OPTIONS,
                   'messages': [{'role': 'user', 'content': 'Write one pytest test for a function add(a,b) that returns a+b. Return Python code only.'}]}
        started = time.monotonic()
        try:
            response = http('/api/chat', request)
        finally:
            stop.set()
            worker.join()
        processors = http('/api/ps')['models']
        resident = next(p for p in processors if p['name'] == model)
        thinking = bool(response['message'].get('thinking')) or '<think>' in response['message']['content']
        row = {'digest': info['digest'], 'details': info['details'], 'wall_seconds': time.monotonic()-started,
               'load_seconds': response.get('load_duration', 0)/1e9,
               'tokens_per_second': response.get('eval_count', 0)/max(response.get('eval_duration', 1)/1e9, 1e-9),
               'peak_gpu_mib': max(samples), 'memory_samples': len(samples), 'thinking_returned': thinking,
               'resident': resident, 'fully_on_gpu': resident.get('size_vram', 0) >= resident.get('size', 1),
               'request': request, 'response': response, 'timestamp':now(),
               'harness_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
               'prompt_template':'model_check_inline_v1',
               'prompt_sha256':digest(request['messages'][0]['content']),
               'prompt_template_sha256':digest(request['messages'][0]['content'])}
        config['models'][model] = row
        write_json(directory / 'model_check.json', config)
        print(model, json.dumps({k: row[k] for k in ('digest','wall_seconds','tokens_per_second','peak_gpu_mib','thinking_returned','fully_on_gpu')}), flush=True)
    if all(model in config['models'] for model in MODELS):
        write_json(ROOT / 'configs' / 'models.json', config)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=MODELS,action='append')
    check(parser.parse_args().model)
