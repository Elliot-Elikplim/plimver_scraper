"""
Simple Zyte (Scrapy Cloud) helper utilities.

These helpers are intentionally minimal and conservative: they use the
`ZYTE_SCRAPY_CLOUD_APIKEY` environment variable (set locally in `.env`) and an
API base URL that defaults to `https://app.zyte.com/api/v2` (configurable).

This module does not rely on official Zyte client libraries; instead it uses
`requests` and basic auth with the key used as the username (Scrapinghub
compatibility). If Zyte's API changes, adjust `API_BASE` accordingly.
"""
import os
from typing import Any, Dict, List

import requests

API_BASE = os.getenv('ZYTE_API_BASE', 'https://app.zyte.com/api/v2')


class ZyteAPIError(RuntimeError):
    pass


def get_session() -> requests.Session:
    api_key = os.getenv('ZYTE_SCRAPY_CLOUD_APIKEY')
    if not api_key:
        raise ZyteAPIError('Zyte API key is not set. Please set ZYTE_SCRAPY_CLOUD_APIKEY.')
    session = requests.Session()
    # Historical Scrapinghub authentication used Basic Auth with API key as username.
    # We keep an empty password here for compatibility; update if Zyte requires a header.
    session.auth = (api_key, '')
    return session


def list_projects(api_base: str = API_BASE) -> List[Dict[str, Any]]:
    """Return a list of projects for the current Zyte account.

    Returns JSON-decoded list. For unexpected responses a ZyteAPIError is raised.
    """
    session = get_session()
    url = f"{api_base}/projects"
    r = session.get(url, timeout=15)
    if r.status_code != 200:
        raise ZyteAPIError(f'Failed to list Zyte projects: {r.status_code} - {r.text}')
    return r.json()


def get_project_usage(project_id: int, api_base: str = API_BASE) -> Dict[str, Any]:
    """Get usage metrics for a project_id. The path depends on Zyte API; this is
    a reasonable default for older Scrapinghub APIs but may need adjusting.
    """
    session = get_session()
    url = f"{api_base}/projects/{project_id}/stats"
    r = session.get(url, timeout=15)
    if r.status_code != 200:
        raise ZyteAPIError(f'Failed to fetch project usage: {r.status_code} - {r.text}')
    return r.json()
