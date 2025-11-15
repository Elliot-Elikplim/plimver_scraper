# plimver_scraper settings — tuned for anti-ban and Zyte integration
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file in local development

BOT_NAME = 'plimver_scraper'

SPIDER_MODULES = ['plimver_scraper.spiders']
NEWSPIDER_MODULE = 'plimver_scraper.spiders'

# Compliance
ROBOTSTXT_OBEY = True  # respect robots.txt by default — important for legality and compliance

# Anti-ban: random delays, auto-throttle
DOWNLOAD_DELAY = 0.8  # base delay
RANDOMIZE_DOWNLOAD_DELAY = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Download and retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3
DOWNLOAD_TIMEOUT = 30

# Middlewares
DOWNLOADER_MIDDLEWARES = {
    'plimver_scraper.middlewares.rotate_user_agent.RotateUserAgentMiddleware': 400,
    'plimver_scraper.middlewares.random_delay.RandomDelayMiddleware': 450,
    # place Zyte or custom proxy middleware at appropriate order
    'plimver_scraper.middlewares.protocol_proxy.ProtocolProxyMiddleware': 700,
}

# Pipelines
ITEM_PIPELINES = {
    'plimver_scraper.pipelines.compliance.CompliancePipeline': 100,
    'plimver_scraper.pipelines.extraction.ExtractionPipeline': 300,
}

# Zyte / Smart Proxy settings
# The repo may contain a `.env` file (local only; do not commit keys) — `python-dotenv` will load it.
# The `ZYTE_SCRAPY_CLOUD_APIKEY` is often used for Scrapy Cloud deployment; Smart Proxy may use a
# different token (often the Smart Proxy API key). We'll build a Zyte proxy URL automatically
# if the `ZYTE_PROXY_URL` is set or derive it from the `ZYTE_SCRAPY_CLOUD_APIKEY` for convenience.
ZYTE_SCRAPY_CLOUD_APIKEY = os.getenv('ZYTE_SCRAPY_CLOUD_APIKEY')
ZYTE_PROXY_URL = os.getenv('ZYTE_PROXY_URL') or os.getenv('ZYTE_SMARTPROXY')

# Derive a default Zyte proxy if user provided a Zyte Scrapy Cloud API key and no explicit proxy
if not ZYTE_PROXY_URL and ZYTE_SCRAPY_CLOUD_APIKEY:
    # Do not print or log the API key anywhere. Only build a proxy url for internal use.
    # NOTE: Zyte may require a different proxy user format; this is a best-effort derivation.
    ZYTE_PROXY_URL = f"http://{ZYTE_SCRAPY_CLOUD_APIKEY}@proxy.zyte.com:8010"

ZYTE_SMARTPROXY_ENABLED = bool(ZYTE_PROXY_URL)

# User agent list for random rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/121.0',
]

LOG_LEVEL = 'INFO'
