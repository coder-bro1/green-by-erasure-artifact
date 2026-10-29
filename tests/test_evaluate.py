from gbe import evaluate


def test_flaky_outcomes_are_excluded(monkeypatch):
    outcomes=iter(['PASS','PASS','ASSERT_FAIL','PASS'])
    monkeypatch.setattr(evaluate,'execute',lambda *args, **kwargs: {'outcome':next(outcomes)})
    result=evaluate.evaluate_test({'fixed':'fixed','buggy':'buggy'},'','def test_x(): pass')
    assert result['label']=='FLAKY'
    assert len(result['executions']['fixed'])==len(result['executions']['buggy'])==2
