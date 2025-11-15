import time
import random

class RandomDelayMiddleware:
    """Introduce small random delays - reduces burst traffic and looks more human-like."""
    def __init__(self, base_delay=0.5, jitter=1.5):
        self.base_delay = base_delay
        self.jitter = jitter

    @classmethod
    def from_crawler(cls, crawler):
        return cls(base_delay=crawler.settings.get('DOWNLOAD_DELAY', 0.5),
                   jitter=1.5)

    def process_request(self, request, spider):
        delay = self.base_delay * random.random() * self.jitter
        time.sleep(delay)
