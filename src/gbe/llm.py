import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from .generate import strip_reasoning
from .util import ROOT, digest, now, read_json, write_json

OPTIONS = {'temperature': 0, 'seed': 0, 'num_ctx': 8192, 'num_predict': 2048}
MODELS = ['qwen2.5-coder:7b-instruct', 'qwen3.5:9b', 'gemma4:12b']


def http(endpoint, payload=None):
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request('http://localhost:11434' + endpoint, data=body,
                                     headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=600) as response:
        return json.load(response)


def local_model(model, expected=None):
    if 'cloud' in model.lower():
        raise ValueError('Cloud models forbidden')
    tags = http('/api/tags')['models']
    match = next((row for row in tags if row['name'] == model), None)
    if not match or match.get('remote_host') or match.get('remote_model'):
        raise ValueError('Model must be installed locally')
    if expected and match['digest'] != expected:
        raise ValueError('Pinned model digest changed')
    return match


class Client:
    def __init__(self, run_dir, model, model_digest, options=None):
        local_model(model, model_digest)
        self.run_dir, self.model, self.model_digest = Path(run_dir), model, model_digest
        self.options = dict(options or OPTIONS)
        self.log = self.run_dir / 'llm_calls.jsonl'
        self.logged = {row['call_id'] for row in self.rows()}

    def rows(self):
        if not self.log.exists():
            return []
        contents=self.log.read_bytes()
        lines=contents.splitlines(keepends=True)
        rows=[]
        valid_bytes=0
        for index,line in enumerate(lines):
            try:
                if line.strip():
                    rows.append(json.loads(line))
            except (json.JSONDecodeError, UnicodeDecodeError):
                if index!=len(lines)-1 or line.endswith(b'\n'):
                    raise
                # A killed append can leave an incomplete last record. Its full
                # response is already cached and will be re-logged without a call.
                with self.log.open('r+b') as handle:
                    handle.truncate(valid_bytes)
                return rows
            valid_bytes+=len(line)
        if contents and not contents.endswith(b'\n'):
            with self.log.open('ab') as handle:
                handle.write(b'\n')
        return rows

    def call(self, template, fields, *, unit_id, purpose, policy='', test_id='', round=0):
        template_text = (ROOT / 'prompts' / (template + '.txt')).read_text(encoding='utf-8')
        prompt = template_text.format_map(fields)
        request = {'model': self.model, 'stream': False, 'think': False,
                   'options': self.options, 'messages': [{'role': 'user', 'content': prompt}]}
        key = digest({'digest': self.model_digest, 'options': self.options, 'prompt': digest(prompt),
                      'think': False})
        path = self.run_dir / 'cache' / (key + '.json')
        call_id = digest([unit_id, purpose, policy, test_id, round, key])
        cache_hit = path.exists()
        if cache_hit:
            cached = read_json(path)
        else:
            started = time.monotonic()
            try:
                response = http('/api/chat', request)
            except urllib.error.HTTPError as error:
                body = error.read().decode('utf-8', 'replace')
                # Ollama stops a generation that loops on the same tokens and answers HTTP 500.
                # At temperature 0 this is deterministic for the prompt, so it is recorded (and
                # cached) as an empty answer: generation then retries or fails, a repair round
                # fails, and a judge call parses as UNSURE. Every other server error still stops.
                if error.code != 500 or 'repeat limit' not in body:
                    raise
                response = {'message': {'role': 'assistant', 'content': ''}, 'done_reason': 'aborted',
                            'aborted_error': body, 'prompt_eval_count': 0, 'eval_count': 0}
            cached = {'request': request, 'response': response,
                      'duration_s': time.monotonic() - started, 'timestamp': now()}
            write_json(path, cached)
        response = cached['response']
        if call_id not in self.logged:
            row = dict(call_id=call_id, unit_id=unit_id, purpose=purpose, policy=policy,
                       test_id=test_id, round=round, model=self.model, model_digest=self.model_digest,
                       options=self.options, think=False, prompt_template=template,
                       prompt_sha256=digest(prompt), template_sha256=digest(template_text), prompt=prompt,
                       response=response, request=cached['request'],
                       prompt_eval_count=response.get('prompt_eval_count', 0),
                       eval_count=response.get('eval_count', 0), duration_s=0 if cache_hit else cached['duration_s'],
                       request_duration_s=cached['duration_s'], cache_hit=cache_hit,
                       timestamp=cached['timestamp'], cache_key=key,
                       aborted=response.get('done_reason') == 'aborted')
            self.log.parent.mkdir(parents=True, exist_ok=True)
            with self.log.open('a', encoding='utf-8') as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + '\n')
                handle.flush()
            self.logged.add(call_id)
        return strip_reasoning(response['message']['content'])


class FakeClient:
    def __init__(self, responses):
        self.responses, self.calls, self.cache = list(responses), [], {}

    def call(self, template, fields, **metadata):
        key = digest([template, fields, metadata])
        if key not in self.cache:
            self.cache[key] = self.responses.pop(0)
            self.calls.append(dict(template=template, fields=fields, **metadata))
        return self.cache[key]
