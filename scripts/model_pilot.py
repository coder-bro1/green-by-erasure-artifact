"""Configure the existing pilot for a user-requested supplemental local model.

The adapter leaves the active study package untouched. Its source hash is stored
alongside the standard run manifest before any model call.
"""
import argparse
import subprocess
from pathlib import Path

from gbe import runner
from gbe.llm import MODELS, local_model
from gbe.util import ROOT, digest, now, read_json, write_json


def run_model(model, run_id):
    if model not in MODELS or 'cloud' in model.lower():
        raise ValueError('Only approved local study models are allowed')
    if run_id == 'phase1_pilot':
        raise ValueError('Supplemental runs must not reuse the primary pilot ID')
    config = read_json(ROOT/'configs/models.json')
    local_model(model, config['models'][model]['digest'])
    path = ROOT/'runs'/run_id/'execution_driver.json'
    source_hash = digest(Path(__file__).read_text(encoding='utf-8'))
    if path.exists():
        saved = read_json(path)
        if saved['model'] != model or saved['source_sha256'] != source_hash:
            raise ValueError('Supplemental driver or model changed on resume')
    else:
        write_json(path, {
            'script': 'scripts/model_pilot.py', 'source_sha256': source_hash,
            'model': model, 'model_digest': config['models'][model]['digest'],
            'timestamp': now(),
            'harness_commit': subprocess.check_output(
                ['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'reason': f'User requested a supplemental {model} pilot after the primary Qwen2.5 pilot.',
            'configuration_adapter': 'Select runner.MODELS[0] in this process only; pipeline code is unchanged.'})
    # runner has no model argument. This process-local configuration changes only
    # which already-approved tag its existing model selection chooses.
    runner.MODELS = [model]
    runner.run(run_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model',choices=MODELS,required=True)
    parser.add_argument('--run-id',required=True)
    args = parser.parse_args()
    run_model(args.model,args.run_id)
