import os
import scrapy
from plimver_scraper.middlewares.protocol_proxy import ProtocolProxyMiddleware


def test_zyte_proxy_from_api_key(monkeypatch):
    # Set env var for Zyte API key and ensure proxy is built
    monkeypatch.setenv('ZYTE_SCRAPY_CLOUD_APIKEY', 'FAKE_KEY')
    request = scrapy.Request('http://example.com')
    mw = ProtocolProxyMiddleware()
    mw.process_request(request, spider=None)
    assert request.meta.get('proxy') is not None
    assert 'FAKE_KEY' in request.meta.get('proxy')


def test_proxy_prioritizes_explicit_proxy(monkeypatch):
    # If PROXY is set explicitly, it should be used instead of Zyte derived proxy
    monkeypatch.setenv('PROXY', 'http://myproxy:1234')
    monkeypatch.setenv('ZYTE_SCRAPY_CLOUD_APIKEY', 'FAKE_KEY2')
    request = scrapy.Request('http://example.com')
    mw = ProtocolProxyMiddleware()
    mw.process_request(request, spider=None)
    assert request.meta.get('proxy') == 'http://myproxy:1234'
