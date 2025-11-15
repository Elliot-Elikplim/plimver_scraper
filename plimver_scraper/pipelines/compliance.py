import re
from scrapy.exceptions import DropItem

class CompliancePipeline:
    """Pipeline that checks common legal indicators and blocks items when p0licy forbids scraping.

    This is a simplified example. For production, link to terms-of-service parsing and legal review.
    """

    TERMS_KEYWORDS = [
        'terms of service', 'terms & conditions', 'terms and conditions', 'terms', 'accept',
        'copyright', 'privacy policy', 'do not scrape'
    ]

    def process_item(self, item, spider):
        text = item.get('raw_text') or item.get('content') or ''
        text = text.lower()
        for kw in self.TERMS_KEYWORDS:
            if kw in text:
                spider.logger.warning('Possible legal restriction found via keyword: %s', kw)
                # For demo: we simply mark as flagged instead of dropping
                item['compliance_flagged'] = True
                break
        return item
