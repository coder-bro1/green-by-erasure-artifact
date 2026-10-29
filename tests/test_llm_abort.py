import io
import json
import urllib.error

import pytest

from gbe import llm

TAGS = {'models': [{'name': 'm:1', 'digest': 'd'}]}


def fake_http(error_body, code=500):
    def http(endpoint, payload=None):
        if endpoint == '/api/tags':
            return TAGS
        raise urllib.error.HTTPError('http://x', code, 'err', {}, io.BytesIO(error_body.encode()))
    return http


def test_repeat_limit_abort_becomes_empty_cached_answer(tmp_path, monkeypatch):
    monkeypatch.setattr(llm, 'http', fake_http('{"error":"prediction aborted, token repeat limit reached"}'))
    monkeypatch.setattr(llm, 'ROOT', tmp_path)
    (tmp_path / 'prompts').mkdir()
    (tmp_path / 'prompts' / 't.txt').write_text('hello {x}', encoding='utf-8')
    client = llm.Client(tmp_path / 'run', 'm:1', 'd')
    assert client.call('t', {'x': 1}, unit_id='u', purpose='generate') == ''
    row = json.loads((tmp_path / 'run' / 'llm_calls.jsonl').read_text(encoding='utf-8').splitlines()[0])
    assert row['aborted'] is True
    # The abort is cached, so a resumed run does not call the model again.
    monkeypatch.setattr(llm, 'http', lambda *a, **k: (_ for _ in ()).throw(AssertionError('called')))
    client2 = llm.Client.__new__(llm.Client)
    client2.__dict__.update(client.__dict__)
    assert client2.call('t', {'x': 1}, unit_id='u', purpose='generate', round=1) == ''


def test_other_server_errors_still_stop(tmp_path, monkeypatch):
    monkeypatch.setattr(llm, 'http', fake_http('{"error":"model runner crashed"}'))
    monkeypatch.setattr(llm, 'ROOT', tmp_path)
    (tmp_path / 'prompts').mkdir()
    (tmp_path / 'prompts' / 't.txt').write_text('hello', encoding='utf-8')
    client = llm.Client(tmp_path / 'run', 'm:1', 'd')
    with pytest.raises(urllib.error.HTTPError):
        client.call('t', {}, unit_id='u', purpose='generate')
