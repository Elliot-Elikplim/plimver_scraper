import os

class ProtocolProxyMiddleware:
    """Simple middleware to add Zyte or other proxy to requests.

    Expects env var PROXY to be a valid proxy url e.g. http://username:pass@proxy:port
    Or Zyte Smart Proxy Manager can be used with its environment variable.
    """
    def process_request(self, request, spider):
        # Use explicitly provided `PROXY` or `ZYTE_PROXY_URL`
        proxy = os.getenv('PROXY') or os.getenv('ZYTE_PROXY_URL') or os.getenv('ZYTE_SMARTPROXY')
        # If we didn't find one, try the Zyte Scrapy Cloud API key to build a proxy URL
        if not proxy:
            zyte_key = os.getenv('ZYTE_SCRAPY_CLOUD_APIKEY')
            if zyte_key:
                # DO NOT log the key. Build a proxy string for Zyte's Smart Proxy service.
                proxy = f"http://{zyte_key}@proxy.zyte.com:8010"
        if proxy:
            request.meta['proxy'] = proxy
