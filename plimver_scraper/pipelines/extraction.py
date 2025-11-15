from readability import Document
from bs4 import BeautifulSoup
import json

class ExtractionPipeline:
    """Heuristic-based smart extraction pipeline.

    Steps:
      1. Try JSON-LD containing Article
      2. Try OpenGraph meta tags
      3. Try 'article' or `main` element
      4. Fallback to readability-lxml
    """

    def _extract_json_ld(self, response_text):
        soup = BeautifulSoup(response_text, 'lxml')
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string or "{}")
            except json.JSONDecodeError:
                continue
            # If data is a dict and type is Article
            if isinstance(data, dict) and data.get('@type', '').lower() == 'article':
                return data.get('articleBody') or data.get('mainEntityOfPage') or None
            # If it's a list of elements, search
            if isinstance(data, list):
                for d in data:
                    if isinstance(d, dict) and d.get('@type', '').lower() == 'article':
                        return d.get('articleBody') or d.get('mainEntityOfPage')
        return None

    def _extract_og(self, soup):
        og = soup.find('meta', property='og:type')
        if og and og.get('content') == 'article':
            desc = soup.find('meta', property='og:description')
            if desc:
                return desc.get('content')
        return None

    def process_item(self, item, spider):
        response_text = item.get('raw_text') or ''
        if not response_text:
            return item

        json_ld = self._extract_json_ld(response_text)
        if json_ld:
            item['content'] = json_ld
            return item

        soup = BeautifulSoup(response_text, 'lxml')
        og = self._extract_og(soup)
        if og:
            item['content'] = og
            return item

        article = soup.find('article') or soup.find('main') or soup.find(id='main')
        if article:
            text = article.get_text('\n', strip=True)
            if text and len(text) > 100:
                item['content'] = text
                return item

        # fallback: readability
        doc = Document(response_text)
        summary = doc.summary()
        if summary:
            item['content'] = BeautifulSoup(summary, 'lxml').get_text('\n', strip=True)
            return item

        # fallback: whole page text
        item['content'] = soup.get_text('\n', strip=True)[:10000]
        return item
