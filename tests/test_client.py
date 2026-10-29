import json

import pytest

from gbe import llm
from gbe.util import read_json


def test_client_pin_think_raw_log_and_persistent_cache(tmp_path, monkeypatch):
    requests = []
    def fake_http(endpoint, payload=None):
        requests.append((endpoint,payload))
        if endpoint=='/api/tags':
            return {'models':[{'name':'toy:local','digest':'a'*64}]}
        return {'message':{'content':'<think>hidden</think>```python\ndef test_x(): pass\n```',
                           'thinking':'hidden field'}, 'eval_count':12,'prompt_eval_count':30}
    monkeypatch.setattr(llm,'http',fake_http)
    with pytest.raises(ValueError,match='digest'):
        llm.Client(tmp_path,'toy:local','b'*64)
    metadata=dict(unit_id='toy',purpose='generate')
    fields=dict(entry_point='add',generation_input='def add(a,b): return a+b',reminder='')
    client=llm.Client(tmp_path,'toy:local','a'*64)
    text=client.call('generate_v1',fields,**metadata)
    resumed=llm.Client(tmp_path,'toy:local','a'*64)
    assert resumed.call('generate_v1',fields,**metadata)==text
    assert len([r for r in requests if r[0]=='/api/chat'])==1
    assert '<think>' not in text
    rows=[json.loads(line) for line in (tmp_path/'llm_calls.jsonl').read_text().splitlines()]
    assert len(rows)==1
    assert rows[0]['request']['think'] is False
    assert rows[0]['response']['message']['thinking']=='hidden field'
    assert rows[0]['model_digest']=='a'*64
    assert rows[0]['options']==llm.OPTIONS
    with (tmp_path/'llm_calls.jsonl').open('a') as handle:
        handle.write('{"call_id":"interrupted')
    recovered=llm.Client(tmp_path,'toy:local','a'*64)
    assert len(recovered.rows())==1
    assert recovered.call('generate_v1',fields,**metadata)==text
    assert len([r for r in requests if r[0]=='/api/chat'])==1


def test_remote_metadata_rejected(monkeypatch):
    monkeypatch.setattr(llm,'http',lambda *args: {'models':[{'name':'remote:local',
        'digest':'a'*64,'remote_host':'https://remote.example'}]})
    with pytest.raises(ValueError,match='locally'):
        llm.local_model('remote:local')
