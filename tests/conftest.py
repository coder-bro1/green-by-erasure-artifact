import pytest
from pathlib import Path


def pytest_configure(config):
    # Keep all fixture artifacts inside this checkout, including fresh clones.
    if config.option.basetemp is None:
        config.option.basetemp=str(Path(__file__).resolve().parents[1]/'.scratch'/'pytest')
    Path(config.option.basetemp).resolve().parent.mkdir(parents=True,exist_ok=True)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    import urllib.request
    def forbidden(*args, **kwargs):
        raise AssertionError('Network forbidden in offline unit tests')
    monkeypatch.setattr(urllib.request, 'urlopen', forbidden)
