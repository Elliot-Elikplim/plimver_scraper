import os
import json

import pytest

from plimver_scraper import zyte_utils


class DummyResponse:
    def __init__(self, code, json_val=None, text=''):
        self.status_code = code
        self._json = json_val
        self.text = text

    def json(self):
        return self._json


class DummySession:
    def __init__(self, resp):
        self._resp = resp

    def get(self, *args, **kwargs):
        return self._resp


def test_list_projects(monkeypatch):
    monkeypatch.setenv('ZYTE_SCRAPY_CLOUD_APIKEY', 'FAKE')
    impl = DummyResponse(200, json_val=[{'id': 1, 'name': 'test'}])
    monkeypatch.setattr(zyte_utils, 'get_session', lambda: DummySession(impl))
    projects = zyte_utils.list_projects()
    assert isinstance(projects, list)
    assert projects[0]['id'] == 1


def test_list_projects_404(monkeypatch):
    monkeypatch.setenv('ZYTE_SCRAPY_CLOUD_APIKEY', 'FAKE')
    impl = DummyResponse(404, json_val=None, text='not found')
    monkeypatch.setattr(zyte_utils, 'get_session', lambda: DummySession(impl))
    with pytest.raises(zyte_utils.ZyteAPIError):
        zyte_utils.list_projects()
