from plimver_scraper.pipelines.extraction import ExtractionPipeline

SAMPLE_HTML = '''
<html>
<head>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","articleBody":"Hello from json-ld"}</script>
</head>
<body><article><p>this is article</p></article></body>
</html>
'''


def test_jsonld_extraction():
    pipeline = ExtractionPipeline()
    item = {'raw_text': SAMPLE_HTML}
    result = pipeline.process_item(item, spider=None)
    assert 'Hello from json-ld' in result['content']
