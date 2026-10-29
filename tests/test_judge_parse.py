from gbe.policies import judge_parse


def test_json_fence_is_parsed():
    text = '```json\n{\n  "verdict": "BUG",\n  "reason": "Output differs from the docstring."\n}\n```'
    assert judge_parse(text)['verdict'] == 'BUG'


def test_plain_and_python_fenced_json_are_parsed():
    assert judge_parse('{"verdict": "TEST_WRONG", "reason": "r"}')['verdict'] == 'TEST_WRONG'
    assert judge_parse('```\n{"verdict": "UNSURE", "reason": "r"}\n```')['verdict'] == 'UNSURE'


def test_unparseable_and_invalid_verdicts_become_unsure():
    assert judge_parse('no json here')['reason'] == 'Unparseable judge response'
    assert judge_parse('{"verdict": "MAYBE", "reason": "r"}')['reason'] == 'Unparseable judge response'
