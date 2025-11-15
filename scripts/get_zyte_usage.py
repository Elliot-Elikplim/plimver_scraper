#!/usr/bin/env python
"""CLI to list Zyte projects and show usage for a selected project.

Example:
  python scripts/get_zyte_usage.py --list
  python scripts/get_zyte_usage.py --project 12345

Set `ZYTE_SCRAPY_CLOUD_APIKEY` in your environment, or create a local `.env`.
"""
import argparse
import json

from plimver_scraper.zyte_utils import list_projects, get_project_usage


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true', help='List all Zyte projects')
    parser.add_argument('--project', type=int, help='ID of project to fetch usage for')
    args = parser.parse_args()

    if args.list:
        projects = list_projects()
        print(json.dumps(projects, indent=2))
    elif args.project:
        usage = get_project_usage(args.project)
        print(json.dumps(usage, indent=2))
    else:
        parser.print_help()
