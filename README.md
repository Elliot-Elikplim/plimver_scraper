# Plimver Scraper (Scrapy) — Anti-ban, Smart Extraction & Zyte integration

This repository contains a small Scrapy project scaffold demonstrating:
- Anti-ban features (rotating User-Agent, random delays, throttling)
- Smart extraction pipeline (JSON-LD, OpenGraph, article/main tag, Readability fallback)
- Basic compliance checks (robots.txt obedience, Terms/Privacy detection)
- Zyte Scrapy Cloud and Smart Proxy integration hints

## Quick start

1. Create a virtual environment and install requirements

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
To run the unit tests:

```powershell
pip install pytest
pytest -q
```

2. Run the example spider locally

```powershell
scrapy runspider plimver_scraper/spiders/example_spider.py -a urls="https://httpbin.org/html" -o output.json
```

3. Zyte Smart Proxy + Scrapy Cloud
- Sign up to Zyte: https://www.zyte.com/ — they provide a free forever Scrapy Cloud unit
- Use Smart Proxy Manager to avoid IP ban; set it via environment variables: `ZYTE_SMARTPROXY` or `PROXY` before running scrapers
- Deploy to Scrapy Cloud: create a Zyte account and push your Scrapy project, then schedule crawls
 - Zyte Smart Proxy and Scrapy Cloud quick tips:
	- Install the command line tool for Scrapy Cloud deployment (`shub`) if you use Zyte/older Scrapy Cloud flows:

```powershell
pip install shub
shub login
shub deploy
```

	- Configure your Smart Proxy credentials as environment variables. For example:

```powershell
$env:ZYTE_SMARTPROXY = "http://apiKey@proxy.zyte.com:8010"
```

	- In `plimver_scraper/settings.py`, you can enable the proxy by populating the `ZYTE_SMARTPROXY` env var and leaving `ProtocolProxyMiddleware` enabled.

	- For JavaScript-heavy sites consider Zyte's Browser rendering (may be a paid feature) or the `scrapy-playwright`/`scrapy-selenium` integrations for local runs.

Zyte API & usage stats
- If you want to fetch usage stats from Zyte for reporting or automation, add `ZYTE_SCRAPY_CLOUD_APIKEY` (Scrapy Cloud API key) to your `.env` or environment.
- The repository includes `plimver_scraper/zyte_utils.py` and a small CLI `scripts/get_zyte_usage.py` that can list projects and show per-project metrics. Example usage below.

Example usage:
```powershell
# Set the key (do not commit)
$env:ZYTE_SCRAPY_CLOUD_APIKEY = "<your-zyte-key>"

# List projects
python scripts/get_zyte_usage.py --list

# Get project usage
python scripts/get_zyte_usage.py --project 123456
```

Example environment for Zyte Smart Proxy (simplified):

```powershell
# Option A: explicit proxy string (recommended if you know the host/port/user/pass)
$env:ZYTE_PROXY_URL = "http://user:pass@proxy.zyte.com:8010"

# Option B: Scrapy Cloud API key (if you have it set in .env as `ZYTE_SCRAPY_CLOUD_APIKEY`,
# our settings will derive a default Zyte proxy URL automatically — this is only a convenience
# for local testing and should not be used in production without confirming Zyte's required format):
$env:ZYTE_SCRAPY_CLOUD_APIKEY = "<your-zyte-key>"

```

## Files & features
- `plimver_scraper/middlewares`: Anti-ban middleware (UA rotation, random delays, simple proxy middleware)
- `plimver_scraper/pipelines`: Smart extraction and compliance
- `plimver_scraper/spiders`: Example spiders and hooks
- `requirements.txt`: Python libs

## Further improvements and next steps
- Add Browser rendering (Playwright) or Zyte Browser to handle heavy JS pages
- Integrate Smart Proxy headers and use Zyte tokens
- Add cookie banner detectors, more advanced legal analysis, per-site throttling settings
- Add unit and integration tests for middlewares and pipelines

## Publishing to GitHub (recommended)

Follow these steps to create a GitHub repository and push this project. There are two recommended ways:

- Using GitHub CLI (preferred):

```powershell
# 1. Install GitHub CLI: https://cli.github.com/ and authenticate (gh auth login)
# 2. Create repo and push
cd "c:\Users\Kweku Elliot\Desktop\Plimver-Scraping\plimver_scraper"
.\.\scripts\create_github_repo.ps1 -Name "plimver_scraper" -Visibility public
```

- Without the CLI (manual):

```powershell
cd "c:\Users\Kweku Elliot\Desktop\Plimver-Scraping\plimver_scraper"
git init
git add -A
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/plimver_scraper.git
git push -u origin main
```

Tips:
- If you prefer SSH push use `git remote add origin git@github.com:<user>/<repo>.git` instead.
- The repository already contains a GitHub Actions workflow at `.github/workflows/ci.yml` which runs tests on push and PRs.
- Add secrets to the GitHub repository (Repo > Settings > Secrets) for Zyte tokens if you use them in CI or for deployment.

## Legal & Compliance
- Always respect `robots.txt` and the website's Terms of Service
- Use lawful scraping practices and consult legal counsel if unsure about use cases
