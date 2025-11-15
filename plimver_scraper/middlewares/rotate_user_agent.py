import random
from scrapy import signals

class RotateUserAgentMiddleware:
    """Rotate the User-Agent header to reduce fingerprinting.

    Add to DOWNLOADER_MIDDLEWARES.
    """

    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(user_agents=crawler.settings.get('USER_AGENTS', []))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info('RotateUserAgentMiddleware enabled with %d agents', len(self.user_agents))

    def process_request(self, request, spider):
        if self.user_agents:
            ua = random.choice(self.user_agents)
            request.headers.setdefault('User-Agent', ua)
            # Prevent scrambled UA being overridden
            request.headers['User-Agent'] = ua
            # Add a short random Accept-Language header to further reduce fingerprinting
            if 'Accept-Language' not in request.headers:
                request.headers['Accept-Language'] = 'en-US,en;q=0.9'
